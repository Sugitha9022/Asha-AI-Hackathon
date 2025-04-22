import requests
import json
from pathlib import Path
from typing import Dict, List, Any
import os

# Mock data paths
# Ensure absolute mock data paths using os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MOCK_JOBS_PATH = Path(os.path.join(BASE_DIR, "../data", "mock_jobs.json"))
MOCK_EVENTS_PATH = Path(os.path.join(BASE_DIR, "../data", "mock_events.json"))

def get_jobs(filters=None):
    """Load mock jobs from external file and apply filters"""
    if MOCK_JOBS_PATH.exists():
        with open(MOCK_JOBS_PATH, "r") as f:
            mock_jobs = json.load(f)
    else:
        mock_jobs = []

    return apply_filters(mock_jobs, filters or {})

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

    try:
        with open(MOCK_EVENTS_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def get_mentorships() -> List[Dict]:
    """Get mentorship programs"""
    # In a real implementation, this would call an API
    return [
        {"name": "Tech Career Path", "mentor": "Riya Sharma (Google)", "focus": "Software Engineering"},
        {"name": "Entrepreneurship Guide", "mentor": "Priya Patel (Founder, SheVentures)", "focus": "Startups"}
    ]
