from scrappers.welcome_to_the_jungle_scraper import WelcomeToTheJungleScraper
from scrappers.free_work_scraper import FreeWorkScraper


def main():
    print("Hello World!")

    try:
        scraper = WelcomeToTheJungleScraper()
        scraper = FreeWorkScraper()
        jobs = scraper.search_jobs("Data Engineer", "Paris", num_pages=1)
        print(f"Found {len(jobs)} jobs:")
        print("---")
        # for job in jobs:
        #     print(f"Title: {job['title']}")
        #     print(f"Company: {job['company']}")
        #     print(f"Location: {job['location']}")
        #     print(f"Description: {job['description']}")
        #     print(f"Date Posted: {job['posted_time']}")
        #     print(f"Contract Type: {job['contract_type']}")
        #     print(f"Remote status: {job['remote_status']}")
        #     print(f"URL: {job['url']}")
        #     print("---")
        print(jobs[0]["description"])
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
