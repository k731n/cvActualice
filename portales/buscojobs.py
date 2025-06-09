#!/usr/bin/env python3

import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import threading
import itertools

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

def actualizar_cv(navegador, email, password, path_cv, spinner):
    wait = WebDriverWait(navegador, 15)
   
    def safe_click(by, locator):
        for _ in range(3):
            try:
                element = wait.until(EC.element_to_be_clickable((by, locator)))
                element.click()
                return
            except StaleElementReferenceException:
                time.sleep(1)
        raise Exception(f"No se pudo hacer click en {locator}")

    def safe_send_keys(by, locator, keys):
        for _ in range(3):
            try:
                element = wait.until(EC.presence_of_element_located((by, locator)))
                element.send_keys(keys)
                return
            except StaleElementReferenceException:
                time.sleep(1)
        raise Exception(f"No se pudo enviar keys a {locator}")

    try:
        navegador.get("https://www.buscojobs.com.ar/login")
        wait.until(EC.url_contains("buscojobs.com.ar/login"))
        
        safe_send_keys(By.ID, "user", email)
        safe_send_keys(By.ID, "password", password)
        safe_click(By.ID, "sign-in")

        wait.until(EC.url_contains("/postulante"))
        navegador.get("https://www.buscojobs.com.ar/app/postulante/mi-cv")

        safe_click(By.XPATH, "//button[.//span[text()='Subir archivo']]")
        
        safe_send_keys(By.NAME, "archivo", path_cv)

        safe_click(By.XPATH, "//button[.//span[text()='Subir']]")

        time.sleep(2)  # Podrías reemplazar esto también por una espera explícita si querés más precisión.
        
        spinner.stop("CV subido con éxito a BuscoJobs")

    except TimeoutException as e:
        spinner.stop_error("Timeout: No se encontró algún elemento a tiempo.")
        print(e)
    except NoSuchElementException as e:
        spinner.stop_error("No se encontró un elemento esperado en el DOM.")
        print(e)
    except Exception as e:
        spinner.stop_error(f"Error inesperado en BuscoJobs: {e}")
