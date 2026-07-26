import fitz  # PyMuPDF


def extract_text(uploaded_file) -> str:
    """
    Extract text from a PDF using PyMuPDF.
    """

    text = ""

    pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    for page in pdf:

        page_text = page.get_text()

        if page_text:
            text += page_text + "\n"

    pdf.close()

    return text