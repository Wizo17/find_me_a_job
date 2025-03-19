from typing import List, Dict, Any, Optional
from datetime import datetime
from scrappers.base_scraper import BaseScraper
import re
import urllib.parse

class WelcomeToTheJungleScraper(BaseScraper):
    """
    Scraper implementation for Welcome to the Jungle job board.
    """
    
    BASE_URL = "https://www.welcometothejungle.com"
    SEARCH_URL = f"{BASE_URL}/fr/jobs"

    def __init__(self):
        super().__init__()

    def search_jobs(self, keywords: str, location: str, num_pages: int = 1) -> List[Dict[str, Any]]:
        """
        Search for jobs on Welcome to the Jungle.
        
        Args:
            keywords: Job title or keywords
            location: Location for the job search
            num_pages: Number of pages to scrape
            
        Returns:
            List of job listings
        """
        jobs = []
        
        for page in range(1, num_pages + 1):
            params = {
                'query': keywords,
                'page': page,
                'aroundQuery': location,
                'sortBy': 'mostRecent'
            }
            search_url = f"{self.SEARCH_URL}?{urllib.parse.urlencode(params).replace('+', '%20')}"
            self.logger.info(f"Reading page {page}: {search_url}")
            html_content = self.get_dynamic_page_playwright(search_url)
            
            if not html_content:
                continue
                
            soup = self.parse_html(html_content)
            if not soup:
                continue
            
            # Find all job cards
            job_cards = soup.find_all('div', {'data-role': 'jobs:thumb'}) 

            if not job_cards:
                self.logger.warning("No job cards found")
                continue

            # self.logger.info(f"Found {len(job_cards)} job cards")

            count = 0

            for card in job_cards:
                try:
                    count += 1
                    # self.logger.info(f"Processing job {count} on page")

                    # Extract basic job information from card
                    link = card.find('a')
                    if not link:
                        continue
                        
                    # Title 
                    title_elem = "" 
                    try:
                        title_card = card.find('h4', {'class': 'wui-text'})
                        if title_card:
                            # Extract all text inside any em tags and join them
                            title_parts = title_card.find_all('em')
                            title_elem = ' '.join([part.text for part in title_parts]) if title_parts else title_card.text.strip()
                    except Exception as e:
                        self.logger.error(f"Error parsing job title: {e}")

                    self.logger.info(f"Processing job {count} - {title_elem}")

                    # Company
                    company_elem = ""
                    try:
                        company_card = card.find('span', {'class': 'wui-text'})
                        if company_card:
                            company_elem = company_card.text.strip()
                    except Exception as e:
                        self.logger.error(f"Error parsing company name: {e}")

                    # Location
                    location_elem = ""
                    try:
                        location_icon = card.find('i', {'name': 'location'})
                        if location_icon:
                            # Navigate to the innermost span that contains the location
                            location_container = location_icon.find_next('p')
                            if location_container:
                                # Get the most deeply nested span with the actual location text
                                deepest_span = location_container.find('span')
                                if deepest_span:
                                    location_elem = deepest_span.text.strip()
                                else:
                                    # Fallback to the container text if the specific span isn't found
                                    location_elem = location_container.text.strip()
                    except Exception as e:
                        self.logger.error(f"Error parsing location: {e}")
                    
                    # Contract type
                    contract_type_elem = ""
                    try:
                        contract_type_iccon = card.find('i', {'name': 'contract'})
                        if contract_type_iccon:
                            contract_type_elem = contract_type_iccon.find_next('span').text.strip()
                    except Exception as e:
                        self.logger.error(f"Error parsing contract type: {e}")

                    # Remote status
                    remote_status_elem = ""
                    try:
                        remote_status_icon = card.find('i', {'name': 'remote'})
                        if remote_status_icon:
                            remote_status_elem = remote_status_icon.find_next('span').text.strip()
                    except Exception as e:
                        self.logger.error(f"Error parsing remote status: {e}")

                    # Posted time
                    posted_time_elem = ""
                    try:
                        date_icon = card.find('i', {'name': 'date'})
                        if date_icon and date_icon.find_next('p'):
                            time_elem = date_icon.find_next('p').find('time')
                            if time_elem:
                                # Get the standardized datetime attribute
                                posted_time_elem = time_elem.get('datetime') if time_elem.get('datetime') else time_elem.text.strip()
                    except Exception as e:
                        self.logger.error(f"Error parsing posted time: {e}")
                                        
                    if not all([title_elem, company_elem, location_elem]):
                        continue
                        
                    # Clean company text to remove "chez"
                    company_name = company_elem.replace('chez', '').strip()
                    
                    job_url = f"{self.BASE_URL}{link['href']}"
                    
                    job_info = {
                        'title': self.clean_text(title_elem),
                        'company': company_name,
                        'location': self.clean_text(location_elem),
                        'contract_type': self.clean_text(contract_type_elem),
                        'remote_status': self.clean_text(remote_status_elem),
                        'posted_time': self.clean_text(posted_time_elem),
                        'url': job_url,
                        'source': 'Welcome to the Jungle'
                    }

                    # Get detailed information
                    detailed_info = self.get_job_details(job_url)
                    if detailed_info:
                        job_info["description"] = detailed_info.get('description', "")
                    
                    jobs.append(job_info)
                    
                except Exception as e:
                    self.logger.error(f"Error parsing job card: {e}")
                    continue
                    
        return jobs

    def get_job_details(self, job_url: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific job listing.
        
        Args:
            job_url: URL of the job listing
            
        Returns:
            Dictionary containing job details
        """
        html_content = self.get_page(job_url)
        if not html_content:
            return None
            
        soup = self.parse_html(html_content)
        if not soup:
            return None
            
        try:
            # Find job description
            description_elem = soup.find('div', {'id': 'the-position-section'})
            description = self.clean_text(description_elem.text) if description_elem else ""

            # TODO Add more fields as needed

            return {
                'description': description
            }
            
        except Exception as e:
            self.logger.error(f"Error getting job details from {job_url}: {e}")
            return None