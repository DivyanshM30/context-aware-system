import math


def center_of_bbox(bbox):
    x = [point[0] for point in bbox]
    y = [point[1] for point in bbox]

    return (
        sum(x) / len(x),
        sum(y) / len(y),
    )


def distance(point1, point2):
    return math.sqrt(
        (point1[0] - point2[0]) ** 2
        + (point1[1] - point2[1]) ** 2
    )


def point_inside_bbox(x, y, bbox):
    xs = [point[0] for point in bbox]
    ys = [point[1] for point in bbox]

    return (
        min(xs) <= x <= max(xs)
        and min(ys) <= y <= max(ys)
    )


def find_context(ocr_results, tap_x, tap_y, max_context=6):
    tapped_item = None

    # First, find the OCR box directly under the tap.
    for item in ocr_results:
        if point_inside_bbox(
            tap_x,
            tap_y,
            item["bbox"],
        ):
            tapped_item = item
            break

    # If the tap is not on text, use the closest OCR item.
    if tapped_item is None and ocr_results:
        tap_point = (tap_x, tap_y)
        closest = None
        closest_distance = float("inf")

        for item in ocr_results:
            center = center_of_bbox(item["bbox"])
            d = distance(tap_point, center)

            if d < closest_distance:
                closest_distance = d
                closest = item

        tapped_item = closest

    if tapped_item is None:
        return None, []

    selected_center = center_of_bbox(tapped_item["bbox"])
    scored_items = []

    for item in ocr_results:
        center = center_of_bbox(item["bbox"])
        d = distance(selected_center, center)
        scored_items.append((d, item))

    scored_items.sort(key=lambda x: x[0])

    context = [
        item for _, item in scored_items[:max_context]
    ]

    return tapped_item, context
