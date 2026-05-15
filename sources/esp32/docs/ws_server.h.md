
# ws_server.h

## Propósito
Archivo de cabecera para el servidor WebSocket del firmware ESP32-CAM.

Define:

- interfaz pública de la clase `WS_Server`
- constantes de configuración
- estados de conexión
- parámetros del protocolo WebSocket

Este archivo expone la API necesaria para inicializar, operar y monitorear el servidor WebSocket.

## Dependencias
- `WebSocketsServer.h`

## Constantes

### Regiones de datos
```cpp
#define REGIONS (char[26]){'A','B','C',...,'Z'}
#define REGIONS_LENGTH 26
```

Define 26 regiones o canales identificados por letras.

Uso:
- mapeo de campos JSON recibidos
- construcción de protocolo serial `WS+`

---

### Tamaño de buffer
```cpp
#define WS_BUFFER_SIZE 1024
```

Tamaño máximo permitido para JSON recibido.

---

### Timeouts

#### Timeout heartbeat
```cpp
#define TIMEOUT 3000
```

Tiempo máximo sin recibir pong.

Unidad:
- milisegundos.

---

#### Timeout comandos
```cpp
#define CMD_TIMEOUT 300
```

Tiempo máximo sin recibir comandos válidos antes de marcar stream como obsoleto.

---

#### Anti-flood
```cpp
#define MIN_PROCESS_INTERVAL 30
```

Tiempo mínimo entre procesamiento de paquetes.

Evita saturación del microcontrolador.

---

#### Intervalo de transmisión
```cpp
#define SEND_INTERVAL 50
```

Tiempo mínimo entre comandos enviados al rover.

## Enumeraciones

### `WS_STATE`
Estados operativos del WebSocket.

```cpp
enum WS_STATE {
  DISCONNECTED,
  STALE,
  VALID_STREAM
};
```

#### Estados

- `DISCONNECTED`
  - sin cliente conectado.

- `STALE`
  - conexión presente pero stream inválido o expirado.

- `VALID_STREAM`
  - flujo de comandos válido y activo.

## Clase `WS_Server`

### Constructor
```cpp
WS_Server();
```

Inicializa objeto servidor.

---

### `begin(int port)`
Inicializa servidor usando puerto indicado.

**Parámetros:**
- `port`: puerto WebSocket.

---

### `begin(int port, String name, String type, String check)`
Inicializa servidor con metadata adicional.

**Parámetros:**
- `port`: puerto
- `name`: nombre dispositivo
- `type`: tipo dispositivo
- `check`: identificador de validación

Se usa para handshake inicial con cliente.

---

### `close()`
Cierra servidor y limpia estado interno.

---

### `loop()`
Mantiene procesamiento de eventos WebSocket.

Debe ejecutarse continuamente.

---

### `send(String data)`
Envía texto al cliente conectado.

**Parámetros:**
- `data`: mensaje texto.

---

### `sendBIN(uint8_t* payload, size_t length)`
Envía datos binarios.

**Parámetros:**
- `payload`: buffer
- `length`: longitud

---

### `is_connected()`
Consulta estado de conexión.

**Retorna:**
- `true`: cliente conectado.
- `false`: sin cliente.

## Variables privadas

### `port`
```cpp
int port;
```

Puerto configurado para servidor WebSocket.

## Modificaciones respecto al original

Este archivo fue añadido/modificado para soportar comunicación WebSocket personalizada.

Cambios principales:

- definición de protocolo basado en regiones A-Z
- timeouts de seguridad
- control de frecuencia de procesamiento
- estados explícitos de stream

Estas configuraciones soportan la integración del rover con cliente remoto y mecanismos fail-safe.

## Notas
- Los parámetros de timeout están ajustados para operación en tiempo real.
- El protocolo depende de mensajes JSON estructurados.
