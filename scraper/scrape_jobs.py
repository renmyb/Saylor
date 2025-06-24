import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_test_jobs():
    jobs = []

    # Sample public source - replace with real later
    url = "https://remoteok.com/remote-dev-jobs"  # TEMP public source for example only

    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.content, "html.parser")
        listings = soup.select("tr.job")[:10]

        for row in listings:
            title = row.get("data-position")
            company = row.get("data-company")
            link = "https://remoteok.com" + row.get("data-href")

            if title and company:
                jobs.append({
                    "title": f"{title} – {company}",
                    "location": "Worldwide",
                    "link": link,
                    "timestamp": datetime.utcnow().isoformat()
                })

    except Exception as e:
        print("Error scraping:", e)

    with open("jobs/jobs.json", "w") as f:
        json.dump(jobs, f, indent=2)

if __name__ == "__main__":
    scrape_test_jobs()
