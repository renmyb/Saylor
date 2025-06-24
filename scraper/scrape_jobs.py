import os
import json
import feedparser

def parse_rss(url, source):
    print(f"Fetching from {source}: {url}")
    feed = feedparser.parse(url)
    
    if feed.bozo:
        print(f"⚠️ Error parsing {source}: {feed.bozo_exception}")
        return []
    
    if not hasattr(feed, "entries") or len(feed.entries) == 0:
        print(f"❌ No entries found in {source}")
        return []
    
    jobs = []
    for entry in feed.entries:
        jobs.append({
            "title": entry.title,
            "location": entry.get("location", "N/A"),
            "link": entry.link,
            "source": source
        })
    return jobs

def main():
    rss_sources = [
        {
            "url": "https://www.dockwalk.com/jobs.rss",
            "source": "Dockwalk"
        },
        {
            "url": "https://www.bluewateryachting.com/rss/jobfeed",
            "source": "Bluewater"
        }
    ]

    all_jobs = []
    for source in rss_sources:
        jobs = parse_rss(source["url"], source["source"])
        print(f"✔️ {len(jobs)} jobs from {source['source']}")
        all_jobs.extend(jobs)

    os.makedirs("jobs", exist_ok=True)
    with open("jobs/jobs.json", "w") as f:
        json.dump(all_jobs, f, indent=2)

    print(f"✅ Saved {len(all_jobs)} total jobs to jobs/jobs.json")

if __name__ == "__main__":
    main()
