from typing import List, Dict, Any
from app.knowledge_base import KnowledgeBase

kb = KnowledgeBase()


class ResponseGenerator:
    def __init__(self):
        pass

    @staticmethod
    def generate(response_type: str, data=None) -> str:
        if response_type == "jobs":
            if not data:
                return "No current job openings matching your criteria."
            return "\n".join(
                f"📌 {job['title']} at {job['company']}\n"
                f"   Location: {job.get('location', 'Remote')}\n"
                f"   Type: {job.get('type', 'Full-time')}\n"
                for job in data[:3]
            )

        elif response_type == "events":
            if not data:
                return "No upcoming events currently."
            return "\n".join(
                f"📅 {event['name']}\n"
                f"   When: {event.get('date', 'TBD')}\n"
                f"   Where: {event.get('location', 'Online')}\n"
                for event in data[:3]
            )

        elif response_type == "greeting":
            return ("Hello! I'm Asha, your career assistant for women in tech.\n"
                    "I can help with:\n- Job opportunities\n- Career events\n- Mentorship\n"
                    "What would you like to explore today?")

        elif response_type == "fallback":
            return "I'm here to support your career growth. How can I help?"

        elif response_type == "faq":
            return data if data else "I can connect you with a human advisor if needed"

        return "I can help with jobs and career resources. What would you like to know?"

    @staticmethod
    def _format_jobs(jobs: List[Dict]) -> str:
        if not jobs:
            return "Currently no job listings match your criteria. Try different filters or check back later."

        response = "Here are some job opportunities:\n\n"
        for job in jobs[:3]:  # Limit to 3 jobs
            response += (
                f"🏢 {job.get('title', 'N/A')} at {job.get('company', 'N/A')}\n"
                f"📍 {job.get('location', 'Remote')} | {job.get('type', 'Full-time')}\n"
                f"🔗 {job.get('url', 'Apply on our website')}\n\n"
            )
        return response + "Would you like more details about any of these?"

    @staticmethod
    def _format_events(events: List[Dict]) -> str:
        if not events:
            return "No upcoming events at the moment. Check back soon!"

        response = "Upcoming events for women professionals:\n\n"
        for event in events[:3]:
            response += (
                f"📅 {event.get('name', 'Event')}\n"
                f"🗓 {event.get('date', 'TBD')} | "
                f"📍 {event.get('location', 'Online')}\n"
                f"ℹ️ {event.get('description', 'Great networking opportunity!')}\n\n"
            )
        return response

    @staticmethod
    def _format_mentorships(mentorships: List[Dict]) -> str:
        response = "Available mentorship programs:\n\n"
        for program in mentorships:
            response += (
                f"👩‍💼 {program.get('name', 'Mentorship Program')}\n"
                f"🧠 Mentor: {program.get('mentor', 'Industry Expert')}\n"
                f"⭐ Focus: {program.get('focus', 'Career Growth')}\n\n"
            )
        return response + "Would you like help connecting with a mentor?"

    @staticmethod
    def _format_resources(resources: List[Dict]) -> str:
        response = "Empowerment resources:\n\n"
        for resource in resources:
            response += (
                f"📚 {resource.get('title', 'Resource')}\n"
                f"🔗 {resource.get('url', 'Link available on our website')}\n"
                f"💡 Type: {resource.get('type', 'General')}\n\n"
            )
        return response