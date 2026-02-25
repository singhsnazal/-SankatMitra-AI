import re

def clean_text(text: str) -> str:
    """
    Advanced cleaning for better RAG performance.
    """

    # Remove null characters
    text = text.replace("\x00", "")

    # Remove weird unicode artifacts
    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    # Fix broken hyphenated words
    text = re.sub(r"-\s+", "", text)

    # Collapse multiple spaces/newlines
    text = re.sub(r"\s+", " ", text)

    return text.strip()