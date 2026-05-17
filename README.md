# Sistema de navegación autónoma para rover de exploración lunar

Implementación de un sistema de navegación autónoma para rover terrestre inspirado en escenarios de exploración lunar, desarrollado como Trabajo Final de Graduación del Instituto Tecnológico de Costa Rica.

El sistema integra percepción visual mediante segmentación semántica, navegación híbrida reactiva/deliberativa, comunicación distribuida y despliegue embebido sobre Raspberry Pi 5 utilizando Yocto.

---

## Descripción general

Este repositorio contiene el desarrollo completo del sistema de navegación autónoma utilizado en el rover experimental del proyecto.

La arquitectura general integra:

- percepción visual basada en redes neuronales TensorFlow Lite
- navegación reactiva mediante sensores IR y LIDAR
- control de rover mediante ESP32
- generación de imagen embebida con Yocto
- visualización remota y debugging

El objetivo es permitir navegación autónoma en terrenos no estructurados similares a superficies lunares.

---

## Estructura del proyecto

```text
.
├── documentation
│   └── project_proposal
├── images
│   ├── LogoTec.png
│   └── Rasp.png
├── LICENSE
├── README.md
├── requirements.txt
└── sources
    ├── development
    ├── esp32
    ├── navigation
    ├── rover_firmware
    └── yocto-project
```

### Descripción de carpetas

| Carpeta | Descripción |
|---------|-------------|
| `documentation/` | documentación académica del proyecto |
| `documentation/project_proposal/` | anteproyecto en LaTeX |
| `images/` | imágenes utilizadas en documentación |
| `sources/development/` | pruebas y scripts de desarrollo |
| `sources/esp32/` | código asociado al ESP32 |
| `sources/navigation/` | sistema principal de navegación ejecutado en Raspberry Pi 5 |
| `sources/rover_firmware/` | firmware del rover |
| `sources/yocto-project/` | configuración y capas para generación de imagen Yocto |

---

## Arquitectura del sistema

El sistema está compuesto por múltiples subsistemas:

### 1. Percepción visual
Implementa segmentación semántica mediante TensorFlow Lite.

Funciones:
- preprocesamiento de imágenes
- inferencia
- generación de máscaras navegables

Ubicación:
```text
sources/navigation/
```

---

### 2. Navegación autónoma
Combina:

- navegación visual deliberativa
- evasión reactiva por sensores
- lógica híbrida de control

Módulos principales:
- `main.py`
- `navigation.py`
- `sensors.py`
- `rover_ws.py`

---

### 3. SLAM semántico
Construcción incremental de mapa semántico local.

Características:
- grid occupancy semántico
- trayectoria estimada
- expansión dinámica del mapa

Módulo:
- `slam.py`

---

### 4. Comunicación rover
Comunicación distribuida mediante:

- WebSocket Raspberry Pi ↔ ESP32
- streaming TCP para visualización remota

---

### 5. Sistema embebido
Despliegue sobre:

- Raspberry Pi 5
- imagen Linux generada con Yocto

Incluye:
- dependencias Python
- modelo TFLite
- configuración de ejecución

---

## Requisitos

## Hardware
- Raspberry Pi 5
- Rover móvil Sunfounder GalaxyRVR

## Software
- Python 3.10
- OpenCV
- NumPy
- TensorFlow Lite Runtime
- websockets

Dependencias Python:

```bash
pip install -r requirements.txt
```

> `requirements.txt` se utiliza principalmente para ejecución externa o herramientas de visualización como `socket_rpi.py`.  
> El sistema embebido principal utiliza dependencias integradas en la imagen Yocto.

---

## Ejecución

El sistema principal se instala mediante Yocto como una aplicación integrada dentro de la imagen final de Raspberry Pi 5.

Durante el proceso de build:

- el launcher principal se instala en:

```text
/usr/bin/navigation
```

- los archivos del sistema se copian en:

```text
/usr/share/navigation
```

### Ejecución del sistema

Una vez iniciada la Raspberry Pi, el sistema puede ejecutarse mediante:

```bash
navigation
```

Este comando:

1. muestra banner de inicio
2. cambia automáticamente al directorio:

```text
/usr/share/navigation
```

3. ejecuta:

```bash
python3 main.py
```

sin requerir navegación manual entre directorios.

### Archivos instalados
El directorio de ejecución contiene:

- modelo TensorFlow Lite
- configuración global
- scripts Python del sistema
- datasets y utilidades auxiliares

Ruta:

```text
/usr/share/navigation
```

## Documentación interna

Cada módulo principal contiene documentación individual en formato Markdown.

Ejemplo:

```text
sources/navigation/docs/
```

Archivos documentados:
- config.py
- frame_source.py
- main.py
- model.py
- navigation.py
- perception.py
- rover_ws.py
- sensors.py
- slam.py
- socket_rpi.py
- visualization.py

---

## Modelos incluidos

El proyecto incluye modelos TensorFlow Lite optimizados:

- `model_int8.tflite`
- `model_fp16.tflite`

Actualmente el sistema utiliza:

```text
model_int8.tflite
```

por compatibilidad y estabilidad en Raspberry Pi 5.

---

## Trabajo académico

Proyecto desarrollado como Trabajo Final de Graduación para optar por el grado de:

**Licenciatura en Ingeniería en Electrónica**


**Instituto Tecnológico de Costa Rica**

**Escuela de Ingeniería Electrónica**

---

## Autor

**Carlos Enrique Elizondo Alfaro**  


---

## Licencia

Este proyecto se distribuye bajo la licencia incluida en:

[LICENSE](LICENSE)

**SETEC Lab – Laboratorio de Sistemas Espaciales**