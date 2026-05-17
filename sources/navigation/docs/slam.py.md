# slam.py

## Propósito
Implementa un mapa semántico simplificado tipo SLAM para navegación local del rover.

Este módulo mantiene el estado global del mapa, la pose estimada del rover y la trayectoria histórica. Además integra observaciones provenientes de segmentación semántica para construir un mapa incremental del entorno.

## Dependencias
- `numpy`: almacenamiento y manipulación del mapa global.
- `math`: operaciones trigonométricas y actualización de pose.
- `config`: constantes globales del sistema.

## Variables globales
| Variable | Tipo | Descripción |
|----------|------|-------------|
| `grid` | ndarray | mapa semántico global |
| `x_m` | float | posición X del rover en metros |
| `y_m` | float | posición Y del rover en metros |
| `theta` | float | orientación actual del rover en radianes |
| `origin_x` | int | origen X del mapa en coordenadas de grid |
| `origin_y` | int | origen Y del mapa en coordenadas de grid |
| `trajectory` | list | historial de poses del rover |

## Entradas y salidas

### Entradas
- decisiones de movimiento del rover
- máscaras de segmentación semántica

### Salidas
- mapa semántico actualizado
- trayectoria histórica
- pose actual del rover

## Funciones

### `meters_to_cell()`
Convierte coordenadas métricas del rover a coordenadas discretas del grid.

**Parámetros:**
- ninguno

**Retorna:**
- `rx`: coordenada X en grid
- `ry`: coordenada Y en grid

---

### `expand_map_if_needed(rx, ry)`
Expande dinámicamente el mapa cuando el rover se acerca a los bordes.

Se agregan márgenes adicionales y se actualiza el origen del mapa.

**Parámetros:**
- `rx`: posición X actual en grid
- `ry`: posición Y actual en grid

**Retorna:**
- no retorna valor

---

### `move_rover(decision)`
Actualiza pose y orientación del rover según decisión de navegación.

Decisiones soportadas:
- `IZQUIERDA`
- `DERECHA`
- `RETROCEDER`
- avance implícito

**Parámetros:**
- `decision`: comando de movimiento

**Retorna:**
- no retorna valor

---

### `integrate_observation(mask)`
Integra observaciones semánticas dentro del mapa global.

Transforma coordenadas de imagen segmentada a coordenadas globales del mapa usando orientación actual del rover.

Proceso:
- recorte de región relevante
- downsampling
- proyección aproximada profundidad/lateral
- pintado de clases sobre grid

**Parámetros:**
- `mask`: máscara semántica segmentada

**Retorna:**
- no retorna valor

## Flujo interno
1. Inicializar mapa global con celdas desconocidas.
2. Mantener pose actual del rover.
3. Convertir pose a coordenadas grid.
4. Expandir mapa dinámicamente si es necesario.
5. Actualizar pose según decisiones de navegación.
6. Integrar observaciones semánticas proyectadas.
7. Registrar trayectoria histórica.

## Modificaciones respecto al original
- Se implementó mapa semántico basado en clases detectadas.
- Se añadió expansión dinámica del grid.
- Se agregó registro histórico de trayectoria.
- Se incorporó integración de observaciones desde segmentación.
- Se añadió proyección aproximada depth/lateral hacia mapa global.

## Consideraciones de rendimiento
- `integrate_observation()` usa iteración doble sobre máscara reducida.
- Se aplica downsampling (`[::6, ::6]`) para reducir carga computacional.
- El mapa crece dinámicamente, por lo que el uso de memoria aumenta conforme avanza exploración.

## Notas
- Este módulo implementa un pseudo-SLAM simplificado; no realiza optimización probabilística ni corrección de drift.
- La pose depende únicamente de odometría estimada por comandos ejecutados.
- Diseñado para exploración local en entorno estructurado tipo lunar/simulado.