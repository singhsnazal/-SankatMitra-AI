from pathlib import Path
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
    UnstructuredWordDocumentLoader
)

def load_documents(folder_path: str):
    """
    Loads documents (PDF, TXT, DOCX, CSV) from a folder.
    Adds metadata including source filename and file type.
    Returns LangChain Documents.
    """

    docs = []
    folder = Path(folder_path)

    for file_path in folder.glob("*"):

        suffix = file_path.suffix.lower()

        try:
            # ------------------ PDF ------------------
            if suffix == ".pdf":
                loader = PyPDFLoader(str(file_path))
                loaded = loader.load()

            # ------------------ TXT ------------------
            elif suffix == ".txt":
                loader = TextLoader(str(file_path), encoding="utf-8")
                loaded = loader.load()

            # ------------------ DOCX ------------------
            elif suffix == ".docx":
                loader = UnstructuredWordDocumentLoader(str(file_path))
                loaded = loader.load()

            # ------------------ CSV ------------------
            elif suffix == ".csv":
                loader = CSVLoader(str(file_path))
                loaded = loader.load()

            else:
                continue  # skip unsupported files

            # Add metadata
            for d in loaded:
                d.metadata["source"] = file_path.name
                d.metadata["file_type"] = suffix

            docs.extend(loaded)

        except Exception as e:
            print(f"⚠️ Failed to load {file_path.name}: {e}")

    return docs