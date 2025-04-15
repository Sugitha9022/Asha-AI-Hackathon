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

# Import modules using absolute imports
from app.nlp_engine import process_input
from app.dialog_manager import DialogManager
from app.context_manager import ContextManager
from app.bias_handler import check_for_bias

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
        intent, entities = process_input(user_input)

        # Check for bias
        bias_detected, bias_type = bias_handler(user_input)
        if bias_detected:
            return {
                "response": f"Gender bias detected. {bias_handler.get_positive_response(bias_type)}",
                "session_id": session_id,
                "bias_detected": True
            }

        # Manage dialog
        dialog_manager.update_dialog(session_id, user_input, intent)

        # Generate response
        response = dialog_manager.generate_response(intent, entities, context)

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