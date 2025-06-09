#!/usr/bin/env python3

import time
import random
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def escribir_como_humano(elemento, texto):
    for caracter in texto:
        elemento.send_keys(caracter)
        time.sleep(random.uniform(0.05, 0.2))  # Pausa rápida entre teclas

def actualizar_cv(navegador, email, password, path_cv):
    wait = WebDriverWait(navegador, 15)
    
    try:
        navegador.get("https://ar.jooble.org")
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Iniciar sesión']]"))).click()
        
        except TimeoutException:
            # Esperamos que esté presente el botón (no importa si habilitado o no)
            boton_menu = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-test-name="_hamburgerMenuButton"]')))
            
            # Forzamos el click por si no responde bien
            navegador.execute_script("arguments[0].click();", boton_menu)
            
            # Esperamos a que realmente se abra (aria-expanded="true")
            wait.until(lambda driver: driver.find_element(By.CSS_SELECTOR, 'button[data-test-name="_hamburgerMenuButton"]').get_attribute("aria-expanded") == "true")

            boton_iniciar_sesion = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test-name="_hamburgerLogin"]')))
            boton_iniciar_sesion.click()


        #WebDriverWait(navegador, 10).until(EC.url_contains("jooble.org/auth/login/email"))
        
        email_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="email"]')))
        time.sleep(random.uniform(0.5, 1.5))
        escribir_como_humano(email_input, email)
        time.sleep(random.uniform(0.5, 1.5))
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Continuar']]"))).click()

        password_input = wait.until(EC.presence_of_element_located((By.ID, "input_:r0:")))
        escribir_como_humano(password_input, password)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Iniciar sesión']]"))).click()
        
        navegador.get("https://ar.jooble.org/CV/Manage")

        wait.until(EC.element_to_be_clickable((By.ID, "downloadCvFile"))).click()
        
        input_cv.send_keys(path_cv)

        
        time.sleep(2) 
        
        # Por ejemplo, podemos verificar si el botón "Subir archivo" ya no está disponible
        #wait.until(EC.invisibility_of_element_located((By.NAME, "archivo")))
        print("[+] CV subido con éxito a Jooble\n")
        
    except TimeoutException as e:
        print("[!] Timeout: No se encontró algún elemento a tiempo.")
        print(e)
    except NoSuchElementException as e:
        print("[!] No se encontró un elemento esperado en el DOM.")
        print(e)
    except Exception as e:
        print(f"[!] Error inesperado en Jooble: {e}")
