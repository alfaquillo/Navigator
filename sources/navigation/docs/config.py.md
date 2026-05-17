# config.py

## Propósito
Centraliza la configuración global del sistema de navegación autónoma.

Este archivo define:
- rutas de archivos
- parámetros de inferencia
- configuración de navegación
- parámetros SLAM
- configuración de sensores
- modos de entrada
- opciones de debug y streaming

Permite modificar el comportamiento del sistema sin alterar lógica interna de módulos.

## Dependencias
- `os`: creación automática de directorios.

## Variables globales

## Modelo e inferencia
| Variable | Tipo | Descripción |
|----------|------|-------------|
| `MODEL_PATH` | str | ruta al modelo TensorFlow Lite |
| `MODEL_H` | int | alto entrada modelo |
| `MODEL_W` | int | ancho entrada modelo |
| `IMG_DATASET_H` | int | alto dataset |
| `IMG_DATASET_W` | int | ancho dataset |

## Salidas y debug
| Variable | Tipo | Descripción |
|----------|------|-------------|
| `SAVE_DIR` | str | carpeta de resultados |
| `DEBUG` | bool | habilita overlays visuales |
| `SAVE_IMAGES` | bool | guarda imágenes procesadas |
| `SLAM_SHOW` | bool | visualización mapa SLAM |
| `TCP_STREAM` | bool | habilita streaming TCP |

## Navegación
| Variable | Tipo | Descripción |
|----------|------|-------------|
| `NAV_CLASSES` | list | clases consideradas navegables |
| `FRAMES_PER_DECISION` | int | buffer temporal de decisiones |
| `USE_TRAPEZOID` | bool | ROI trapezoidal |

### Umbrales navegación
| Variable | Tipo | Descripción |
|----------|------|-------------|
| `MIN_FORWARD` | float | mínimo score para avanzar |
| `DELTA_SIDE` | float | diferencia lateral mínima |
| `DELTA_CENTER` | float | tolerancia región central |

## SLAM
| Variable | Tipo | Descripción |
|----------|------|-------------|
| `CELL_M` | float | tamaño de celda en metros |
| `MAP_W_M` | int | ancho mapa en metros |
| `MAP_H_M` | int | alto mapa en metros |
| `MAP_W` | int | ancho mapa discretizado |
| `MAP_H` | int | alto mapa discretizado |

### Clases semánticas
| Variable | Valor | Descripción |
|----------|-------|-------------|
| `UNKNOWN_CLASS` | 0 | clase desconocida modelo |
| `CRATER` | 1 | cráter |
| `ROCK` | 2 | roca |
| `MOUNTAIN` | 3 | montaña |
| `SKY` | 4 | cielo |
| `UNKNOWN` | 255 | celda no observada |

### Movimiento rover
| Variable | Tipo | Descripción |
|----------|------|-------------|
| `TURN_ANGLE_DEG` | float | ángulo giro estimado |
| `STEP_METERS` | float | avance estimado por comando |

## Sensores y comunicación
| Variable | Tipo | Descripción |
|----------|------|-------------|
| `WS_URI` | str | URI WebSocket rover |
| `DEFAULT_IR` | int | valor default sensor IR |
| `DEFAULT_LIDAR` | int | valor default LIDAR |

## Fuente de entrada
| Variable | Tipo | Descripción |
|----------|------|-------------|
| `INPUT_MODE` | str | modo (`camera` o `dataset`) |
| `IMAGE_DIR` | str | carpeta dataset |
| `CAMERA_URL` | str | URL MJPEG cámara |

## Inicialización automática
Al cargar el módulo:

### `os.makedirs(SAVE_DIR, exist_ok=True)`
Crea automáticamente carpeta de resultados si no existe.

## Flujo interno
1. Definir parámetros globales.
2. Configurar modelo y resolución.
3. Configurar navegación.
4. Configurar mapa SLAM.
5. Configurar sensores.
6. Configurar fuente de entrada.
7. Crear carpeta de salida.

## Modificaciones respecto al original
- Se centralizó toda configuración del sistema.
- Se añadieron parámetros de navegación híbrida.
- Se incorporó configuración de SLAM semántico.
- Se agregó soporte dataset/cámara.
- Se añadieron opciones debug, guardado y streaming.

## Consideraciones de rendimiento
- Permite tuning rápido sin modificar código fuente.
- Facilita pruebas comparativas variando parámetros.
- Reduce acoplamiento entre módulos.

## Notas
- Archivo fundamental para configuración experimental.
- Cambios aquí afectan comportamiento global del sistema.
- Debe mantenerse sincronizado con resolución del modelo utilizado.
- Recomendado modificar parámetros aquí antes de pruebas o despliegue.