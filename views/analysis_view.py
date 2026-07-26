import json
import streamlit as st


# ============================================================
# JSON Response Parser
# ============================================================

def _parse_ai_response(response):

    if response is None:
        raise ValueError(
            "AI returned an empty response."
        )

    # Already parsed
    if isinstance(response, dict):
        return response

    if not isinstance(response, str):
        raise ValueError(
            "Unsupported AI response format."
        )

    response_text = response.strip()

    if not response_text:
        raise ValueError(
            "AI returned an empty response."
        )

    # --------------------------------------------------------
    # Remove Markdown code fences
    # --------------------------------------------------------

    if response_text.startswith("```json"):
        response_text = response_text[7:]

    elif response_text.startswith("```"):
        response_text = response_text[3:]

    if response_text.endswith("```"):
        response_text = response_text[:-3]

    response_text = response_text.strip()

    # --------------------------------------------------------
    # First attempt: normal JSON
    # --------------------------------------------------------

    try:
        return json.loads(response_text)

    except json.JSONDecodeError:
        pass

    # --------------------------------------------------------
    # Second attempt:
    # Extract JSON if model added surrounding text
    # --------------------------------------------------------

    start = response_text.find("{")
    end = response_text.rfind("}")

    if (
        start == -1
        or end == -1
        or end <= start
    ):
        raise ValueError(
            "AI response does not contain a valid JSON object."
        )

    json_text = response_text[
        start:end + 1
    ]

    try:
        return json.loads(json_text)

    except json.JSONDecodeError as error:

        raise ValueError(
            "AI returned malformed JSON."
        ) from error


# ============================================================
# Helper for lists
# ============================================================

def _show_list(items, message_type="write"):

    if not items:
        st.write("Not Found")
        return

    for item in items:

        if isinstance(item, dict):

            for key, value in item.items():

                label = key.replace(
                    "_",
                    " "
                ).title()

                st.write(
                    f"**{label}:**",
                    value
                )

        else:

            if message_type == "success":
                st.success(item)

            elif message_type == "warning":
                st.warning(item)

            elif message_type == "info":
                st.info(item)

            else:
                st.write("•", item)


# ============================================================
# Main Analysis View
# ============================================================

def show_analysis(result):

    if not result:
        return

    st.subheader(
        "🧠 AI Resume Analysis"
    )

    try:

        analysis = _parse_ai_response(
            result
        )

    except Exception as error:

        st.error(
            "The AI analysis was generated, "
            "but its response format could not be processed."
        )

        with st.expander(
            "Technical details"
        ):
            st.exception(error)

        return


    # ========================================================
    # Resume Score
    # ========================================================

    score = analysis.get(
        "resume_score"
    )

    if isinstance(
        score,
        (int, float)
    ):

        safe_score = max(
            0,
            min(float(score), 100)
        )

        st.metric(
            "Resume Score",
            f"{safe_score:g}/100"
        )

        st.progress(
            safe_score / 100
        )

    st.divider()


    # ========================================================
    # Personal Information
    # ========================================================

    st.subheader(
        "👤 Personal Information"
    )

    personal = analysis.get(
        "personal_information",
        {}
    )

    st.write(
        personal.get(
            "summary",
            "Not Found"
        )
    )

    positioning = personal.get(
        "professional_positioning"
    )

    if positioning:

        st.write(
            "**Professional Positioning:**",
            positioning
        )

    st.divider()


    # ========================================================
    # Education
    # ========================================================

    st.subheader(
        "🎓 Education"
    )

    education = analysis.get(
        "education_evaluation",
        {}
    )

    st.write(
        education.get(
            "summary",
            "Not Found"
        )
    )

    relevance = education.get(
        "relevance_to_target_career"
    )

    if relevance:

        st.write(
            "**Career Relevance:**",
            relevance
        )

    missing = education.get(
        "missing_items",
        []
    )

    if missing:

        st.write(
            "**Missing / Weak Information:**"
        )

        _show_list(
            missing,
            "warning"
        )

    st.divider()


    # ========================================================
    # Work Experience
    # ========================================================

    st.subheader(
        "💼 Work Experience"
    )

    work = analysis.get(
        "work_experience_evaluation",
        {}
    )

    st.write(
        work.get(
            "summary",
            "Not Found"
        )
    )

    impact_level = work.get(
        "impact_level"
    )

    if impact_level:

        st.write(
            "**Impact Level:**",
            impact_level
        )

    achievement_quality = work.get(
        "achievement_quality"
    )

    if achievement_quality:

        st.write(
            "**Achievement Quality:**",
            achievement_quality
        )

    work_missing = work.get(
        "missing_items",
        []
    )

    if work_missing:

        st.write(
            "**Missing / Weak Information:**"
        )

        _show_list(
            work_missing,
            "warning"
        )

    st.divider()


    # ========================================================
    # Technical Skills
    # ========================================================

    st.subheader(
        "🛠 Technical Skills"
    )

    skills = analysis.get(
        "technical_skills_evaluation",
        {}
    )

    identified_skills = skills.get(
        "identified_skills",
        []
    )

    if identified_skills:

        for skill in identified_skills:
            st.write(
                "✅",
                skill
            )

    else:

        st.write(
            "No technical skills were identified."
        )

    skill_depth = skills.get(
        "skill_depth_assessment"
    )

    if skill_depth:

        st.write(
            "**Skill Depth Assessment:**",
            skill_depth
        )

    skill_missing = skills.get(
        "missing_items",
        []
    )

    if skill_missing:

        st.write(
            "**Potential Skill Gaps:**"
        )

        _show_list(
            skill_missing,
            "warning"
        )

    st.divider()


    # ========================================================
    # Project Evaluation
    # ========================================================

    project = analysis.get(
        "project_evaluation"
    )

    if project:

        st.subheader(
            "📁 Project Evaluation"
        )

        st.write(
            project.get(
                "summary",
                "Not Found"
            )
        )

        project_missing = project.get(
            "missing_items",
            []
        )

        if project_missing:

            st.write(
                "**Missing / Weak Information:**"
            )

            _show_list(
                project_missing,
                "warning"
            )

        project_suggestions = project.get(
            "improvement_suggestions",
            []
        )

        if project_suggestions:

            st.write(
                "**Project Improvements:**"
            )

            _show_list(
                project_suggestions,
                "info"
            )

        st.divider()


    # ========================================================
    # ATS Evaluation
    # ========================================================

    ats = analysis.get(
        "ats_evaluation"
    )

    if ats:

        st.subheader(
            "🤖 ATS Evaluation"
        )

        ats_score = ats.get(
            "score"
        )

        if isinstance(
            ats_score,
            (int, float)
        ):

            st.metric(
                "ATS Score",
                f"{ats_score}/100"
            )

        problems = ats.get(
            "problems",
            []
        )

        if problems:

            st.write(
                "**ATS Problems:**"
            )

            _show_list(
                problems,
                "warning"
            )

        suggestions = ats.get(
            "suggestions",
            []
        )

        if suggestions:

            st.write(
                "**ATS Suggestions:**"
            )

            _show_list(
                suggestions,
                "info"
            )

        st.divider()


    # ========================================================
    # Strengths
    # ========================================================

    st.subheader(
        "💪 Strengths"
    )

    strengths = analysis.get(
        "strengths",
        []
    )

    _show_list(
        strengths,
        "success"
    )

    st.divider()


    # ========================================================
    # Weaknesses
    # ========================================================

    st.subheader(
        "⚠️ Weaknesses"
    )

    weaknesses = analysis.get(
        "weaknesses",
        []
    )

    _show_list(
        weaknesses,
        "warning"
    )

    st.divider()


    # ========================================================
    # Recommendations
    # ========================================================

    st.subheader(
        "🚀 Recommendations"
    )

    recommendations = analysis.get(
        "recommendations",
        []
    )

    _show_list(
        recommendations,
        "info"
    )