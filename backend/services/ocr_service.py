import easyocr
import numpy as np
from PIL import Image


class OCRService:
    def __init__(self):
        print("Loading OCR model...")

        self.reader = easyocr.Reader(
            ["en"],
            gpu=False,
        )

        print("OCR model loaded.")

    def extract_text(self, image_path: str):
        image = np.array(
            Image.open(image_path).convert("RGB")
        )

        results = self.reader.readtext(image)
        output = []

        for bbox, text, confidence in results:
            bbox = [
                [int(point[0]), int(point[1])]
                for point in bbox
            ]

            output.append({
                "text": text,
                "bbox": bbox,
                "confidence": float(confidence),
            })

        return output
