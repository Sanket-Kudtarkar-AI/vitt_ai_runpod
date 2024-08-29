import runpod


def handler(event):
    """
    This is a sample handler function that echoes the input
    and adds a greeting.
    """
    try:
        # Extract the prompt from the input
        prompt = event["input"]["prompt"]

        result = f"Hello! You said: {prompt}"

        # Return the result
        return {"output": result}
    except Exception as e:
        # If there's an error, return it
        return {"error": str(e)}


# Start the serverless function
runpod.serverless.start({"handler": handler})