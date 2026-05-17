# perception.py

## Propósito
Implementa el preprocesamiento de imágenes y generación de máscaras utilizadas por el sistema de percepción visual.

Este módulo prepara frames de cámara para inferencia en el modelo de segmentación semántica, genera máscaras binarias de navegación y define la región de interés usada por el sistema de navegación.

## Dependencias
- `cv2`: redimensionamiento, conversión de color y operaciones geométricas.
- `numpy`: manipulación matricial y generación de máscaras.
- `config`: constantes globales del sistema.

## Variables globales
Las constantes utilizadas provienen de `config.py`.

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `MODEL_W` | int | ancho de entrada del modelo |
| `MODEL_H` | int | alto de entrada del modelo |
| `NAV_CLASSES` | list | clases consideradas navegables |
| `USE_TRAPEZOID` | bool | habilita ROI trapezoidal |

## Entradas y salidas

### Entradas
- frame RGB/BGR de cámara
- máscara segmentada
- detalles de entrada del modelo TFLite

### Salidas
- tensor preprocesado para inferencia
- máscara binaria navegable
- máscara ROI trapezoidal

## Funciones

### `preprocess(img, input_details)`
Preprocesa una imagen para inferencia en modelo de segmentación.

Operaciones realizadas:
- resize a resolución del modelo
- conversión BGR → RGB
- normalización `[0,1]`
- transformación HWC → CHW
- batch dimension
- cuantización opcional para modelos INT8

**Parámetros:**
- `img`: frame original
- `input_details`: detalles del intérprete TFLite

**Retorna:**
- tensor listo para inferencia.

---

### `create_navigation_mask(mask)`
Genera máscara binaria indicando regiones navegables.

Las clases válidas se definen en `NAV_CLASSES`.

**Parámetros:**
- `mask`: máscara segmentada multicategoría

**Retorna:**
- máscara binaria (`0` no navegable, `1` navegable)

---

### `trapezoid_roi(shape)`
Genera región de interés trapezoidal para navegación.

Permite limitar análisis a una región frontal relevante.

Si `USE_TRAPEZOID=False`, retorna máscara completa.

**Parámetros:**
- `shape`: tupla `(alto, ancho)`

**Retorna:**
- máscara ROI
- puntos del polígono trapezoidal

## Flujo interno
1. Recibir frame de cámara.
2. Ajustar resolución al modelo.
3. Convertir formato y normalizar.
4. Preparar tensor para inferencia.
5. Procesar máscara segmentada.
6. Generar máscara navegable.
7. Definir ROI frontal trapezoidal.

## Modificaciones respecto al original
- Se añadió soporte para modelos cuantizados INT8.
- Se implementó conversión automática HWC → CHW.
- Se incorporó generación de máscara binaria navegable.
- Se añadió ROI trapezoidal configurable.

## Consideraciones de rendimiento
- Preprocesamiento optimizado mediante operaciones vectorizadas.
- ROI reduce área analizada por navegación.
- Cuantización permite compatibilidad con modelos livianos para inferencia edge.

## Notas
- Este módulo no ejecuta inferencia; únicamente prepara datos.
- Diseñado para integrarse con modelos TFLite ejecutados en Raspberry Pi.
- Forma parte del pipeline principal de percepción visual.