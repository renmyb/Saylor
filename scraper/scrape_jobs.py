import json
import feedparser
from datetime import datetime

def parse_yotspot_rss():
    jobs = []
    feed_url = "https://www.yotspot.com/feed/jobs.rss"
    feed = feedparser.parse(feed_url)

    for entry in feed.entries[:30]:  # Limit to 30 jobs
        job = {
            "title": entry.title,
            "location": "Various",
            "link": entry.link,
            "timestamp": datetime.utcnow().isoformat()
        }
        jobs.append(job)

    return jobs

def save_jobs(jobs):
    with open("jobs/jobs.json", "w") as f:
        json.dump(jobs, f, indent=2)

if __name__ == "__main__":
    all_jobs = []
    all_jobs += parse_yotspot_rss()
    save_jobs(all_jobs)
