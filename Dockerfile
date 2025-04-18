FROM python:3.11-slim

   # Install system dependencies
   RUN apt-get update && apt-get install -y \
       libportaudio2 \
       libportaudio-dev \
       portaudio19-dev \
       ffmpeg \
       gcc \
       && apt-get clean

   # Set working directory
   WORKDIR /app

   # Copy requirements.txt and install Python dependencies
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   # Copy application files
   COPY . .

   # Expose port for Gradio
   EXPOSE 7860

   # Run the application
   CMD ["python", "app.py"]