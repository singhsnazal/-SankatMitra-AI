from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from config import CHROMA_PATH, EMBEDDING_MODEL

def build_vectorstore(chunks):
    """
    Stores embeddings in Chroma DB. Persists on disk.
    """
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )

    vectordb.persist()
    return vectordb
