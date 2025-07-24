import speech_recognition as sr

def transcribe_from_microphone(timeout=5, retries=3):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("🎙️ Listening... Please speak.")
        
        # Adding timeout and retries
        for attempt in range(retries):
            try:
                audio = recognizer.listen(source, timeout=timeout)
                print("🧠 Recognizing...")
                text = recognizer.recognize_google(audio)
                return text
            except sr.WaitTimeoutError:
                print("⏳ Timeout reached. Please try again.")
                continue
            except sr.UnknownValueError:
                print("❓ Sorry, I couldn't understand the audio. Please speak clearly.")
                continue
            except sr.RequestError:
                print("⚠️ Service is down. Retrying...")
                continue

        return "Failed to transcribe after multiple attempts."

# Example usage
if __name__ == "__main__":
    result = transcribe_from_microphone()
    print(f"Recognized Text: {result}")
