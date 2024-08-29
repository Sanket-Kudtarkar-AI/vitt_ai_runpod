# Use an official Python runtime as a parent image
FROM nvidia/cuda:12.1.0-base-ubuntu22.04
FROM python:3.9.19-slim
RUN ldconfig /usr/local/cuda-12.1/compat/
COPY builder/requirements.txt /requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    python3 -m pip install --upgrade pip && \
    python3 -m pip install --upgrade -r /requirements.txt


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
#RUN HF_HUB_ENABLE_HF_TRANSFER=1 huggingface-cli download microsoft/Phi-3.5-mini-instruct --local-dir /app/microsoft/Phi-3.5-mini-instruct --local-dir-use-symlinks False

# Set execute permissions for the startup script
RUN chmod +x /app/builder/start.sh

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /app/builder/requirements.txt

# Run the startup script
ENTRYPOINT ["sh", "-c", "/app/builder/start.sh && python3 /src/handler.py"]


