# services/llm_service.py

from services.gemini_service import generate_with_gemini
from services.openrouter_service import generate_with_openrouter


def _should_fallback_from_gemini(error):
    """
    Returns True only when Gemini fails because of
    quota, rate limit, or temporary service availability.
    """

    error_text = str(error).lower()

    fallback_errors = [
        "429",
        "resource_exhausted",
        "quota",
        "rate limit",
        "503",
        "unavailable",
        "service unavailable"
    ]

    return any(
        keyword in error_text
        for keyword in fallback_errors
    )


def generate_llm_response(prompt):

    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    # -----------------------------------------
    # Primary Provider: Gemini
    # -----------------------------------------

    try:

        print("[LLM] Trying Gemini...")

        response = generate_with_gemini(prompt)

        print("[LLM] Gemini succeeded.")

        return response

    except Exception as gemini_error:

        print(
            "[LLM] Gemini failed:",
            gemini_error
        )

        # Programming/configuration errors should
        # NOT silently trigger another provider.
        if not _should_fallback_from_gemini(
            gemini_error
        ):
            raise


    # -----------------------------------------
    # Fallback Provider: OpenRouter
    # -----------------------------------------

    try:

        print(
            "[LLM] Switching to OpenRouter..."
        )

        response = generate_with_openrouter(
            prompt
        )

        print(
            "[LLM] OpenRouter succeeded."
        )

        return response

    except Exception as openrouter_error:

        print(
            "[LLM] OpenRouter failed:",
            openrouter_error
        )

        raise RuntimeError(
            "All available LLM providers failed. "
            f"OpenRouter error: {openrouter_error}"
        ) from openrouter_error