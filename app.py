from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from rag.chain import answer_question

from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import shutil
import os

# ===============================
# Initialize FastAPI
# ===============================
app = FastAPI(title="SankatMitra AI")

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "web" / "templates"
STATIC_DIR = BASE_DIR / "web" / "static"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ===============================
# Load Image Caption Model (CPU Safe)
# ===============================
device = "cpu"

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
).to(device)

model.eval()


# ===============================
# Convert Image → Caption
# ===============================
def image_to_text(image_path: str) -> str:
    try:
        image = Image.open(image_path).convert("RGB")
        inputs = processor(image, return_tensors="pt").to(device)

        with torch.no_grad():
            output = model.generate(**inputs, max_new_tokens=25)

        caption = processor.decode(output[0], skip_special_tokens=True)
        return caption

    except Exception as e:
        print("Image processing error:", e)
        return "Unable to understand the image."


# ===============================
# Home Page
# ===============================
@app.get("/", response_class=HTMLResponse)
def home():
    html_path = TEMPLATES_DIR / "index.html"
    return html_path.read_text(encoding="utf-8")


# ===============================
# Text-only endpoint
# ===============================
@app.get("/ask")
def ask(q: str):
    return format_response(answer_question(q))


# ===============================
# Unified Image + Text endpoint
# ===============================
@app.post("/query")
async def query(
    question: str = Form(None),
    image: UploadFile = File(None)
):

    # -------- IMAGE FLOW --------
    if image is not None:

        # Basic file validation
        if not image.content_type.startswith("image/"):
            return {"error": "Uploaded file is not an image."}

        temp_path = f"temp_{image.filename}"

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        try:
            caption = image_to_text(temp_path)

            # Optional disaster hint extraction
            disaster_hint = detect_disaster_type(caption)

            structured_query = f"""
Emergency situation detected from image.

Image description:
{caption}

Disaster hint: {disaster_hint}

Provide response strictly according to official disaster management norms.
"""

            result = answer_question(structured_query)

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

        return format_response(result)

    # -------- TEXT FLOW --------
    elif question is not None:
        result = answer_question(question)
        return format_response(result)

    else:
        return {"error": "No input provided"}


# ===============================
# Simple Disaster Keyword Detector
# ===============================
def detect_disaster_type(text: str) -> str:
    text = text.lower()

    if "flood" in text or "water" in text:
        return "Flood"
    elif "fire" in text or "smoke" in text:
        return "Fire"
    elif "crack" in text or "collapse" in text:
        return "Earthquake / Structural Damage"
    elif "landslide" in text:
        return "Landslide"
    else:
        return "Unknown"


# ===============================
# Normalize RAG Response
# ===============================
def format_response(res):
    if isinstance(res, (tuple, list)):
        answer = res[0] if len(res) > 0 else ""
        sources = res[1] if len(res) > 1 else []
    elif isinstance(res, dict):
        answer = res.get("answer", "")
        sources = res.get("sources", [])
    else:
        answer = str(res)
        sources = []

    return {
        "answer": answer,
        "sources": sources
    }


# ===============================
# Health Check
# ===============================
@app.get("/health")
def health():
    return {"status": "ok"}