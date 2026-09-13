from typing import List
from pydantic import BaseModel


class OCRItem(BaseModel):
    text: str
    bbox: List[List[int]]
    confidence: float


class OCRResponse(BaseModel):
    image_id: str
    results: List[OCRItem]


class ContextRequest(BaseModel):
    image_id: str
    x: int
    y: int


class ContextResponse(BaseModel):
    selected_text: str | None
    bbox: List[List[int]] | None
    context: List[OCRItem]
