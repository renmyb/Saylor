import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_allcruisejobs():
    url = "https://www.allcruisejobs.com/yacht/"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    jobs = []

    for box in soup.select('.box'):
        title_el = box.select_one('h2')
        link_el = box.select_one('a[href]')
        if title_el and link_el:
            jobs.append({
                "title": title_el.text.strip(),
                "link": "https://www.allcruisejobs.com" + link_el['href'],
                "location": "N/A",
                "source": "AllCruiseJobs"
            })
    return jobs

def scrape_yacrew():
    url = "https://www.yacrew.com/find-a-job/"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    jobs = []

    for job_item in soup.select('.job_item'):
        title_el = job_item.select_one('h2')
        link_el = job_item.select_one('a[href]')
        if title_el and link_el:
            jobs.append({
                "title": title_el.text.strip(),
                "link": "https://www.yacrew.com" + link_el['href'],
                "location": "N/A",
                "source": "YaCrew"
            })
    return jobs

def main():
    all_jobs = []
    try:
        print("📦 Scraping AllCruiseJobs...")
        all_jobs += scrape_allcruisejobs()
    except Exception as e:
        print(f"Failed to fetch AllCruiseJobs: {e}")

    try:
        print("📦 Scraping YaCrew...")
        all_jobs += scrape_yacrew()
    except Exception as e:
        print(f"Failed to fetch YaCrew: {e}")

    os.makedirs("jobs", exist_ok=True)
    with open("jobs/jobs.json", "w") as f:
        json.dump(all_jobs, f, indent=2)

    print(f"✅ Saved {len(all_jobs)} jobs to jobs/jobs.json")

if __name__ == "__main__":
    main()
