import cv2
import numpy as np
from PIL import Image, ImageOps
from controlnet_aux import HEDdetector, LineartDetector, PidiNetDetector

_models = {}
_CLASSES = {
    "hed": HEDdetector,
    "lineart": LineartDetector,
    "pidinet": PidiNetDetector,
}


def _load(mode: str):
    if mode not in _models:
        _models[mode] = _CLASSES[mode].from_pretrained("lllyasviel/Annotators")
    return _models[mode]


def classic_sketch(img: Image.Image) -> Image.Image:
    """Baseline (no deep learning): pencil sketch with OpenCV."""
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    inverted = 255 - gray
    blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
    sketch = cv2.divide(gray, 255 - blurred, scale=256)
    return Image.fromarray(sketch)


def dl_sketch(img: Image.Image, mode: str) -> Image.Image:
    """Deep learning sketch: pretrained edge/line network."""
    model = _load(mode)
    out = model(img).convert("L")
    # these models output white lines on black; flip to dark lines on white paper
    if np.array(out).mean() < 127:
        out = ImageOps.invert(out)
    return out