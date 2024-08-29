""" Example handler file. """
import runpod
import asyncio
from llm_token_streaming import function_stream

from flask import jsonify


async def process_request(job):
    try:
        query = job['query']
        if not query:
            return jsonify({"status": "error", "message": "Query parameter is missing"}), 400

        llm_response = function_stream(prompt=query)
        return jsonify({"status": "success", "llm_response": llm_response})

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error in : get_llm_response\n\n Error details: {str(e)}"}), 500


# Start the serverless function with the handler and concurrency modifier
runpod.serverless.start(
    {"handler": process_request}
)
