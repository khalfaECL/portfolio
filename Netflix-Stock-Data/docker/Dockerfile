# Use Python slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies needed for Selenium + Chrome
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    chromium-driver \
    chromium \
    wget \
    curl \
    unzip \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    libnss3 \
    libxss1 \
    libappindicator1 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    && apt-get clean

# Copy requirements first (to use Docker cache smartly)
COPY ./docker/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY ./flask ./flask
COPY ./model ./model

# Expose Flask port
EXPOSE 5000

# Launch the Flask app
CMD ["python", "./flask/flaskIA.py"]
