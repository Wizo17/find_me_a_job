from typing import List, Dict, Any, Optional
from datetime import datetime
from scrappers.base_scraper import BaseScraper
import re
import urllib.parse

class FreeWorkScraper(BaseScraper):
    """
    Scraper implementation for Freework job board.
    """
    
    BASE_URL = "https://www.free-work.com/"
    SEARCH_URL = f"{BASE_URL}/fr/tech-it/jobs"

    def __init__(self):
        super().__init__()

    def search_jobs(self, keywords: str, location: str, num_pages: int = 1) -> List[Dict[str, Any]]:
        """
        Search for jobs on Freework.
        
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
                'page': page
            }
            
            url = f"{self.SEARCH_URL}?{urllib.parse.urlencode(params)}"
            soup = self._fetch_page(url)
            
            if not soup:
                continue
                
            job_cards = soup.find_all('div', {'data-v-798f5146': True, 'class': 'mb-4 relative flex'})
            
            for card in job_cards:
                try:
                    title = card.find('h2', {'data-highlightable': True}).text.strip()
                    company = card.find('div', {'data-highlightable': True}).text.strip()
                    location_el = card.find('span', text='Lieu').find_next('span')
                    location = location_el.text.strip() if location_el else ''
                    
                    job_url = self.BASE_URL.rstrip('/') + card.find('a')['href']
                    
                    contract_type = "Freelance"  # Based on the tag class 'bg-contractor'
                    
                    # Extract additional information from the right column
                    info_col = card.find('div', {'class': 'lg:w-64'})
                    salary = info_col.find('span', text='TJM').find_next('span').text.strip() if info_col.find('span', text='TJM') else None
                    
                    job = {
                        'title': title,
                        'company': company,
                        'location': location,
                        'url': job_url,
                        'contract_type': contract_type,
                        'salary': salary,
                        'published_at': None,  # Not visible in search results
                        'source': 'freework'
                    }
                    
                    jobs.append(job)
                except Exception as e:
                    print(f"Error parsing job card: {e}")
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
        soup = self._fetch_page(job_url)
        if not soup:
            return None
            
        try:
            # Extract basic information
            title = soup.find('h1').text.strip()
            company = soup.find('p', class_='font-semibold text-sm').text.strip()
            location = soup.find('h2').text.strip()
            
            # Extract date
            date_text = soup.find('span', text=re.compile('Publiée le')).text.strip()
            published_at = datetime.strptime(date_text.replace('Publiée le ', ''), '%d/%m/%Y')
            
            # Extract contract details from sidebar
            sidebar = soup.find('div', class_='flex flex-col gap-4 shadow p-4 rounded-lg bg-white')
            contract_type = "Freelance"  # Based on the tag class
            salary = sidebar.find('span', text=re.compile('€')).text.strip() if sidebar.find('span', text=re.compile('€')) else None
            
            # Extract description sections
            description_div = soup.find('div', class_='html-renderer prose-content')
            description = description_div.text.strip() if description_div else ""
            
            # Extract requirements
            requirements_div = soup.find_all('div', class_='html-renderer prose-content')[1]
            requirements = requirements_div.text.strip() if requirements_div else ""
            
            # Extract company info
            company_desc = soup.find('div', class_='mt-4 line-clamp-3').text.strip()
            
            return {
                'title': title,
                'company': company,
                'company_description': company_desc,
                'location': location,
                'contract_type': contract_type,
                'salary': salary,
                'description': description,
                'requirements': requirements,
                'published_at': published_at,
                'url': job_url,
                'source': 'freework'
            }
            
        except Exception as e:
            print(f"Error parsing job details: {e}")
            return None