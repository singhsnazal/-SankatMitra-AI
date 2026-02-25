from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from config import CHROMA_PATH, TOP_K

# ✅ Load embedding model ONCE at server startup
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# ✅ Load Chroma DB ONCE
db = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embeddings
)

# ✅ Create retriever ONCE
retriever = db.as_retriever(
    search_kwargs={"k": TOP_K}
)

def get_retriever():
    """
    Returns preloaded retriever.
    No heavy initialization per request.
    """
    return retriever