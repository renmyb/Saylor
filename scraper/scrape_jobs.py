import asyncio
import os
import json
from playwright.async_api import async_playwright

async def scrape_bluewater(page):
    print("🔍 Visiting Bluewater...")
    await page.goto("https://www.bluewateryachting.com/yacht-crew-job-list")
    
    # Wait up to 10 seconds for jobs to appear
    await page.wait_for_selector("ul.job-listings > li", timeout=10000)

    jobs = await page.query_selector_all("ul.job-listings > li")
    job_data = []

    for job in jobs:
        try:
            title = await job.query_selector_eval("h3", "el => el.textContent")
            location = await job.query_selector_eval("span.location", "el => el.textContent")
            link = await job.query_selector_eval("a", "el => el.href")

            job_data.append({
                "title": title.strip(),
                "location": location.strip(),
                "link": link.strip()
            })
        except Exception as e:
            print(f"⚠️ Skipped one job due to error: {e}")
            continue

    print(f"✅ Found {len(job_data)} jobs on Bluewater")
    return job_data

async def scrape():
    all_jobs = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            bluewater_jobs = await scrape_bluewater(page)
            all_jobs.extend(bluewater_jobs)
        except Exception as e:
            print(f"❌ Error scraping Bluewater: {e}")

        await browser.close()

    os.makedirs("jobs", exist_ok=True)
    with open("jobs/jobs.json", "w") as f:
        json.dump(all_jobs, f, indent=2)

    print(f"📦 Saved {len(all_jobs)} jobs to jobs/jobs.json")

if __name__ == "__main__":
    asyncio.run(scrape())
