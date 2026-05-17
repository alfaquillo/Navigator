# frame_source.py

## Propósito
Gestiona la adquisición de frames para el sistema de navegación.

Este módulo abstrae la fuente de imágenes permitiendo operar en dos modos:
- dataset de imágenes
- cámara en tiempo real

También realiza preprocesamiento geométrico básico para frames provenientes de cámara.

## Dependencias
- `os`: manejo de archivos y directorios.
- `cv2`: lectura de imágenes y captura de cámara.
- `config`: parámetros globales del sistema.

## Variables globales
Las configuraciones provienen desde `config.py`.

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `INPUT_MODE` | str | modo de entrada (`dataset` o `camera`) |
| `IMAGE_DIR` | str | directorio de imágenes |
| `CAMERA_URL` | str/int | fuente de cámara |
| `MODEL_W` | int | ancho de entrada requerido |
| `MODEL_H` | int | alto de entrada requerido |

## Entradas y salidas

### Entradas
- imágenes desde carpeta dataset
- frames desde cámara/video stream

### Salidas
- frames listos para pipeline principal
- índice de frame actual

## Clases

### `FrameSource`
Clase encargada de gestionar la fuente de imágenes del sistema.

Soporta:
- lectura secuencial desde dataset
- captura continua desde cámara

#### Atributos
| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `mode` | str | modo de adquisición |
| `cap` | VideoCapture | captura de cámara |
| `image_paths` | list | rutas del dataset |
| `idx` | int | índice actual |

## Métodos

### `__init__()`
Inicializa fuente de frames según configuración.

Modos soportados:

#### Dataset
- lista imágenes `.jpg` y `.png`
- ordena secuencialmente

#### Camera
- abre dispositivo o stream configurado

Valida:
- apertura correcta de cámara
- modo válido

**Parámetros:**
- ninguno

**Retorna:**
- instancia inicializada

---

### `_prepare_camera_frame(frame)`
Preprocesa frames provenientes de cámara.

Proceso:
1. obtener dimensiones originales
2. calcular crop cuadrado central
3. recortar imagen
4. redimensionar a tamaño del modelo

Objetivo:
- normalizar formato de entrada para inferencia

**Parámetros:**
- `frame`: frame original

**Retorna:**
- frame procesado

---

### `read()`
Obtiene siguiente frame disponible.

Comportamiento:

#### Dataset
- retorna siguiente imagen
- incrementa índice
- finaliza al terminar dataset

#### Camera
- captura nuevo frame
- aplica crop y resize
- incrementa contador

**Parámetros:**
- ninguno

**Retorna:**
- `ret`: éxito lectura
- `frame`: imagen obtenida
- `idx`: índice actual

---

### `release()`
Libera recursos de captura.

Cierra cámara si está activa.

**Parámetros:**
- ninguno

**Retorna:**
- no retorna valor

## Flujo interno
1. Leer configuración de entrada.
2. Inicializar dataset o cámara.
3. Obtener frame.
4. Si es cámara:
   - crop cuadrado central
   - resize a resolución modelo
5. Retornar frame al pipeline principal.

## Modificaciones respecto al original
- Se añadió soporte dual dataset/cámara.
- Se implementó crop central automático.
- Se agregó resize consistente al tamaño del modelo.
- Se añadió validación robusta de entrada.

## Consideraciones de rendimiento
- Lectura dataset adecuada para pruebas offline.
- Captura cámara optimizada para pipeline en tiempo real.
- Preprocesamiento geométrico de bajo costo.

## Notas
- Permite reutilizar el pipeline sin modificar lógica principal.
- Facilita testing offline con datasets y operación online con cámara real.
- Diseñado para integrarse directamente con `main.py`.