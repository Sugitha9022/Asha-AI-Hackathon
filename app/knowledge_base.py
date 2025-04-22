from typing import Dict, List, Optional
import json
from pathlib import Path
import os

# Ensure absolute mock data paths using os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FAQS_PATH = Path(os.path.join(BASE_DIR, "../data", "faqs.json"))


class KnowledgeBase:
    def __init__(self):
        with open(FAQS_PATH, "r") as f:
            self.faq_data = json.load(f)
        self.faqs = self._load_faqs()
        self.resources = self._load_resources()

    def _load_faqs(self):
        try:
            with open(FAQS_PATH, 'r') as f:
                return json.load(f)
        except:
            return {
                "help": "I can help with jobs, events, and mentorship programs",
                "jobs": "Looking for job opportunities? Tell me your preferred domain like AI/ML",
                "events": "We host regular career workshops and networking events",
                "free": "Yes, all services are completely free for women professionals",
                "industry": "We partner with tech, finance, healthcare and education companies",
                "python": "We have many Python opportunities. Here are some: <python job listings>",
                "data science": "Looking for data science roles? Try these resources...",
                "contract": "We have contract positions available. Searching now...",
                "restart": "We specialize in career restart programs and returnships"
            }


    def get_faq_answer(self, question: str) -> str:
        question = question.lower().strip()
        keyword_map = {
            "connect": "We integrate with women’s professional networks to help you find mentors and peers.",
            "network": "We integrate with women’s professional networks to help you find mentors and peers.",
            "mentor": "We offer a variety of mentorship programs tailored to your needs.",
            "mentorship": "We offer a variety of mentorship programs tailored to your needs.",
            "restart": "We specialize in career restart programs and returnships.",
            "returnship": "We specialize in career restart programs and returnships.",
            "jobs": "Looking for job opportunities? Tell me your preferred domain like AI/ML.",
            "events": "We host regular career workshops and networking events.",
            "free": "Yes, all services are completely free for women professionals.",
            "industry": "We partner with tech, finance, healthcare and education companies.",
            "python": "We have many Python opportunities. Here are some: <python job listings>",
            "data science": "Looking for data science roles? Try these resources...",
            "contract": "We have contract positions available. Searching now..."
        }

        """Returns the best matching FAQ answer based on input question"""
        question = question.lower().strip()
        for q, a in self.faq_data.items():
            if q.lower() in question or question in q.lower():
                    return a
        return "Sorry, I couldn't find an answer to that FAQ."

    def _load_resources(self) -> List[Dict]:
        return [
            {
                "title": "Women in Tech Guide",
                "url": "https://example.com/women-in-tech",
                "type": "e-book"
            },
            {
                "title": "Career Reboot Webinar",
                "url": "https://example.com/career-reboot",
                "type": "video"
            }
        ]


    def get_resources(self, category: str = None) -> List[Dict]:
        """Get empowerment resources, optionally filtered by category"""
        if category:
            return [r for r in self.resources if category.lower() in r.get("type", "").lower()]
        return self.resources
