# Asha Bot - JobsForHer Assistant

A context-aware chatbot designed to provide career guidance for women.

## Features
- Job search assistance
- Event information
- Mentorship program details
- Gender bias detection and handling
- Contextual conversation management

## Setup
1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Download spaCy model: `python -m spacy download en_core_web_sm`
6. Run the app: `uvicorn app.main:app --reload`

## Deployment
1. Create account on Render/Heroku
2. Connect your GitHub repository
3. Deploy as Python service with command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## Configuration
Edit files in `data/` directory to customize:
- `mock_jobs.json` - Sample job listings
- `mock_events.json` - Sample events
- `faqs.json` - Frequently asked questions