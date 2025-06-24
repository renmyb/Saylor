import os
import json
from playwright.sync_api import sync_playwright

def scrape_bluewater(page):
    page.goto("https://www.bluewateryachting.com/yacht-crew-job-list")
    page.wait_for_selector(".job-listing")
    jobs = []
    listings = page.query_selector_all(".job-listing")

    for job in listings:
        try:
            title = job.query_selector(".job-title").inner_text().strip()
            location = job.query_selector(".job-location").inner_text().strip()
            link = job.query_selector("a").get_attribute("href")
            jobs.append({
                "title": title,
                "location": location,
                "link": f"https://www.bluewateryachting.com{link}",
                "source": "Bluewater"
            })
        except:
            continue
    return jobs

def scrape_dockwalk(page):
    page.goto("https://www.dockwalk.com/jobs")
    page.wait_for_selector(".job-title")
    jobs = []
    listings = page.query_selector_all(".job-list-card")

    for job in listings:
        try:
            title = job.query_selector(".job-title").inner_text().strip()
            location = job.query_selector(".location").inner_text().strip()
            link = job.query_selector("a").get_attribute("href")
            jobs.append({
                "title": title,
                "location": location,
                "link": f"https://www.dockwalk.com{link}",
                "source": "Dockwalk"
            })
        except:
            continue
    return jobs

def main():
    all_jobs = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            print("🔵 Bluewater...")
            all_jobs += scrape_bluewater(page)
        except Exception as e:
            print(f"❌ Bluewater failed: {e}")

        try:
            print("🟢 Dockwalk...")
            all_jobs += scrape_dockwalk(page)
        except Exception as e:
            print(f"❌ Dockwalk failed: {e}")

        browser.close()

    os.makedirs("jobs", exist_ok=True)
    with open("jobs/jobs.json", "w") as f:
        json.dump(all_jobs, f, indent=2)

    print(f"✅ Saved {len(all_jobs)} jobs to jobs/jobs.json")

if __name__ == "__main__":
    main()
