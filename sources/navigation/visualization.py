import cv2
import numpy as np
import math
from config import *
import slam 


# ==============================
# SEGMENTACIÓN 
# ==============================
def colorize_mask(mask):
    colors = np.array([
        [60, 60, 60], #grey unknown         
        [0, 255, 255], #yellow craters
        [0, 0, 255],   #red rocks
        [255, 200, 0], #blue mountains
        [0, 255, 0]    #green sky
    ], dtype=np.uint8)

    return colors[mask]


# ==============================
# SLAM VIEW
# ==============================
def draw_slam():

    grid = slam.grid
    rx, ry = slam.meters_to_cell()
    theta = slam.theta

    # BGR (OpenCV)
    colors = np.array([
        [60, 60, 60],      # 0 background model 
        [0, 255, 255],     # 1 crater   -> yellow
        [0, 0, 255],       # 2 rock     -> red
        [255, 200, 0],     # 3 mountain -> cyan
        [0, 255, 0],       # 4 sky      -> green 
    ], dtype=np.uint8)

    h, w = grid.shape
    vis = np.zeros((h, w, 3), dtype=np.uint8)

    # -----------------------------------
    # fondo mapa no observado
    # -----------------------------------
    vis[:] = (40, 40, 40)

    # -----------------------------------
    # pintar clases semánticas
    # -----------------------------------
    observed = grid != UNKNOWN

    valid_classes = observed & (grid <= 4)
    vis[valid_classes] = colors[grid[valid_classes]]

    # -----------------------------------
    # trayectoria histórica
    # -----------------------------------
    for tx, ty, _ in slam.trajectory:

        gx = int(slam.origin_x + tx / slam.CELL_M)
        gy = int(slam.origin_y - ty / slam.CELL_M)

        if 0 <= gx < w and 0 <= gy < h:
            vis[gy, gx] = (255, 0, 255)   # magenta

    # -----------------------------------
    # ventana centrada en rover
    # -----------------------------------
    VIEW = 120
    half = VIEW // 2

    canvas = np.zeros((VIEW, VIEW, 3), dtype=np.uint8)

    for dy in range(-half, half):
        for dx in range(-half, half):

            gx = rx + dx
            gy = ry + dy

            cx = dx + half
            cy = dy + half

            if 0 <= gx < w and 0 <= gy < h:
                canvas[cy, cx] = vis[gy, gx]
            else:
                canvas[cy, cx] = (0, 0, 0)

    # -----------------------------------
    # rover actual
    # -----------------------------------
    canvas[half, half] = (0, 255, 0)

    # -----------------------------------
    # heading
    # -----------------------------------
    hx = int(half + 8 * np.cos(theta))
    hy = int(half - 8 * np.sin(theta))

    if 0 <= hx < VIEW and 0 <= hy < VIEW:
        canvas[hy, hx] = (255, 255, 255)

    # -----------------------------------
    # escalar visualización
    # -----------------------------------
    return cv2.resize(
        canvas,
        None,
        fx=5,
        fy=5,
        interpolation=cv2.INTER_NEAREST
    )