from typing import List, Dict, Any, Optional
import urllib.parse
from langchain.schema import SystemMessage, HumanMessage
from scrappers.base_scraper import BaseScraper
from templates.prompts import JOB_SEARCH_SYSTEM_PROMPT, JOB_SEARCH_HUMAN_PROMPT

class WelcomeToTheJungleScraper(BaseScraper):
    """
    Automatic Scraper implementation with LLM.
    """

    def __init__(self, llm_session):
        super().__init__()
        self.llm_session = llm_session

    def get_base_url(url):
        # TODO : Write docstring
        parsed_url = urllib.parse.urlparse(url)
        return f"{parsed_url.scheme}://{parsed_url.netloc}/"

    def search_jobs(self, keywords: str, location: str, num_pages: int = 1) -> List[Dict[str, Any]]:
        self.logger.warning(f"Not allowed with this class!")
        return []
    
    def get_job_details(self, job_url: str) -> Optional[Dict[str, Any]]:
        self.logger.warning(f"Not allowed with this class!")
        return []

    def search_jobs_with_llm(self, base_url: str, page_key: str, num_pages: int = 1) -> List[Dict[str, Any]]:
        # TODO : Write docstring
        jobs = []
        for page in range(1, num_pages + 1):
            search_url = base_url.format(page_key=page_key, num_page=page)
            search_url = urllib.parse.urlencode(search_url).replace('+', '%20')
            
            self.logger.info(f"Reading page {page}: {search_url}")
            html_content = self.get_dynamic_page_playwright(search_url)

            if not html_content:
                continue

            input_messages = [
                    SystemMessage(content=JOB_SEARCH_SYSTEM_PROMPT),
                    HumanMessage(content=JOB_SEARCH_HUMAN_PROMPT.format(base_url=self.get_base_url(base_url), html_content=html_content))
                ]

            jobs = self.llm_session.search_job(input_messages)

        return jobs

    def get_job_details_with_llm(self, job_url: str) -> Optional[Dict[str, Any]]:
        # TODO : Write docstring
        pass

