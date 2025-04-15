from typing import Tuple


class BiasHandler:
    def __init__(self):
        self.bias_patterns = {
            "ability": [
                "can women", "women can't", "are women capable",
                "women shouldn't", "female competence"
            ],
            "leadership": [
                "women leaders", "female executives",
                "are women good leaders", "women in charge"
            ],
            "workplace": [
                "women belong", "women in workplace",
                "female employees", "women colleagues"
            ]
        }

        self.positive_responses = {
            "ability": "Women have demonstrated excellence in all fields. Would you like examples of successful women in technology?",
            "leadership": "Research shows companies with women leaders often outperform others. Would you like to see some leadership success stories?",
            "workplace": "Diverse workplaces including women have been shown to be more innovative and productive. Would you like resources about creating inclusive workplaces?"
        }

    def detect_bias(self, text: str) -> Tuple[bool, str]:
        """Check for biased language"""
        text_lower = text.lower()
        for bias_type, patterns in self.bias_patterns.items():
            if any(pattern in text_lower for pattern in patterns):
                return True, bias_type
        return False, None

    def get_positive_response(self, bias_type: str) -> str:
        """Get constructive response to biased queries"""
        return self.positive_responses.get(bias_type,
                                           "We focus on empowering women in their careers. How can I help you today?")


def check_for_bias(text: str) -> Tuple[bool, str]:
    handler = BiasHandler()
    return handler.detect_bias(text)