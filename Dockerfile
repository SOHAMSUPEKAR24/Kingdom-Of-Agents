FROM python:3.11-slim

WORKDIR /app

# Install system dependencies needed for compiling python packages, cryptography, and automation
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium --with-deps

# Copy application source code
COPY . .

# Expose FastAPI backend port
EXPOSE 8000

# Start Uvicorn async server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
