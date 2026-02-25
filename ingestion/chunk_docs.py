from langchain_text_splitters import RecursiveCharacterTextSplitter
from ingestion.clean_text import clean_text
from config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_documents(docs):
    """
    Production-optimized chunking for structured documents like:
    - Disaster SOPs
    - Government guidelines
    - FAQs
    - Bullet lists
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n## ",     # Major headings
            "\n### ",    # Sub-headings
            "\n\n",      # Paragraph breaks
            "\n- ",      # Bullet points
            "\n",        # Line breaks
            ". ",        # Sentence boundary
            " "          # Word boundary fallback
        ]
    )

    # ✅ Clean documents before splitting
    for d in docs:
        d.page_content = clean_text(d.page_content)

    # ✅ Perform splitting
    chunks = splitter.split_documents(docs)

    # ✅ Add metadata for traceability
    for i, chunk in enumerate(chunks):
        source = chunk.metadata.get("source", "unknown")
        chunk.metadata["chunk_id"] = f"{source}_{i}"
        chunk.metadata["chunk_size"] = len(chunk.page_content)

    return chunks