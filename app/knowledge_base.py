from typing import Dict, List, Optional
import json
from pathlib import Path


class KnowledgeBase:
    def __init__(self):
        with open("/Users/sugithar/Desktop/asha-bot/data/faqs.json", "r") as f:
            self.faq_data = json.load(f)
        self.faqs = self._load_faqs
        self.resources = self._load_resources()
        # self.faqs = {
        #     "free": "Yes, all services are completely free for women professionals",
        #     "industr": "We partner with tech, finance, healthcare and education companies",
        #     "python": "We have many Python opportunities. Here are some: <python job listings>",
        #     "data science": "Looking for data science roles? Try these resources...",
        #     "contract": "We have contract positions available. Searching now...",
        #     "restart": "We specialize in career restart programs and returnships"
        # }

    @staticmethod
    def _load_faqs(self):
        try:
            with open("/Users/sugithar/Desktop/asha-bot/data/faqs.json") as f:
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
        """Returns the best matching FAQ answer based on input question"""
        question = question.lower().strip()
        for q, a in self.faq_data.items():
            if q.lower() in question or question in q.lower():
                return a
        return "Sorry, I couldn't find an answer to that FAQ."

# class KnowledgeBase:
#     def __init__(self):
#         self.faqs = self._load_faqs()
#         self.resources = self._load_resources()
#
#     def _load_faqs(self) -> Dict[str, str]:
#         faq_path = Path("data/faqs.json")
#         if faq_path.exists():
#             with open(faq_path, "r") as f:
#                 return json.load(f)
#         return {
#             "What is JobsForHer?": "JobsForHer is a platform dedicated to helping women restart their careers.",
#             "How can I find mentors?": "We offer mentorship programs through our partner network. Ask me about mentorship opportunities!",
#             "Are there remote jobs?": "Yes! Many of our job listings offer remote work options."
#         }

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

    # def get_faq_answer(self, question: str) -> Optional[str]:
    #     """Find the best matching FAQ answer using simple keyword matching"""
    #     question_lower = question.lower()
    #     for q, a in self.faqs.items():
    #         if any(keyword in question_lower for keyword in q.lower().split()[:3]):
    #             return a
    #     return None

    def get_resources(self, category: str = None) -> List[Dict]:
        """Get empowerment resources, optionally filtered by category"""
        if category:
            return [r for r in self.resources if category.lower() in r.get("type", "").lower()]
        return self.resources