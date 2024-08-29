from openai import OpenAI

openai_api_key = "EMPTY"
openai_api_base = "http://0.0.0.0:5001/v1/"
# openai_api_base = "https://repeatedly-pleasing-narwhal.ngrok-free.app/v1/"
client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)


def function_stream(prompt):
    models = client.models.list()
    model = models.data[0].id

    prompt_template = (
        "<|system|>\n"
        "You are a helpful assistant.<|end|>\n"
        "<|user|>\n"
        "{prompt}<|end|>\n"
        "<|assistant|>"
    )
    formatted_prompt = prompt_template.format(prompt=prompt)

    completion_params = {
        "model": model,
        "prompt": formatted_prompt,
        "echo": False,
        "stream": False,
        "max_tokens": 500,
        "stop": ["<|end|>"]
    }

    completion = client.completions.create(**completion_params)
    return completion.choices[0].text
