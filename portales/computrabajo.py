#!/usr/bin/env python3

import time
from selenium.webdriver.common.by import By # Para seleccionar elementos (por ID, name, etc.)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import itertools
import threading
import sys

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
    wait = WebDriverWait(navegador, 0.5)

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
                if element.is_displayed():
                    element.clear()
                    element.send_keys(keys)
                    return
            except StaleElementReferenceException:
                time.sleep(1)
        raise Exception(f"No se pudo enviar keys a {locator}")

#    navegador.get("https://ar.computrabajo.com") # Abre la página principal
#    time.sleep(2)

#    navegador.find_element(By.LINK_TEXT, "Login").click() # Hace click en el botón "Ingresar"
#    time.sleep(1)
#    navegador.find_element(By.LINK_TEXT, "Ingresar").click() # Hace click en el botón "Login"
#    time.sleep(2) # Espera 2 segundos para que cargue la página de login
    
    navegador.get("https://candidato.ar.computrabajo.com/acceso/?rfl=641DEC02F5F800F2430E37385F343F6944AD5DB24E78E22C38C9788C9E6224BF&f=FEE939887FF3D46C")
    #time.sleep(3)

    navegador.find_element(By.ID, "Email").send_keys(email)
    #time.sleep(1)
    navegador.find_element(By.ID, "continueWithMailButton").click()
    time.sleep(0.5)

    navegador.find_element(By.ID, "password").send_keys(password) # Escribe la contraseña
    navegador.find_element(By.ID, "btnSubmitPass").click() # Hace click en "Iniciar sesión"
    time.sleep(1) # Espera a que cargue

    navegador.get ("https://candidato.ar.computrabajo.com/candidate/cv/uploadcv") # Va directo a la página para subir el CV
    #time.sleep(3)

# 1. Hacer click en el botón para que cargue todo (por si falta algo dinámico)
 #   boton_subir = navegador.find_element(By.ID, "lnkUploadCv")
 #   boton_subir.click()
 #   time.sleep(2)  # Esperar a que cargue bien el input
    try:
# 2. Encontrar el input oculto
        wait.until(EC.visibility_of_element_located((By.ID, "it-error")))
        spinner.stop_error("Alcanzó el máximo de CVs en Computrabajo. Debe borrar al menos 1 CV")
    except TimeoutException:
        input_cv = navegador.find_element(By.ID, "ContainerGeneralOverWrite_ContainerGeneral_fuUploadCv")

# 3. Hacer visible el input
        navegador.execute_script("arguments[0].style.display = 'block';", input_cv)

# 4. Subir el archivo
        input_cv.send_keys(path_cv)

        spinner.stop("CV subido con éxito a Computrabajo")
