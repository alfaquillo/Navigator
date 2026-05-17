# model.py

## Propósito
Gestiona la carga e inferencia del modelo de segmentación semántica en formato TensorFlow Lite.

Este módulo encapsula la inicialización del intérprete TFLite, configuración de tensores y ejecución de inferencia sobre imágenes preprocesadas.

## Dependencias
- `tflite_runtime.interpreter`: ejecución de modelos TensorFlow Lite.
- `numpy`: manipulación de tensores y logits.
- `cv2`: redimensionamiento de máscaras de salida.

## Variables globales
Este archivo no define variables globales.

## Entradas y salidas

### Entradas
- ruta al modelo `.tflite`
- tensor preprocesado para inferencia
- tamaño de salida deseado

### Salidas
- intérprete inicializado
- máscara segmentada final

## Funciones

### `load_model(path)`
Carga e inicializa un modelo TensorFlow Lite.

Proceso:
- crear intérprete
- asignar hilos de ejecución
- reservar tensores
- extraer detalles de entrada y salida
- detectar tipo de entrada

Información almacenada:
- intérprete
- tensores de entrada/salida
- flags de tipo de modelo

**Parámetros:**
- `path`: ruta al archivo `.tflite`

**Retorna:**
- diccionario `model_info` con configuración del modelo.

Contenido retornado:
- `interpreter`
- `input_details`
- `output_details`
- `is_int8`
- `is_float`

---

### `infer(model_info, model_img, resize_shape)`
Ejecuta inferencia sobre una imagen preprocesada.

Proceso:
1. cargar tensor de entrada
2. ejecutar inferencia
3. obtener logits de salida
4. desquantizar salida si modelo es INT8
5. calcular clase dominante por píxel
6. redimensionar máscara al tamaño deseado

El método detecta automáticamente orientación del tensor de salida:
- formato `CHW`
- formato `HWC`

**Parámetros:**
- `model_info`: configuración retornada por `load_model`
- `model_img`: tensor preprocesado
- `resize_shape`: tamaño final de máscara

**Retorna:**
- máscara segmentada como `numpy.ndarray`

## Flujo interno
1. Cargar modelo TFLite.
2. Inicializar intérprete.
3. Preparar tensores.
4. Recibir imagen preprocesada.
5. Ejecutar inferencia.
6. Obtener logits.
7. Aplicar argmax por clase.
8. Redimensionar salida final.

## Modificaciones respecto al original
- Se agregó soporte para modelos cuantizados INT8.
- Se implementó desquantización automática de salida.
- Se añadió detección automática de layout de logits.
- Se configuró ejecución multihilo (`num_threads=8`).

## Consideraciones de rendimiento
- Uso de 8 hilos para aprovechar CPU multinúcleo de la Raspberry Pi.
- Compatible con modelos livianos TFLite optimizados para edge.
- Redimensionamiento final usa interpolación nearest-neighbor para preservar clases.

## Notas
- Actualmente optimizado para modelos INT8.
- Compatible también con modelos float32.
- No realiza preprocesamiento; espera tensor ya preparado.
- Forma parte central del pipeline de percepción visual.