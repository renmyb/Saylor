import asyncio
import json
import os
from datetime import datetime
from playwright.async_api import async_playwright

async def scrape_bluewater(page):
    await page.goto("https://www.bluewateryachting.com/yacht-crew-job-list", timeout=60000)
    await page.wait_for_selector("div.job-title a", timeout=15000)
    links = await page.query_selector_all("div.job-title a")

    jobs = []
    for link in links[:25]:  # First 25
        title = await link.inner_text()
        href = await link.get_attribute("href")
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
        browser = await p.chromium.launch()
        page = await browser.new_page()

        try:
            bluewater_jobs = await scrape_bluewater(page)
            all_jobs.extend(bluewater_jobs)
        except Exception as e:
            print("Error scraping Bluewater:", e)

        await browser.close()

    os.makedirs("jobs", exist_ok=True)
    with open("jobs/jobs.json", "w") as f:
        json.dump(all_jobs, f, indent=2)
    print(f"✅ Scraped and saved {len(all_jobs)} jobs")

if __name__ == "__main__":
    asyncio.run(scrape())
