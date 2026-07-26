import base64
from pathlib import Path

import streamlit as st


def _font_to_base64(font_path):
    with open(font_path, "rb") as font_file:
        return base64.b64encode(font_file.read()).decode()


def apply_custom_style():
    base_dir = Path(__file__).resolve().parent
    fonts_dir = base_dir / "assets" / "fonts"

    regular_font = _font_to_base64(
        fonts_dir / "Vazirmatn-Regular.woff2"
    )

    medium_font = _font_to_base64(
        fonts_dir / "Vazirmatn-Medium.woff2"
    )

    bold_font = _font_to_base64(
        fonts_dir / "Vazirmatn-Bold.woff2"
    )

    st.markdown(
        f"""
        <style>

        /* -------------------- Fonts -------------------- */

        @font-face {{
            font-family: "Vazirmatn";
            src: url(data:font/woff2;base64,{regular_font}) format("woff2");
            font-weight: 400;
            font-style: normal;
        }}

        @font-face {{
            font-family: "Vazirmatn";
            src: url(data:font/woff2;base64,{medium_font}) format("woff2");
            font-weight: 500;
            font-style: normal;
        }}

        @font-face {{
            font-family: "Vazirmatn";
            src: url(data:font/woff2;base64,{bold_font}) format("woff2");
            font-weight: 700;
            font-style: normal;
        }}


        /* -------------------- Main Persian UI -------------------- */

        html,
        body,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"] {{
            font-family: "Vazirmatn", sans-serif;
        }}


        /* -------------------- Markdown / Text -------------------- */

        [data-testid="stMarkdownContainer"],
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stMarkdownContainer"] strong {{
            font-family: "Vazirmatn", sans-serif !important;
            direction: rtl;
            text-align: right;
        }}


        /* -------------------- Headings -------------------- */

        h1,
        h2,
        h3,
        h4,
        h5,
        h6 {{
            font-family: "Vazirmatn", sans-serif !important;
            direction: rtl;
            text-align: right;
        }}

        h1 {{
            font-weight: 700 !important;
        }}

        h2,
        h3 {{
            font-weight: 700 !important;
        }}


        /* -------------------- Buttons -------------------- */

        .stButton > button,
        .stButton > button p,
        .stButton > button span,
        [data-testid="stBaseButton-secondary"],
        [data-testid="stBaseButton-primary"],
        [data-testid="stBaseButton-secondary"] p,
        [data-testid="stBaseButton-primary"] p {{
            font-family: "Vazirmatn", sans-serif !important;
        }}

        .stButton > button {{
            direction: rtl;
        }}


        /* -------------------- File Uploader -------------------- */

        [data-testid="stFileUploader"],
        [data-testid="stFileUploader"] small,
        [data-testid="stFileUploader"] button {{
            font-family: "Vazirmatn", sans-serif !important;
        }}

        [data-testid="stFileUploader"] label {{
            font-family: "Vazirmatn", sans-serif !important;
            direction: rtl;
            text-align: right;
        }}


        /* -------------------- Alerts -------------------- */

        [data-testid="stAlert"],
        [data-testid="stAlert"] p,



        /* -------------------- Metrics -------------------- */

        [data-testid="stMetric"],
        [data-testid="stMetric"] * {{
            font-family: "Vazirmatn", sans-serif !important;
        }}

        [data-testid="stMetricLabel"] {{
            direction: rtl;
            text-align: right;
        }}

        [data-testid="stMetricLabel"] p {{
            font-family: "Vazirmatn", sans-serif !important;
        }}

        [data-testid="stMetricValue"] {{
            font-family: "Vazirmatn", sans-serif !important;
            direction: ltr;
            text-align: right;
        }}


        /* -------------------- Expanders -------------------- */

        [data-testid="stExpander"],
        [data-testid="stExpander"] summary,
        [data-testid="stExpander"] summary p {{
            font-family: "Vazirmatn", sans-serif !important;
        }}

        [data-testid="stExpander"] summary {{
            direction: rtl;
            text-align: right;
        }}

        [data-testid="stExpander"] [data-testid="stMarkdownContainer"],
        [data-testid="stExpander"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stExpander"] [data-testid="stMarkdownContainer"] strong {{
            font-family: "Vazirmatn", sans-serif !important;
            direction: rtl;
            text-align: right;
        }}


        /* -------------------- Text Areas / Inputs -------------------- */

        textarea,
        input {{
            font-family: "Vazirmatn", sans-serif !important;
        }}

        textarea {{
            direction: rtl !important;
            text-align: right !important;
        }}

        [data-testid="stTextArea"],
        [data-testid="stTextArea"] label,
        [data-testid="stTextArea"] label p {{
            font-family: "Vazirmatn", sans-serif !important;
        }}


        /* -------------------- Captions -------------------- */

        [data-testid="stCaptionContainer"],
        [data-testid="stCaptionContainer"] p {{
            font-family: "Vazirmatn", sans-serif !important;
            direction: rtl;
            text-align: right;
        }}


        /* -------------------- Generic Streamlit text -------------------- */

        .stText,
        .stCaption,
        .stSuccess,
        .stWarning,
        .stInfo,
        .stError {{
            font-family: "Vazirmatn", sans-serif !important;
        }}


        /* -------------------- Keep English / Numbers Stable -------------------- */

        code,
        pre {{
            direction: ltr;
            text-align: left;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )