# Use slim Python base image compatible with amd64
FROM --platform=linux/amd64 python:3.9-slim

# Set working directory
WORKDIR /app

# Copy all project files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command: run the main ranking script
CMD ["python", "main_rank.py"]
