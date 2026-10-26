import cv2
import numpy as np
from PIL import Image, ImageOps

_models = {}


def _load(mode: str):
    if mode not in _models:
        from controlnet_aux import HEDdetector, LineartDetector, PidiNetDetector
        classes = {
            "hed": HEDdetector,
            "lineart": LineartDetector,
            "pidinet": PidiNetDetector,
        }
        _models[mode] = classes[mode].from_pretrained("lllyasviel/Annotators")
    return _models[mode]


def classic_sketch(img: Image.Image) -> Image.Image:
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    inverted = 255 - gray
    blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
    sketch = cv2.divide(gray, 255 - blurred, scale=256)
    return Image.fromarray(sketch)


def dl_sketch(img: Image.Image, mode: str) -> Image.Image:
    model = _load(mode)
    out = model(img).convert("L")
    if np.array(out).mean() < 127:
        out = ImageOps.invert(out)
    return out