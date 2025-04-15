import spacy
import re
from typing import Tuple, Dict
# Add to top with other imports
from textblob import TextBlob


def correct_spelling(text):
    return str(TextBlob(text).correct())

nlp = spacy.load("en_core_web_sm")


def process_input(text: str) -> Tuple[str, Dict]:
    """Process user input to extract intent and entities"""
    text = correct_spelling(text.lower())
    doc = nlp(text)

    # Fixed and simplified intent patterns
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
        (r"\b(bye|goodbye)\b", "goodbye")
    ]

    # Check patterns
    for pattern, intent in intent_patterns:
        if re.search(pattern, text.lower()):
            return intent, extract_entities(doc, intent)

    return "unknown", extract_entities(doc)


def extract_entities(doc, intent=None) -> Dict:
    """Extract entities from processed text"""
    domains = ["aiml", "ai", "machine learning", "ml", "data science", "python","marketing","cybersecurity","banking"]
    skills = ["python", "java", "management", "leadership", "marketing"]

    entities = {
        "job_type": extract_entity(doc, ["full-time", "part-time", "contract", "remote"]),
        "location": extract_location(doc),
        "skill": extract_skills(doc, skills),
        "domain": extract_domain(doc, domains)
    }

    # Enhance domain detection for job searches
    if intent == "job_search" and not entities["domain"]:
        entities["domain"] = detect_domain_from_context(doc, domains)

    return entities


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

# import spacy
# import re
# from typing import Tuple, Dict
#
# nlp = spacy.load("en_core_web_sm")
#
#
# def process_input(text: str) -> Tuple[str, Dict]:
#     doc = nlp(text.lower())
#
#     # Intent patterns with priority matching
#     intent_patterns = [
#         (r"\b(jobs?|careers?|openings?|vacanc(y|ies)|hiring\b", "job_search"),
#         (r"\b(looking|searching|seeking|find).*(job|career|position)\b", "job_search"),
#         (r"\b(current|latest).*(openings|jobs)\b", "job_search"),
#         (r"\b(events?|workshops?|meetups?|conferences?|webinars?)\b", "events"),
#         (r"\b(mentors?|guidance|advice|coaching)\b", "mentorship"),
#         (r"\b(resources?|learn|training|skills?)\b", "resources"),
#         (r"\b(hello|hi|hey)\b", "greeting"),
#         (r"\b(bye|goodbye)\b", "goodbye")
#     ]
#
#     for pattern, intent in intent_patterns:
#         if re.search(pattern, text.lower()):
#             return intent, extract_entities(doc, intent)
#
#     return "unknown", extract_entities(doc)
#
#
# def extract_entities(doc, intent=None):
#     domains = ["aiml", "ai", "machine learning", "ml", "data science"]
#     skills = ["python", "java", "management", "leadership", "marketing"]
#
#     entities = {
#         "job_type": extract_entity(doc, ["full-time", "part-time", "contract", "remote"]),
#         "location": next((ent.text for ent in doc.ents if ent.label_ == "GPE"), None),
#         "skill": [token.text for token in doc if token.text.lower() in skills],
#         "domain": next((token.text.lower() for token in doc if token.text.lower() in domains), None)
#     }
#
#     # Post-process for job searches
#     if intent == "job_search":
#         if not entities["domain"]:
#             for chunk in doc.noun_chunks:
#                 if any(d in chunk.text.lower() for d in domains):
#                     entities["domain"] = chunk.text.lower()
#
#     return entities
#
#
# def extract_entity(doc, options):
#     return next((token.text for token in doc if token.text in options), None)