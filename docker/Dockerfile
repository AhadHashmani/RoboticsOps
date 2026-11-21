FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Copy env
COPY .env.example .env

# Expose ports
EXPOSE 8000 8501

# Set environment
ENV PYTHONUNBUFFERED=1

# Run application
CMD ["python", "main.py"]
