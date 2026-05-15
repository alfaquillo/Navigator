
# Rover Firmware

## Descripción general
Este directorio contiene el firmware principal del rover, basado en una arquitectura multitarea usando FreeRTOS y el framework de agentes MAES.

El firmware controla:

- locomoción del rover
- sensores
- periféricos
- integración con cámara AI
- comunicaciones WiFi y WebSocket

La arquitectura busca desacoplar funcionalidades mediante agentes independientes ejecutados sobre RTOS.

## Proyecto base / referencias

Proyecto original utilizado como base:

- https://github.com/Oscar-FZ/FreeMAES-for-ATmega-Devices

El objetivo fue mantener íntegra la arquitectura original del framework y modificar únicamente los componentes necesarios para integración con la red del sistema rover-cámara-Raspberry Pi.

## Estructura del directorio

```text
rover_firmware/
├── docs
│   └── wifi_agent.h.md
├── FreeMAESvsFreeRTOS
│   ├── rock_paper_scissors_agents.ino
│   ├── rock_paper_scissors_tasks.ino
│   ├── sender_receiver_agents.ino
│   ├── sender_receiver_tasks.ino
│   ├── telemetry_agents.ino
│   └── telemetry_tasks.ino
├── FreeRTOSConfig.h
├── maes-rtos
│   ├── Agent.cpp
│   ├── Agent_Msg.cpp
│   ├── Agent_Organization.cpp
│   ├── Agent_Platform.cpp
│   ├── Behaviour.cpp
│   ├── examples
│   │   ├── rock_paper_scissors.cpp
│   │   ├── sender_receiver.cpp
│   │   └── telemetry.cpp
│   ├── maes-rtos.h
│   ├── sysVars.cpp
│   └── User_Cond.cpp
├── README.md
├── sketch_sep24a
│   ├── mode_handler_agent.cpp
│   ├── mode_handler_agent.h
│   ├── peripherals_control_agent.cpp
│   ├── peripherals_control_agent.h
│   ├── sensor_control_agent.cpp
│   ├── sensor_control_agent.h
│   ├── sketch_sep24a.ino
│   ├── wifi_agent.cpp
│   └── wifi_agent.h
└── Supporting_Functions
    ├── supporting_functions.cpp
    └── supporting_functions.h
```

## Documentación técnica

La documentación de modificaciones realizadas se encuentra en:

- [wifi_agent.h](docs/wifi_agent.h.md)

## Funcionalidades principales

### Arquitectura por agentes
El sistema utiliza agentes concurrentes para:

- manejo de sensores
- control de motores
- control de periféricos
- comunicaciones WiFi

### Control multitarea
Basado en:

- FreeRTOS
- framework MAES

Permite ejecución concurrente y desacoplada.

### Integración con cámara AI
Se integra con:

- SunFounder AI Camera
- comunicación WebSocket

### Control remoto
Permite recepción de comandos remotos para:

- dirección
- velocidad
- servo
- iluminación

## Requisitos

### Hardware
- Rover SunFounder / compatible
- microcontrolador Arduino/ATmega
- módulo WiFi/cámara AI

### Software
- Arduino IDE
- FreeRTOS
- librerías MAES

## Instalación

### 1. Clonar repositorio
```bash
git clone https://github.com/alfaquillo/TFG_Quillo_CEA_ITCR.git
```

### 2. Abrir proyecto principal en sources/rover_firmware
Abrir:

```text
sketch_sep24a/sketch_sep24a.ino
```

### 3. Instalar dependencias
Instalar librerías requeridas:
- FreeRTOS
- SoftPWM
- SunFounder AI Camera

### 4. Compilar y cargar
Seleccionar placa correspondiente y cargar firmware.

## Flujo de operación

1. Inicialización del sistema RTOS.
2. Creación de agentes.
3. Inicialización WiFi.
4. Conexión al sistema de red.
5. Recepción de comandos remotos.
6. Control del rover.

## Modificaciones realizadas sobre proyecto original

Se realizaron modificaciones mínimas para preservar la arquitectura original.

Archivo modificado:

- `sketch_sep24a/wifi_agent.h`

Cambio principal:

- incorporación de modo WiFi STA

Esto permite que el rover se conecte a una red centralizada creada por Raspberry Pi.

Configuración anterior:
- rover como Access Point

Configuración actual:
- Raspberry Pi como Access Point/router
- rover como cliente WiFi

No se modificó lógica interna de agentes, scheduler ni framework MAES.

## Dependencias
- Arduino_FreeRTOS
- MAES RTOS
- SoftPWM
- SunFounder_AI_Camera

## Notas
- Se buscó mantener intacto el trabajo original del proyecto base.
- Las modificaciones realizadas son exclusivamente de integración de red.
- El rover forma parte de una arquitectura distribuida junto con Raspberry Pi y ESP32-CAM.

## Referencias
- https://github.com/Oscar-FZ/FreeMAES-for-ATmega-Devices
