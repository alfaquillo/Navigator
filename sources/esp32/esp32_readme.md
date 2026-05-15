
# AI Camera Firmware (ESP32-CAM)

## Descripción general
Este directorio contiene el firmware utilizado para la cámara ESP32-CAM del rover, encargado de:

- Captura y transmisión de video.
- Configuración de parámetros de cámara.
- Gestión de conectividad WiFi.
- Comunicación por WebSocket con el sistema de control.

Este proyecto está basado en el firmware original de SunFounder:

- Proyecto original: https://github.com/sunfounder/ai-camera-firmware

## Estructura del directorio

```text
esp32/
├── ai-camera-firmware/
│   ├── ai-camera-firmware.ino
│   ├── camera_server.cpp
│   ├── camera_server.hpp
│   ├── led_status.cpp
│   ├── led_status.hpp
│   ├── pins.h
│   ├── Readme.md
│   ├── setting_server_index.html
│   ├── settings_server.cpp
│   ├── settings_server.hpp
│   ├── settings_server_index_html.hpp
│   ├── who_camera.c
│   ├── who_camera.h
│   ├── wifi_helper.cpp
│   ├── wifi_helper.h
│   ├── ws_server.cpp
│   └── ws_server.h
├── docs/
│   ├── wifi_helper.cpp.md
│   ├── ws_server.cpp.md
│   └── ws_server.h.md
└── esp32_readme.md
```

## Documentación técnica

La documentación detallada de los archivos modificados se encuentra en:

- [wifi_helper.cpp](docs/wifi_helper.cpp.md)
- [ws_server.cpp](docs/ws_server.cpp.md)
- [ws_server.h](docs/ws_server.h.md)

Estas modificaciones corresponden a extensiones realizadas sobre el firmware original para soportar:

- modo WiFi STA con IP estática
- control explícito de canal y ancho de banda WiFi
- comunicación WebSocket en tiempo real
- mecanismos de heartbeat y fail-safe

## Funcionalidades principales

### Streaming de cámara
Permite transmisión MJPEG desde la ESP32-CAM mediante servidor HTTP integrado.

### Configuración web
Incluye interfaz web para modificar parámetros como:

- resolución
- brillo
- contraste
- calidad JPEG
- mirror / flip

### Comunicación WebSocket
Se añadió soporte WebSocket para intercambio de datos en tiempo real con el centro de control.

### Conectividad WiFi
Soporta:

- Access Point (AP)
- Station mode (STA)

## Requisitos

### Hardware
- ESP32-CAM (AI Thinker)
- Programador USB-TTL

### Software
#### Entorno de desarrollo:
    - Arduino IDE 2.0.3
#### Herramientas:
    - Arduino AVR Boards 2.0.3
    - esp32 (Espressif Systems) 2.0.7
#### Librerias:
    - ArduinoJson (Benoit Blanchon)
    - WebSockets (Markus Sattler) (Links2004)

## Instalación

### 1. Instalar soporte ESP32
Seguir guía visual:

https://lastminuteengineers.com/getting-started-with-esp32-cam/

### 2. Descargar el repositorio 

```bash
git clone https://github.com/alfaquillo/TFG_Quillo_CEA_ITCR.git
```

### 3. Abrir firmware de la carpeta sources/esp32

Abrir:

```text
ai-camera-firmware.in
```

en Arduino IDE.

### 4. Seleccionar placa

```text
AI Thinker ESP32-CAM
```

### 5. Configurar puerto
Seleccionar puerto serial correspondiente.

### 6. Cargar firmware
Compilar y subir.

## Flujo de operación

1. Inicialización de hardware.
2. Configuración WiFi.
3. Inicio servidor HTTP.
4. Inicio servidor WebSocket.
5. Captura y transmisión.

## Modificaciones realizadas sobre proyecto original

Las modificaciones específicas se documentan a nivel de archivo e incluyen:

- soporte WebSocket
- modo STA
- configuración de IP/red
- ajustes de integración con rover

## Referencias

- https://github.com/sunfounder/ai-camera-firmware
- https://lastminuteengineers.com/getting-started-with-esp32-cam/

