import os
import streamlit as st
from openai import OpenAI

# --------------------------------------------------
# Page setup: title, icon, and basic layout
# --------------------------------------------------
st.set_page_config(
    page_title="INTJ Architect",
    page_icon="🧠"
)

# --------------------------------------------------
# Read API key from server environment
# This keeps the key hidden from users and GitHub
# --------------------------------------------------
API_KEY = os.getenv("OPENROUTER_API_KEY")

# If the key is missing, stop the app safely
if not API_KEY:
    st.error("API key not set on server.")
    st.stop()

# --------------------------------------------------
# Create OpenAI client configured for OpenRouter
# --------------------------------------------------
client = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        # Required by OpenRouter for usage tracking
        "HTTP-Referer": "https://streamlit.io",
        "X-Title": "INTJ-Architect-Web"
    }
)

# --------------------------------------------------
# Fast, lightweight model for quick responses
# --------------------------------------------------
MODEL_ID = "meta-llama/llama-3.1-8b-instruct"

# --------------------------------------------------
# System prompt: defines the agent’s behavior
# --------------------------------------------------
SYSTEM_PROMPT = """
You are The Architect.
Respond only with:
1. Diagnosis
2. Strategy
"""

# --------------------------------------------------
# Session memory:
# Persists conversation while the browser tab is open
# --------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# --------------------------------------------------
# UI: title and short description
# --------------------------------------------------
st.title("🧠 INTJ Architect")
st.caption("Strategic AI • Fast • No fluff")

# --------------------------------------------------
# Text input area for the user’s objective or problem
# --------------------------------------------------
user_input = st.text_area(
    "Enter your objective:",
    height=120
)

# --------------------------------------------------
# Action button: sends input to the AI when clicked
# --------------------------------------------------
if st.button("Analyze"):

    # Ignore empty input
    if user_input.strip():

        # Add user message to conversation history
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )

        # Show a spinner while the model processes
        with st.spinner("Thinking..."):
            res = client.chat.completions.create(
                model=MODEL_ID,
                messages=st.session_state.messages,
                temperature=0.3
            )

        # Extract the AI response text
        reply = res.choices[0].message.content

        # Save AI response to session memory
        st.session_state.messages.append(
            {"role": "assistant", "content": reply}
        )

        # Display result cleanly
        st.markdown("---")
        st.markdown(reply)
