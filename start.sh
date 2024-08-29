#!/bin/bash

# Run the first command to start the vllm server and download the model
CUDA_VISIBLE_DEVICES=0,1 python -m vllm.entrypoints.openai.api_server --model microsoft/Phi-3.5-mini-instruct --max-model-len 1024 --dtype=half --tensor-parallel-size 2 --gpu-memory-utilization 0.90 --port 5001 --trust-remote-code --disable-log-requests &

# Wait for the vllm server to start up
echo "Waiting for the vllm server to be up..."
while ! nc -z localhost 5001; do
  sleep 1 # wait for 1 second before checking again
done
echo "vllm server is up!"

# Run the second command
python -m gunicorn -w 3 -k eventlet --threads 20 -b 0.0.0.0:3008 llm_websocket_server:app
