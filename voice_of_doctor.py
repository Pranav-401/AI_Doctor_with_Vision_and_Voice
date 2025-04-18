import os
import logging
from dotenv import load_dotenv
from elevenlabs import ElevenLabs
import subprocess
import platform
from pydub import AudioSegment
import tempfile

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

def text_to_speech_with_elevenlabs(input_text, output_filepath="final.mp3"):
    if not isinstance(input_text, str) or not input_text.strip():
        logging.error("Invalid input: Text must be a non-empty string")
        return None

    logging.info(f"Generating audio for text: {input_text[:50]}...")
    try:
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        audio = client.text_to_speech.convert(
            voice_id="LcfcDJNUP1GQjkzn1xUU",
            output_format="mp3_44100_128",
            text=input_text,
            model_id="eleven_multilingual_v2"
        )

        logging.info(f"Writing audio to {output_filepath}")
        with open(output_filepath, "wb") as f:
            for chunk in audio:
                f.write(chunk)

        # Convert MP3 to WAV for playback
        wav_filepath = os.path.join(tempfile.gettempdir(), "temp_audio.wav")
        logging.info(f"Converting {output_filepath} to WAV: {wav_filepath}")
        audio_segment = AudioSegment.from_mp3(output_filepath)
        audio_segment.export(wav_filepath, format="wav")

        # Play audio based on operating system
        os_name = platform.system()
        logging.info(f"Playing audio on {os_name}")
        try:
            if os_name == "Darwin":  # macOS
                subprocess.run(['afplay', output_filepath], check=True)
            elif os_name == "Windows":  # Windows
                subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_filepath}").PlaySync();'], check=True)
            elif os_name == "Linux":  # Linux
                subprocess.run(['aplay', wav_filepath], check=True)
            else:
                raise OSError("Unsupported operating system")
        except Exception as e:
            logging.error(f"Error playing audio: {e}")
        finally:
            if os.path.exists(wav_filepath):
                os.remove(wav_filepath)

        return output_filepath

    except Exception as e:
        logging.error(f"Error in text-to-speech: {e}")
        return None