import os
import json
import requests
from bs4 import BeautifulSoup

def fetch_bluewater():
    url = "https://www.bluewateryachting.com/yacht-crew-job-list"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []
    for card in soup.select("div.jobs-listing div.job"):
        title = card.select_one("h3")
        link = card.select_one("a")
        location = card.select_one("p")

        if title and link:
            jobs.append({
                "title": title.text.strip(),
                "location": location.text.strip() if location else "N/A",
                "link": "https://www.bluewateryachting.com" + link["href"],
                "source": "Bluewater"
            })
    return jobs

def fetch_crewseekers():
    url = "https://www.crewseekers.net/crew-positions/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []
    for card in soup.select("div.view-content div.views-row"):
        title = card.select_one("h3")
        link = card.select_one("a[href]")
        location = card.select_one(".views-field-field-position-country")

        if title and link:
            jobs.append({
                "title": title.text.strip(),
                "location": location.text.strip() if location else "N/A",
                "link": "https://www.crewseekers.net" + link["href"],
                "source": "CrewSeekers"
            })
    return jobs

def deduplicate_jobs(jobs):
    seen = set()
    unique = []
    for job in jobs:
        key = (job["title"], job["link"])
        if key not in seen:
            seen.add(key)
            unique.append(job)
    return unique

def main():
    all_jobs = fetch_bluewater() + fetch_crewseekers()
    unique_jobs = deduplicate_jobs(all_jobs)

    os.makedirs("jobs", exist_ok=True)
    with open("jobs/jobs.json", "w") as f:
        json.dump(unique_jobs, f, indent=2)

    print(f"✅ Saved {len(unique_jobs)} jobs to jobs/jobs.json")

if __name__ == "__main__":
    main()
