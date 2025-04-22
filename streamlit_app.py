import streamlit as st
from app.nlp_engine import process_input
from app.dialog_manager import DialogManager

# --- Streamlit UI ---
st.set_page_config(page_title="Asha Bot 🤖")
st.title("Asha Bot - Career Assistant for Women")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

# User input
user_input = st.chat_input("Ask about jobs, events, or mentorship...")
if user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "text": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get bot response
    manager = DialogManager()
    intent, entities = process_input(user_input)
    response = manager.generate_response(
        intent,
        entities,
        {"last_user_input": user_input}
    )

    # Display bot response
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "text": response})