FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install git (required for GitAnalyzer)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Create a non-root user (Hugging Face requirement)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Copy requirements and install dependencies
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=user . .

# Expose port 7860 (Hugging Face requirement)
EXPOSE 7860

# Set environment variables
ENV APP_HOST=0.0.0.0
ENV APP_PORT=7860

# Start the application
CMD ["python", "run.py"]
