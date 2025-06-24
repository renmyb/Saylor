import json
import os
from playwright.sync_api import sync_playwright

def fetch_bluewater(page):
    print("🔵 Bluewater")
    jobs = []
    page.goto("https://www.bluewateryachting.com/yacht-crew-job-listings", timeout=60000)
    page.wait_for_selector(".job-listing", timeout=30000)
    cards = page.query_selector_all(".job-listing")
    for card in cards:
        title = card.query_selector("h4").inner_text()
        link = card.query_selector("a").get_attribute("href")
        location = card.query_selector(".location").inner_text() if card.query_selector(".location") else "N/A"
        jobs.append({
            "title": title,
            "link": "https://www.bluewateryachting.com" + link,
            "location": location,
            "source": "Bluewater"
        })
    return jobs

def fetch_crewseekers(page):
    print("🟠 CrewSeekers")
    jobs = []
    page.goto("https://www.crewseekers.net/crew-positions/", timeout=60000)
    page.wait_for_selector(".views-row", timeout=30000)
    cards = page.query_selector_all(".views-row")
    for card in cards:
        title = card.query_selector("h3").inner_text()
        link = card.query_selector("a").get_attribute("href")
        jobs.append({
            "title": title,
            "link": "https://www.crewseekers.net" + link,
            "location": "N/A",
            "source": "CrewSeekers"
        })
    return jobs

def fetch_yacrew(page):
    print("🟢 YaCrew")
    jobs = []
    page.goto("https://www.yacrew.com/find-a-job/", timeout=60000)
    page.wait_for_selector(".job_item", timeout=30000)
    cards = page.query_selector_all(".job_item")
    for card in cards:
        title = card.query_selector("h2").inner_text()
        link = card.query_selector("a").get_attribute("href")
        jobs.append({
            "title": title,
            "link": "https://www.yacrew.com" + link,
            "location": "N/A",
            "source": "YaCrew"
        })
    return jobs

def fetch_luxuryyachtgroup(page):
    print("🟤 Luxury Yacht Group")
    jobs = []
    page.goto("https://www.luxyachts.com/jobs", timeout=60000)
    page.wait_for_selector(".job-listing", timeout=30000)
    cards = page.query_selector_all(".job-listing")
    for card in cards:
        title = card.query_selector("h4").inner_text()
        link = card.query_selector("a").get_attribute("href")
        jobs.append({
            "title": title,
            "link": "https://www.luxyachts.com" + link,
            "location": "N/A",
            "source": "LuxuryYachtGroup"
        })
    return jobs

def fetch_allcruisejobs(page):
    print("🔷 All Cruise Jobs")
    jobs = []
    page.goto("https://www.allcruisejobs.com/yacht/", timeout=60000)
    page.wait_for_selector(".box", timeout=30000)
    cards = page.query_selector_all(".box")
    for card in cards:
        title = card.query_selector("h2").inner_text()
        link = card.query_selector("a").get_attribute("href")
        jobs.append({
            "title": title,
            "link": "https://www.allcruisejobs.com" + link,
            "location": "N/A",
            "source": "AllCruiseJobs"
        })
    return jobs

def main():
    all_jobs = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        all_jobs += fetch_bluewater(page)
        all_jobs += fetch_crewseekers(page)
        all_jobs += fetch_yacrew(page)
        all_jobs += fetch_luxuryyachtgroup(page)
        all_jobs += fetch_allcruisejobs(page)

        browser.close()

    # Deduplicate
    seen = set()
    unique_jobs = []
    for job in all_jobs:
        key = (job["title"], job["link"])
        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)

    os.makedirs("jobs", exist_ok=True)
    with open("jobs/jobs.json", "w") as f:
        json.dump(unique_jobs, f, indent=2)

    print(f"✅ Saved {len(unique_jobs)} jobs to jobs/jobs.json")

if __name__ == "__main__":
    main()
