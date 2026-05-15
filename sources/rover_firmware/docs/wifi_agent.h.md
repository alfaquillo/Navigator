
# wifi_agent.h

## Propósito
Archivo de configuración e interfaz del agente WiFi del rover.

Este módulo define:

- parámetros de conexión WiFi
- modos de operación remota
- estructuras de comunicación
- variables globales compartidas
- declaración del agente WiFi basado en RTOS

Permite integrar el rover con la cámara ESP32 y el sistema de control remoto.

## Dependencias
- `Arduino.h`
- `Arduino_FreeRTOS.h`
- `task.h`
- `queue.h`
- `supporting_functions.h`
- `maes-rtos.h`
- `SoftPWM.h`
- `SunFounder_AI_Camera.h`

## Configuración WiFi

### Configuración activa (STA)
```cpp
#define WIFI_MODE WIFI_MODE_STA
#define SSID      "Moon_rpi_AP"
#define PASSWORD  "seteclab2026"
#define NAME      "GalaxyRVR"
#define TYPE      "GalaxyRVR"
#define PORT      "8765"
#define WS_HEADER "WS+"
```

Modo actual:
- **Station mode (STA)**

El rover se conecta a una red WiFi existente creada por la Raspberry Pi.

Parámetros:
- SSID: `Moon_rpi_AP`
- puerto WebSocket: `8765`

---

### Configuración alternativa (AP)
Se conserva configuración original comentada:

```cpp
//#define WIFI_MODE WIFI_MODE_AP
```

Modo original:
- Access Point

En este modo el rover crea su propia red WiFi.

Actualmente deshabilitado.

## Modos de operación

### Enumeración `WiFiInstructions`
```cpp
typedef enum WiFiInstructions : uint8_t
```

Estados soportados:

| Estado | Descripción |
|---|---|
| `MODE_NONE` | Sin acción |
| `MODE_OBSTACLE_FOLLOWING` | Seguimiento de obstáculos |
| `MODE_OBSTACLE_AVOIDANCE` | Evasión de obstáculos |
| `MODE_APP_CONTROL` | Control remoto |
| `MODE_VOICE_CONTROL` | Control por voz |
| `MODE_DISCONNECT` | Desconexión |

## Estructuras

### `WiFiPackage`
```cpp
typedef struct {
    WiFiInstructions instruction;
} WiFiPackage;
```

Empaqueta instrucciones WiFi para colas y tareas.

## Variables globales

| Variable | Tipo | Descripción |
|---|---|---|
| `currentMode` | WiFiInstructions | Modo actual |
| `leftMotorPower` | int8_t | Potencia motor izquierdo |
| `rightMotorPower` | int8_t | Potencia motor derecho |
| `servoAngle` | uint8_t | Ángulo servo |
| `cam_lamp_status` | bool | Estado lámpara cámara |
| `ir_result` | byte | Lectura IR |
| `us_distance` | float | Distancia ultrasónica |

## Objetos externos

### Cámara
```cpp
extern AiCamera aiCam;
```

Interfaz de cámara AI.

---

### Agente WiFi
```cpp
extern Agent WiFi_Agent;
```

Agente principal RTOS para comunicaciones WiFi.

## Funciones

### `wifi(void* pvParameters)`
Task principal del sistema WiFi.

Responsabilidades:
- conexión de red
- recepción de comandos
- actualización de estado

Ejecutado como tarea FreeRTOS.

## Flujo interno

1. Inicialización del agente WiFi.
2. Conexión STA a Raspberry Pi.
3. Apertura de comunicación WebSocket.
4. Recepción de comandos remotos.
5. Control del rover.

## Modificaciones respecto al original

### Cambio de AP a STA
Configuración original:

```cpp
#define WIFI_MODE WIFI_MODE_AP
```

Nueva configuración:

```cpp
#define WIFI_MODE WIFI_MODE_STA
```

Motivación:
- la Raspberry Pi actúa como nodo central de red
- el rover pasa a ser cliente WiFi

Esto centraliza comunicaciones en la RPi.

---

### Comentado de configuración AP
Se preservó configuración original como referencia:

```cpp
//#define WIFI_MODE WIFI_MODE_AP
```

Permite rollback rápido para debugging.

---

### Integración con arquitectura de red distribuida
Nueva topología:

```text
Raspberry Pi (AP/router)
├── ESP32-CAM
├── Rover
└── Laptop/control station
```

Beneficios:
- red única
- menor complejidad operativa
- mejor interoperabilidad entre nodos

## Notas
- Este archivo contiene credenciales WiFi embebidas.
- La Raspberry Pi es el centro de comando de red.
- El protocolo WebSocket usa prefijo `WS+`.
