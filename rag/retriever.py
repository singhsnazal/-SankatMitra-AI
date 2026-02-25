from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from config import CHROMA_PATH, EMBEDDING_MODEL, TOP_K

def get_retriever():
    """
    Loads persistent Chroma DB and returns retriever.
    """
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)

    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )

    retriever = db.as_retriever(search_kwargs={"k": TOP_K})
    return retriever
