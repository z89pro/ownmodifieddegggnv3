FROM python:3.10-slim

# Install system dependencies (FFmpeg, 7zip for splitting, build tools)
RUN apt-get update && apt-get install -y \
    git \
    curl \
    ffmpeg \
    wget \
    bash \
    p7zip-full \
    build-essential \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -U -r requirements.txt

# Copy all files
COPY . .

# Expose port for Web Support
EXPOSE 5000

# Command to run Bot + Web Server
CMD gunicorn -w 1 -b 0.0.0.0:5000 app:app & python3 main.py
