import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_jobs():
    jobs = []

    urls = [
        "https://www.bluewateryachting.com/yacht-crew-job-list",
        "https://www.dockwalk.com/jobs"
    ]

    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            if "bluewater" in url:
                for job in soup.select(".job-card"):
                    title = job.select_one(".job-title")
                    location = job.select_one(".job-location")
                    link = job.select_one("a")

                    if title and link:
                        jobs.append({
                            "title": title.text.strip(),
                            "location": location.text.strip() if location else "N/A",
                            "link": link["href"]
                        })

            if "dockwalk" in url:
                for job in soup.select(".JobCardstyles__JobCardWrapper-sc-1bsod2n-0"):
                    title = job.select_one("h2")
                    location = job.select_one("p")
                    link = job.find("a")

                    if title and link:
                        jobs.append({
                            "title": title.text.strip(),
                            "location": location.text.strip() if location else "N/A",
                            "link": "https://www.dockwalk.com" + link["href"]
                        })

        except Exception as e:
            print(f"Error scraping {url}: {e}")

    os.makedirs("jobs", exist_ok=True)
    with open("jobs/jobs.json", "w") as f:
        json.dump(jobs, f, indent=2)

if __name__ == "__main__":
    scrape_jobs()
