
# wifi_helper.cpp

## Propósito
Este archivo implementa la lógica de conectividad WiFi para la ESP32-CAM, permitiendo operar en dos modos:

- **AP (Access Point):** la ESP32 crea su propia red WiFi.
- **STA (Station):** la ESP32 se conecta a una red WiFi existente.

Además, mantiene control básico del estado de conexión y asignación de dirección IP.

## Dependencias
- `WiFi.h`
- `wifi_helper.h`
- `esp_wifi.h`

## Variables globales
| Variable | Tipo | Descripción |
|----------|------|-------------|
| `ssid` | String | Nombre de red WiFi |
| `password` | String | Contraseña WiFi |
| `ip` | String | Dirección IP asignada |
| `apChannel` | int | Canal WiFi para modo AP |
| `is_connected` | bool | Estado de conexión |

## Funciones

### `connect_STA()`
Configura la ESP32 en modo cliente WiFi.

**Proceso:**
1. Activa modo `WIFI_STA`.
2. Limpia conexiones previas.
3. Configura IP estática.
4. Inicia conexión a red.
5. Espera confirmación de conexión.

**Configuración IP estática:**
- IP: `192.168.3.2`
- Gateway: `192.168.3.1`
- Subnet: `255.255.255.0`

**Retorna:**
- `true`: conexión exitosa.
- `false`: fallo de conexión.

---

### `connect_AP()`
Configura la ESP32 como punto de acceso.

**Proceso:**
1. Activa modo `WIFI_AP`.
2. Fuerza ancho de banda WiFi a 20 MHz.
3. Inicia Access Point.
4. Obtiene IP local del AP.

**Retorna:**
- `true`: AP creado correctamente.
- `false`: error al iniciar AP.

---

### `connect(int mode, String _ssid, String _password, int _apChannel)`
Selecciona dinámicamente el modo de conexión.

**Parámetros:**
- `mode`: AP o STA.
- `_ssid`: nombre de red.
- `_password`: contraseña.
- `_apChannel`: canal WiFi.

**Retorna:**
- `true`: conexión exitosa.
- `false`: error.

---

### `check_status()`
Monitorea el estado WiFi y detecta desconexiones.

**Acciones:**
- verifica `WiFi.status()`
- desconecta y actualiza bandera interna en caso de pérdida de enlace.

## Flujo interno
1. Se reciben parámetros de red.
2. Se selecciona AP o STA.
3. Se inicializa conexión.
4. Se almacena IP resultante.
5. Se monitorea estado de conexión.

## Modificaciones respecto al original

### Soporte mejorado para modo STA
Se agregó configuración explícita de IP estática:

```cpp
IPAddress local_IP(192,168,3,2);
IPAddress gateway(192,168,3,1);
IPAddress subnet(255,255,255,0);
WiFi.config(local_IP, gateway, subnet);
```

Esto garantiza direccionamiento determinista dentro de la red del rover.

---

### Reinicio limpio de interfaz STA
Cambio:

```cpp
WiFi.disconnect(true);
delay(100);
```

en lugar de:

```cpp
WiFi.disconnect();
```

Permite limpiar completamente configuraciones previas antes de reconectar.

---

### Configuración de ancho de banda AP a 20 MHz
Se añadió:

```cpp
esp_wifi_set_bandwidth(WIFI_IF_AP, WIFI_BW_HT20);
```

Objetivo:
- mejorar compatibilidad WiFi
- evitar problemas con clientes incompatibles con HT40

---

### Parámetros adicionales en `softAP()`
Cambio de:

```cpp
WiFi.softAP(ssid, password, apChannel);
```

a:

```cpp
WiFi.softAP(ssid, password, apChannel, 0, 1);
```

Configuración:
- red visible (`hidden = 0`)
- máximo 1 cliente

Esto restringe conexiones al sistema esperado.

## Notas
- La IP estática está diseñada para integrarse con la topología del rover.
- El gateway `192.168.3.1` corresponde al nodo principal de red.
- Limitar AP a un cliente reduce consumo y conexiones no deseadas.
