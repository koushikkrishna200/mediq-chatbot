import spacy

# Load SciSpaCy model (do this only once, handle model loading error)
try:
    nlp = spacy.load("en_core_sci_sm")
except OSError:
    print("SciSpaCy model 'en_core_sci_sm' not found. Please install it using 'pip install spacy[transformers]' and 'python -m spacy download en_core_sci_sm'.")

def extract_medical_entities(text):
    """
    Extract medical entities from the input text using SciSpaCy model.

    :param text: Input medical text to extract entities from.
    :return: A list of unique medical entities along with their types.
    """
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    unique_entities = list(set(entities))  # remove duplicates
    return unique_entities
