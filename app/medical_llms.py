from transformers import AutoModelForCausalLM, AutoTokenizer

# Load BioGPT model
bio_model = AutoModelForCausalLM.from_pretrained("microsoft/biogpt")
bio_tokenizer = AutoTokenizer.from_pretrained("microsoft/biogpt")

# Load PubMedGPT model (example)
pubmed_model = AutoModelForCausalLM.from_pretrained("pubmedpubmed/pubmedgpt")
pubmed_tokenizer = AutoTokenizer.from_pretrained("pubmedpubmed/pubmedgpt")

# Load ClinicalBERT model (example)
clinicalbert_model = AutoModelForCausalLM.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")
clinicalbert_tokenizer = AutoTokenizer.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")

# Optional: Load fine-tuned models if you have them
fine_tuned_bio_model = AutoModelForCausalLM.from_pretrained("./biogpt_finetuned")
fine_tuned_bio_tokenizer = AutoTokenizer.from_pretrained("./biogpt_finetuned")

# Function to generate responses from a given model and tokenizer
def generate_answer(model, tokenizer, query):
    try:
        # Tokenize the input query
        inputs = tokenizer(query, return_tensors="pt")
        
        # Generate response from the model
        output = model.generate(**inputs, max_length=500, num_return_sequences=1)  # Adjust parameters as needed
        
        # Decode and return the generated answer
        answer = tokenizer.decode(output[0], skip_special_tokens=True)
        return answer
    except Exception as e:
        return f"Error generating answer: {str(e)}"

# Function to get answers from each model
def get_biogpt_answer(query):
    return generate_answer(bio_model, bio_tokenizer, query)

def get_pubmedgpt_answer(query):
    return generate_answer(pubmed_model, pubmed_tokenizer, query)

def get_clinicalbert_answer(query):
    return generate_answer(clinicalbert_model, clinicalbert_tokenizer, query)

def get_finetuned_biogpt_answer(query):
    return generate_answer(fine_tuned_bio_model, fine_tuned_bio_tokenizer, query)
