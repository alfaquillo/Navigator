
# meta-rpi-navigator

## Descripción general
Este directorio contiene una capa personalizada de Yocto utilizada para generar la imagen Linux de la Raspberry Pi empleada como nodo central del sistema.

La imagen construida incluye:

- configuración de red WiFi/AP
- servidor DHCP
- aplicación principal de navegación
- soporte OpenCV y TensorFlow Lite
- entorno headless optimizado

La Raspberry Pi cumple el rol de:

- router WiFi del sistema
- host de inferencia
- centro de coordinación entre rover, ESP32-CAM y estación de control

## Estructura del directorio

```text
meta-rpi-navigator/
├── conf
│   └── layer.conf
├── recipes-apps
│   └── navigator
│       └── navigator.bb
├── recipes-bsp
│   └── bootfiles
│       ├── files
│       │   └── config.txt
│       └── rpi-bootfiles.bbappend
├── recipes-core
│   └── images
│       └── core-image-minimal.bbappend
└── recipes-support
    ├── network-config
    │   ├── files
    │   │   ├── dnsmasq.conf
    │   │   ├── hostapd.conf
    │   │   └── network-init.sh
    │   └── network-config.bb
    └── opencv
        └── opencv_%.bbappend
```

## Componentes principales

## `conf/layer.conf`
Define la capa Yocto:

- nombre de colección
- prioridad
- compatibilidad con release `kirkstone`

Responsabilidad:
- registrar la capa en el sistema BitBake.

---

## `recipes-apps/navigator/navigator.bb`
Receta principal de la aplicación de navegación.

Responsabilidades:

- descarga repositorio del proyecto
- instala aplicación Python
- copia `sources/navigation`
- crea launcher ejecutable:

```bash
navigation
```

Dependencias incluidas:

- Python 3
- OpenCV
- NumPy
- TensorFlow Lite
- GStreamer

Aplicación principal:

```bash
python3 main.py
```

---

## `recipes-core/images/core-image-minimal.bbappend`
Extiende imagen base de Yocto.

Agrega:

### Red
- hostapd
- dnsmasq
- iptables
- iw

### Python
- python3
- numpy
- opencv
- websockets

### ML
- tensorflow-lite

### Multimedia
- GStreamer plugins

### Utilidades
- nano
- htop
- procps
- curl
- wget
- git

### SSH
- dropbear

Además:
- elimina X11 y Wayland para operación headless.

---

## `recipes-support/network-config/`
Configura red autónoma de Raspberry Pi.

### `hostapd.conf`
Configura Access Point:

- SSID: `Moon_rpi_AP`
- canal: 6
- WPA2

Permite conexión de:

- rover
- ESP32-CAM
- laptop

---

### `dnsmasq.conf`
Configura DHCP:

```text
192.168.3.30 - 192.168.3.50
```

Red:
- `192.168.3.0/24`

---

### `network-init.sh`
Script de inicialización de red.

Responsabilidades:

1. espera interfaces
2. configura Ethernet
3. configura WiFi AP
4. asigna IP estática:
   - `192.168.3.1`

5. inicia:
   - hostapd
   - dnsmasq

Convierte la Raspberry Pi en router autónomo.

---

### `network-config.bb`
Instala:

- hostapd.conf
- dnsmasq.conf
- network-init.sh

También registra script en arranque:

```text
/etc/rcS.d/S99network-init
```

---

## `recipes-support/opencv/opencv_%.bbappend`
Ajusta configuración OpenCV.

Habilita:

- `v4l`
- `dnn`

Deshabilita:

- gtk
- qt5

Objetivo:
- reducir tamaño
- mantener visión por computador headless

---

## `recipes-bsp/bootfiles/`
Configuración de arranque Raspberry Pi.

### `config.txt`
Parámetros:

```text
dtoverlay=vc4-kms-v3d
gpu_mem=256
max_framebuffers=2
```

Optimiza:
- memoria GPU
- framebuffer
- aceleración gráfica

---

### `rpi-bootfiles.bbappend`
Añade `config.txt` al boot final.

## Flujo de construcción

1. BitBake registra layer.
2. Se construye imagen minimal.
3. Se agregan paquetes custom.
4. Se instala app navigator.
5. Se configura red AP.
6. Se genera imagen final.

## Topología de red resultante

```text
Raspberry Pi (192.168.3.1)
├── DHCP server
├── Access Point: Moon_rpi_AP
├── Navigation app
├── Rover
├── ESP32-CAM
└── Laptop
```

## Dependencias
- Yocto Project
- BitBake
- Raspberry Pi BSP
- OpenCV
- TensorFlow Lite
- GStreamer

## Modificaciones realizadas
Esta layer fue creada para:

- transformar Raspberry Pi en nodo central autónomo
- integrar red WiFi local
- desplegar aplicación de navegación automáticamente
- soportar inferencia y streaming

## Notas
- Diseño optimizado para operación headless.
- La imagen resultante funciona sin monitor ni periféricos externos.
