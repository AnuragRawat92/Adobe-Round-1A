# Use Python 3.10 slim base image for compact size and compatibility
FROM --platform=linux/amd64 python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy all project files
COPY . .

# Install required packages
RUN pip install --no-cache-dir -r requirements.txt

# Create input/output folders (if not already created)
RUN mkdir -p input output

# Command to run your script
CMD ["python", "main.py"]
