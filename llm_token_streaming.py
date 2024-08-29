from openai import OpenAI
from flask_socketio import emit
import eventlet

openai_api_key = "EMPTY"
openai_api_base = "http://0.0.0.0:5001/v1/"
client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)


def function_stream(room_id, sessionid, prompt, stream=False):
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
        "stream": stream,
        "max_tokens": 500,
        "stop": ["<|end|>"]
    }

    if stream:
        completion = client.completions.create(**completion_params)
        final_string = ""
        for c in completion:
            print(c)
            # finish_reason='stop'
            # finish_reason='length'
            token = c.choices[0].text
            finish_reason = c.choices[0].finish_reason
            final_string += token

            emit('messagefromserver', {
                "status": "success",
                "text": token,
                "sessionid": sessionid,
                "query": prompt,
                "finish_reason": finish_reason
                # If last token --> finish_reason='length' or finish_reason='stop' else finish_reason=None
            }, room=room_id)
            eventlet.sleep()

    else:
        completion = client.completions.create(**completion_params)
        return completion.choices[0].text
