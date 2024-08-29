# Use an official Python runtime as a parent image
FROM python:3.9.19-slim

# Set the working directory in the container
WORKDIR /app

# Install netcat-openbsd for checking the server status
RUN apt-get update && apt-get install -y netcat-openbsd

# Copy the current directory contents into the container at /app
COPY . /app

# Install hf_transfer and huggingface-cli
RUN pip install hf_transfer huggingface_hub

# Create a directory for the model files

# Download the model using huggingface-cli with hf_transfer
RUN mkdir -p /app
RUN HF_HUB_ENABLE_HF_TRANSFER=1 huggingface-cli download microsoft/Phi-3.5-mini-instruct --local-dir /app/microsoft/Phi-3.5-mini-instruct --local-dir-use-symlinks False

# Set execute permissions for the startup script
RUN chmod +x /app/start.sh

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make ports available to the world outside this container
EXPOSE 5001
EXPOSE 3008

# Run the startup script
ENTRYPOINT ["./start.sh"]
