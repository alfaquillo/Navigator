import numpy as np
import math
from config import *

# ==============================
# ESTADO GLOBAL
# ==============================
grid = np.full((MAP_H, MAP_W), UNKNOWN, dtype=np.uint8)

x_m, y_m = 0.0, 0.0
theta = math.pi / 2 

origin_x = MAP_W // 2
origin_y = MAP_H // 2

trajectory = [(x_m, y_m, theta)]


# ==============================
# COORDENADAS
# ==============================
def meters_to_cell():
    rx = int(origin_x + x_m / CELL_M)
    ry = int(origin_y - y_m / CELL_M)
    return rx, ry


# ==============================
# EXPANSIÓN DINÁMICA
# ==============================
def expand_map_if_needed(rx, ry):
    global grid, origin_x, origin_y, MAP_W, MAP_H

    pad = 120
    MARGIN = 40
    
    expand_left   = rx < MARGIN
    expand_right  = rx > MAP_W - MARGIN - 1
    expand_top    = ry < MARGIN
    expand_bottom = ry > MAP_H - MARGIN - 1

    if not (expand_left or expand_right or expand_top or expand_bottom):
        return

    old_h, old_w = grid.shape

    new_h = old_h + pad * (expand_top + expand_bottom)
    new_w = old_w + pad * (expand_left + expand_right)

    new_grid = np.full((new_h, new_w), UNKNOWN, dtype=np.uint8)

    off_x = pad if expand_left else 0
    off_y = pad if expand_top else 0

    new_grid[
        off_y:off_y + old_h,
        off_x:off_x + old_w
    ] = grid

    grid = new_grid

    origin_x += off_x
    origin_y += off_y

    MAP_H, MAP_W = new_grid.shape


# ==============================
# MOVIMIENTO
# ==============================
def move_rover(decision):
    global x_m, y_m, theta

    if decision == "IZQUIERDA":
        theta += math.radians(TURN_ANGLE_DEG)

    elif decision == "DERECHA":
        theta -= math.radians(TURN_ANGLE_DEG)

    if decision == "RETROCEDER":
        step = -STEP_METERS
    else:
        step = STEP_METERS

    x_m += step * math.cos(theta)
    y_m += step * math.sin(theta)

    trajectory.append((x_m, y_m, theta))

    rx, ry = meters_to_cell()

    h, w = grid.shape

    if 0 <= rx < w and 0 <= ry < h:
        grid[ry, rx] = FREE


# ==============================
# INTEGRACIÓN OBSERVACIÓN
# ==============================
def integrate_observation(mask):
    global grid

    rx, ry = meters_to_cell()

    expand_map_if_needed(rx, ry)

    rx, ry = meters_to_cell()

    h, w = grid.shape

    if not (0 <= rx < w and 0 <= ry < h):
        return

    # -----------------------------------
    # recorte inferior (suelo)
    # -----------------------------------
    start_row = int(mask.shape[0] * 0.45)
    cropped = mask[start_row:, :]

    # -----------------------------------
    # downsample
    # -----------------------------------
    mini = cropped[::10, ::10]

    mh, mw = mini.shape

    DEPTH_SCALE = 0.7
    LATERAL_SCALE = 0.9

    painted = 0
    free_painted = 0

    # -----------------------------------
    # recorrer observaciones
    # -----------------------------------
    for r in range(mh):
        for c in range(mw):

            val = int(mini[r, c])

            # -----------------------------------
            # ignorar solo desconocido
            # -----------------------------------
            if val == UNKNOWN_CLASS:
                continue

            # -----------------------------------
            # determinar si es obstáculo real
            # -----------------------------------
            is_obstacle = (val != SKY)

            # -----------------------------------
            # profundidad relativa
            # -----------------------------------
            depth = (mh - r) * DEPTH_SCALE

            # -----------------------------------
            # desplazamiento lateral
            # -----------------------------------
            lateral = (mw / 2 - c) * LATERAL_SCALE

            # -----------------------------------
            # coordenadas mundo relativas
            # -----------------------------------
            wx = (
                depth * math.cos(theta)
                - lateral * math.sin(theta)
            )

            wy = (
                depth * math.sin(theta)
                + lateral * math.cos(theta)
            )

            # -----------------------------------
            # celda global objetivo
            # -----------------------------------
            gx = int(rx + wx)
            gy = int(ry - wy)

            # -----------------------------------
            # pintar espacio libre
            # -----------------------------------
            steps = max(1, int(depth))

            for s in range(steps):

                fx = int(rx + (wx * s / depth))
                fy = int(ry - (wy * s / depth))

                if 0 <= fx < w and 0 <= fy < h:

                    # -----------------------------------
                    # expandir free space localmente
                    # -----------------------------------
                    R = 2

                    for oy in range(-R, R + 1):
                        for ox in range(-R, R + 1):

                            nx = fx + ox
                            ny = fy + oy

                            if 0 <= nx < w and 0 <= ny < h:

                                # solo llenar unknown
                                if grid[ny, nx] == UNKNOWN:

                                    grid[ny, nx] = FREE
                                    free_painted += 1

            # -----------------------------------
            # pintar obstáculo si aplica
            # -----------------------------------
            if is_obstacle:

                if 0 <= gx < w and 0 <= gy < h:

                    # obstáculo sobrescribe FREE
                    grid[gy, gx] = val

                    painted += 1

    print(
        f"[SLAM] Obstacles: {painted} | "
        f"Free: {free_painted} | "
        f"Map: {grid.shape}"
    )
    