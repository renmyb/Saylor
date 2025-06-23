import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_jobs():
    jobs = []

    # Example source: yaCrew.com (hypothetical, scrape properly from public sources)
    urls = [
        "https://someyachtjobboard.com/jobs",
        "https://anothercrewsite.org/latest-jobs"
    ]

    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            job_cards = soup.select(".job-card")  # Adjust this selector for real sites

            for card in job_cards:
                title = card.select_one(".job-title").get_text(strip=True)
                location = card.select_one(".location").get_text(strip=True)
                link = card.select_one("a")["href"]

                jobs.append({
                    "title": title,
                    "location": location,
                    "link": link,
                    "timestamp": datetime.utcnow().isoformat()
                })

        except Exception as e:
            print(f"Failed to scrape {url}: {e}")

    with open("jobs/jobs.json", "w") as f:
        json.dump(jobs[:100], f, indent=2)  # save top 100 only

if __name__ == "__main__":
    scrape_jobs()
