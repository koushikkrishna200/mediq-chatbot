import spacy

# Load the SciSpacy model (make sure you've installed it as shown below)
nlp = spacy.load("en_core_sci_sm")

def extract_umls_entities(text):
    doc = nlp(text)
    results = []
    for ent in doc.ents:
        # Note: scispaCy doesn't return CUIs by default unless linking is used
        results.append((ent.text, ent.label_, []))  # (term, entity type, placeholder for semtypes)
    return results

# Example usage
if __name__ == "__main__":
    text = "The patient has been diagnosed with hypertension."
    entities = extract_umls_entities(text)
    for entity in entities:
        print(f"Term: {entity[0]}, Label: {entity[1]}")
