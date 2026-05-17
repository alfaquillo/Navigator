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
│   └── final_document
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
| `documentation/final_document/` | informe final en LaTeX |
| `images/` | imágenes utilizadas en documentación |
| `sources/development/` | pruebas y scripts de desarrollo |
| `sources/esp32/` | firmware del ESP32 |
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
### Conexión a red local del sistema

La Raspberry Pi 5 funciona como punto de acceso Wi-Fi principal del sistema.

Topología de red:

```text
Laptop / cliente ---> Raspberry Pi 5 (AP) ---> Rover / ESP32
```

Configuración:

- La Raspberry Pi genera la red local utilizada por el sistema.
- El rover (ESP32) se conecta automáticamente a esta red al iniciar.
- Los clientes externos (por ejemplo laptop para monitoreo) deben conectarse manualmente a la misma red Wi-Fi.
Todos los dispositivos deben conectarse a esta red local:

```text
SSID: Moon_rpi_AP
Password: seteclab2026
```

### Pasos de conexión

1. Encender Raspberry Pi 5 y rover.
2. Esperar a que la red Wi-Fi del sistema esté disponible.
3. Conectar la laptop a la red generada por Raspberry Pi.
4. Ejecutar visualización remota:


Una vez conectado, el cliente recibirá el stream TCP generado por el sistema de navegación.

### Direcciones utilizadas

- Raspberry Pi:
```text
192.168.3.1
```

- Rover / ESP32:
```text
192.168.3.2
```

- Puerto streaming TCP:
```text
8080
```

- WebSocket rover:
```text
ws://192.168.3.2:8765
```

## Acceso remoto por SSH

La Raspberry Pi 5 opera en modo headless, por lo que la administración y ejecución del sistema se realiza remotamente mediante SSH.

Establecer conexión SSH:

```bash
ssh root@192.168.3.1
```

> La imagen Yocto utilizada habilita acceso SSH para administración remota.

## Ejecución

El sistema principal se instala mediante Yocto como una aplicación integrada dentro de la imagen final de Raspberry Pi 5.

Durante el proceso de build:

- se instala un launcher ejecutable en:

```text
/usr/bin/navigation
```

- los archivos del sistema se copian en:

```text
/usr/share/navigation
```

### Método recomendado

El sistema puede ejecutarse directamente mediante:

```bash
navigation
```

Este comando inicia automáticamente el sistema principal de navegación autónoma.

### Ejecución manual

También es posible ejecutar manualmente desde el directorio de instalación:

```bash
cd /usr/share/navigation
python3 main.py
```

Esta modalidad es útil para debugging, pruebas o modificaciones rápidas.

### Visualización remota de transmisión

Si se encuentra habilitado `TCP_STREAM = True` en `config.py`, el sistema transmite frames procesados vía TCP.

Para visualizar la transmisión desde una laptop u otro equipo cliente, ejecutar este archivo de python desde el equipo cliente:

```bash
python3 socket_rpi.py
```

Este script permite:

- visualizar segmentación en tiempo real
- observar overlays y debugging visual
- monitorear salida remota sin interfaz local en Raspberry Pi

## Archivos instalados

El directorio principal contiene:

- modelo TensorFlow Lite
- scripts Python
- configuración global
- datasets auxiliares
- utilidades de visualización

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