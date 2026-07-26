import streamlit as st


def show_precheck(result):

    if not result:
        return

    # ==================================================
    # Score
    # ==================================================

    st.subheader("🔎 ارزیابی اولیه رزومه")

    score = result.get("rule_based_score", 0)
    score_breakdown = result.get("score_breakdown", {})

    with st.expander("📊 مشاهده جزئیات امتیازدهی"):

        score_labels = {
            "contact_information": "اطلاعات تماس",
            "professional_links": "لینک‌های حرفه‌ای",
            "resume_structure": "ساختار رزومه",
            "achievement_quality": "کیفیت دستاوردها",
            "writing_quality": "کیفیت نگارش",
            "content_completeness": "کامل بودن محتوا",
        }

        max_scores = {
            "contact_information": 15,
            "professional_links": 10,
            "resume_structure": 25,
            "achievement_quality": 20,
            "writing_quality": 10,
            "content_completeness": 20,
        }

        for key, value in score_breakdown.items():

            label = score_labels.get(key, key)
            maximum = max_scores.get(key, "")

            st.write(
                f"**{label}:** {value} از {maximum}"
            )

    st.metric(
        "امتیاز ارزیابی اولیه",
        f"{score}/100"
    )

    st.progress(
        max(0, min(score, 100)) / 100
    )

    st.divider()

    # ==================================================
    # Contact Information
    # ==================================================

    st.subheader("📞 اطلاعات تماس")

    contact = result.get(
        "contact_information",
        {}
    )

    col1, col2 = st.columns(2)

    with col1:

        if contact.get("email_found"):
            st.success("ایمیل شناسایی شد.")
        else:
            st.warning("ایمیل شناسایی نشد.")

    with col2:

        if contact.get("phone_found"):
            st.success("شماره تلفن شناسایی شد.")
        else:
            st.warning("شماره تلفن شناسایی نشد.")

    st.divider()

    # ==================================================
    # Professional Links
    # ==================================================

    st.subheader("🔗 لینک‌های حرفه‌ای")

    links = result.get(
        "professional_links",
        {}
    )

    col1, col2 = st.columns(2)

    with col1:

        if links.get("linkedin_found"):
            st.success("LinkedIn شناسایی شد.")
        else:
            st.info("LinkedIn شناسایی نشد.")

    with col2:

        if links.get("github_found"):
            st.success("GitHub شناسایی شد.")
        else:
            st.info("GitHub شناسایی نشد.")

    st.divider()

    # ==================================================
    # Resume Structure
    # ==================================================

    st.subheader("📑 ساختار رزومه")

    structure = result.get(
        "structure_analysis",
        {}
    )

    section_names = {
        "education": "تحصیلات",
        "work_experience": "سوابق کاری",
        "experience": "سوابق کاری",
        "skills": "مهارت‌ها",
        "projects": "پروژه‌ها",
        "certifications": "گواهینامه‌ها",
        "languages": "زبان‌ها",
        "summary": "خلاصه حرفه‌ای",
        "objective": "هدف شغلی",
        "contact_information": "اطلاعات تماس",
    }

    for section, detected in structure.items():

        section_name = section_names.get(
            section,
            section.replace("_", " ")
        )

        if detected:
            st.success(
                f"بخش «{section_name}» شناسایی شد."
            )
        else:
            st.warning(
                f"بخش «{section_name}» شناسایی نشد."
            )

    st.divider()

    # ==================================================
    # Achievement Analysis
    # ==================================================

    st.subheader("🏆 تحلیل دستاوردها")

    achievement = result.get(
        "achievement_analysis",
        {}
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "افعال اثرگذار",
            achievement.get(
                "action_verbs_detected",
                0
            )
        )

    with col2:

        st.metric(
            "نتایج قابل‌اندازه‌گیری",
            achievement.get(
                "measurable_results_detected",
                0
            )
        )

    with col3:

        status = achievement.get(
            "status",
            "Unknown"
        )

        status_translation = {
            "Excellent": "عالی",
            "Good": "خوب",
            "Strong": "قوی",
            "Moderate": "متوسط",
            "Average": "متوسط",
            "Weak": "ضعیف",
            "Poor": "ضعیف",
            "Unknown": "نامشخص",
        }

        status = status_translation.get(
            status,
            status
        )

        st.metric(
            "وضعیت دستاوردها",
            status
        )

    st.divider()

    # ==================================================
    # Writing Quality
    # ==================================================

    st.subheader("✍️ کیفیت نگارش")

    writing = result.get(
        "writing_quality",
        {}
    )

    st.metric(
        "تعداد Bullet Pointها",
        writing.get(
            "bullet_points",
            0
        )
    )

    st.divider()

    # ==================================================
    # Detected Issues
    # ==================================================

    st.subheader("⚠️ موارد نیازمند بهبود")

    issues = result.get(
        "issues",
        []
    )

    if not issues:

        st.success(
            "در ارزیابی قانون‌محور، مشکل مهمی شناسایی نشد."
        )

    else:

        severity_translation = {
            "High": "اهمیت زیاد",
            "Medium": "اهمیت متوسط",
            "Low": "اهمیت کم",
            "Critical": "بحرانی",
            "Unknown": "نامشخص",
        }

        category_translation = {
            "Contact Information": "اطلاعات تماس",
            "Contact": "اطلاعات تماس",
            "Professional Profile": "پروفایل حرفه‌ای",
            "Technical Portfolio": "پورتفولیوی فنی",
            "Resume Structure": "ساختار رزومه",
            "Structure": "ساختار رزومه",
            "Achievements": "دستاوردها",
            "Writing Quality": "کیفیت نگارش",
            "Skills": "مهارت‌ها",
            "Technical Skills": "مهارت‌های فنی",
            "Experience": "سوابق کاری",
            "Work Experience": "سوابق کاری",
            "Education": "تحصیلات",
            "Projects": "پروژه‌ها",
            "General": "عمومی",
        }

        for index, issue in enumerate(
            issues,
            start=1
        ):

            severity = issue.get(
                "severity",
                "Unknown"
            )

            category = issue.get(
                "category",
                "General"
            )

            problem = issue.get(
                "issue",
                "یافت نشد"
            )

            suggestion = issue.get(
                "suggestion",
                "یافت نشد"
            )

            severity_fa = severity_translation.get(
                severity,
                severity
            )

            category_fa = category_translation.get(
                category,
                category
            )

            with st.expander(
                f"{index}. {category_fa} — {severity_fa}"
            ):

                st.markdown(
                    f"**مشکل:** {problem}"
                )

                st.markdown(
                    f"**پیشنهاد:** {suggestion}"
                )