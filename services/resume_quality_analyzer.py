import json

from prompts.quality_analysis_prompt import build_quality_analysis_prompt
from services.llm_service import generate_llm_response


def analyze_resume_quality(structured_resume):

    if not structured_resume:
        raise ValueError(
            "Structured resume data cannot be empty."
        )

    resume_data = json.dumps(
        structured_resume,
        ensure_ascii=False,
        indent=2
    )

    prompt = build_quality_analysis_prompt(
        resume_data
    )

    response_text = generate_llm_response(
        prompt
    )

    if not response_text:
        raise ValueError(
            "LLM returned an empty response."
        )

    return response_text