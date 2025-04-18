FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libportaudio2 \
        libportaudio-dev \
        portaudio19-dev \
        ffmpeg \
        gcc \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

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
CMD ["python", "gradio_app.py"]FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libportaudio2 \
        libportaudio-dev \
        portaudio19-dev \
        ffmpeg \
        gcc \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Set working directory
WORKDIR /app

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY  C:\Users\lenovo\Downloads\ffmpeg-7.1.1-full_build\ffmpeg-7.1.1-full_build\bin
Copy  C:\Users\lenovo\Downloads\pa_stable_v190700_20210406\portaudio

# Expose port for Gradio
EXPOSE 7860

# Run the application
CMD ["python", "gradio_app.py"]