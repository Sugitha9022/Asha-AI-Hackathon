import requests
import json
from pathlib import Path
from typing import Dict, List, Any

# Mock data paths
MOCK_JOBS_PATH = Path("/Users/sugithar/Desktop/asha-bot/data/mock_jobs.json")
MOCK_EVENTS_PATH = Path("/Users/sugithar/Desktop/asha-bot/data/mock_events.json")


def get_jobs(filters=None):
    """Better mock data with domain support"""
    mock_jobs = [
        {
            "title": "Machine Learning Engineer",
            "company": "WomenTech AI",
            "location": "Remote",
            "type": "Full-time",
            "description": "aiml python tensorflow",
            "url": "#"
        },
        {
            "title": "AI Research Scientist",
            "company": "FemTech Research",
            "location": "Bangalore",
            "type": "Full-time",
            "description": "aiml deep learning",
            "url": "#"
        }
    ]

    if not filters:
        return mock_jobs

    filtered = []
    for job in mock_jobs:
        match = True
        for key, value in filters.items():
            if key in job:
                if str(value).lower() not in str(job[key]).lower():
                    match = False
                    break
        if match:
            filtered.append(job)

    return filtered


def apply_filters(items: List[Dict], filters: Dict[str, Any]) -> List[Dict]:
    """Enhanced filtering"""
    if not filters:
        return items

    filtered = []
    for item in items:
        match = True
        for key, value in filters.items():
            if key in item:
                item_value = str(item[key]).lower()
                filter_value = str(value).lower()
                if filter_value not in item_value:
                    match = False
                    break
        if match:
            filtered.append(item)
    return filtered


def get_events() -> List[Dict]:
    """Get events from API or mock data"""
    try:
        response = requests.get("https://api.exampleevents.com/women-events")
        if response.status_code == 200:
            return response.json()
    except:
        pass

    with open(MOCK_EVENTS_PATH, "r") as f:
        return json.load(f)


def get_mentorships() -> List[Dict]:
    """Get mentorship programs"""
    # In a real implementation, this would call an API
    return [
        {"name": "Tech Career Path", "mentor": "Riya Sharma (Google)", "focus": "Software Engineering"},
        {"name": "Entrepreneurship Guide", "mentor": "Priya Patel (Founder, SheVentures)", "focus": "Startups"}
    ]
