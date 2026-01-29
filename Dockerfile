# Use a lightweight Python base image to minimize container size
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# 1. Copy the shared utility module to the project root
# This is crucial because the server script expects utils.py in the parent directory
COPY utils.py .

# 2. Copy the entire server directory into /app/server
COPY server/ ./server/

# Environment Variables:
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing .pyc files
# PYTHONUNBUFFERED: Ensures logs are flushed immediately to the terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expose the TCP port defined in the protocol
EXPOSE 65432

# Define the entry point command
# We execute from /app so the script can resolve paths correctly
CMD ["python", "server/server_main.py"]