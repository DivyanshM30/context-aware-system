# Tap2Explain Backend

CPU-friendly first version of the Tap2Explain backend.

## Features

- FastAPI API
- CPU-only EasyOCR
- Image upload
- OCR text + bounding boxes
- Tap-coordinate based context selection
- Placeholder explanation service

## Setup

Create and activate a virtual environment:

### Windows

    python -m venv venv
    venv\Scripts\activate

### Linux/macOS

    python -m venv venv
    source venv/bin/activate

Install dependencies:

    pip install -r requirements.txt

Run:

    uvicorn main:app --reload

Open:

    http://127.0.0.1:8000/docs

## Current API

### GET /

Health-style root endpoint.

### GET /health

Returns:

    {"status": "ok"}

### POST /api/image

Upload a JPG or PNG image. The endpoint returns an image ID and OCR results.

### POST /api/context

Send:

    {
      "image_id": "...",
      "x": 420,
      "y": 280
    }

The endpoint identifies the tapped OCR item and returns nearby OCR context.

## Next steps

1. Cache OCR results instead of running OCR again.
2. Add image cropping around the tapped region.
3. Add the VLM/LLM explanation endpoint.
4. Connect the frontend.
