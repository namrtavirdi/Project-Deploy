# Use Python 3.10 (compatible with TensorFlow 2.10)
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only requirements first (for Docker layer caching)
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Flask application port
EXPOSE 5000

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=src/app.py
ENV FLASK_ENV=production

# Start the application
CMD ["python", "src/app.py"]
