# rover_ws.py

## Propósito
Gestiona la comunicación bidireccional entre la Raspberry Pi y el rover mediante WebSocket.

Este módulo:
- establece conexión con el rover,
- recibe datos de sensores desde el ESP32,
- fusiona decisiones de navegación visual y evasión reactiva,
- convierte decisiones en comandos motores,
- transmite continuamente comandos de movimiento.

## Dependencias
- `asyncio`: ejecución asíncrona y manejo de tareas concurrentes.
- `websockets`: cliente WebSocket.
- `json`: serialización/deserialización de mensajes.
- `time`: temporización y watchdog de conexión.
- `re`: utilidades de procesamiento de strings.
- `config`: configuración global (`WS_URI`).
- `sensors`: procesamiento reactivo de sensores.
- `navigation`: lógica de navegación visual.

## Variables globales
| Variable | Tipo | Descripción |
|----------|------|-------------|
| `VEL_MAX` | int | velocidad base máxima |
| `CMD_TIME` | int | duración del comando enviado (ms) |
| `bias_d` | float | compensación motor derecho |
| `bias_i` | float | compensación motor izquierdo |
| `OVERRIDE_CYCLES` | int | ciclos de prioridad para evasión |

## Entradas y salidas

### Entradas
- datos WebSocket del rover
- máscaras de navegación visual
- ROI procesada

### Salidas
- comandos motores serializados en JSON
- respuestas PONG
- estado interno de sensores

## Funciones

### `decision_to_motors(decision)`
Convierte decisión de alto nivel en escalas de velocidad diferencial.

Mapeos:
- `ADELANTE` → avance recto
- `IZQUIERDA` → giro izquierdo
- `DERECHA` → giro derecho
- `RETROCEDER` → reversa

**Parámetros:**
- `decision`: string de decisión

**Retorna:**
- tupla `(motor_izq, motor_der)`

## Clases

### `RoverClient`
Cliente WebSocket principal del sistema.

Responsable de:
- conexión
- recepción
- decisión
- envío de comandos

#### Atributos
| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `uri` | str | endpoint WebSocket |
| `ws` | websocket | conexión activa |
| `sensors` | Sensors | instancia de sensores |
| `last_override` | str | última acción reactiva |
| `override_timer` | int | duración de prioridad reactiva |
| `current_command` | str | comando actual |
| `send_interval` | float | periodo de envío |
| `connected` | bool | estado de conexión |
| `reconnecting` | bool | bandera de reconexión |
| `last_rx_time` | float | último paquete recibido |

## Métodos

### `connect()`
Establece conexión inicial con rover y lanza tareas asíncronas.

Inicia:
- recepción (`receiver_loop`)
- transmisión (`command_stream`)

---

### `reconnect()`
Realiza reconexión automática tras pérdida de enlace.

Incluye:
- cierre seguro
- reintentos periódicos

---

### `receiver_loop()`
Loop asíncrono de recepción.

Procesa:
- mensajes WebSocket
- limpieza de payloads
- parsing JSON
- ping/pong
- actualización de sensores

---

### `compute_decision(nav_mask, roi_mask)`
Fusiona decisiones de:
- sensores reactivos
- navegación visual

Prioridad:
1. evasión sensores
2. navegación visual

Usa temporizador de override para mantener maniobras críticas.

**Parámetros:**
- `nav_mask`
- `roi_mask`

**Retorna:**
- decisión final prefijada:
  - `sens_*`
  - `nav_*`

---

### `send_command(decision)`
Convierte decisión en velocidades de motores y envía comando JSON.

Incluye:
- compensación de bias motores
- limitación de velocidad máxima
- serialización

Formato enviado:
- `K`: motor izquierdo
- `Q`: motor derecho
- `D`: dirección servo
- `M`: modo
- `duracion_ms`

---

### `command_stream()`
Loop continuo de transmisión de comandos.

Funciones:
- watchdog RX
- envío periódico de comandos
- reconexión automática

---

### `close()`
Cierra conexión WebSocket y detiene cliente.

## Flujo interno
1. Conectar al rover vía WebSocket.
2. Lanzar loops RX y TX.
3. Recibir datos de sensores.
4. Actualizar módulo `Sensors`.
5. Fusionar navegación + evasión.
6. Convertir decisión a velocidades.
7. Enviar comando JSON.
8. Monitorear timeout y reconectar si falla.

## Modificaciones respecto al original
- Se agregó arquitectura asíncrona completa.
- Se implementó reconexión automática robusta.
- Se añadió watchdog por timeout RX.
- Se incorporó prioridad de evasión reactiva.
- Se implementó conversión de decisiones a control diferencial.
- Se añadieron factores de calibración por motor.

## Consideraciones de rendimiento
- Arquitectura no bloqueante mediante `asyncio`.
- Envío periódico configurable (`send_interval`).
- Watchdog de 5 s para robustez de conexión.
- Baja latencia para control continuo.

## Notas
- Este módulo actúa como puente principal entre navegación y rover físico.
- La evasión por sensores tiene prioridad temporal sobre navegación visual.
- Requiere servidor WebSocket activo en el rover.
- Constituye uno de los módulos centrales del sistema.