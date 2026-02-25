from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from rag.chain import answer_question

app = FastAPI(title="AapdaAssist AI")

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "web" / "templates"
STATIC_DIR = BASE_DIR / "web" / "static"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", response_class=HTMLResponse)
def home():
    html_path = TEMPLATES_DIR / "index.html"
    return html_path.read_text(encoding="utf-8")


@app.get("/ask")
def ask(q: str):
    res = answer_question(q)

    # ✅ Case 1: tuple/list returned
    if isinstance(res, (tuple, list)):
        answer = res[0] if len(res) > 0 else ""
        sources = res[1] if len(res) > 1 else []
    # ✅ Case 2: dict returned
    elif isinstance(res, dict):
        answer = res.get("answer", "")
        sources = res.get("sources", [])
    # ✅ Case 3: string returned
    else:
        answer = str(res)
        sources = []

    return {"question": q, "answer": answer, "sources": sources}

