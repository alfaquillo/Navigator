
# Yocto Project

## Descripción general
Este directorio contiene la configuración y personalización del entorno Yocto utilizado para generar la imagen Linux de la Raspberry Pi 5 empleada como nodo central del sistema.

La imagen generada cumple múltiples funciones:

- punto de acceso WiFi (Access Point)
- servidor DHCP
- host de inferencia y navegación
- coordinador de comunicaciones entre dispositivos

La Raspberry Pi actúa como núcleo del sistema distribuido.

## Estructura del directorio

```text
yocto-project/
├── docs
│   ├── install_guide.md
│   └── meta-rpi-navigator.md
└── meta-rpi-navigator
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

## Documentación disponible

### Guía de instalación y compilación
Contiene instrucciones completas para:

- creación del contenedor Ubuntu 24.04
- instalación del entorno Yocto
- integración de capas
- compilación de imagen Raspberry Pi 5
- flasheo de tarjeta SD

Documento:

- [Install Guide](docs/install_guide.md)

---

### Documentación de capa personalizada
Describe la layer custom utilizada para integrar:

- aplicación de navegación
- configuración de red
- paquetes adicionales
- ajustes de OpenCV
- configuración de boot

Documento:

- [meta-rpi-navigator](docs/meta-rpi-navigator.md)

## Funcionalidades principales

### Imagen Linux personalizada
Genera una imagen headless basada en:

- `core-image-minimal`

Extendida con:

- Python 3
- OpenCV
- TensorFlow Lite
- GStreamer

---

### Configuración de red autónoma
La Raspberry Pi se configura como:

- Access Point WiFi
- servidor DHCP

Red generada:

```text
SSID: Moon_rpi_AP
Subnet: 192.168.3.0/24
Gateway: 192.168.3.1
```

---

### Aplicación de navegación integrada
Instala automáticamente:

```bash
navigation
```

Aplicación principal basada en:

```bash
python3 main.py
```

---

### Arquitectura distribuida
Topología final:

```text
Raspberry Pi
├── Rover firmware
├── ESP32-CAM
└── Laptop/control station
```

## Flujo de uso recomendado

1. Seguir guía de instalación:
   - [Install Guide](docs/install_guide.md)

2. Construir imagen Yocto.

3. Flashear SD.

4. Iniciar Raspberry Pi.

5. Verificar red y servicios.

## Dependencias externas

- Yocto Project (kirkstone)
- meta-raspberrypi
- meta-openembedded
- meta-tensorflow

## Notas
- Proyecto orientado a Raspberry Pi 5.
- Configuración optimizada para operación headless.
- Toda personalización se encapsula en `meta-rpi-navigator`.
