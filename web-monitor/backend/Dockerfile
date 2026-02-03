# Base Image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (if needed for pandas/scikit build)
# RUN apt-get update && apt-get install -y gcc

# Copy requirements first to leverage caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (FastAPI default)
EXPOSE 8085

# Command to run the application
CMD ["python", "start_service.py"]
