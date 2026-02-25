from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

def load_documents(folder_path: str):
    """
    Loads all PDFs from the raw_docs folder and returns LangChain Documents.
    Adds metadata (source filename).
    """
    docs = []
    for pdf_path in Path(folder_path).glob("*.pdf"):
        loader = PyPDFLoader(str(pdf_path))
        loaded = loader.load()

        for d in loaded:
            d.metadata["source"] = pdf_path.name  # store filename

        docs.extend(loaded)

    return docs
