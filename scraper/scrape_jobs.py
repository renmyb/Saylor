import os
import json
import feedparser

def parse_rss(url, source):
    feed = feedparser.parse(url)
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
            "url": "https://www.bluewateryachting.com/rss/jobs",  # replace if needed
            "source": "Bluewater"
        },
        {
            "url": "https://www.dockwalk.com/jobs.rss",  # replace if needed
            "source": "Dockwalk"
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
