import json
import streamlit as st


def _parse_quality_response(response):

    if response is None:
        raise ValueError(
            "Quality analysis response is empty."
        )

    if isinstance(response, dict):
        return response

    if not isinstance(response, str):
        raise ValueError(
            "Unsupported quality response format."
        )

    text = response.strip()

    if not text:
        raise ValueError(
            "Quality analysis response is empty."
        )

    if text.startswith("```json"):
        text = text[7:]

    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()

    try:
        return json.loads(text)

    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}")

    if (
        start == -1
        or end == -1
        or end <= start
    ):
        raise ValueError(
            "Quality analysis does not contain valid JSON."
        )

    json_text = text[
        start:end + 1
    ]

    try:
        return json.loads(
            json_text
        )

    except json.JSONDecodeError as error:

        raise ValueError(
            "Quality analysis returned malformed JSON."
        ) from error


def _show_issue(issue):

    if isinstance(issue, str):
        st.warning(issue)
        return

    if not isinstance(issue, dict):
        st.write(issue)
        return

    problem = issue.get(
        "issue",
        "Not Found"
    )

    st.warning(problem)

    why = issue.get(
        "why_it_matters"
    )

    if why:

        st.write(
            "**Why it matters:**",
            why
        )

    suggestion = issue.get(
        "improvement_suggestion"
    )

    if suggestion:

        st.write(
            "**Suggestion:**",
            suggestion
        )


def show_quality_analysis(result):

    if not result:
        return

    st.subheader(
        "🔍 Resume Quality Assessment"
    )

    try:

        quality = _parse_quality_response(
            result
        )

    except Exception as error:

        st.error(
            "The quality analysis was generated, "
            "but its response format could not be processed."
        )

        with st.expander(
            "Technical details"
        ):
            st.exception(error)

        return


    # ========================================================
    # Overall Score
    # Supports both old and new JSON structures
    # ========================================================

    overall = quality.get(
        "overall_quality",
        {}
    )

    if overall:

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Overall Score",
                f"{overall.get('overall_score', 0)}/100"
            )

        with col2:

            st.metric(
                "Content Score",
                f"{overall.get('content_score', 0)}/100"
            )

        with col3:

            st.metric(
                "Presentation Score",
                f"{overall.get('presentation_score', 0)}/100"
            )

    else:

        overall_score = quality.get(
            "overall_quality_score"
        )

        if isinstance(
            overall_score,
            (int, float)
        ):

            safe_score = max(
                0,
                min(float(overall_score), 100)
            )

            st.metric(
                "Overall Quality Score",
                f"{safe_score:g}/100"
            )

            st.progress(
                safe_score / 100
            )

    st.divider()


    # ========================================================
    # ATS
    # ========================================================

    ats = quality.get(
        "ats_evaluation",
        {}
    )

    if ats:

        ats_score = ats.get(
            "score"
        )

        if ats_score is not None:

            st.subheader(
                f"🤖 ATS Evaluation — {ats_score}/100"
            )

        else:

            st.subheader(
                "🤖 ATS Evaluation"
            )

        positives = ats.get(
            "positive_points",
            []
        )

        for item in positives:
            st.success(item)

        issues = ats.get(
            "issues",
            []
        )

        for issue in issues:

            _show_issue(issue)

            st.divider()


    # ========================================================
    # Structure
    # ========================================================

    structure = quality.get(
        "structure_evaluation",
        {}
    )

    if structure:

        structure_score = structure.get(
            "score"
        )

        if structure_score is not None:

            st.subheader(
                f"📑 Structure Evaluation — "
                f"{structure_score}/100"
            )

        else:

            st.subheader(
                "📑 Structure Evaluation"
            )

        positives = structure.get(
            "positive_points",
            []
        )

        for item in positives:
            st.success(item)

        for issue in structure.get(
            "issues",
            []
        ):

            _show_issue(issue)

            st.divider()


    # ========================================================
    # Experience Quality
    # ========================================================

    experience = quality.get(
        "experience_quality",
        {}
    )

    if experience:

        experience_score = experience.get(
            "score"
        )

        if experience_score is not None:

            st.subheader(
                f"💼 Experience Quality — "
                f"{experience_score}/100"
            )

        else:

            st.subheader(
                "💼 Experience Quality"
            )

        positives = experience.get(
            "positive_points",
            []
        )

        for item in positives:
            st.success(item)

        for issue in experience.get(
            "issues",
            []
        ):

            _show_issue(issue)

            st.divider()


    # ========================================================
    # Technical Profile
    # ========================================================

    technical = quality.get(
        "technical_profile",
        {}
    )

    if technical:

        technical_score = technical.get(
            "score"
        )

        if technical_score is not None:

            st.subheader(
                f"🛠 Technical Profile — "
                f"{technical_score}/100"
            )

        else:

            st.subheader(
                "🛠 Technical Profile"
            )

        for strength in technical.get(
            "strengths",
            []
        ):
            st.success(strength)

        gaps = technical.get(
            "skill_gaps",
            []
        )

        for gap in gaps:

            _show_issue(gap)

            st.divider()


    # ========================================================
    # Recruiter Perspective
    # ========================================================

    recruiter = quality.get(
        "recruiter_perspective",
        {}
    )

    if recruiter:

        st.subheader(
            "👤 Recruiter Perspective"
        )

        st.write(
            recruiter.get(
                "first_impression",
                "Not Found"
            )
        )

        concerns = recruiter.get(
            "main_concerns",
            []
        )

        if concerns:

            st.write(
                "**Main Concerns:**"
            )

            for concern in concerns:
                st.warning(concern)

        st.divider()


    # ========================================================
    # Priority Improvements
    # ========================================================

    improvements = quality.get(
        "priority_improvements",
        []
    )

    if improvements:

        st.subheader(
            "🚀 Priority Improvements"
        )

        for index, item in enumerate(
            improvements,
            start=1
        ):

            if not isinstance(
                item,
                dict
            ):
                st.info(item)
                continue

            priority = item.get(
                "priority",
                "Not Found"
            )

            issue = item.get(
                "issue",
                "Not Found"
            )

            with st.expander(
                f"{index}. {priority} — {issue}",
                expanded=True
            ):

                st.write(
                    "**Impact:**",
                    item.get(
                        "impact",
                        "Not Found"
                    )
                )

                st.write(
                    "**Recommendation:**",
                    item.get(
                        "recommendation",
                        "Not Found"
                    )
                )