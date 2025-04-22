import spacy
import re
from typing import Tuple, Dict
from textblob import TextBlob
import json
from pathlib import Path

# Load FAQ data from faqs.json
def load_faqs():
    faq_file_path = Path(__file__).resolve().parent.parent / 'data' / 'faqs.json'
    with open(faq_file_path, 'r') as file:
        return json.load(file)

# Load the FAQs into a dictionary
faqs = load_faqs()

def correct_spelling(text):
    return str(TextBlob(text).correct())

# Load the SpaCy model
nlp = spacy.load("en_core_web_sm")

def process_input(text: str) -> Tuple[str, Dict]:
    """Process user input to extract intent and entities"""
    text = correct_spelling(text.lower())  # Normalize the text
    doc = nlp(text)

    # Check for FAQ first (match the question exactly or normalized)
    faq_answer = faqs.get(text.strip(), None)
    if faq_answer:
        return "faq", {"faq_answer": faq_answer}

    # Intent patterns to detect other types of input
    intent_patterns = [
        (r"\b(jobs?|careers?|openings?|vacanc(?:y|ies)|hiring)\b", "job_search"),
        (r"\b(looking|searching|seeking|find).*(job|career|position)\b", "job_search"),
        (r"\b(current|latest).*(openings|jobs)\b", "job_search"),
        (r"\b(events?|workshops?|meetups?|conferences?|webinars?)\b", "events"),
        (r"\b(mentors?|guidance|advice|coaching)\b", "mentorship"),
        (r"\b(resources?|learn|training|skills?)\b", "resources"),
        (r"\b(hello|hi|hey)\b", "greeting"),
        (r"\b(data.?science|python|contract|datascience)\b", "job_search"),
        (r"\b(free|cost|payment|industr|service)\b", "faq"),
        (r"\b(security|privacy|data protection|safety|personal data)\b", "faq"),
        (r"\b(restart|career change|career advice|re-entering the workforce)\b", "faq"),
        (r"\b(background|experience|specific to me|tailored)\b.*(career advice)\b", "faq"),
        (r"\b(will you remember|previous conversations)\b", "faq"),
        (r"\b(industries|sectors)\b", "faq"),
        (r"\b(bye|goodbye)\b", "goodbye")
    ]

    # Check intent patterns
    for pattern, intent in intent_patterns:
        if re.search(pattern, text.lower()):
            return intent, extract_entities(doc, intent)

    return "unknown", extract_entities(doc)

def extract_entities(doc, intent=None) -> Dict:
    """Extract entities from processed text based on intent"""
    domains = ["aiml", "ai", "machine learning", "ml", "data science", "python", "marketing", "cybersecurity", "banking"]
    skills = ["python", "java", "management", "leadership", "marketing"]

    # Initialize entities dict with None values for job-related entities
    entities = {
        "job_type": None,
        "location": None,
        "skill": [],
        "domain": None
    }

    # For FAQ intents, we don't need to extract job-related entities, just return a response.
    if intent == "faq":
        # You can customize this part to include more specific answers for FAQ intents if needed
        return entities  # Return empty or minimal entities for faq

    # Entity extraction for job-related or other intents
    entities["job_type"] = extract_entity(doc, ["full-time", "part-time", "contract", "remote"])
    entities["location"] = extract_location(doc)
    entities["skill"] = extract_skills(doc, skills)
    entities["domain"] = extract_domain(doc, domains)

    # Enhance domain detection for job searches
    if intent == "job_search" and not entities["domain"]:
        entities["domain"] = detect_domain_from_context(doc, domains)

    return entities


# def extract_entities(doc, intent=None) -> Dict:
#     """Extract entities from processed text"""
#     domains = ["aiml", "ai", "machine learning", "ml", "data science", "python", "marketing", "cybersecurity", "banking"]
#     skills = ["python", "java", "management", "leadership", "marketing"]
#
#     entities = {
#         "job_type": extract_entity(doc, ["full-time", "part-time", "contract", "remote"]),
#         "location": extract_location(doc),
#         "skill": extract_skills(doc, skills),
#         "domain": extract_domain(doc, domains)
#     }
#
#     # Enhance domain detection for job searches
#     if intent == "job_search" and not entities["domain"]:
#         entities["domain"] = detect_domain_from_context(doc, domains)
#
#     return entities

def extract_entity(doc, options):
    """Extract specific entity from options"""
    for token in doc:
        if token.text in options:
            return token.text
    return None

def extract_location(doc):
    """Extract location entities"""
    for ent in doc.ents:
        if ent.label_ == "GPE":
            return ent.text
    return None

def extract_skills(doc, skills):
    """Extract mentioned skills"""
    return [token.text for token in doc if token.text.lower() in skills]

def extract_domain(doc, domains):
    """Extract mentioned domains"""
    for token in doc:
        if token.text.lower() in domains:
            return token.text.lower()
    return None

def detect_domain_from_context(doc, domains):
    """Detect domain from noun phrases when not explicitly mentioned"""
    for chunk in doc.noun_chunks:
        chunk_text = chunk.text.lower()
        for domain in domains:
            if domain in chunk_text:
                return domain
    return None

