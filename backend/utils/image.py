from PIL import Image


def get_image_size(image_path: str):
    image = Image.open(image_path)
    return image.size


def crop_image(
    image_path: str,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    padding: int = 50,
):
    image = Image.open(image_path)
    width, height = image.size

    x1 = max(0, x1 - padding)
    y1 = max(0, y1 - padding)
    x2 = min(width, x2 + padding)
    y2 = min(height, y2 + padding)

    return image.crop((x1, y1, x2, y2))
