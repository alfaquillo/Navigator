# Navigation Module

## Descripción general
Módulo principal de navegación autónoma ejecutado en Raspberry Pi 5.

Este sistema integra percepción visual basada en segmentación semántica, navegación reactiva y deliberativa, mapeo SLAM semántico y comunicación en tiempo real con el rover mediante WebSocket.

Su objetivo es procesar imágenes provenientes de cámara o dataset, inferir terreno navegable, tomar decisiones de movimiento y transmitir comandos al rover de manera autónoma.

## Proyecto base / referencias
- Proyecto original: implementación propia del sistema de navegación autónoma.
- Framework de inferencia: TensorFlow Lite Runtime.
- Comunicación rover: WebSocket sobre red local WiFi.
- Visualización remota: streaming TCP MJPEG-like.

## Estructura del directorio

```text
navigation/
├── config.py
├── frame_source.py
├── main.py
├── model.py
├── navigation.py
├── perception.py
├── rover_ws.py
├── sensors.py
├── slam.py
├── socket_rpi.py
├── visualization.py
├── model_int8.tflite
├── model_fp16.tflite
├── dataset_test_384/
├── results/
└── docs/
    ├── config.py.md
    ├── frame_source.py.md
    ├── main.py.md
    ├── model.py.md
    ├── navigation.py.md
    ├── perception.py.md
    ├── rover_ws.py.md
    ├── sensors.py.md
    ├── slam.py.md
    ├── socket_rpi.py.md
    └── visualization.py.md
```

## Funcionalidades principales

### Percepción visual
Realiza inferencia de segmentación semántica usando modelos TensorFlow Lite.

Componentes:
- carga de modelo
- preprocesamiento
- inferencia
- generación de máscaras navegables

Archivos:
- `model.py`
- `perception.py`

Documentación:
- [model.py.md](docs/model.py.md)
- [perception.py.md](docs/perception.py.md)

### Navegación visual
Analiza regiones navegables y decide movimiento visual.

Acciones:
- avanzar
- girar izquierda
- girar derecha

Archivo:
- `navigation.py`

Documentación:
- [navigation.py.md](docs/navigation.py.md)

### Evasión reactiva
Procesa sensores IR y LIDAR para evitar colisiones.

Prioridad sobre navegación visual.

Archivo:
- `sensors.py`

Documentación:
- [sensors.py.md](docs/sensors.py.md)

### Comunicación rover
Gestiona conexión WebSocket con ESP32/rover y envío continuo de comandos.

Funciones:
- conexión
- reconexión
- parsing JSON
- streaming de comandos

Archivo:
- `rover_ws.py`

Documentación:
- [rover_ws.py.md](docs/rover_ws.py.md)

### SLAM semántico
Construye mapa semántico local basado en observaciones visuales.

Funciones:
- integración de observaciones
- expansión dinámica
- actualización pose estimada

Archivo:
- `slam.py`

Documentación:
- [slam.py.md](docs/slam.py.md)

### Visualización y debugging
Genera overlays visuales y visualización local del mapa.

Funciones:
- máscara colorizada
- overlay segmentación
- render mapa SLAM

Archivo:
- `visualization.py`

Documentación:
- [visualization.py.md](docs/visualization.py.md)

### Fuente de imágenes
Abstrae adquisición de frames desde:
- dataset
- cámara MJPEG

Archivo:
- `frame_source.py`

Documentación:
- [frame_source.py.md](docs/frame_source.py.md)

### Streaming remoto
Cliente TCP para visualización remota de frames procesados.

Archivo:
- `socket_rpi.py`

Documentación:
- [socket_rpi.py.md](docs/socket_rpi.py.md)

### Configuración global
Centraliza parámetros del sistema.

Archivo:
- `config.py`

Documentación:
- [config.py.md](docs/config.py.md)

## Requisitos

### Hardware
- Raspberry Pi 5
- cámara IP / MJPEG
- rover con ESP32
- sensores IR
- sensor LIDAR

### Software
- Python 3
- OpenCV
- NumPy
- TensorFlow Lite Runtime
- websockets

## Despliegue y ejecución

Este módulo forma parte de la imagen embebida generada mediante Yocto para Raspberry Pi 5.

Las dependencias Python, modelo TensorFlow Lite y archivos de configuración son incluidos durante el proceso de build de la imagen.

### Ejecución
Una vez iniciado el sistema:

```bash
navigation
```


### Configuración previa
Antes de generar la imagen se recomienda validar en `config.py`:

- ruta del modelo
- modo de entrada (`camera` o `dataset`)
- dirección IP del rover
- parámetros de debug
- streaming TCP

## Flujo de operación

1. Cargar configuración.
2. Inicializar modelo TFLite.
3. Inicializar fuente de frames.
4. Conectar rover vía WebSocket.
5. Capturar frame.
6. Ejecutar segmentación.
7. Calcular máscara navegable.
8. Evaluar evasión por sensores.
9. Tomar decisión final.
10. Actualizar SLAM.
11. Enviar comando al rover.
12. Visualizar/guardar resultados.

## Modificaciones realizadas sobre proyecto original
- integración de navegación híbrida visual + sensores
- soporte TensorFlow Lite INT8
- SLAM semántico
- streaming TCP remoto
- soporte dataset/cámara
- overlays debug
- arquitectura modular documentada

## Dependencias
- opencv-python
- numpy
- tflite-runtime
- websockets

## Notas
- `main.py` es el punto de entrada principal.
- Compatible con ejecución headless.
- Diseñado para pruebas offline y operación en tiempo real.
- Optimizado para Raspberry Pi 5.

## Referencias
- TensorFlow Lite
- OpenCV
- WebSockets Python