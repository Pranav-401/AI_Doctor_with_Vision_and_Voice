import os
import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
from groq import Groq
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")
            
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete...")
            
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")
            
            logging.info(f"Audio saved to {file_path}")
            return file_path
            
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return None

def transcribe_with_groq(audio_file_path):
    if not os.path.exists(audio_file_path):
        logging.error(f"Audio file {audio_file_path} does not exist")
        return "No audio file found"

    try:
        client = Groq(api_key=GROQ_API_KEY)
        with open(audio_file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="distil-whisper-large-v3-en",
                file=audio_file,
                language="en",
                response_format="text"
            )
        return transcription
    except Exception as e:
        logging.error(f"Transcription error: {e}")
        return f"Transcription failed: {str(e)}"