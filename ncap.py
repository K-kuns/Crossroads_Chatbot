import streamlit as st
import google.generativeai as genai
import warnings
import os
import random

warnings.filterwarnings("ignore")

# ✅ Configure Gemini API key
api_key = "AIzaSyC1gLQLeywaERy3PrV-AAgZEVV-pjU1tE8"
genai.configure(api_key=api_key)

# Chatbot configuration
generation_config = {
    "temperature": 0.1,
    "top_p": 0.85,
    "top_k": 40,
    "max_output_tokens": 32768,
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
)

# System prompt for Crossroads
SYSTEM_PROMPT = (
    "You are Crossroads, a professional and helpful traffic advisor specializing in the No Contact Apprehension Program (NCAP) in the Philippines. "
    "You provide clear, accurate, and concise answers to questions about NCAP policies, how to check violations, pay fines, and avoid infractions. "
    "You always remain polite, focused, and professional. If someone asks something unrelated to NCAP or traffic enforcement, politely inform them you can only help with NCAP matters. "
    "You never break character or reveal that you are an AI assistant."
)

st.set_page_config(page_title="Crossroads NCAP Chatbot", page_icon="", layout="wide")

# Session state initialization
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize chat session and first message ONCE
if "chat_initialized" not in st.session_state or not st.session_state.chat_initialized:
    st.session_state.chat_session = model.start_chat(history=[])

    # First message / intro greeting
    intro_message = (
        "Hello! I’m **Crossroads**, your reliable NCAP companion. 🚦\n\n"
        "Ask me anything about:\n"
        "- NCAP notices and violations,\n"
        "- How to check your status online,\n"
        "- Tips to stay compliant and safe on the road.\n\n"
        "Let’s get started! 🚗"
    )
    st.session_state.messages = [{"role": "assistant", "content": intro_message}]
    st.session_state.chat_initialized = True

# Chat avatars
bot_avatar = "crossroads.png"  # Update this to your bot avatar
user_avatar = "user_avatar.png"

st.title("💬 NCAP Chat with Crossroads")

# Show chat history
for message in st.session_state.messages:
    if message["role"] == "system":
        continue

    avatar = user_avatar if message["role"] == "user" else bot_avatar

    try:
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])
    except Exception:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Input field for new messages
if user_message := st.chat_input("Ask me anything about NCAP... 🚦"):
    st.session_state.messages.append({"role": "user", "content": user_message})

    with st.chat_message("user", avatar=user_avatar):
        st.markdown(user_message)

    # Create final prompt for the chatbot, focused on NCAP guidance
    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"User’s question: {user_message}\n"
        "Please respond in a clear and helpful manner."
    )

    response = st.session_state.chat_session.send_message(prompt)
    reply = response.text.strip()

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant", avatar=bot_avatar):
        st.markdown(reply)
