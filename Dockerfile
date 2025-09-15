# Use newer Python version (compatible with Django & asgiref)
FROM python:3.11-slim

# Prevent Python from writing pyc files & buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Expose port
EXPOSE 8000

# Use Django dev server (for local dev)
# ⚠️ For production, use gunicorn instead of runserver
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
