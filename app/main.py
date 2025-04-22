from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import json
from pathlib import Path
from datetime import datetime
import uuid
import os
from fuzzywuzzy import process

# Import modules using absolute imports
from app.nlp_engine import process_input
from app.dialog_manager import DialogManager
from app.context_manager import ContextManager
from app.bias_handler import check_for_bias
from app.knowledge_base import KnowledgeBase  # Ensure the KnowledgeBase class is imported

app = FastAPI()

# Get the base directory of your project
BASE_DIR = Path(__file__).resolve().parent.parent

# Configure static files
static_dir = os.path.join(BASE_DIR, "static")
templates_dir = os.path.join(BASE_DIR, "templates")

# Create directories if they don't exist
os.makedirs(static_dir, exist_ok=True)
os.makedirs(templates_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

# Initialize components
context_manager = ContextManager()
dialog_manager = DialogManager()
bias_handler = check_for_bias

class ChatInput(BaseModel):
    message: str
    session_id: str = None


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/chat")
async def chat(chat_input: ChatInput):
    try:
        # Get or create session
        session_id = chat_input.session_id or str(uuid.uuid4())
        context = context_manager.get_context(session_id)

        # Process input
        user_input = chat_input.message
        print(f"User Input: {user_input}")  # Debugging user input
        intent, entities = process_input(user_input)

        # Debugging intent and entities
        print(f"Intent: {intent}, Entities: {entities}")

        # Check for bias
        bias_detected, bias_type = bias_handler(user_input)
        if bias_detected:
            return {
                "response": f"Gender bias detected. {bias_handler.get_positive_response(bias_type)}",
                "session_id": session_id,
                "bias_detected": True
            }

        # Check if the intent is FAQ and process it
        if intent == "faq":
            faq_answer = get_faq_answer(user_input)
            return {
                "response": faq_answer,
                "session_id": session_id,
                "bias_detected": False
            }

        # Manage dialog for other intents
        dialog_manager.update_dialog(session_id, user_input, intent)

        # Generate response
        response = dialog_manager.generate_response(intent, entities, context)

        # Debugging the final response
        print(f"Asha's Response: {response}")

        # Update context
        context_manager.update_context(session_id, {
            "last_interaction": datetime.now().isoformat(),
            "last_intent": intent,
            "conversation_history": context.get("conversation_history", []) + [
                {"user": user_input, "bot": response}
            ]
        })

        return {
            "response": response,
            "session_id": session_id,
            "bias_detected": False
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_faq_answer(user_input: str) -> str:
    """Fetch FAQ answer using fuzzy matching"""
    # Define a set of FAQ questions and their answers
    faq_data = {
        "How do I restart my career?": "We offer tailored programs for career re-entry, including mentorship and returnships. Just ask me about 'returnships' to get started!",
        "Can I get career advice specific to my background?": "Absolutely! Asha personalizes guidance based on your skills, interests, and goals. Just tell me a bit about yourself.",
        "What industries do you work with?": "We partner with companies across tech, finance, healthcare, and more.",
        "Will you remember what we talked about earlier?": "Yes! Asha stores context securely to give you a smooth, continuous experience. You can always pick up where you left off.",
        "Can I connect with other women professionals?": "Yes! We integrate with women’s professional networks and communities to help you network, find mentorship, and grow your career.",
        "Who powers Asha's career advice?": "Asha uses advanced Large Language Models (LLMs) to provide smart, adaptive support customized for women’s unique career paths.",
        "Is Asha designed for women like me?": "Yes! Asha is built to recognize when you're seeking gender-specific support and mitigates bias to ensure fair, respectful advice.",
        "Is my personal data safe here?": "Your data is encrypted and protected. We follow strict guardrails to prevent misuse or exposure of sensitive information.",
        "What security measures are in place?": "We use end-to-end encryption, secure session handling, and privacy-first design to keep your information safe at all times.",
        "Will Asha improve over time?": "Yes! Asha learns from anonymized patterns (not your personal data) to continuously enhance performance and support quality.",
        "What if something goes wrong?": "You’ll receive clear feedback if there's a hiccup, and our support team is here to help. You can also report issues directly."
    }

    # Use fuzzy matching to find the best matching FAQ
    best_match, score = process.extractOne(user_input, faq_data.keys())

    if score > 70:  # If a good match is found (score threshold can be adjusted)
        return faq_data[best_match]
    else:
        return "Sorry, I couldn't find an answer to that. Can you please rephrase?"


