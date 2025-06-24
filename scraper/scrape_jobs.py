import feedparser
import json

FEED_URL = "https://www.yotspot.com/feed/job.xml"

def fetch_yotspot_jobs():
    feed = feedparser.parse(FEED_URL)
    jobs = []

    for entry in feed.entries:
        job = {
            "title": entry.title,
            "location": entry.get("location", "Unknown"),
            "link": entry.link
        }
        jobs.append(job)

    return jobs

if __name__ == "__main__":
    jobs = fetch_yotspot_jobs()

    # Write to jobs/jobs.json
    with open("jobs/jobs.json", "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"✅ Fetched {len(jobs)} jobs and saved to jobs/jobs.json")
