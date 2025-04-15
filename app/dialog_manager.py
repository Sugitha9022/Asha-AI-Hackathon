from app.integration_layer import get_jobs, get_events, get_mentorships
from app.knowledge_base import KnowledgeBase
from app.response_generator import ResponseGenerator


class DialogManager:
    def __init__(self):
        self.conversation_states = {}
        self.response_gen = ResponseGenerator()
        self.knowledge_base = KnowledgeBase()  # Create instance

    def update_dialog(self, session_id: str, user_input: str, intent: str):
        """Track conversation state and history"""
        if session_id not in self.conversation_states:
            self.conversation_states[session_id] = {
                "state": "initial",
                "history": []
            }

        # Update state based on intent
        if intent in ["greeting", "job_search", "events", "mentorship", "resources"]:
            self.conversation_states[session_id]["state"] = intent

        # Keep last 5 messages in history
        self.conversation_states[session_id]["history"].append(user_input)
        self.conversation_states[session_id]["history"] = self.conversation_states[session_id]["history"][-5:]

    @staticmethod
    def _handle_typos(self, text: str) -> str:
        typo_map = {
            "wokshop": "workshop",
            "datascience": "data science",
            "pthon": "python"
        }
        for typo, correct in typo_map.items():
            text = text.replace(typo, correct)
        return text

    def generate_response(self, intent: str, entities: dict, context: dict = None) -> str:
        """Generate appropriate response based on intent and entities"""
        context = context or {}
        last_input = context.get("last_user_input", "")

        # Handle unknown intents
        if intent == "unknown":
            if entities.get("domain"):
                intent = "job_search"
            elif any(kw in last_input.lower() for kw in ["event", "workshop"]):
                intent = "events"
            else:
                # Call on instance, not class
                faq_answer = self.knowledge_base.get_faq_answer(last_input)
                return faq_answer if faq_answer else self.response_gen.generate("fallback")

        # Handle specific intents
        if intent == "greeting":
            return self.response_gen.generate("greeting")

        elif intent == "job_search":
            filters = {
                "description": entities.get("domain"),
                "location": entities.get("location"),
                "type": entities.get("job_type"),
                "skill": entities.get("skill", [])
            }
            filters = {k: v for k, v in filters.items() if v}

            jobs = get_jobs(filters)
            return self.response_gen.generate("jobs", jobs)

        elif intent == "events":
            events = get_events()
            return self.response_gen.generate("events", events)

        elif intent == "mentorship":
            mentorships = get_mentorships()
            return self.response_gen.generate("mentorships", mentorships)

        elif intent == "resources":
            return self.response_gen.generate("resources")

        return self.response_gen.generate("fallback")