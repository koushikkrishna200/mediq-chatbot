import os
from dotenv import load_dotenv


load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
PDF_DIR = "./data/medical_docs"
FAISS_INDEX_PATH = "./data/faiss_index"
