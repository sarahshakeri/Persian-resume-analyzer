def build_structured_resume_prompt(text):

    prompt = f"""
You are a professional resume information extraction system.

Your task is to extract structured information from a Persian resume
and return ONLY valid JSON.

Important rules:

1. Extract ONLY information explicitly available in the resume.
2. Never invent missing information.
3. If a field is not available, use null.
4. Preserve Persian names, organizations, dates, and technical terms.
5. Do not summarize.
6. Do not evaluate the candidate.
7. Do not provide strengths, weaknesses, or suggestions.
8. Do not add explanations outside JSON.
9. Return exactly the requested JSON structure.
10. Do not wrap JSON inside Markdown code blocks.

Make sure you extract all available sections:
- Personal Information
- Education
- Work Experience
- Skills
- Languages
- Certificates
- Projects

JSON Structure:

{{
    "personal_information": {{
        "name": null,
        "phone": null,
        "email": null,
        "location": null,
        "marital_status": null,
        "birth_date": null
    }},

    "education": [],

    "work_experience": [],

    "skills": {{
        "programming_languages": [],
        "libraries_frameworks": [],
        "ai_ml_topics": [],
        "computer_skills": []
    }},

    "languages": [],

    "certificates": [],

    "projects": []
}}


Resume:

--- START ---

{text}

--- END ---
"""

    return prompt