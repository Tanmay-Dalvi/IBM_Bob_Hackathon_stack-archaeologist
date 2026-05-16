FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install git (required for GitAnalyzer)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (default 8000)
EXPOSE 8000

# Set environment variables
ENV APP_HOST=0.0.0.0
ENV APP_PORT=8000

# Start the application
CMD ["python", "run.py"]
