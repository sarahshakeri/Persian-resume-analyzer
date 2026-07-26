import os
import requests

from dotenv import load_dotenv


load_dotenv()


API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)


MODEL_NAME = "meta-llama/llama-3.1-8b-instruct"


def generate_with_openrouter(prompt):


    if not API_KEY:
        raise ValueError(
            "OpenRouter API key is missing."
        )


    url = "https://openrouter.ai/api/v1/chat/completions"


    headers = {

        "Authorization":
            f"Bearer {API_KEY}",

        "Content-Type":
            "application/json"
    }


    data = {

        "model": MODEL_NAME,

        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],

        "temperature": 0.3
    }


    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=60
    )


    response.raise_for_status()


    result = response.json()


    return (
        result["choices"][0]
        ["message"]
        ["content"]
    )