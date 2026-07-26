import streamlit as st

from style import apply_custom_style

from utils.pdf_reader import extract_text
from utils.text_cleaner import clean_text

from services.llm_service import generate_llm_response
from prompts.repair_prompt import build_repair_prompt

from services.resume_analyzer import analyze_resume
from services.structured_extractor import extract_structured_resume
from services.resume_quality_analyzer import analyze_resume_quality
from services.rule_based_analyzer import analyze_resume_rules

from views.precheck_view import show_precheck
from views.structured_view import show_structured_resume
from views.analysis_view import show_analysis
from views.quality_view import show_quality_analysis


# ============================================================
# Streamlit Configuration
# ============================================================

st.set_page_config(
    page_title="تحلیل‌گر رزومه فارسی",
    page_icon="📄",
    layout="wide"
)


# ============================================================
# Application Style
# ============================================================

apply_custom_style()


# ============================================================
# Page Header
# ============================================================

st.title("📄 تحلیل‌گر هوشمند رزومه فارسی")

st.write(
    "رزومه خود را بارگذاری کنید تا مراحل استخراج، بررسی و تحلیل آن انجام شود."
)


# ============================================================
# Session State
# ============================================================

default_states = {
    "repaired_text": None,
    "structured_data": None,
    "analysis_result": None,
    "quality_result": None,
    "rule_result": None,
    "current_file": None,
}


for key, default_value in default_states.items():

    if key not in st.session_state:
        st.session_state[key] = default_value


# ============================================================
# Reset Analysis State
# ============================================================

def reset_resume_state():

    st.session_state.repaired_text = None
    st.session_state.structured_data = None
    st.session_state.analysis_result = None
    st.session_state.quality_result = None
    st.session_state.rule_result = None


# ============================================================
# File Upload
# ============================================================

uploaded_file = st.file_uploader(
    "📄 رزومه خود را با فرمت PDF بارگذاری کنید",
    type=["pdf"]
)


if uploaded_file is not None:

    # --------------------------------------------------------
    # Detect New Resume
    # --------------------------------------------------------

    file_identifier = (
        uploaded_file.name,
        uploaded_file.size
    )

    if (
        st.session_state.current_file
        != file_identifier
    ):

        reset_resume_state()

        st.session_state.current_file = (
            file_identifier
        )


    st.success(
        "رزومه با موفقیت بارگذاری شد."
    )

    st.write(
        "نام فایل:",
        uploaded_file.name
    )

    st.write(
        "حجم فایل:",
        uploaded_file.size,
        "بایت"
    )


    # ========================================================
    # PDF Text Extraction
    # ========================================================

    try:

        raw_text = extract_text(
            uploaded_file
        )

    except Exception as error:

        st.error(
            "❌ استخراج متن از فایل PDF با خطا مواجه شد."
        )

        st.exception(error)

        st.stop()


    st.subheader(
        "متن استخراج‌شده از رزومه"
    )

    st.text_area(
        "متن اولیه",
        raw_text,
        height=250
    )


    # ========================================================
    # Text Cleaning
    # ========================================================

    try:

        cleaned_text = clean_text(
            raw_text
        )

    except Exception as error:

        st.error(
            "❌ پاک‌سازی متن استخراج‌شده با خطا مواجه شد."
        )

        st.exception(error)

        st.stop()


    st.subheader(
        "متن پس از پاک‌سازی"
    )

    st.text_area(
        "متن پاک‌سازی‌شده",
        cleaned_text,
        height=250
    )


    # ========================================================
    # Rule-Based Resume Pre-Check
    # ========================================================

    if st.button(
        "🔎 اجرای ارزیابی اولیه رزومه",
        use_container_width=True
    ):

        try:

            with st.spinner(
                "در حال بررسی اولیه رزومه..."
            ):

                rule_result = (
                    analyze_resume_rules(
                        cleaned_text
                    )
                )

            st.session_state.rule_result = (
                rule_result
            )

            st.success(
                "ارزیابی اولیه رزومه با موفقیت انجام شد."
            )

        except Exception as error:

            st.error(
                "❌ اجرای ارزیابی اولیه رزومه با خطا مواجه شد."
            )

            st.exception(error)


    # ========================================================
    # Display Rule-Based Results
    # ========================================================

    if st.session_state.rule_result:

        show_precheck(
            st.session_state.rule_result
        )


    # ========================================================
    # AI Text Repair
    # ========================================================

    st.divider()

    if st.button(
        "✨ اصلاح متن رزومه با هوش مصنوعی",
        use_container_width=True
    ):

        try:

            with st.spinner(
                "در حال اصلاح متن فارسی رزومه..."
            ):

                repair_prompt = (
                    build_repair_prompt(
                        cleaned_text
                    )
                )

                repaired_text = (
                    generate_llm_response(
                        repair_prompt
                    )
                )

            st.session_state.repaired_text = (
                repaired_text
            )

            st.session_state.structured_data = None
            st.session_state.analysis_result = None
            st.session_state.quality_result = None

            st.success(
                "اصلاح متن با هوش مصنوعی با موفقیت انجام شد."
            )

        except Exception as error:

            st.error(
                "❌ اصلاح متن با هوش مصنوعی انجام نشد. "
                "ممکن است سرویس‌های هوش مصنوعی در حال حاضر در دسترس نباشند."
            )

            st.exception(error)


    # ========================================================
    # Display Repaired Text
    # ========================================================

    if st.session_state.repaired_text:

        st.subheader(
            "✨ متن اصلاح‌شده با هوش مصنوعی"
        )

        st.text_area(
            "متن اصلاح‌شده",
            st.session_state.repaired_text,
            height=350
        )


        # ====================================================
        # Structured Resume Extraction
        # ====================================================

        if st.button(
            "📊 استخراج اطلاعات ساختاریافته رزومه",
            use_container_width=True
        ):

            try:

                with st.spinner(
                    "در حال استخراج اطلاعات ساختاریافته..."
                ):

                    structured_data = (
                        extract_structured_resume(
                            st.session_state.repaired_text
                        )
                    )

                st.session_state.structured_data = (
                    structured_data
                )

                st.session_state.analysis_result = None
                st.session_state.quality_result = None

                st.success(
                    "اطلاعات ساختاریافته رزومه با موفقیت استخراج شد."
                )

            except Exception as error:

                st.error(
                    "❌ استخراج اطلاعات ساختاریافته با خطا مواجه شد."
                )

                st.exception(error)


    # ========================================================
    # Structured Resume View
    # ========================================================

    if st.session_state.structured_data:

        show_structured_resume(
            st.session_state.structured_data
        )


        # ====================================================
        # AI Analysis Actions
        # ====================================================

        st.divider()

        col1, col2 = st.columns(2)


        # ----------------------------------------------------
        # General Resume Analysis
        # ----------------------------------------------------

        with col1:

            analyze_button = st.button(
                "🧠 تحلیل رزومه با هوش مصنوعی",
                use_container_width=True
            )


        # ----------------------------------------------------
        # Quality Analysis
        # ----------------------------------------------------

        with col2:

            quality_button = st.button(
                "🔍 ارزیابی کیفیت رزومه",
                use_container_width=True
            )


        # ====================================================
        # Run General AI Analysis
        # ====================================================

        if analyze_button:

            try:

                with st.spinner(
                    "در حال تحلیل رزومه..."
                ):

                    analysis_result = (
                        analyze_resume(
                            st.session_state.structured_data
                        )
                    )

                st.session_state.analysis_result = (
                    analysis_result
                )

                st.success(
                    "تحلیل رزومه با موفقیت انجام شد."
                )

            except Exception as error:

                st.error(
                    "❌ تحلیل رزومه با خطا مواجه شد."
                )

                st.exception(error)


        # ====================================================
        # Run Quality Analysis
        # ====================================================

        if quality_button:

            try:

                with st.spinner(
                    "در حال ارزیابی کیفیت رزومه..."
                ):

                    quality_result = (
                        analyze_resume_quality(
                            st.session_state.structured_data
                        )
                    )

                st.session_state.quality_result = (
                    quality_result
                )

                st.success(
                    "ارزیابی کیفیت رزومه با موفقیت انجام شد."
                )

            except Exception as error:

                st.error(
                    "❌ ارزیابی کیفیت رزومه با خطا مواجه شد."
                )

                st.exception(error)


    # ========================================================
    # AI Resume Analysis View
    # ========================================================

    if st.session_state.analysis_result:

        st.divider()

        show_analysis(
            st.session_state.analysis_result
        )


    # ========================================================
    # Resume Quality View
    # ========================================================

    if st.session_state.quality_result:

        st.divider()

        show_quality_analysis(
            st.session_state.quality_result
        )


# ============================================================
# No Resume Uploaded
# ============================================================

else:

    st.info(
        "برای شروع تحلیل، یک رزومه با فرمت PDF بارگذاری کنید."
    )