import openai
import os
import tenacity

# for using OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_INSTRUCTIONS = """You are a brilliant AGI assistant whose goal is to achieve whatever task is given to you, to the best of your abilities. You are just a computer program, and you don’t have a body, so the only way you can interact with the world is by responding to this prompt with a sequence of action requests. The set of actions you have at your disposal, as well as the exact format for these action requests, will be provided to you later in this prompt. This program is running in a continuous loop, so you only need to specify one action, or maybe a few, at a time. You will see this prompt again immediately after you respond to it, with any relevant information updated to reflect the actions that were performed for you."""

@tenacity.retry(
    stop=tenacity.stop_after_attempt(3),
    wait=tenacity.wait_fixed(4),
    retry=(
            tenacity.retry_if_exception_type(openai.error.Timeout)
            | tenacity.retry_if_exception_type(openai.error.APIError)
            | tenacity.retry_if_exception_type(openai.error.APIConnectionError)
            | tenacity.retry_if_exception_type(openai.error.RateLimitError)
    )
)
def openai_api_call(prompt: str, model_name: str = "gpt-3.5-turbo", temperature: float = 0.5, max_tokens: int = 1000):
    """
    Function to call the OpenAI API and get a basic response
    - "gpt-3.5-turbo" or "gpt-4"
    - this function just stuffs the prompt into a human input message to simulate a standard completions model
    """
    max_tokens = int(max_tokens)
    temperature = float(temperature)
    if model_name == "gpt-3.5-turbo" or model_name == "gpt-4":
        openai.api_key = os.getenv("OPENAI_API_KEY")
        system_message = {"role": "system", "content": SYSTEM_INSTRUCTIONS}
        user_input_message = {"role": "user", "content": prompt}
        messages = [system_message] + [user_input_message]
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            request_timeout=120,
        )
        llm_output = response['choices'][0]['message']['content'].strip()
    else:
        print("ERROR: model_name must be gpt-3.5-turbo or gpt-4")
        llm_output = ""
    
    return llm_output