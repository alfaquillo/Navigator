# navigation.py

## Propósito
Implementa la lógica principal de decisión de navegación basada en percepción visual.

Este módulo analiza la máscara binaria navegable y determina la dirección de movimiento más conveniente para el rover, priorizando avance frontal cuando existe suficiente espacio libre.

## Dependencias
- `numpy`: cálculo estadístico sobre regiones de navegación.
- `config`: parámetros y umbrales globales.

## Variables globales
Las constantes utilizadas provienen desde `config.py`.

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `MIN_FORWARD` | float | umbral mínimo para permitir avance frontal |
| `DELTA_CENTER` | float | tolerancia entre región central y laterales |
| `DELTA_SIDE` | float | diferencia mínima entre laterales para girar |

## Entradas y salidas

### Entradas
- máscara binaria navegable
- máscara ROI

### Salidas
- decisión de navegación:
  - `ADELANTE`
  - `IZQUIERDA`
  - `DERECHA`

## Funciones

### `decide_direction(nav_mask, roi_mask)`
Determina dirección de navegación a partir del análisis espacial de regiones navegables.

Proceso:
- aplica ROI sobre máscara navegable
- divide imagen en tres regiones:
  - izquierda
  - centro
  - derecha
- calcula métricas de ocupación navegable
- prioriza avance frontal si existe espacio suficiente
- selecciona lateral dominante cuando es necesario girar

La región central se pondera dando mayor importancia al área cercana al rover.

**Parámetros:**
- `nav_mask`: máscara binaria de navegación
- `roi_mask`: máscara de región de interés

**Retorna:**
- `decision`: dirección elegida
- `center_ratio`: score región central
- `left_ratio`: score región izquierda
- `right_ratio`: score región derecha

## Flujo interno
1. Aplicar ROI sobre máscara navegable.
2. Obtener dimensiones de trabajo.
3. Dividir imagen en regiones izquierda, centro y derecha.
4. Calcular score promedio por región.
5. Ponderar región central por proximidad.
6. Comparar umbrales de avance.
7. Evaluar diferencias laterales.
8. Seleccionar decisión final.

## Modificaciones respecto al original
- Se añadió análisis basado en regiones ponderadas.
- Se incorporó priorización de avance frontal.
- Se agregó comparación lateral para selección de giro.
- Se implementaron umbrales configurables mediante `config.py`.

## Consideraciones de rendimiento
- Implementación completamente vectorizada.
- Costo computacional bajo.
- Diseñado para ejecución en tiempo real por frame.

## Notas
- Este módulo no controla sensores ni comunicación.
- Utiliza únicamente información derivada de visión.
- Constituye la lógica principal de navegación deliberativa del sistema.
- Puede ser sobrescrito temporalmente por módulos reactivos de evasión.