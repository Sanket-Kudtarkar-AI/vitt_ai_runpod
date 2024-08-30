#!/bin/bash

# Run the first command to start the vllm server and download the model
python -m vllm.entrypoints.openai.api_server --model /models/microsoft/Phi-3.5-mini-instruct --max-model-len 1024 --dtype=half --gpu-memory-utilization 0.85 --port 5001 --tensor-parallel-size 1 --trust-remote-code --disable-log-requests &

# Wait for the vllm server to start up
echo "Waiting for the vllm server to be up..."
while ! nc -z localhost 5001; do
  sleep 1 # wait for 1 second before checking again
done
echo "vllm server is up!"


# Start the handler after the server is confirmed to be running
python -u /handler.py