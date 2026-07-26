# services/gemini_service.py

import os

from google import genai
from dotenv import load_dotenv


load_dotenv()


API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = "gemini-3.6-flash"


client = genai.Client(
    api_key=API_KEY
)



def initialize_model():
    return client



# -----------------------------------------
# Direct Gemini Generator
# -----------------------------------------

def generate_with_gemini(prompt):

    if not prompt or not prompt.strip():
        raise ValueError(
            "Prompt cannot be empty."
        )


    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )


    if not response.text:
        raise ValueError(
            "Gemini returned an empty response."
        )


    return response.text



# -----------------------------------------
# Resume Text Repair
# -----------------------------------------

def repair_text(text):

    if not text or not text.strip():
        raise ValueError(
            "Input text cannot be empty."
        )


    from prompts.repair_prompt import build_repair_prompt
    from services.llm_service import generate_llm_response


    prompt = build_repair_prompt(
        text
    )


    return generate_llm_response(
        prompt
    )