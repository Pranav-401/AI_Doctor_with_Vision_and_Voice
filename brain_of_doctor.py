import os
import base64
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        return encoded_image
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None

def analyze_image_with_query(query, image_path):
    if not os.path.exists(image_path):
        print(f"Image file {image_path} does not exist")
        return "Image file not found"

    client = Groq(api_key=GROQ_API_KEY)
    encoded_image = encode_image(image_path)
    
    if not encoded_image:
        return "Failed to encode image"

    try:
        completion = client.chat.completions.create(
            model="compound-beta",
            messages=[
                {
                    "role": "user",
                    "content": f"{query}\n\nPlease analyze the provided image: {image_path}"
                }
            ],
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=False,
        )
        
        response_text = completion.choices[0].message.content
        return response_text

    except Exception as e:
        print(f"Error in Groq API call: {e}")
        return f"Failed to analyze image: {str(e)}"