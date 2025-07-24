# app/chat_history.py

import streamlit as st

def init_chat_history():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

def append_chat(user_msg, bot_msg):
    st.session_state.chat_history.append({"user": user_msg, "bot": bot_msg})

def render_chat_history():
    for chat in st.session_state.chat_history:
        st.write(f"**User:** {chat['user']}")
        st.write(f"**Bot:** {chat['bot']}")
        st.write("---")
