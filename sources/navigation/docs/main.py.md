# main.py

## Propósito
Archivo principal del sistema de navegación autónoma ejecutado en la Raspberry Pi 5.

Este módulo integra todos los componentes del sistema:
- adquisición de imágenes,
- inferencia de segmentación semántica,
- navegación visual,
- evasión reactiva,
- actualización de mapa SLAM,
- comunicación con rover,
- visualización y streaming.

Constituye el punto de entrada principal del software.

## Dependencias
- `os`: manejo de rutas y guardado de archivos.
- `cv2`: visualización y codificación de imágenes.
- `time`: medición temporal y FPS.
- `asyncio`: ejecución asíncrona.
- `numpy`: composición visual.
- `socket`: streaming TCP de frames.

### Módulos internos
- `slam`
- `config`
- `model`
- `perception`
- `navigation`
- `visualization`
- `rover_ws`
- `frame_source`

## Variables globales
Las configuraciones se importan desde `config.py`.

Variables relevantes:
| Variable | Tipo | Descripción |
|----------|------|-------------|
| `MODEL_PATH` | str | ruta al modelo TFLite |
| `TCP_STREAM` | bool | habilita streaming TCP |
| `DEBUG` | bool | habilita overlays visuales |
| `SLAM_SHOW` | bool | muestra visualización SLAM |
| `SAVE_IMAGES` | bool | guarda resultados |
| `FRAMES_PER_DECISION` | int | frames para filtro temporal |

## Entradas y salidas

### Entradas
- frames desde cámara o fuente configurada
- datos sensores vía WebSocket

### Salidas
- comandos de movimiento al rover
- visualización local
- streaming TCP
- archivos debug opcionales

## Funciones

### `main()`
Loop principal del sistema.

Responsabilidades:
- cargar modelo
- inicializar fuente de frames
- conectar rover
- inicializar ROI
- procesar frames continuamente

Pipeline principal:
1. captura frame
2. preprocesamiento
3. inferencia TFLite
4. creación máscara navegable
5. decisión navegación/evasión
6. actualización SLAM
7. actualización comando rover
8. visualización/debug
9. streaming TCP opcional

**Parámetros:**
- ninguno

**Retorna:**
- no retorna valor

## Flujo interno

### Inicialización
1. Cargar modelo TFLite.
2. Inicializar `FrameSource`.
3. Inicializar `RoverClient`.
4. Conectar WebSocket.
5. Crear ROI trapezoidal.
6. Abrir socket TCP opcional.

### Loop por frame
1. Leer frame.
2. Ejecutar preprocesamiento.
3. Ejecutar inferencia.
4. Crear máscara navegable.
5. Obtener decisión final desde rover:
   - navegación visual
   - evasión reactiva
6. Integrar observación en SLAM.
7. Actualizar movimiento estimado.
8. Actualizar comando actual.
9. Construir overlays debug.
10. Mostrar ventanas opcionales.
11. Enviar streaming TCP opcional.
12. Guardar resultados opcionales.

### Finalización
1. Calcular FPS promedio.
2. Cerrar conexión rover.
3. Cerrar sockets.
4. Destruir ventanas OpenCV.

## Lógica de decisión
La selección de movimiento sigue arquitectura híbrida:

1. **Prioridad reactiva**
   - sensores IR/LIDAR

2. **Prioridad deliberativa**
   - navegación visual por segmentación

3. **Filtro temporal**
   - buffer de decisiones
   - anti-oscilación

## Streaming TCP
Si `TCP_STREAM=True`:
- abre servidor TCP puerto `8080`
- transmite frames JPEG
- permite cliente remoto para monitoreo

Características:
- tamaño enviado como 4 bytes
- JPEG calidad 100
- reconexión automática cliente

## Debug y visualización
Modos opcionales:
- máscara colorizada
- overlay segmentación
- visualización SLAM
- guardado de mapas

Archivos generables:
- `frame_XXXX.png`
- `slam_final.png`
- `full_map_classes.csv`

## Modificaciones respecto al original
- Se integró pipeline completo de navegación.
- Se añadió soporte TFLite INT8.
- Se incorporó arquitectura híbrida navegación + evasión.
- Se agregó SLAM semántico.
- Se implementó streaming TCP remoto.
- Se añadió guardado de mapas y frames.
- Se incorporó medición de FPS.

## Consideraciones de rendimiento
- Pipeline optimizado para ejecución edge en Raspberry Pi 5.
- Inferencia multihilo mediante TFLite.
- Streaming opcional para no penalizar rendimiento local.
- Uso de `asyncio` para comunicación no bloqueante.

## Notas
- Este archivo constituye el punto de entrada principal del sistema.
- Diseñado para ejecución headless o con visualización local.
- Integra percepción, navegación, control y monitoreo.
- Requiere modelo TFLite, conexión rover y fuente de video válidas.