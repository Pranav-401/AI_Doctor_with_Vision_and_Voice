import os
import gradio as gr
from brain_of_doctor import encode_image, analyze_image_with_query
from voice_of_patient import transcribe_with_groq
from voice_of_doctor import text_to_speech_with_elevenlabs
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

system_prompt = """You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

def process_inputs(audio_file_path, image_file_path):
    logging.info(f"Processing audio: {audio_file_path}, image: {image_file_path}")
    
    # Transcribe audio
    speech_to_text_output = transcribe_with_groq(audio_file_path=audio_file_path)
    speech_to_text_output = str(speech_to_text_output) if speech_to_text_output else "No transcription available"
    logging.info(f"Transcription: {speech_to_text_output}")

    # Handle the image input
    if image_file_path:
        if not os.path.exists(image_file_path):
            logging.error(f"Image file {image_file_path} does not exist")
            doctor_response = "Image file not found"
        else:
            query = system_prompt + "\n\n" + speech_to_text_output
            try:
                doctor_response = analyze_image_with_query(query=query, image_path=image_file_path)
                logging.info(f"Doctor response: {doctor_response} (type: {type(doctor_response)})")
            except Exception as e:
                logging.error(f"Error in analyze_image_with_query: {e}")
                doctor_response = f"Failed to analyze image: {str(e)}"
    else:
        doctor_response = "No image provided for me to analyze"

    # Generate audio response
    try:
        audio_filepath = text_to_speech_with_elevenlabs(input_text=doctor_response, output_filepath="final.mp3")
        logging.info(f"Audio generated: {audio_filepath}")
    except Exception as e:
        logging.error(f"Error in text_to_speech_with_elevenlabs: {e}")
        audio_filepath = None

    return speech_to_text_output, doctor_response, audio_filepath

iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath", label="Record your question"),
        gr.Image(type="filepath", label="Upload an image")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio(label="Doctor's Audio Response")
    ],
    title="AI Doctor with Vision and Voice",
    description="Record a question and upload an image for medical analysis."
)

if __name__ == "__main__":
    iface.launch(debug=False, server_name="0.0.0.0", server_port=7860)