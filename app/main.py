import os
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from loader import load_pdfs
from vectorstore import create_faiss_index, get_top_k_docs
from app.rag_chain import query_mistral, build_prompt
from app.config import PDF_DIR, FAISS_INDEX_PATH
from settings import sidebar_settings
from chat_history import init_chat_history, append_chat, render_chat_history
from translator import detect_and_translate, translate_back
from voice_input import transcribe_from_microphone
from icd_mapper import extract_umls_entities
from auth import load_auth_config, setup_authenticator
from medical_llms import get_biogpt_answer, get_pubmedgpt_answer, get_clinicalbert_answer
from query_tracker import log_query, visualize_query_trends
from treatment_cost import get_real_time_treatment_cost
from hospital_data import get_nearby_hospitals


# Function to initialize the app and load necessary files
def initialize_app():
    with open("app/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    st.set_page_config(page_title="MediQ", page_icon="🩺")
    st.title("🩺 MediQ: Medical AI Assistant")
    
    # Check if FAISS index exists, else create it
    if not os.path.exists(FAISS_INDEX_PATH + ".pkl"):
        with st.spinner("Indexing documents..."):
            texts = load_pdfs(PDF_DIR)
            create_faiss_index(texts)
        st.success("✅ Index created!")


# Function to handle user queries and get answers
def handle_query(settings):
    query = st.text_input("🔍 Ask a medical question:")
    
    if st.button("Get Answer") and query:
        st.write("📖 Searching documents...")
        context_docs = get_top_k_docs(query, settings["top_k"])
        prompt = build_prompt(query, context_docs)
        response = query_mistral(prompt, settings)
        append_chat(query, response)
        
        st.markdown("### 🧠 Answer")
        st.write(response)


# Function to handle translation (if applicable)
def handle_translation():
    user_lang = st.selectbox("🌐 Your Language", ["en", "fr", "es", "hi", "de", "ar", "zh"], index=0)
    query = st.text_input("🔍 Ask a medical question:")
    
    if st.button("Get Answer") and query:
        st.write("🌍 Translating your question...")
        english_query = detect_and_translate(query, target_lang="en")
        
        st.write("📖 Searching documents...")
        context_docs = get_top_k_docs(english_query, settings["top_k"])
        prompt = build_prompt(english_query, context_docs)
        
        st.write("🤖 Getting answer from Mistral...")
        english_answer = query_mistral(prompt, settings)
        
        translated_answer = translate_back(english_answer, user_lang)
        append_chat(query, translated_answer)

        st.markdown("### 🧠 Answer")
        st.write(translated_answer)


# Function for voice input handling
def handle_voice_input():
    st.markdown("### 🎤 Speak Your Medical Query")
    if st.button("🎙️ Speak"):
        st.info("Listening... speak clearly into your device's mic.")
        voice_text = transcribe_from_microphone()
        st.text_area("📝 Transcribed Text", value=voice_text, height=100)

    if st.button("🎤 Use Voice Input"):
        query = transcribe_from_microphone()
        st.success(f"You said: {query}")
    
    return query


# Function for handling patient queries and ICD tags
def handle_patient_queries():
    entities = extract_umls_entities(english_answer)

    if entities:
        st.markdown("### 🧾 Medical Entities Found (UMLS Tags)")
        for name, cui, semtypes in entities:
            st.write(f"- **{name}** (CUI: `{cui}` | Type: `{', '.join(semtypes)}`)")


# Function to track medical queries and visualize trends
def visualize_trends():
    # Log the query
    log_query(query)
    
    # Display the query statistics for doctors
    st.markdown("### 📊 Medical Query Trends")
    visualize_query_trends()


# Function to display the hospital search and comparison
def hospital_search_comparison():
    # Patient's role dashboard
    if user_role == "patient":
        st.sidebar.header("Patient's Dashboard")
        action = st.sidebar.radio("What would you like to do?", ["Search for Hospitals", "Compare Hospitals", "Get Treatment Cost Estimate"])

        if action == "Search for Hospitals":
            location = st.text_input("Enter Location (e.g., New York, California):")
            if st.button("Search"):
                hospitals = get_nearby_hospitals(location)
                if not hospitals.empty:
                    st.write("### Search Results:")
                    st.write(hospitals)
                else:
                    st.write("No hospitals found near your location.")
        
        elif action == "Compare Hospitals":
            location = st.text_input("Enter Location (e.g., New York):")
            if st.button("Compare"):
                hospitals = get_nearby_hospitals(location)
                if not hospitals.empty:
                    st.write("### Comparison of Hospitals:")
                    st.write(hospitals[['hospital_name', 'location', 'specialty', 'rating']])
                else:
                    st.write("No hospitals found matching your criteria.")
        
        elif action == "Get Treatment Cost Estimate":
            disease = st.text_input("Enter your medical condition (e.g., Cardiac Surgery, Cancer Treatment):")
            if st.button("Get Cost Estimate"):
                cost = get_real_time_treatment_cost(disease)
                st.write(f"Estimated cost for {disease}: ${cost}")


# Main function to tie everything together
def main():
    # Initialize app
    initialize_app()
    
    # Sidebar settings
    settings = sidebar_settings()
    
    # User authentication
    config = load_auth_config()
    authenticator = setup_authenticator(config)
    name, auth_status, username = authenticator.login("Login", "main")
    
    if auth_status:
        authenticator.logout("Logout", "sidebar")
        st.sidebar.success(f"Welcome {name}!")
        
        user_role = config['credentials']['usernames'][username]['role']
        st.sidebar.markdown(f"**Role:** `{user_role}`")
        
        if user_role == "doctor":
            st.markdown("## 👩‍⚕️ Doctor Dashboard")
            action = st.sidebar.radio("What would you like to do?", ["View Medical Query Trends"])
            
            if action == "View Medical Query Trends":
                st.markdown("### 📊 Medical Query Trends")
                visualize_trends()
        
        elif user_role == "patient":
            # Handle patient actions
            hospital_search_comparison()

    elif auth_status is False:
        st.error("Invalid username or password.")
    elif auth_status is None:
        st.warning("Please enter your credentials.")

    # Handling queries and answers
    query = handle_voice_input()
    if query:
        handle_query(settings)

    # Handle translation if applicable
    handle_translation()

    # Display chat history
    render_chat_history()


if __name__ == "__main__":
    main()
