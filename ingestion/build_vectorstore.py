from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import CHROMA_PATH

def build_vectorstore(chunks):
    """
    Stores embeddings in Chroma DB using HuggingFace embeddings.
    Automatically persists to disk (Chroma 0.4+ handles persistence).
    """

    # ✅ Use HuggingFace embedding model (Render-safe)
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )

    # ❌ No need for vectordb.persist() anymore (deprecated)
    return vectordb