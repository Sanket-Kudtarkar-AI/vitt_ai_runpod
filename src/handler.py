""" Example handler file. """
import runpod
from llm_token_streaming import function_stream

from flask import jsonify
print(50*"*")
print("starting handler.py")
print(50*"*")

async def process_request(job):
    try:
        query = job['input']['query']
        if not query:
            return {"status": "error", "message": "Query parameter is missing"}

        llm_response = await function_stream(prompt=query)
        return {"status": "success", "llm_response": llm_response}

    except Exception as e:
        print(str(e))
        return {"status": "error", "message": f"Error in : get_llm_response\n\n Error details: {str(e)}"}


# Start the serverless function with the handler and concurrency modifier
runpod.serverless.start(
    {"handler": process_request, "concurrency_modifier": 100}
)


# python handler.py --test_input '{"input":{"query": "The quick brown fox jumps"}}'