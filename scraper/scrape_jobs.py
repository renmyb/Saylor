import asyncio
import json
import os
from datetime import datetime
from playwright.async_api import async_playwright

async def scrape_bluewater(page):
    print("🔵 Visiting Bluewater...")
    await page.goto("https://www.bluewateryachting.com/yacht-crew-job-list", timeout=60000)
    
    # Save screenshot BEFORE waiting
    os.makedirs("debug", exist_ok=True)
    await page.screenshot(path="debug/bluewater_page.png", full_page=True)
    print("📸 Screenshot saved to debug/bluewater_page.png")
    
    # Try to wait for job elements
    await page.wait_for_selector("div.job-title a", timeout=20000)

    jobs = []
    job_elements = await page.query_selector_all("div.job-title a")
    print(f"🧠 Found {len(job_elements)} job elements")

    for el in job_elements[:25]:
        title = await el.inner_text()
        href = await el.get_attribute("href")
        if title and href:
            jobs.append({
                "title": f"{title.strip()} (Bluewater)",
                "location": "N/A",
                "link": "https://www.bluewateryachting.com" + href,
                "timestamp": datetime.utcnow().isoformat()
            })

    return jobs

async def scrape():
    all_jobs = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            bluewater_jobs = await scrape_bluewater(page)
            print(f"✅ Scraped {len(bluewater_jobs)} Bluewater jobs")
            all_jobs.extend(bluewater_jobs)
        except Exception as e:
            print(f"❌ Bluewater error: {e}")

        await browser.close()

    os.makedirs("jobs", exist_ok=True)
    with open("jobs/jobs.json", "w") as f:
        json.dump(all_jobs, f, indent=2)

    print(f"📦 Saved {len(all_jobs)} jobs to jobs/jobs.json")

if __name__ == "__main__":
    asyncio.run(scrape())
