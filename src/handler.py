import runpod
import aiohttp

print(50 * "*")
print("starting handler.py v2 with async improvements")
print(50 * "*")


vllm_server = "http://0.0.0.0:5001/v1/completions"


async def process_request(job):
    try:
        query = job['input']['query']

        if not query:
            return {"status": "error", "message": "Query parameter is missing"}

        prompt_template = (
            "<|system|>\n"
            "You are a helpful assistant.<|end|>\n"
            "<|user|>\n"
            "{query}<|end|>\n"
            "<|assistant|>"
        )
        formatted_prompt = prompt_template.format(query=query)

        completion_params = {
            "model": "models/microsoft/Phi-3.5-mini-instruct",
            "prompt": formatted_prompt,
            "echo": False,
            "stream": False,
            "temperature": 0.0,
            "max_tokens": 500,
            "stop": ["<|end|>"]
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(vllm_server, json=completion_params) as response:
                response_data = await response.json()
                print(f"response_data : {response_data}")
                llm_response = response_data["choices"][0]['text']

                return {"status": "success", "llm_response": llm_response}

    except Exception as e:
        print(str(e))
        return {"status": "error", "message": f"Error in : get_llm_response\n\n Error details: {str(e)}"}

# Start the serverless function with the handler and concurrency modifier
runpod.serverless.start(
    {"handler": process_request, "concurrency_modifier": lambda x: 10}
)

# python handler.py --test_input '{"input":{"query": "The quick brown fox jumps"}}'
