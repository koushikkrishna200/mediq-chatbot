from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
import torch

# Load the model once
model_name = "facebook/m2m100_418M"
tokenizer = M2M100Tokenizer.from_pretrained(model_name)
model = M2M100ForConditionalGeneration.from_pretrained(model_name)

# Move model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

def detect_and_translate(text, target_lang="en"):
    """
    Detects the language and translates it to the target language.

    :param text: Input text to translate.
    :param target_lang: The language to translate the text into (default: English).
    :return: Translated text.
    """
    try:
        tokenizer.src_lang = "auto"
        encoded = tokenizer(text, return_tensors="pt").to(device)
        generated_tokens = model.generate(**encoded, forced_bos_token_id=tokenizer.get_lang_id(target_lang))
        return tokenizer.decode(generated_tokens[0], skip_special_tokens=True)
    except Exception as e:
        return f"Error in translation: {str(e)}"

def translate_back(text, target_lang="en"):
    """
    Translates a given English text into another target language.

    :param text: Input text to translate.
    :param target_lang: Target language code (e.g., 'hi' for Hindi).
    :return: Translated text.
    """
    try:
        tokenizer.src_lang = "en"
        encoded = tokenizer(text, return_tensors="pt").to(device)
        generated_tokens = model.generate(**encoded, forced_bos_token_id=tokenizer.get_lang_id(target_lang))
        return tokenizer.decode(generated_tokens[0], skip_special_tokens=True)
    except Exception as e:
        return f"Error in reverse translation: {str(e)}"
s