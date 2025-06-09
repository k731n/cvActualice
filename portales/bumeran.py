#!/usr/bin/env python3

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
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
    navegador.get("https://www.bumeran.com.ar/login?returnTo=/")
    wait = WebDriverWait(navegador, 10)

    wait.until(EC.presence_of_element_located((By.ID, "email"))).send_keys(email)
    navegador.find_element(By.ID, "password").send_keys(password)
    navegador.find_element(By.ID, "ingresar").click()
    
    WebDriverWait(navegador, 10).until_not(
        EC.presence_of_element_located((By.ID, "email"))
    )

    navegador.get("https://www.bumeran.com.ar/postulantes/curriculum")

    try:
        borrar_elemento = WebDriverWait(navegador, 1.5).until(
            EC.element_to_be_clickable((By.ID, "archivo-adjunto-borrar"))
        )
        
        borrar_elemento.click()
        navegador.execute_script("""
            var elemento = document.getElementById('objetivo');
            if (elemento) {
                elemento.style.display = 'none';
            }
        """)
        eliminar_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Eliminar']")))
        eliminar_btn.click()

    except TimeoutException:
        pass

    # Hacer clic en el botón 'Subir CV'
#    navegador.find_element(By.XPATH, "//button[contains(., 'Subir CV')]").click()
    #time.sleep(1)

    # Esperar a que aparezca el input de tipo file
    try:
        # Buscar directamente el input de tipo file
        input_cv = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.ID, "archivo-selector"))
        )

        # Asegurarse de que el input esté visible (si está oculto)
        navegador.execute_script("arguments[0].style.display = 'block';", input_cv)

        # Enviar el archivo al input de tipo file
        input_cv.send_keys(path_cv)
        time.sleep(2)  # Esperar que el sistema cargue el archivo

        # Verificar si apareció el botón de borrar como confirmación
        try:
            navegador.find_element(By.ID, "archivo-adjunto-borrar")
            spinner.stop("CV subido con éxito a Bumeran")
        except NoSuchElementException:
            spinner.stop_error("Error: El CV no se subió correctamente en Bumeran.")

    except TimeoutException:
        print("No se encontró el input de archivo a tiempo")

