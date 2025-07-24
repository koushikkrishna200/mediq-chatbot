import os
from PyPDF2 import PdfReader

def load_pdfs(pdf_dir):
    texts = []
    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            file_path = os.path.join(pdf_dir, filename)
            with open(file_path, 'rb') as f:
                reader = PdfReader(f)
                content = ""
                for page_num, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        content += page_text
                    else:
                        print(f"Warning: No text extracted from page {page_num+1} of {filename}")
                if content:
                    texts.append((filename, content))  # Store both filename and content
                else:
                    print(f"Warning: No text extracted from {filename}")
    return texts

# Example usage:
pdf_dir = "C:\\Users\\NANDU\\OneDrive\\Desktop\\mediq-chatbot\\app\\pdfs"
  # Update with the actual path
pdf_texts = load_pdfs(pdf_dir)

# Printing the first PDF content for inspection
if pdf_texts:
    print(f"First PDF File: {pdf_texts[0][0]}")
    print(f"Text Preview: {pdf_texts[0][1][:500]}")  # Show a preview of the first 500 characters

# loader.py (updated)
import os

# Option A: Absolute Windows path:
# pdf_dir = r"C:\Users\NANDU\OneDrive\Desktop\mediq-chatbot\app\pdfs"

# Option B: Relative path (works as long as you run `streamlit run app/main.py` from the repo root):
pdf_dir = os.path.join(os.path.dirname(__file__), "pdfs")
