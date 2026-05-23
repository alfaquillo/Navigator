import os



# ==================================================
# MODELO E INFERENCIA
# ==================================================
MODEL_PATH = "model_int8.tflite"

MODEL_H = 384
MODEL_W = 384

IMG_DATASET_H = 384
IMG_DATASET_W = 384


# ==================================================
# OUTPUT / DEBUG
# ==================================================
SAVE_DIR = "results"

DEBUG = True
SHOW_INFERENCE = True
SAVE_IMAGES = True
SHOW_SLAM = False
TCP_STREAM = True

os.makedirs(SAVE_DIR, exist_ok=True)


# ==================================================
# NAVEGACIÓN VISUAL
# ==================================================
NAV_CLASSES = [0]

FRAMES_PER_DECISION = 1
USE_TRAPEZOID = True

MIN_FORWARD = 0.18
DELTA_SIDE = 0.05
DELTA_CENTER = 0.06


# ==================================================
# SLAM / MAPEO
# ==================================================
CELL_M = 0.5

MAP_W_M = 40
MAP_H_M = 40

MAP_W = int(MAP_W_M / CELL_M)
MAP_H = int(MAP_H_M / CELL_M)

UNKNOWN_CLASS = 0
CRATER = 1
ROCK = 2
MOUNTAIN = 3
SKY = 4
UNKNOWN = 255

TURN_ANGLE_DEG = 0.3
STEP_METERS = 0.1


# ==================================================
# SENSORES Y COMUNICACIÓN
# ==================================================
WS_URI = "ws://192.168.3.2:8765"

DEFAULT_IR = 0
DEFAULT_LIDAR = -1


# ==================================================
# FUENTE DE ENTRADA
# ==================================================
INPUT_MODE = "dataset"   # "camera" o "dataset"

IMAGE_DIR = "dataset_test_384"
CAMERA_URL = "http://192.168.3.2:9000/mjpg"