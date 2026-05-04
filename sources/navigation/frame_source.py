import os
import cv2
from config import INPUT_MODE, IMAGE_DIR, CAMERA_URL, MODEL_W, MODEL_H


class FrameSource:
    def __init__(self):
        self.mode = INPUT_MODE
        self.cap = None
        self.image_paths = []
        self.idx = 0

        if self.mode == "dataset":
            self.image_paths = sorted([
                os.path.join(IMAGE_DIR, x)
                for x in os.listdir(IMAGE_DIR)
                if x.lower().endswith((".jpg", ".png"))
            ])

            print("Imágenes encontradas:", len(self.image_paths))

        elif self.mode == "camera":
            self.cap = cv2.VideoCapture(CAMERA_URL)

            if not self.cap.isOpened():
                raise RuntimeError(
                    f"No se pudo abrir cámara: {CAMERA_URL}"
                )

            print("Cámara conectada")

        else:
            raise ValueError(f"INPUT_MODE inválido: {self.mode}")

    def _prepare_camera_frame(self, frame):
        h, w = frame.shape[:2]

        # 640x480 -> crop central 480x480
        side = min(h, w)

        x0 = (w - side) // 2
        y0 = (h - side) // 2

        cropped = frame[y0:y0 + side, x0:x0 + side]

        resized = cv2.resize(
            cropped,
            (MODEL_W, MODEL_H)
        )

        return resized

    def read(self):
        if self.mode == "dataset":
            if self.idx >= len(self.image_paths):
                return False, None, self.idx

            path = self.image_paths[self.idx]
            frame = cv2.imread(path)

            idx = self.idx
            self.idx += 1

            return True, frame, idx

        elif self.mode == "camera":
            ret, frame = self.cap.read()

            if not ret:
                return False, None, self.idx

            frame = self._prepare_camera_frame(frame)

            self.idx += 1
            return True, frame, self.idx

    def release(self):
        if self.cap is not None:
            self.cap.release()