from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from playwright.sync_api import sync_playwright
import time
import random
import logging
from typing import List, Dict, Any, Optional

logging.basicConfig(
    level=logging.INFO,  # (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class BaseScraper(ABC):
    """
    Base abstract class for all job scraping implementations.
    Defines common interface and utility methods.
    """
    
    def __init__(self, headers: Optional[Dict[str, str]] = None):
        """
        Initialize the scraper with custom HTTP headers.
        
        Args:
            headers: HTTP headers for requests. If None, uses default headers.
        """
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def get_page(self, url: str) -> Optional[str]:
        """
        Fetches webpage content with error handling and anti-blocking delay.
        
        Args:
            url: URL of the page to fetch
            
        Returns:
            The HTML content of the page, or None if error occurs
        """
        try:
            # Add random delay to avoid being blocked
            time.sleep(random.uniform(1, 3))
            
            response = self.session.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching {url}: {e}")
            return None
        
    def get_dynamic_page_selenium(self, url: str, waiting_time: int = 3) -> Optional[str]:
        """
        Fetches webpage content with JavaScript rendering support.
        
        Args:
            url: URL of the page to fetch
            
        Returns:
            The fully rendered HTML content of the page, or None if error occurs
        """
        try:
            # Configure Chrome options for headless browsing
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument(f"user-agent={self.headers['User-Agent']}")
            
            # Initialize the driver
            driver = webdriver.Chrome(options=chrome_options)
            
            # Add random delay to avoid being blocked
            time.sleep(random.uniform(1, 3))
            
            # Load the page
            driver.get(url)
            
            # Wait for a fixed time to allow JavaScript to execute
            time.sleep(waiting_time)
            
            # Get the page source after JavaScript execution
            html_content = driver.page_source
            
            # Close the driver
            driver.quit()
            
            return html_content
        except Exception as e:
            self.logger.error(f"Error fetching dynamic content from {url}: {e}")
            return None
        
    def get_dynamic_page_playwright(self, url: str, waiting_time: int = 3) -> Optional[str]:
        """
        Fetches webpage content with JavaScript rendering using Playwright.
        """
        try:
            # Add random delay to avoid being blocked
            time.sleep(random.uniform(1, 3))
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page(user_agent=self.headers['User-Agent'])
                page.goto(url)
                
                # Wait for a fixed time to allow JavaScript to execute
                time.sleep(waiting_time)
                
                # Get the HTML content
                html_content = page.content()
                
                browser.close()
                return html_content
        except Exception as e:
            self.logger.error(f"Error fetching dynamic content from {url}: {e}")
            return None
    
    def parse_html(self, html: Optional[str]) -> Optional[BeautifulSoup]:
        """
        Converts HTML into BeautifulSoup object for easier parsing.
        
        Args:
            html: HTML content to parse
            
        Returns:
            BeautifulSoup object, or None if HTML is invalid
        """
        if not html:
            return None
        return BeautifulSoup(html, 'html.parser')
    
    @abstractmethod
    def search_jobs(self, keywords: str, location: str, num_pages: int = 1) -> List[Dict[str, Any]]:
        """
        Searches for job listings based on specified criteria.
        
        Args:
            keywords: Search keywords (e.g., "python developer")
            location: Target location (e.g., "Paris")
            num_pages: Number of result pages to scrape
            
        Returns:
            List of found job listings
        """
        pass
    
    @abstractmethod
    def get_job_details(self, job_url: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves complete details of a job listing.
        
        Args:
            job_url: URL of the job listing
            
        Returns:
            Dictionary with job details, or None if error occurs
        """
        pass
    
    def clean_text(self, text: Optional[str]) -> str:
        """
        Cleans text by removing extra spaces and special characters.
        
        Args:
            text: Text to clean
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        # Remove leading and trailing whitespace
        text = text.strip()
        # Replace multiple line breaks with a single space
        text = ' '.join(text.split())
        return text

