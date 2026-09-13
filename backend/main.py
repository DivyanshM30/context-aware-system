import os
import uuid

from fastapi import FastAPI, UploadFile, File, HTTPException

from models.schemas import OCRResponse, ContextRequest, ContextResponse
from services.ocr_service import OCRService
from services.context import find_context

app = FastAPI(
    title="Tap2Explain Backend",
    description="Backend for tap-guided contextual educational understanding.",
    version="0.1.0",
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Load OCR once when the server starts.
ocr_service = OCRService()


@app.get("/")
def root():
    return {"message": "Tap2Explain backend is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/image", response_model=OCRResponse)
async def upload_image(file: UploadFile = File(...)):
    allowed_types = {"image/jpeg", "image/png", "image/jpg"}

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only JPG and PNG images are supported.",
        )

    image_id = str(uuid.uuid4())
    extension = ".png" if file.content_type == "image/png" else ".jpg"
    image_path = os.path.join(UPLOAD_DIR, image_id + extension)

    contents = await file.read()
    with open(image_path, "wb") as f:
        f.write(contents)

    results = ocr_service.extract_text(image_path)

    return {"image_id": image_id, "results": results}


@app.post("/api/context", response_model=ContextResponse)
def get_context(request: ContextRequest):
    possible_files = [
        os.path.join(UPLOAD_DIR, request.image_id + ".jpg"),
        os.path.join(UPLOAD_DIR, request.image_id + ".png"),
    ]

    image_path = next(
        (path for path in possible_files if os.path.exists(path)),
        None,
    )

    if image_path is None:
        raise HTTPException(status_code=404, detail="Image not found.")

    # Temporary implementation: OCR is repeated.
    # We will cache OCR results in the next iteration.
    ocr_results = ocr_service.extract_text(image_path)

    selected, context = find_context(
        ocr_results,
        request.x,
        request.y,
    )

    if selected is None:
        return {
            "selected_text": None,
            "bbox": None,
            "context": [],
        }

    return {
        "selected_text": selected["text"],
        "bbox": selected["bbox"],
        "context": context,
    }
