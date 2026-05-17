# socket_rpi.py

## Propósito
Cliente TCP utilizado para recibir y visualizar en una computadora externa el stream de video enviado por la Raspberry Pi.

Este archivo permite conectarse al servidor TCP ejecutado en la RPi, recibir frames JPEG serializados y desplegarlos en tiempo real para monitoreo y depuración remota.

## Dependencias
- `socket`: comunicación TCP cliente-servidor.
- `cv2`: decodificación JPEG y visualización de frames.
- `numpy`: conversión de buffer binario a arreglo interpretable.
- `time`: temporización para reconexión.
- `sys`: soporte general del sistema.

## Variables globales
| Variable | Tipo | Descripción |
|----------|------|-------------|
| `SERVER_IP` | str | dirección IP del servidor TCP en la Raspberry Pi |
| `PORT` | int | puerto TCP del servidor |
| `frame_count` | int | contador de frames recibidos |
| `no_data_count` | int | contador de errores consecutivos de decodificación |

## Entradas y salidas

### Entradas
- stream TCP proveniente de Raspberry Pi
- frames JPEG serializados

### Salidas
- ventana OpenCV con video en tiempo real
- logs de conexión y errores en consola

## Funciones

### `main()`
Función principal del cliente TCP.

Se encarga de:
- conectarse al servidor de video en la Raspberry Pi,
- recibir frames codificados JPEG,
- decodificarlos,
- mostrarlos en tiempo real,
- reconectar automáticamente ante fallos.

**Parámetros:**
- ninguno

**Retorna:**
- no retorna valor; mantiene ejecución continua hasta salida manual.

## Flujo interno
1. Crear socket TCP cliente.
2. Conectarse al servidor definido por IP y puerto.
3. Recibir 4 bytes con tamaño del frame.
4. Validar tamaño recibido.
5. Recibir buffer completo de imagen JPEG.
6. Decodificar imagen usando OpenCV.
7. Redimensionar frame si excede ancho máximo.
8. Mostrar stream en ventana.
9. Detectar tecla `q` para cierre manual.
10. Manejar errores y reconectar automáticamente.

## Modificaciones respecto al original
- Se implementó protocolo de recepción basado en tamaño prefijado de 4 bytes.
- Se agregó validación de tamaño máximo de frame.
- Se incorporó lógica robusta de reconexión automática.
- Se añadió manejo de errores por timeout y corrupción de frames.
- Se agregó limitación de resolución visual para pantallas pequeñas.

## Consideraciones de rendimiento
- El buffer de recepción usa chunks de hasta 65536 bytes para mejorar throughput.
- El resize solo ocurre cuando el frame excede 1280 px de ancho.
- La visualización depende de `cv2.waitKey(1)`, por lo que requiere entorno gráfico.

## Notas
- Archivo destinado a monitoreo externo y debugging del sistema.
- No forma parte de la lógica principal de navegación.
- Requiere que el servidor TCP en la Raspberry Pi esté activo y transmitiendo imágenes.
- La salida puede cerrarse manualmente presionando `q`.