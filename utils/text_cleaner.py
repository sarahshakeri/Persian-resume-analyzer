from hazm import Normalizer
import re

normalizer = Normalizer()


def normalize_persian(text: str) -> str:
    """
    Normalize Persian text using Hazm.
    """
    return normalizer.normalize(text)


def remove_extra_spaces(text: str) -> str:
    """
    Remove repeated spaces.
    """
    return re.sub(r"[ ]+", " ", text)


def remove_empty_lines(text: str) -> str:
    """
    Remove empty lines.
    """
    lines = text.split("\n")

    lines = [line.strip() for line in lines if line.strip()]

    return "\n".join(lines)


def clean_text(text: str) -> str:
    """
    Main cleaning pipeline.
    """

    text = normalize_persian(text)

    text = remove_extra_spaces(text)

    text = remove_empty_lines(text)

    return text