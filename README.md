# Persian Resume Analyzer

An AI-powered application for analyzing, evaluating, and improving Persian resumes using Large Language Models (LLMs).

The system processes Persian resume documents, extracts and structures their content, evaluates resume quality, identifies potential weaknesses, and provides AI-assisted suggestions for improvement.

---

## Overview

Persian Resume Analyzer is designed to provide an intelligent and structured analysis of Persian-language resumes.

The project combines traditional rule-based processing with Large Language Models to evaluate different aspects of a resume and generate useful feedback for improving its content and overall quality.

The application provides a user-friendly interface built with Streamlit and supports modular AI services for resume processing and analysis.

---

## Features

- Persian resume processing and text extraction
- PDF resume text extraction
- Resume content cleaning and preprocessing
- Structured information extraction
- Rule-based resume analysis
- LLM-based resume analysis
- Resume quality assessment
- Identification of potential weaknesses
- AI-assisted resume improvement suggestions
- Modular support for Gemini and OpenRouter
- Interactive web interface using Streamlit

---

## How It Works

The application follows a multi-stage resume analysis pipeline:

1. **Resume Input**  
   The user provides a resume document for analysis.

2. **Text Extraction & Preprocessing**  
   Resume content is extracted and cleaned before further processing.

3. **Structured Extraction**  
   Important resume information is converted into a structured representation.

4. **Rule-Based Analysis**  
   The resume is evaluated using predefined rules and quality criteria.

5. **LLM-Based Analysis**  
   Large Language Models perform deeper semantic analysis of the resume.

6. **Quality Assessment**  
   Different aspects of the resume are evaluated to identify strengths and weaknesses.

7. **Improvement Suggestions**  
   The system generates suggestions for improving the resume.

---

## Project Structure

```text
Persian-resume-analyzer/
│
├── assets/
│   └── fonts/
│
├── prompts/
│   ├── analysis_prompt.py
│   ├── quality_analysis_prompt.py
│   ├── repair_prompt.py
│   └── structured_resume_prompt.py
│
├── services/
│   ├── gemini_service.py
│   ├── llm_service.py
│   ├── openrouter_service.py
│   ├── resume_analyzer.py
│   ├── resume_quality_analyzer.py
│   ├── rule_based_analyzer.py
│   └── structured_extractor.py
│
├── utils/
│   ├── pdf_reader.py
│   └── text_cleaner.py
│
├── views/
│   ├── analysis_view.py
│   ├── precheck_view.py
│   ├── quality_view.py
│   └── structured_view.py
│
├── app.py
├── style.py
├── requirements.txt
├── .gitignore
└── README.md
