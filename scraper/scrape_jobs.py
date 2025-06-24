import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_bluewater():
    url = "https://www.bluewateryachting.com/yacht-crew-job-list"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []
    listings = soup.select("div.job-listing div.job-title a")

    for a in listings[:25]:  # first 25 jobs
        title = a.get_text(strip=True)
        link = "https://www.bluewateryachting.com" + a.get("href", "#")
        jobs.append({
            "title": f"{title} (Bluewater)",
            "location": "N/A",
            "link": link,
            "timestamp": datetime.utcnow().isoformat()
        })

    return jobs

def scrape_dockwalk():
    url = "https://www.dockwalk.com/jobs"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []
    cards = soup.select("a[href^='/jobs/']")

    seen = set()
    for a in cards[:20]:  # First 20
        href = a.get("href")
        title = a.get_text(strip=True)

        if href and title and href not in seen:
            seen.add(href)
            jobs.append({
                "title": f"{title} (Dockwalk)",
                "location": "N/A",
                "link": "https://www.dockwalk.com" + href,
                "timestamp": datetime.utcnow().isoformat()
            })

    return jobs

if __name__ == "__main__":
    all_jobs = []

    try:
        all_jobs.extend(scrape_bluewater())
    except Exception as e:
        print("Bluewater failed:", e)

    try:
        all_jobs.extend(scrape_dockwalk())
    except Exception as e:
        print("Dockwalk failed:", e)

    os.makedirs("jobs", exist_ok=True)
    with open("jobs/jobs.json", "w") as f:
        json.dump(all_jobs, f, indent=2)

    print(f"✅ Fetched {len(all_jobs)} jobs and saved to jobs/jobs.json")
