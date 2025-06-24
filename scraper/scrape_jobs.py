import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os

def scrape_bluewater():
    print("🔵 Scraping Bluewater...")
    jobs = []
    url = "https://www.bluewateryachting.com/yacht-crew-job-list"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    job_cards = soup.select("div.job-listing > div.row")

    for card in job_cards[:20]:  # Limit to 20 jobs
        title_tag = card.select_one(".job-title a")
        if not title_tag:
            continue
        title = title_tag.get_text(strip=True)
        link = "https://www.bluewateryachting.com" + title_tag["href"]
        location = card.select_one(".job-location")
        location = location.get_text(strip=True) if location else "N/A"

        jobs.append({
            "title": f"{title} (Bluewater)",
            "location": location,
            "link": link,
            "timestamp": datetime.utcnow().isoformat()
        })

    return jobs


def scrape_dockwalk():
    print("🟢 Scraping Dockwalk...")
    jobs = []
    url = "https://www.dockwalk.com/jobs"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    job_cards = soup.select("div.SearchResults__Card-sc")  # fallback for Dockwalk

    for card in job_cards[:15]:  # Limit to 15 jobs
        title_tag = card.find("a", href=True)
        title = title_tag.get_text(strip=True) if title_tag else "Job"
        link = "https://www.dockwalk.com" + title_tag["href"] if title_tag else "#"
        location = "Worldwide"

        jobs.append({
            "title": f"{title} (Dockwalk)",
            "location": location,
            "link": link,
            "timestamp": datetime.utcnow().isoformat()
        })

    return jobs


if __name__ == "__main__":
    all_jobs = []

    try:
        all_jobs.extend(scrape_bluewater())
    except Exception as e:
        print(f"⚠️ Bluewater error: {e}")

    try:
        all_jobs.extend(scrape_dockwalk())
    except Exception as e:
        print(f"⚠️ Dockwalk error: {e}")

    os.makedirs("jobs", exist_ok=True)
    with open("jobs/jobs.json", "w") as f:
        json.dump(all_jobs, f, indent=2)

    print(f"✅ Saved {len(all_jobs)} jobs to jobs/jobs.json")
