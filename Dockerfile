# 1. Use an appropriate Python base image
FROM python:3.11-slim

# 2. Set up a working directory
WORKDIR /app

# 3. Install system-level dependencies for PostgreSQL connectivity
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# 4. Copy and install Python dependencies efficiently
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy application code
COPY . .

# 6. Set environment variables for real-time log output
ENV PYTHONUNBUFFERED=1

# 7. Define default command to run the pipeline
CMD ["python", "scripts/data_generation/generate_data.py"]