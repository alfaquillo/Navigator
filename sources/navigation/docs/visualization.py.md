# visualization.py

## Propósito
Proporciona funciones auxiliares de visualización para el sistema de navegación autónoma.

Este archivo convierte máscaras de segmentación semántica en imágenes coloreadas para depuración visual y genera una representación gráfica del mapa SLAM local, incluyendo clases detectadas, trayectoria histórica y orientación actual del rover.

## Dependencias
- `cv2`: renderizado y escalado de imágenes.
- `numpy`: manipulación matricial y creación de mapas RGB.
- `math`: operaciones matemáticas básicas.
- `config`: constantes globales del sistema (`UNKNOWN`, etc.).
- `slam`: acceso al estado global del mapa, trayectoria y pose del rover.

## Variables globales
| Variable | Tipo | Descripción |
|----------|------|-------------|
| `slam.grid` | ndarray | mapa global de ocupación/semántico |
| `slam.theta` | float | orientación actual del rover |
| `slam.trajectory` | list | historial de poses recorridas |
| `UNKNOWN` | int | valor para celdas no observadas |

## Entradas y salidas

### Entradas
- máscara de segmentación semántica (`mask`)
- estado global del módulo `slam`

### Salidas
- imagen RGB coloreada
- visualización ampliada del mapa local SLAM

## Funciones

### `colorize_mask(mask)`
Convierte una máscara de clases numéricas en una imagen RGB/BGR coloreada.

**Parámetros:**
- `mask`: matriz 2D con etiquetas semánticas por píxel.

**Retorna:**
- imagen RGB coloreada como `numpy.ndarray`.

Colores asignados:
- gris: desconocido
- amarillo: cráteres
- rojo: rocas
- cian: montañas
- verde: cielo

---

### `draw_slam()`
Genera una representación visual del mapa SLAM centrada en la posición actual del rover.

La visualización incluye:
- mapa semántico observado
- regiones desconocidas
- trayectoria histórica
- posición actual del rover
- indicador de heading/orientación

**Parámetros:**
- ninguno (usa estado global de `slam`)

**Retorna:**
- imagen ampliada del mapa local como `numpy.ndarray`.

## Flujo interno
1. Obtener mapa global y pose actual desde `slam`.
2. Inicializar canvas visual.
3. Colorear celdas observadas según clase semántica.
4. Dibujar trayectoria histórica del rover.
5. Extraer ventana local centrada en rover.
6. Dibujar rover actual y vector de heading.
7. Escalar imagen para visualización.

## Modificaciones respecto al original
- Se agregó renderizado semántico basado en clases detectadas.
- Se incorporó visualización de trayectoria histórica.
- Se añadió recorte dinámico centrado en rover.
- Se incluyó indicador de orientación (heading).
- Se implementó escalado por interpolación nearest-neighbor para conservar bloques.

## Consideraciones de rendimiento
- `draw_slam()` usa doble iteración sobre ventana local (`VIEW x VIEW`), por lo que su costo depende del tamaño definido.
- El renderizado se usa principalmente para depuración/monitorización, no para lógica crítica de navegación.

## Notas
- Este módulo no modifica el mapa ni la pose del rover; únicamente visualiza información.
- Diseñado para debugging en tiempo real durante ejecución del sistema de navegación.