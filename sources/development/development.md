# Development

## Descripción general
Carpeta utilizada durante la fase de desarrollo, experimentación y validación del sistema de navegación autónoma.

Contiene scripts, modelos intermedios, pruebas funcionales y archivos generados durante el proceso iterativo de diseño.

Los contenidos de esta carpeta fueron utilizados principalmente para:

- pruebas iniciales de navegación
- benchmarking de modelos TensorFlow Lite
- validación de SLAM
- debugging de sensores y comunicación
- comparación entre variantes de modelos

## Estructura del directorio

```text
development/
├── basic_control.py
├── exported_map_slam.py
├── full_map_classes.csv
├── inferir_especificaciones_rover.py
├── lunarModel_rpi5_cpu.tflite
├── lunar_rpi5_cpu.tflite
├── lunar_rpi5_float16.tflite
├── lunar_rpi5_int8.tflite
├── lunar_test_pi.py
├── lunar_test.py
├── model_fp16.tflite
├── model_int8.tflite
├── navigation.py
├── results/
├── slam_debug_map.png
├── slam_final.png
├── socket_test_rpi.py
├── test_lunar_slam_jp.py
├── test_lunar_slam.py
├── test_sensors.py
├── unet_model/
└── yolo/
```

## Funcionalidades principales

### Pruebas de inferencia
Scripts utilizados para validar modelos de segmentación semántica y medir desempeño sobre Raspberry Pi 5.

Archivos relevantes:
- `lunar_test.py`
- `lunar_test_pi.py`

### Evaluación de modelos
Almacena distintas variantes de modelos exportados:

- float16
- int8
- CPU optimized

Modelos:
- `lunar_rpi5_cpu.tflite`
- `lunar_rpi5_float16.tflite`
- `lunar_rpi5_int8.tflite`

### Debugging de SLAM
Pruebas de generación, exportación y análisis de mapas.

Archivos:
- `exported_map_slam.py`
- `slam_debug_map.png`
- `slam_final.png`
- `full_map_classes.csv`

### Comunicación y sensores
Scripts auxiliares para validar comunicación y sensores.

Archivos:
- `socket_test_rpi.py`
- `test_sensors.py`
- `basic_control.py`

## Estado dentro del proyecto
Los archivos de esta carpeta **no forman parte del sistema final desplegado**.

El sistema funcional y documentado se encuentra en:

```text
sources/navigation/
sources/esp32/
sources/rover_firmware/
sources/yocto-project/
```

Esta carpeta se conserva únicamente como referencia histórica del desarrollo y apoyo para futuras pruebas o benchmarking.

## Notas
- Contiene versiones experimentales y scripts de prueba.
- No se recomienda usar estos archivos para despliegue final.
- Algunos modelos y scripts fueron reemplazados por versiones finales integradas en el sistema principal.