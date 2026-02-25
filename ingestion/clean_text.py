import re

def clean_text(text: str) -> str:
    """
    Cleans PDF extracted text to improve chunking + embeddings quality.
    """
    text = text.replace("\x00", "")        # remove null chars
    text = re.sub(r"\s+", " ", text)       # collapse multiple spaces/newlines
    return text.strip()
