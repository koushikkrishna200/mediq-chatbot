import streamlit as st

def sidebar_settings():
    st.sidebar.title("⚙️ Settings")
    
    # Slider for number of context documents
    top_k = st.sidebar.slider(
        "📚 Number of context documents",
        1, 10, 3,
        help="Number of relevant context documents to use for generating the response."
    )
    
    # Slider for model temperature (controls randomness)
    temperature = st.sidebar.slider(
        "🔥 Model Temperature",
        0.0, 1.0, 0.3,
        help="Controls the creativity of the response. Lower values make it more deterministic, higher values make it more creative."
    )
    
    # Slider for maximum tokens (response length)
    max_tokens = st.sidebar.slider(
        "🔢 Max Tokens",
        64, 1024, 512,
        help="Maximum length of the generated response. Higher values result in longer answers."
    )
    
    st.sidebar.markdown("---")
    st.sidebar.caption("Adjust context size, creativity, and response length.")
    
    # Display selected settings for transparency
    st.sidebar.subheader("Current Settings:")
    st.sidebar.write(f"Context Documents: {top_k}")
    st.sidebar.write(f"Temperature: {temperature}")
    st.sidebar.write(f"Max Tokens: {max_tokens}")
    
    return {"top_k": top_k, "temperature": temperature, "max_tokens": max_tokens}
