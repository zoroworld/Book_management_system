# Use official Python slim image
FROM python:3.8-slim

# Prevent Python from writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (better caching)
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Expose Django port
EXPOSE 8000

# Run Gunicorn (better than runserver)
CMD ["gunicorn", "bookmanagement.wsgi:application", "--bind", "0.0.0.0:8000", "--workers=3"]
