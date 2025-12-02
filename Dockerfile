FROM python:3.10-slim

# Install system dependencies
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

# Copy requirements and install
COPY requirements.txt .
RUN pip3 install --no-cache-dir -U -r requirements.txt

# Copy all files
COPY . .

# Expose port
EXPOSE 5000

# Run with -u for unbuffered output to see errors in logs
CMD gunicorn -w 1 -b 0.0.0.0:5000 app:app & python3 -u main.py
