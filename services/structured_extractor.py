import json

from prompts.structured_resume_prompt import build_structured_resume_prompt
from services.llm_service import generate_llm_response



def extract_structured_resume(text):

    if not text or not text.strip():
        raise ValueError(
            "Input resume text is empty."
        )


    prompt = build_structured_resume_prompt(
        text
    )


    response_text = generate_llm_response(
        prompt
    )


    if not response_text:
        raise ValueError(
            "LLM returned an empty response."
        )


    response_text = response_text.strip()



    # Remove Markdown JSON fences if returned

    if response_text.startswith("```json"):

        response_text = response_text.replace(
            "```json",
            "",
            1
        )


    if response_text.endswith("```"):

        response_text = response_text[:-3]


    response_text = response_text.strip()



    try:

        return json.loads(
            response_text
        )


    except json.JSONDecodeError as e:

        raise ValueError(
            "LLM response is not valid JSON."
        ) from e