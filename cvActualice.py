#!/usr/bin/env python3

import signal
import sys
import getpass
import tkinter as tk
from tkinter import filedialog
import os
import readline
from utils.navegador import iniciar_navegador, cerrar_pestana_adblock
from portales import computrabajo, bumeran, zonajobs, buscojobs, trabajosdiarios 
import itertools
import threading
import time

HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"

PORTALES_DISPONIBLES = {
    "1": ("Computrabajo", "computrabajo"),
    "2": ("Bumeran", "bumeran"),
    "3": ("Zonajobs", "zonajobs"),
    "4": ("Buscojobs", "buscojobs"),
    "5": ("TrabajosDiarios", "trabajosdiarios"),
}

# Spinner

class Spinner:
    def __init__(self, mensaje="Procesando"):
        self.mensaje = mensaje
        self._spinner = itertools.cycle(['/', '-', '\\', '|'])
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._spin)
        self._thread.daemon = True

    def _spin(self):
        while not self._stop_event.is_set():
            char = next(self._spinner)
            sys.stdout.write(f'\r[{char}] {self.mensaje}')
            sys.stdout.flush()
            time.sleep(0.1)

    def start(self):
        self._stop_event.clear()
        self._thread.start()

    def stop(self, mensaje_final="Completado"):
        self._stop_event.set()
        self._thread.join()
        sys.stdout.write(f'\r[✔] {mensaje_final}{" " * 20}\n')
        sys.stdout.flush()

    def stop_error(self, mensaje_error="Error"):
        self._stop_event.set()
        self._thread.join()
        sys.stdout.write(f'\r[!] {mensaje_error}{" " * 20}\n')
        sys.stdout.flush()

interrumpido = False

def ctrl_c(signal, frame):
    global interrumpido
    interrumpido = True
    print("\n\n[!] Saliendo...\n")
    sys.stdout.write(SHOW_CURSOR)
    sys.stdout.flush()
    global navegador
    if 'navegador' in globals() and navegador:
        navegador.quit()    
    sys.exit(130)

# Ctrl + C
signal.signal(signal.SIGINT, ctrl_c)

def seleccionar_portales():
    print("\nSeleccione los portales donde desea actualizar el CV:\n")
    for k, (nombre, _) in PORTALES_DISPONIBLES.items():
        print (f"  {k}. {nombre}")
    seleccion = input("\nIngrese los identificadores númericos de los portales a actualizar (ej: 1 3 5) (Deje en blanco para actualizar en todos): ").split()
    if not seleccion:
        return [portal[1] for portal in PORTALES_DISPONIBLES.values()]
    return [PORTALES_DISPONIBLES[num][1] for num in seleccion if num in PORTALES_DISPONIBLES]

def limpiar_consola():
    sistema_operativo = os.name
    if sistema_operativo == 'posix':  # Para Linux o macOS
        os.system('clear')
    else:  # Para Windows
        os.system('cls')

def obtener_ruta_cv():
    sys.stdout.write(HIDE_CURSOR)
    sys.stdout.flush()
    print()
    spinner = Spinner("Seleccione el archivo del CV...")
    spinner.start()
    # Abrir un cuadro de diálogo para seleccionar el archivo
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal de tkinter
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo del CV",
        filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
    )
    if not archivo:
        spinner.stop_error("No se seleccionó ningún archivo. El proceso se detendrá...")
        print()
        sys.stdout.write(SHOW_CURSOR)
        sys.stdout.flush()
        sys.exit(1)

    spinner.stop("CV seleccionado")
    print()
    return archivo
    sys.stdout.write(SHOW_CURSOR)
    sys.stdout.flush()

def obtener_credenciales(portales_seleccionados):
    # Inicialización por defecto para evitar errores si no se usan
    correo_computrabajo = correo_zonajobs = correo_bumeran = correo_buscojobs = correo_trabajosdiarios = correo_randstad = ""
    contrasena_computrabajo = contrasena_zonajobs = contrasena_bumeran = contrasena_buscojobs = contrasena_trabajosdiarios = contrasena_randstad = ""
    # Preguntamos si usar el mismo correo para todas las plataformas
    usar_mismo_correo = input("¿Desea usar el mismo correo para todas las plataformas? (s/n): ").strip().lower()
        

    # Si la respuesta es 'n', pedimos los correos individualmente para cada plataforma
    if usar_mismo_correo != 's':
        # Pedimos el correo principal
        correo_principal = input("\nIngrese su correo principal (el que más se repite): ")
        if "computrabajo" in portales_seleccionados:
            correo_computrabajo = input("\nIngrese el correo para Computrabajo (deje en blanco para usar el principal): ").strip()
            if not correo_computrabajo:
                correo_computrabajo = correo_principal
        if "zonajobs" in portales_seleccionados:
            correo_zonajobs = input("Ingrese el correo para Zonajobs (deje en blanco para usar el principal): ").strip()
            if not correo_zonajobs:
                correo_zonajobs = correo_principal
        if "bumeran" in portales_seleccionados:
            correo_bumeran = input("Ingrese el correo para Bumeran (deje en blanco para usar el principal): ").strip()
            if not correo_bumeran:
                correo_bumeran = correo_principal
        if "buscojobs" in portales_seleccionados:
            correo_buscojobs = input("Ingrese el correo para BuscoJobs (deje en blanco para usar el principal): ").strip()
            if not correo_buscojobs in portales_seleccionados:
                correo_buscojobs = correo_principal
        if "trabajosdiarios" in portales_seleccionados:
            correo_trabajosdiarios = input("Ingrese el correo para Trabajos Diarios (deje en blanco para usar el principal): ").strip()
            if not correo_trabajosdiarios:
                correo_trabajosdiarios = correo_principal
    else:
        # Pedimos el correo principal
        correo_principal = input("\nIngrese su correo electrónico: ")

        correo_computrabajo = correo_principal
        correo_zonajobs = correo_principal
        correo_bumeran = correo_principal
        correo_buscojobs = correo_principal 
        correo_trabajosdiarios = correo_principal

    # Ahora pedimos la contraseña para todas las plataformas
    contrasena_principal = getpass.getpass("\nIngrese su contraseña principal (la que más se repita): ")

    # Pedimos contraseñas específicas para cada plataforma si es necesario
    if "computrabajo" in portales_seleccionados:
        contrasena_computrabajo = getpass.getpass(f"\nIngrese la contraseña para Computrabajo (deje en blanco para usar la contraseña principal): ").strip()
        if not contrasena_computrabajo:
            contrasena_computrabajo = contrasena_principal
            if not contrasena_principal:
                print("\n\nDebe ingresar una contraseña\n")
                sys.exit(1)
    if "zonajobs" in portales_seleccionados:
        contrasena_zonajobs = getpass.getpass(f"Ingrese la contraseña para ZonaJobs (deje en blanco para usar la contraseña principal): ").strip()
        if not contrasena_zonajobs:
            contrasena_zonajobs = contrasena_principal
    if "bumeran" in portales_seleccionados:
        contrasena_bumeran = getpass.getpass(f"Ingrese la contraseña para Bumeran (deje en blanco para usar la contraseña principal): ").strip()
        if not contrasena_bumeran:
            contrasena_bumeran = contrasena_principal
    if "buscojobs" in portales_seleccionados:
        contrasena_buscojobs = getpass.getpass(f"Ingrese la contraseña para BuscoJobs (deje en blanco para usar la contraseña principal): ").strip()
        if not contrasena_buscojobs:
            contrasena_buscojobs = contrasena_principal
    if "trabajosdiarios" in portales_seleccionados:
        contrasena_trabajosdiarios = getpass.getpass(f"Ingrese la contraseña para Trabajos Diarios (deje en blanco para usar la contraseña principal): ").strip()
        if not contrasena_trabajosdiarios:
            contrasena_trabajosdiarios = contrasena_principal

    return correo_principal, correo_computrabajo, correo_zonajobs, correo_bumeran, correo_buscojobs, correo_trabajosdiarios, correo_randstad, contrasena_principal, contrasena_computrabajo, contrasena_zonajobs, contrasena_bumeran, contrasena_buscojobs, contrasena_trabajosdiarios, contrasena_randstad

def main():
    portales_seleccionados = seleccionar_portales()
    correo_principal, correo_computrabajo, correo_zonajobs, correo_bumeran, correo_buscojobs, correo_trabajosdiarios, correo_randstad, contrasena_principal, contrasena_computrabajo, contrasena_zonajobs, contrasena_bumeran, contrasena_buscojobs, contrasena_trabajosdiarios, contrasena_randstad = obtener_credenciales(portales_seleccionados)
    
    CV_PATH = obtener_ruta_cv()
   
   
    usar_adblock = "trabajosdiarios" in portales_seleccionados

    global navegador
    navegador = iniciar_navegador(usar_adblock=usar_adblock)

    if usar_adblock:
        spinner = Spinner("Ultimando detalles...")
        spinner.start()
        cerrar_pestana_adblock(navegador)
        spinner.stop("Todo listo para iniciar")
        

    limpiar_consola()

    try:
        sys.stdout.write(HIDE_CURSOR)
        sys.stdout.flush()
        if "computrabajo" in portales_seleccionados:
            print()
            spinner = Spinner("Actualizando CV en Computrabajo...")
            spinner.start()
            computrabajo.actualizar_cv(navegador, correo_computrabajo, contrasena_computrabajo, CV_PATH, spinner)            
        if "zonajobs" in portales_seleccionados:
            print()
            spinner = Spinner("Actualizando CV en ZonaJobs...")
            spinner.start()
            zonajobs.actualizar_cv(navegador, correo_zonajobs, contrasena_zonajobs, CV_PATH, spinner)
        if "bumeran" in portales_seleccionados:
            print()
            spinner = Spinner("Actualizando CV en Bumeran...")
            spinner.start()
            bumeran.actualizar_cv(navegador, correo_bumeran, contrasena_bumeran, CV_PATH, spinner)
        if "buscojobs" in portales_seleccionados:
            print()
            spinner = Spinner("Actualizando CV en BuscoJobs...")
            spinner.start()
            buscojobs.actualizar_cv(navegador, correo_buscojobs, contrasena_buscojobs, CV_PATH, spinner)
        if "trabajosdiarios" in portales_seleccionados:
            print()
            spinner = Spinner("Actualizando CV en Trabjos Diarios...")
            spinner.start()
            trabajosdiarios.actualizar_cv(navegador, correo_trabajosdiarios, contrasena_trabajosdiarios, CV_PATH, spinner)


    finally:
        navegador.quit()  # Cerrar navegador al final de todo el proceso
        if not interrumpido:
            print(f"\n\n[+] CV actualizado con éxito en {len(portales_seleccionados)} portales\n")
        sys.stdout.write(SHOW_CURSOR)
        sys.stdout.flush()

if __name__ == "__main__":
    main()
