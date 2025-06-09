#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import time
import sys
import signal
import threading
import itertools
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"

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

def ctrl_c(signal, frame):
    print("\n[!] Saliendo con Ctrl+C...")
    sys.stdout.write(SHOW_CURSOR)
    sys.stdout.flush()
    if navegador:
        navegador.quit()
    sys.exit(0)

signal.signal(signal.SIGINT, ctrl_c)

def cerrar_pestana_adblock(navegador, timeout=10):
    num_pestanas_inicial = len(navegador.window_handles)
    
    try:
        WebDriverWait(navegador, timeout).until(
            lambda driver: len(driver.window_handles) > num_pestanas_inicial
        )
    except:
        print("No se abrió ninguna pestaña nueva del adblocker dentro del tiempo de espera.")
        return

    for handle in navegador.window_handles:
        navegador.switch_to.window(handle)
        titulo = navegador.title.lower()
        url = navegador.current_url.lower()
        if "adblock" in titulo or "welcome" in url:
            navegador.close() 

# Volver a la pestaña principal
    if navegador.window_handles:
        navegador.switch_to.window(navegador.window_handles[0])

def iniciar_navegador(usar_adblock=False):
    options = Options()
    options.add_argument("--start-maximized") 
    if usar_adblock:
        sys.stdout.write(HIDE_CURSOR)
        sys.stdout.flush()
        spinner = Spinner ("Instalando AdBlock...")
        spinner.start()
        options.add_extension("utils/AdBlock.crx")
    
        
    
    #options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    #options.add_argument("--headless")  # si querés que corra sin mostrar la ventana

    ruta_driver = os.path.abspath("drivers/chromedriver")
    
    # Verificar si el archivo 'chromedriver' existe
    if not os.path.isfile(ruta_driver):
        print(f"[!] El archivo chromedriver no se encuentra en la ruta: {ruta_driver}")
        return None
    
    # Crear el servicio y navegador
    service = Service(ruta_driver)
    navegador = webdriver.Chrome(service=service, options=options)
    
    if usar_adblock:
        sys.stdout.write(HIDE_CURSOR)
        sys.stdout.flush()
        spinner.stop("AdBlock instalado con éxito")
        print() 
        
    return navegador
    sys.stdout.write(SHOW_CURSOR)
    sys.stdout.flush()
