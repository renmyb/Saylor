import json
import os
from datetime import datetime

# Mock job listings (you can replace this later with real scraping logic)
jobs = [
    {
        "title": "Deckhand – 45m Private Yacht",
        "location": "Monaco",
        "link": "https://www.yotspot.com/job-example-1",
        "source": "Yotspot",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    },
    {
        "title": "Stewardess – Charter Motor Yacht",
        "location": "Antibes",
        "link": "https://www.bluewateryachting.com/job-example-2",
        "source": "Bluewater",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    },
    {
        "title": "Engineer – Sailing Yacht",
        "location": "Palma",
        "link": "https://www.crewseekers.net/job-example-3",
        "source": "CrewSeekers",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
]

# ✅ Ensure the 'jobs' folder exists before writing the file
os.makedirs("jobs", exist_ok=True)

# ✅ Write to jobs/jobs.json
with open("jobs/jobs.json", "w") as f:
    json.dump(jobs, f, indent=2)

print("✅ jobs.json successfully updated.")
