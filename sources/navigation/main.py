import os
import cv2
import time
import asyncio
import numpy as np
import socket

from slam import grid
from config import *
from model import load_model, infer
from perception import preprocess, create_navigation_mask, trapezoid_roi
from navigation import decide_direction
from slam import integrate_observation, move_rover
from visualization import colorize_mask, draw_slam
from rover_ws import RoverClient
from frame_source import FrameSource


async def main():

    model_info = load_model(MODEL_PATH)

    source = FrameSource()
    rover = RoverClient()
    await rover.connect()

    decision_buffer = []
    last_command = "nav_ADELANTE"

    input_details = model_info["input_details"] 

    # inicializar frame para ROI
    ret, img, _ = source.read()
    if not ret:
        return

    h, w = img.shape[:2]
    roi_mask, roi_pts = trapezoid_roi((h, w))

    if TCP_STREAM:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', 8080))
        sock.listen(1)
        print("Esperando conexión del cliente...")
        conn, addr = sock.accept()
        print(f"Conectado a {addr}")

    start = time.time()
    frame_count = 0

    while True:
        loop_start = time.time()

        ret, img, idx = source.read()
        if not ret:
            break

        model_img = preprocess(img, input_details)

        mask = infer(
            model_info,
            model_img,
            (w, h)
        )

        nav_mask = create_navigation_mask(mask)

        # --------------------------
        # DECISIÓN
        # --------------------------
        final_step_decision = rover.compute_decision(nav_mask, roi_mask)

        # --------------------------
        # SLAM
        # --------------------------
        integrate_observation(mask)

        # --------------------------
        # CONTROL
        # --------------------------
        if final_step_decision.startswith("sens_"):

            command = final_step_decision
            decision_buffer = []

            print(f"Frame {idx} | EVASION | DECISION={command}")

        else:

            decision_buffer.append(final_step_decision)

            if len(decision_buffer) == FRAMES_PER_DECISION:

                # filtro simple anti-oscilación
                if decision_buffer.count(decision_buffer[-1]) > len(decision_buffer)//2:
                    command = decision_buffer[-1]
                else:
                    command = last_command

                decision_buffer = []

                print(f"Frame {idx} | DECISION={command}")

            else:
                command = last_command

        # --------------------------
        # SLAM MOVIMIENTO
        # --------------------------
        slam_decision = command.replace("sens_", "").replace("nav_", "")
        move_rover(slam_decision)

        # --------------------------
        # ACTUALIZAR COMANDO 
        # --------------------------
        rover.current_command = command
        last_command = command

        # --------------------------
        # DEBUG VIEWS
        # ==================================================

        inference_view = None
        slam_view = None
        stream_frame = None

        if DEBUG:

            # --------------------------------------------------
            # INFERENCE VIEW
            # --------------------------------------------------

            color_mask = colorize_mask(mask)

            overlay = cv2.addWeighted(
                img,
                0.6,
                color_mask,
                0.4,
                0
            )

            if roi_pts is not None:

                cv2.polylines(
                    overlay,
                    [roi_pts],
                    True,
                    (255, 0, 255),
                    2
                )

            # [img | mask | overlay]
            inference_view = np.hstack([
                img,
                color_mask,
                overlay
            ])


            # --------------------------------------------------
            # SLAM VIEW
            # --------------------------------------------------

            slam_view = draw_slam()


        # ==================================================
        # TCP STREAM VIEW SELECTION
        # ==================================================

        if TCP_STREAM:

            if SHOW_INFERENCE:

                stream_frame = inference_view

            elif SHOW_SLAM:

                stream_frame = slam_view

            else:

                print(
                    "TCP_STREAM activo pero "
                    "no hay vista seleccionada"
                )


        # ==================================================
        # TCP STREAM
        # ==================================================

        if TCP_STREAM and stream_frame is not None:

            try:

                _, jpeg = cv2.imencode(
                    '.jpg',
                    stream_frame,
                    [cv2.IMWRITE_JPEG_QUALITY, 85]
                )

                data = jpeg.tobytes()

                # Enviar tamaño
                conn.sendall(
                    len(data).to_bytes(4, 'big')
                )

                # Enviar frame
                conn.sendall(data)

                print(
                    f"Frame {idx} enviado, "
                    f"tamaño: {len(data)} bytes"
                )

            except (
                BrokenPipeError,
                ConnectionResetError
            ) as e:

                print(
                    f"Cliente desconectado "
                    f"(frame {idx}): {e}"
                )

                try:

                    conn.close()

                    print(
                        "Esperando nueva conexión..."
                    )

                    conn, addr = sock.accept()

                    print(
                        f"Reconectado a {addr}"
                    )

                    # Reintentar envío
                    _, jpeg = cv2.imencode(
                        '.jpg',
                        stream_frame,
                        [cv2.IMWRITE_JPEG_QUALITY, 85]
                    )

                    data = jpeg.tobytes()

                    conn.sendall(
                        len(data).to_bytes(4, 'big')
                    )

                    conn.sendall(data)

                    print(
                        f"Frame {idx} re-enviado"
                    )

                except Exception as recon_error:

                    print(
                        f"Error reconectando: "
                        f"{recon_error}"
                    )

            except Exception as e:

                print(
                    f"Error enviando frame "
                    f"{idx}: {e}"
                )


        # ==================================================
        # SAVE DEBUG IMAGES
        # ==================================================

        if SAVE_IMAGES:

            # --------------------------------------------------
            # SAVE INFERENCE FRAMES
            # --------------------------------------------------

            if SHOW_INFERENCE and inference_view is not None:

                inference_dir = os.path.join(
                    SAVE_DIR,
                    "inference"
                )

                os.makedirs(
                    inference_dir,
                    exist_ok=True
                )

                out_path = os.path.join(
                    inference_dir,
                    f"inference_{idx:04d}.png"
                )

                cv2.imwrite(
                    out_path,
                    inference_view
                )

        await asyncio.sleep(0.3)

        frame_count += 1
        loop_time = time.time() - loop_start
        instant_fps = 1 / loop_time if loop_time > 0 else 0 

    # ==================================================
    # GUARDAR RESULTADOS FINALES SLAM
    # ==================================================

    if SAVE_IMAGES and SHOW_SLAM:

        slam_dir = os.path.join(
            SAVE_DIR,
            "slam"
        )

        os.makedirs(
            slam_dir,
            exist_ok=True
        )

        final_map = draw_slam()

        cv2.imwrite(
            os.path.join(
                slam_dir,
                "slam_final.png"
            ),
            final_map
        )

        np.savetxt(
            os.path.join(
                slam_dir,
                "full_map_classes.csv"
            ),
            grid,
            fmt="%d",
            delimiter=","
        )

        print("Mapa SLAM final guardado")    

    # ==================================================
    # RESULTADOS
    # ==================================================
             
    total_time = time.time() - start
    avg_fps = frame_count / total_time if total_time > 0 else 0

    print("\n==== RESULTADOS ====")
    print(f"Frames procesados: {frame_count}")
    print(f"Tiempo total: {total_time:.2f}s")
    print(f"FPS promedio: {avg_fps:.2f}")

    await rover.close()
    if TCP_STREAM:
        conn.close()
        sock.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    asyncio.run(main())