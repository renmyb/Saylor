import os
import json
from playwright.async_api import async_playwright

async def scrape_bluewater(page):
    print("🔍 Visiting Bluewater...")
    await page.goto("https://www.bluewateryachting.com/yacht-crew-job-list")
    await page.wait_for_selector("div.job-title", timeout=15000)  # 15 seconds timeout

    # 📸 Save screenshot after page loads
    os.makedirs("debug", exist_ok=True)
    await page.screenshot(path="debug/bluewater_loaded.png", full_page=True)

    job_elements = await page.query_selector_all("div.job-title")

    jobs = []
    for job in job_elements:
        title = await job.inner_text()
        link_tag = await job.query_selector("a")
        link = await link_tag.get_attribute("href") if link_tag else None

        if title and link:
            jobs.append({
                "title": title.strip(),
                "location": "Bluewater",
                "link": f"https://www.bluewateryachting.com{link.strip()}"
            })

    print(f"✅ Found {len(jobs)} jobs on Bluewater")
    return jobs

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
    import asyncio
    asyncio.run(scrape())
