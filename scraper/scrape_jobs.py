import json
from datetime import datetime

jobs = [
    {
        "title": "Deckhand – MY in Monaco",
        "location": "Monaco",
        "link": "https://www.yotspot.com/job-example-1",
        "source": "Yotspot",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    },
    {
        "title": "Engineer – SY in Palma",
        "location": "Palma de Mallorca",
        "link": "https://www.bluewateryachting.com/job-example-2",
        "source": "Bluewater",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
]

with open("jobs/jobs.json", "w") as f:
    json.dump(jobs, f, indent=2)
