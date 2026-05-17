# sensors.py

## Propósito
Gestiona el estado de sensores de proximidad y distancia del rover, así como la lógica local de evasión de obstáculos.

Este módulo recibe datos provenientes del ESP32 mediante WebSocket, actualiza el estado interno de sensores y determina acciones correctivas inmediatas cuando se detectan obstáculos cercanos.

## Dependencias
- `time`: temporización y control de duración de maniobras.
- `config`: constantes por defecto de sensores.

## Variables globales
Este archivo no define variables globales; utiliza atributos internos de clase.

## Entradas y salidas

### Entradas
- datos de sensores provenientes de WebSocket
- lecturas IR izquierda/derecha
- distancia LIDAR

### Salidas
- acciones de evasión:
  - `LIBRE`
  - `RETROCEDER`
  - `IZQUIERDA`
  - `DERECHA`

## Clases

### `Sensors`
Clase principal para almacenamiento y procesamiento de sensores.

Mantiene:
- estado actual de sensores
- estado de conexión
- acción correctiva activa
- temporizadores de acción

#### Atributos
| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `prox_izq` | int | lectura sensor IR izquierdo |
| `prox_der` | int | lectura sensor IR derecho |
| `dist` | int/float | distancia medida por LIDAR |
| `connected` | bool | indica recepción válida de datos |
| `lidar_block_count` | int | contador auxiliar de bloqueo |
| `current_action` | str | acción actualmente activa |
| `action_until` | float | timestamp límite de acción |

## Funciones

### `__init__()`
Inicializa sensores con valores por defecto.

**Parámetros:**
- ninguno

**Retorna:**
- instancia inicializada.

---

### `update(data)`
Actualiza lecturas internas a partir de datos recibidos por WebSocket.

Valida:
- tipo diccionario
- existencia de clave principal de distancia

Campos utilizados:
- `N`: IR izquierdo
- `P`: IR derecho
- `O`: distancia LIDAR

**Parámetros:**
- `data`: diccionario JSON recibido

**Retorna:**
- no retorna valor

---

### `decide_avoidance(th_dist=30)`
Determina acción de evasión basada en lecturas actuales.

Implementa:
- lógica LIDAR con hysteresis
- retroceso temporal
- evasión por sensores IR laterales
- timeout de seguridad

Acciones posibles:
- libre tránsito
- retroceso
- giro correctivo

**Parámetros:**
- `th_dist`: umbral nominal de distancia (actualmente reemplazado por thresholds internos)

**Retorna:**
- string con acción recomendada

## Flujo interno
1. Recibir datos del ESP32.
2. Actualizar estado interno de sensores.
3. Verificar conexión activa.
4. Evaluar acción previa en curso.
5. Aplicar lógica LIDAR con hysteresis:
   - entrada por proximidad
   - salida por distancia segura
6. Evaluar sensores IR laterales.
7. Retornar acción correctiva.

## Modificaciones respecto al original
- Se agregó integración de datos vía WebSocket.
- Se implementó lógica de evasión basada en hysteresis.
- Se añadieron timers para mantener acciones temporales.
- Se integró combinación LIDAR + sensores IR.
- Se agregó control de conexión activa.

## Consideraciones de rendimiento
- Carga computacional mínima.
- Ejecutado en tiempo real como filtro rápido previo a navegación visual.
- Uso intensivo de timestamps para control temporal.

## Notas
- Este módulo tiene prioridad de seguridad sobre navegación visual.
- Si no hay conexión con sensores, retorna `LIBRE`.
- Diseñado para evasión reactiva inmediata ante obstáculos cercanos.
- Complementa navegación basada en visión y SLAM.