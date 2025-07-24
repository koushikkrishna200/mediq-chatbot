import requests
from .config import HUGGINGFACE_API_KEY
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def query_mistral(prompt, settings):
    """
    Query the Mistral-7B model on Hugging Face's Inference API.

    :param prompt: The prompt to send to the model.
    :param settings: A dictionary containing settings for the model's inference (e.g., temperature, max_tokens).
    :return: The generated text from the model.
    """
    url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": settings["temperature"],
            "max_new_tokens": settings["max_tokens"]
        }
    }

    try:
        # Set a timeout of 30 seconds for the request
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()  # Raise an error for bad HTTP status codes

        # Check if the response has the expected structure
        if "generated_text" in response.json()[0]:
            return response.json()[0]["generated_text"]
        else:
            logging.error("Unexpected response structure: %s", response.json())
            return "Error: Unexpected response from the model."
    
    except requests.exceptions.Timeout:
        logging.error("Request to Hugging Face API timed out.")
        return "Error: The request timed out."
    except requests.exceptions.RequestException as e:
        logging.error("Error with the request: %s", e)
        return f"Error: {str(e)}"

def build_prompt(query, context_docs):
    """
    Builds the prompt to send to the Mistral-7B model.
    
    :param query: The question/query the user has.
    :param context_docs: The context documents that will provide information for the model.
    :return: The formatted prompt string.
    """
    context = "\n\n".join(context_docs)
    return f"""You are a helpful medical assistant.

Context:
{context}

Question: {query}

Answer:"""

# Example usage:
settings = {"temperature": 0.7, "max_tokens": 150}
context_docs = ["Document 1 text", "Document 2 text"]
query = "What is the treatment for diabetes?"

prompt = build_prompt(query, context_docs)
response = query_mistral(prompt, settings)
print(response)
