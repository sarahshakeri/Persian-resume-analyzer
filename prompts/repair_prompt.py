def build_repair_prompt(text):

    prompt = f"""
You are a Persian resume text reconstruction assistant.

The following text has been extracted from a Persian PDF resume.
Due to PDF text extraction and RTL/LTR layout issues, the extracted text
may contain broken Persian words, incorrect character spacing, misplaced
line breaks, or incorrect reading order.

Your task is to reconstruct the extracted text while preserving the
original resume content as faithfully as possible.

Rules:

1. Repair incorrectly separated or broken Persian words.
2. Fix unnecessary line breaks inside words, phrases, and sentences.
3. Normalize Persian spacing and half-spaces where appropriate.
4. Correct obvious RTL/LTR extraction artifacts when they can be repaired
   without guessing or inventing information.
5. Preserve English technical terms such as Python, NLP, SVM, ICDL,
   Machine Learning, Transformer, etc.
6. Preserve section titles, bullet points, and resume structure whenever possible.
7. Do NOT summarize the text.
8. Do NOT rewrite, enhance, or professionally improve the resume content.
9. Do NOT add any information that does not exist in the input.
10. Do NOT remove information from the input.
11. Preserve names, dates, numbers, universities, organizations,
    project names, and technical terminology exactly.
12. If a corrupted fragment cannot be reconstructed confidently,
    preserve it rather than guessing.
13. Return ONLY the repaired resume text.
14. Do not provide explanations, comments, introductions,
    Markdown formatting, or code blocks.

Extracted resume text:

--- START OF RESUME ---

{text}

--- END OF RESUME ---
"""

    return prompt