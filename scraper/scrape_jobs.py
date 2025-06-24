import asyncio
import os
import json
from playwright.async_api import async_playwright

async def scrape_bluewater(page):
    print("🔍 Visiting Bluewater...")
    await page.goto("https://www.bluewateryachting.com/yacht-crew-job-list", timeout=60000)

    try:
        await page.wait_for_selector("div.jobs-listing", timeout=30000)  # extended wait
        jobs = await page.query_selector_all("div.jobs-listing > div.job")

        job_data = []

        for job in jobs:
            try:
                title = await job.query_selector_eval("h3", "el => el.textContent.trim()")
                location = await job.query_selector_eval("p", "el => el.textContent.trim()")
                link = await job.query_selector_eval("a", "el => el.href")
                job_data.append({
                    "title": title,
                    "location": location,
                    "link": link
                })
            except Exception as e:
                print(f"⚠️ Skipped job: {e}")
                continue

        print(f"✅ Found {len(job_data)} jobs on Bluewater")
        return job_data

    except Exception as e:
        print(f"❌ Bluewater scrape failed: {e}")
        os.makedirs("debug", exist_ok=True)
        await page.screenshot(path="debug/bluewater_page.png", full_page=True)
        return []

async def scrape():
    all_jobs = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        bluewater_jobs = await scrape_bluewater(page)
        all_jobs.extend(bluewater_jobs)

        await browser.close()

    os.makedirs("jobs", exist_ok=True)
    with open("jobs/jobs.json", "w") as f:
        json.dump(all_jobs, f, indent=2)

    print(f"📦 Saved {len(all_jobs)} jobs to jobs/jobs.json")

if __name__ == "__main__":
    asyncio.run(scrape())
