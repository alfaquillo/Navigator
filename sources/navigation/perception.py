import cv2
import numpy as np
from config import *


def preprocess(img, input_details):

    img = cv2.resize(img, (MODEL_W, MODEL_H))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    dtype = input_details[0]["dtype"]

    img = img.astype(np.float32) / 255.0

    # HWC -> CHW (CRÍTICO)
    img = np.transpose(img, (2, 0, 1))

    # batch
    img = np.expand_dims(img, 0)

    if dtype == np.int8:
        scale, zero_point = input_details[0]["quantization"]

        img = img / scale + zero_point
        img = np.round(img)
        img = np.clip(img, -128, 127).astype(np.int8)

    return img


def create_navigation_mask(mask):
    return np.isin(mask, NAV_CLASSES).astype(np.uint8)


def trapezoid_roi(shape):
    h, w = shape

    if not USE_TRAPEZOID:
        return np.ones((h, w), dtype=np.uint8), None

    mask = np.zeros((h, w), dtype=np.uint8)

    pts = np.array([
        (int(w * 0.05), int(h * 0.10)),
        (int(w * 0.95), int(h * 0.10)),
        (int(w * 0.98), int(h * 0.50)),
        (int(w * 0.02), int(h * 0.50))
    ], dtype=np.int32)

    cv2.fillPoly(
        img=mask,
        pts=[pts],
        color=(1,)
    )

    return mask, pts