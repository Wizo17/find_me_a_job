from scrappers.welcome_to_the_jungle_scraper import WelcomeToTheJungleScraper
from scrappers.free_work_scraper import FreeWorkScraper
from scrappers.llm_scraper import LLMScraper
from models.llm_session import LLMSession

def main():
    print("Hello World!")

    try:
        # scraper = WelcomeToTheJungleScraper()
        # scraper = FreeWorkScraper()
        # jobs = scraper.search_jobs("Data Engineer", "Paris", num_pages=1)

        llm_session = LLMSession()
        scraper = LLMScraper(llm_session=llm_session)

        # url = "https://www.welcometothejungle.com/fr/jobs?query=Data%20Engineer&page={num_page}&aroundQuery=Paris&sortBy=mostRecent"
        # examples = [
        #     "https://www.welcometothejungle.com/fr/companies/axa/jobs/stage-data-engineer-analyst-cx_malakoff?q=c99d9b57e70ebc54bf7bdbf008a2d9ae&o=4681050a-9db8-4289-afb7-2e7592fe2e97",
        #     "https://www.welcometothejungle.com/fr/companies/accenture-france/jobs/data-engineer-h-f_paris_AF_lGjgWaV?q=c99d9b57e70ebc54bf7bdbf008a2d9ae&o=5b125e3e-795b-4f46-b4a9-5d4f85a91cfa",
        #     "https://www.welcometothejungle.com/fr/companies/renault-digital/jobs/data-engineer-machine-learning-engineer-f-h_boulogne-billancourt?q=c99d9b57e70ebc54bf7bdbf008a2d9ae&o=be355317-6a47-4bad-a469-64880dc240f5"
        # ]

        url = "https://www.free-work.com/fr/tech-it/jobs?query=data%20engineer&page={num_page}&sort=date"
        examples = [
            "https://www.free-work.com/fr/tech-it/data-engineer/job-mission/data-engineer-snowflake-sagemaker",
            "https://www.free-work.com/fr/tech-it/data-engineer/job-mission/data-engineer-snowflake-30",
            "https://www.free-work.com/fr/tech-it/data-engineer/job-mission/data-engineer-f-h-79"
        ]
        # print(scraper.get_base_url(url))
        jobs = scraper.search_jobs_with_llm(base_url=url, num_pages=1, examples=examples)

        print(f"Type {type(jobs)} jobs:")
        # print(f"Found {len(jobs)} jobs:")

        # print(jobs[0]["description"])
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
