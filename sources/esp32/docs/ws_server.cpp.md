
# ws_server.cpp

## Propósito
Este archivo implementa el servidor WebSocket principal utilizado para la comunicación en tiempo real entre la ESP32-CAM y el centro de control del rover.

Sus funciones principales incluyen:

- establecimiento de conexión WebSocket
- intercambio de mensajes JSON
- heartbeat (ping/pong)
- supervisión de timeout
- validación de comandos
- transmisión segura de comandos seriales hacia el rover

## Dependencias
- `ws_server.h`
- `ArduinoJson.h`
- `led_status.hpp`
- `Ticker.h`

## Variables globales

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `ws` | WebSocketsServer | Servidor WebSocket en puerto 8765 |
| `client_num` | uint8_t | Cliente conectado actual |
| `ws_connected` | bool | Estado de conexión |
| `ws_state` | WS_STATE | Estado lógico del stream |
| `ws_name` | String | Nombre del dispositivo |
| `ws_type` | String | Tipo de dispositivo |
| `videoUrl` | String | URL de streaming |
| `timer` | Ticker | Temporizador de supervisión |
| `lastPingSent` | uint32_t | Último ping enviado |
| `lastPongReceived` | uint32_t | Último pong recibido |
| `last_valid_cmd_time` | uint32_t | Último comando válido |
| `last_seq` | uint32_t | Última secuencia aceptada |

## Funciones

### `intToString(uint8_t* value, size_t length)`
Convierte payload binario recibido a `String`.

**Retorna:**
- String convertido.

---

### `sendSTOP()`
Envía comando serial de parada segura al rover.

```text
WS+0;0;0;90;0;0;...
```

Se usa como mecanismo fail-safe ante:
- desconexión
- timeout
- stream inválido

---

### `supervisionTask()`
Rutina periódica ejecutada cada 100 ms.

Funciones:

#### Heartbeat
- envía ping periódico
- verifica recepción de pong

Si excede timeout:

- desconecta cliente
- reinicia estado
- ejecuta STOP seguro

#### Timeout de comandos
Si no se reciben comandos válidos:

- cambia estado a `STALE`
- ejecuta STOP

---

### `begin(int port, String _name, String _type, String _check)`
Inicializa servidor WebSocket.

**Proceso:**
1. inicia servidor
2. registra callback de eventos
3. configura temporizador de supervisión

Eventos manejados:

#### `WStype_CONNECTED`
- registra cliente
- obtiene IP remota
- envía información de identificación JSON

Ejemplo:

```json
{
  "Name": "...",
  "Type": "...",
  "Check": "...",
  "video": "..."
}
```

- inicializa heartbeat

---

#### `WStype_DISCONNECTED`
Acciones:
- actualiza LED
- limpia cliente
- cambia estado
- ejecuta STOP

---

#### `WStype_TEXT`
Procesa mensajes JSON.

Flujo:

1. parse JSON
2. valida integridad
3. procesa ping/pong
4. valida secuencia
5. aplica anti-flood
6. construye comando serial

Ejemplo salida:

```text
WS+1;0;0;90;...
```

Solo transmite si:
- datos válidos
- stream activo
- respeta intervalo mínimo

---

#### `WStype_BIN`
Actualiza heartbeat para paquetes binarios.

---

#### `WStype_ERROR`
Indica error mediante LED.

---

### `loop()`
Mantiene servidor WebSocket activo.

Debe llamarse continuamente desde loop principal.

---

### `send(String data)`
Envía texto al cliente.

Validaciones:
- conexión activa
- cliente válido
- caracteres ASCII seguros

---

### `sendBIN(uint8_t* payload, size_t length)`
Envía payload binario.

---

### `is_connected()`
Consulta estado de conexión.

**Retorna:**
- `true` si cliente conectado.

## Flujo interno

1. Cliente se conecta.
2. Servidor envía handshake JSON.
3. Se inicia heartbeat.
4. Cliente envía comandos JSON.
5. Se validan secuencias y tiempos.
6. Se genera comando serial.
7. Rover ejecuta acciones.
8. Ante fallo → STOP seguro.

## Modificaciones respecto al original

Este archivo constituye una modificación mayor respecto al firmware original.

### Integración WebSocket
Se añadió servidor:

```cpp
WebSocketsServer ws(8765);
```

para comunicación bidireccional en tiempo real.

---

### Heartbeat robusto
Implementado mecanismo ping/pong:

- detección de clientes muertos
- desconexión automática
- limpieza de estado

Variables:
- `lastPingSent`
- `lastPongReceived`

---

### Timeout de comandos
Se añadió supervisión de comandos válidos:

```cpp
last_valid_cmd_time
```

Si no llegan comandos:
- stream pasa a `STALE`
- rover se detiene

---

### Sistema fail-safe
Implementación de:

```cpp
sendSTOP();
```

Protección ante:
- timeout
- desconexión
- datos inválidos

Evita movimiento no controlado.

---

### Anti-flood
Se limita frecuencia de procesamiento:

```cpp
MIN_PROCESS_INTERVAL
```

Previene saturación del microcontrolador.

---

### Control de secuencia
Validación de paquetes mediante:

```cpp
seq
```

Descarta paquetes:
- duplicados
- fuera de orden

---

### Sanitización de datos
Validaciones:
- JSON corrupto
- caracteres inválidos
- datos vacíos

Mejora robustez frente a entradas erróneas.

## Notas
- Este módulo es crítico para seguridad operacional del rover.
- Cualquier pérdida de comunicación genera parada automática.
- El protocolo serial generado usa prefijo `WS+`.
