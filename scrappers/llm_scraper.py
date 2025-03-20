from typing import List, Dict, Any, Optional
import urllib.parse
from langchain.schema import SystemMessage, HumanMessage
from scrappers.base_scraper import BaseScraper
from templates.prompts import JOB_SEARCH_SYSTEM_PROMPT, JOB_SEARCH_HUMAN_PROMPT

class LLMScraper(BaseScraper):
    """
    Automatic Scraper implementation with LLM.
    """

    def __init__(self, llm_session):
        super().__init__()
        self.llm_session = llm_session

    def get_base_url(self, url):
        # TODO : Write docstring
        parsed_url = urllib.parse.urlparse(url)
        return f"{parsed_url.scheme}://{parsed_url.netloc}/"

    def search_jobs(self, keywords: str, location: str, num_pages: int = 1) -> List[Dict[str, Any]]:
        self.logger.warning(f"Not allowed with this class!")
        return []
    
    def get_job_details(self, job_url: str) -> Optional[Dict[str, Any]]:
        self.logger.warning(f"Not allowed with this class!")
        return []

    def search_jobs_with_llm(self, base_url: str, num_pages: int = 1, examples: list = []) -> List[Dict[str, Any]]:
        # TODO : Write docstring
        jobs = []

        for page in range(1, num_pages + 1):
            search_url = base_url.format(num_page=page)
            # search_url = urllib.parse.urlencode(search_url).replace('+', '%20')

            self.logger.info(f"Reading page {page}: {search_url}")
            html_content = self.get_dynamic_page_playwright(search_url, waiting_time=5)
            # html_content = self.get_dynamic_page_selenium(search_url, waiting_time=3)

            if not html_content:
                continue

            soup = self.parse_html(html_content)
            if not soup:
                continue
            body = soup.body

            input_messages = [
                SystemMessage(content=JOB_SEARCH_SYSTEM_PROMPT),
                HumanMessage(content=JOB_SEARCH_HUMAN_PROMPT.format(
                    base_url = self.get_base_url(base_url), 
                    html_content = body, 
                    job_url_examples = "; ".join(examples)
                    ))
            ]

            jobs = self.llm_session.search_job(input_messages)
            # TODO get details

        print(jobs)
        return jobs

    def get_job_details_with_llm(self, job_url: str) -> Optional[Dict[str, Any]]:
        # TODO : Write docstring
        pass

