# from app.nlp_engine import process_input
# from app.dialog_manager import DialogManager
#
#
# def test_queries():
#     manager = DialogManager()
#     test_cases = [
#         "hi",
#         "data-science jobs",
#         "python workshop",  # Tests typo handling
#         "Is this free?",
#         "contract work",
#         "How restart career?"
#     ]
#
#     for query in test_cases:
#         print(f"\nUser: {query}")
#         intent, entities = process_input(query)
#         response = manager.generate_response(intent, entities, {"last_user_input": query})
#         print(f"Asha: {response}")
#
#
# if __name__ == "__main__":
#     test_queries()


from app.nlp_engine import process_input
from app.dialog_manager import DialogManager


def test_queries():
    manager = DialogManager()
    test_cases = [
        # Basic interactions
        "hi",
        "hello",
        "hey there",

        # Job-related queries
        "data science jobs",
        # "python developer positions",
        "remote jobs for women",
        "full-time opportunities",
        "part-time work in bangalore",
        "contract positions in AI",
        "machine learning engineer roles",

        # Event queries
        "upcoming workshops",
        "tech conferences",
        "career events for women",
        "networking meetups",

        # Career support
        "how to restart my career",
        "career guidance",
        "mentorship programs",
        "returnships for women",

        # FAQ questions
        "is this service free?",
        "what industries do you work with?",
        "do you have python jobs?",
        "are there remote opportunities?",

        # Edge cases
        "wokshops",  # intentional typo
        "datascience",  # no space
        "pyton jobs",  # misspelled
        "contarct work"  # misspelled
    ]

    for query in test_cases:
        print(f"\nUser: {query}")
        intent, entities = process_input(query)
        response = manager.generate_response(intent, entities, {"last_user_input": query})
        print(f"Asha: {response}")


if __name__ == "__main__":
    test_queries()