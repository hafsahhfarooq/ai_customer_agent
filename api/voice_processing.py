import speech_recognition as sr
from fastapi import APIRouter, HTTPException

voiceprocessing_router = APIRouter()

@voiceprocessing_router.get("/voice-to-text/")
def voice_to_text():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        try:
            print("Listening...")
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            return {"transcription": text}
        except sr.UnknownValueError:
            raise HTTPException(status_code=400, detail="Could not understand the audio")
        except sr.RequestError:
            raise HTTPException(status_code=500, detail="Error connecting to Google Speech Recognition API")
