import streamlit as st


def show_structured_resume(structured_data):

    if not structured_data:
        return

    st.subheader("📋 Structured Resume Data")

    st.success(
        "Structured resume data is available."
    )

    with st.expander(
        "Show extracted JSON",
        expanded=False
    ):
        st.json(
            structured_data
        )