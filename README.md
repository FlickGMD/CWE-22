# CWE-22: Herramienta para Auditoría de Path Traversal

![CWE-22](https://img.shields.io/badge/Security-CWE--22-red)

## Descripción
CWE-22 es una herramienta escrita en Python para auditar vulnerabilidades de Path Traversal. Permite explorar posibles fallos de seguridad en aplicaciones web al intentar acceder a archivos en el sistema del servidor mediante manipulaciones en la URL.

## Características
- Especificar un objetivo a auditar mediante una URL.
- Buscar archivos con extensiones específicas.
- Leer archivos del sistema objetivo, por defecto `/etc/passwd`.
- Multithreading para mejorar la eficiencia.

## Instalación
Clona el repositorio:
```bash
$ git clone https://github.com/FlickGMD/CWE-22.git
$ cd CWE-22
```
Instala las dependencias necesarias:
```bash
$ pip install -r requirements.txt
```

## Uso
```bash
python3 CWE-22.py [-h] -t TARGET [-x EXTENSION] [-f FILE]
```

### Opciones
```
  -h, --help            Mostrar la ayuda y salir
  -t, --target TARGET   URL que será auditada, ejemplo: (https://firefox.com/?users=FUZZ)
  -x, --extension EXTENSION   Buscar por un archivo con un tipo de extensión, ejemplo: (.jpg | jpg)
  -f, --file FILE       Archivo a leer del sistema, por defecto será /etc/passwd
```

### Ejemplo de Uso
```bash
python3 CWE-22.py -t "https://example.com/?file=FUZZ" -f "/etc/passwd"
```

## Dependencias
La herramienta utiliza los siguientes módulos de Python:
- `sys`
- `argparse`
- `threading`
- `urllib3`
- `signal`
- `Colors` (módulo personalizado para manejar colores en la salida)

## Advertencia
Este script está diseñado para fines educativos y de auditoría de seguridad en entornos autorizados. **El uso indebido de esta herramienta puede ser ilegal.**

## Autor
[FlickGMD](https://github.com/FlickGMD)


