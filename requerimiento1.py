from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Configurar Chrome para descargas automáticas
download_path = "D:\\WorkSpaceVisualStudio\\Algoritmos\\automatizao"


options = webdriver.ChromeOptions()
# Habilitar descargas automáticas
prefs = {
    "download.default_directory": download_path,
    "profile.default_content_setting_values.automatic_downloads": 1,  # Permite descargas automáticas
    "download.prompt_for_download": False,  # No preguntar por ubicación de descarga
    "download.directory_upgrade": True,  # Permitir cambios en el directorio de descarga
    "safebrowsing.enabled": True  # Evita advertencias de descargas inseguras
}

options.add_experimental_option("prefs", prefs)

# Iniciar el navegador con las opciones configuradas
driver = webdriver.Chrome(options=options)
driver.get("https://ieeexplore.ieee.org")  # Asegúrate de poner la URL correcta

# Abrir la página de la biblioteca
driver.get("https://library.uniquindio.edu.co/")

# Esperar y hacer clic en 'BASES DATOS x FACULTAD'
wait = WebDriverWait(driver, 10)
bases_facultad_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'BASES DATOS x FACULTAD')]")))
bases_facultad_button.click()
print("Se hizo clic en 'BASES DATOS x FACULTAD'.")

# Esperar a que desaparezca el div de carga
wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "onload-background")))

# Clic en 'Fac. Ingeniería'
fac_ingenieria_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//summary[@role='button'][.//div[@data-content-listing-item='fac-ingenier-a']]")))
driver.execute_script("arguments[0].click();", fac_ingenieria_button)
print("Se desplegaron las bases de datos de 'Fac. Ingeniería'.")

# Obtener todos los enlaces de bases de datos
database_links = driver.find_elements(By.XPATH, "//h3[@class='result-title']/a")

# Buscar el enlace de ScienceDirect
sciencedirect_link = None
for link in database_links:
    if "sciencedirect.com" in link.get_attribute("href").lower():
        sciencedirect_link = link
        break

# Si se encuentra el enlace, hacer clic en él
if sciencedirect_link:
    driver.execute_script("arguments[0].click();", sciencedirect_link)
    print("Se hizo clic en 'SCIENCEDIRECT - Consorcio Colombia'.")
else:
    print("No se encontró el enlace de ScienceDirect.")
    driver.quit()
    exit()

# Esperar a que cargue la página de inicio de sesión de Google
time.sleep(3)

# Intentar hacer clic en "Acceder con Google"
try:
    google_button = driver.find_element(By.ID, "btn-google")
    google_button.click()
    print("Botón de Google presionado correctamente.")
except Exception as e:
    print("Error al hacer clic en el botón:", e)
    driver.quit()
    exit()

# Esperar a que aparezca el campo del correo
time.sleep(3)

# Ingresar el correo electrónico
try:
    email_input = driver.find_element(By.ID, "identifierId")
    email_input.send_keys("orlando.diazr@uqvirtual.edu.co")  # Reemplaza con tu correo
    email_input.send_keys(Keys.ENTER)
    print("Correo ingresado correctamente.")
except Exception as e:
    print("Error al ingresar el correo:", e)
    driver.quit()
    exit()

# Esperar a que aparezca el campo de la contraseña
time.sleep(3)

# Ingresar la contraseña
try:
    password_input = driver.find_element(By.NAME, "Passwd")
    password_input.send_keys("JUNIORDIAZ")  # Reemplaza con tu contraseña
    password_input.send_keys(Keys.ENTER)
    print("Contraseña ingresada correctamente.")
except Exception as e:
    print("Error al ingresar la contraseña:", e)
    driver.quit()
    exit()

# Esperar a que cargue ScienceDirect después del login
time.sleep(5)

# BUSCAR "Computational Thinking" con comillas para filtrar resultados
try:
    search_box = wait.until(EC.presence_of_element_located((By.ID, "qs")))
    search_box.send_keys('"Computational Thinking"')  # Agregar comillas para búsqueda exacta
    search_box.send_keys(Keys.ENTER)
    print("Búsqueda realizada correctamente.")
except Exception as e:
    print("No se pudo ingresar la búsqueda:", e)
    driver.quit()
    exit()

# Esperar a que aparezcan los resultados
time.sleep(5)

# ===== PRIMER PASO: SELECCIONAR '100' RESULTADOS POR PÁGINA =====
try:
    boton_100 = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//ol[contains(@class, 'ResultsPerPage')]//a[contains(@data-aa-name, 'srp-100-results-per-page')]")
    ))
    driver.execute_script("arguments[0].scrollIntoView();", boton_100)
    driver.execute_script("arguments[0].click();", boton_100)
    print("Se hizo clic en el botón '100'.")
except Exception as e:
    print("No se pudo hacer clic en el botón '100':", e)

time.sleep(3)  # Esperar a que la página se actualice

# ===== FUNCIÓN PARA PROCESAR UNA PÁGINA =====
def procesar_pagina():
    try:
        time.sleep(3)  # Esperar carga

        # SELECCIONAR TODOS LOS ARTÍCULOS
        select_all_checkbox = wait.until(EC.presence_of_element_located((By.ID, "select-all-results")))
        driver.execute_script("arguments[0].click();", select_all_checkbox)
        print("Se seleccionaron todos los artículos.")

        # EXPORTAR LOS ARTÍCULOS
        export_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'export-all-link-button')]")
        ))
        driver.execute_script("arguments[0].click();", export_button)
        print(" Se hizo clic en el botón de exportar.")

        # EXPORTAR A BIBTEX
        time.sleep(2)
        bibtex_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(text(), 'Export citation to BibTeX')]")
        ))
        driver.execute_script("arguments[0].click();", bibtex_button)
        print("Se hizo clic en 'Export Citation to BibTeX'.")

        # VERIFICAR DESCARGA
        download_path = "D:\\WorkSpaceVisualStudio\\Algoritmos\\automatizao"
        file_name = "sciencedirect_export.bib"
        file_path = os.path.join(download_path, file_name)

        time.sleep(5)  # Esperar descarga
        if os.path.exists(file_path):
            print(f"Archivo descargado correctamente: {file_path}")
        else:
            print("No se encontró el archivo descargado.")

        # ===== CERRAR EL POPUP DESPUÉS DE LA DESCARGA =====
        try:
            close_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//i[contains(@class, 'fa-times')]")
            ))
            driver.execute_script("arguments[0].click();", close_button)
            print("Se cerró la ventana emergente.")
            time.sleep(2)  # Pequeña pausa antes de continuar
        except:
            print("No se encontró el botón para cerrar el popup.")

    except Exception as e:
        print("Error al procesar la página:", e)

# ===== BUCLE PARA REPETIR EL PROCESO EN CADA PÁGINA =====
while True:
    procesar_pagina()

    # PASAR A LA SIGUIENTE PÁGINA SI EXISTE
    try:
        next_button = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//span[contains(@class, 'anchor-text') and text()='next']")
        ))
        driver.execute_script("arguments[0].scrollIntoView();", next_button)
        driver.execute_script("arguments[0].click();", next_button)
        print("Avanzando a la siguiente página...")

        time.sleep(3)  # Esperar carga

        # DESELECCIONAR TODO AL CARGAR LA NUEVA PÁGINA
        select_all_checkbox = wait.until(EC.presence_of_element_located((By.ID, "select-all-results")))
        driver.execute_script("arguments[0].click();", select_all_checkbox)
        print("Se deseleccionaron los artículos de la nueva página.")

        time.sleep(2)

    except:
        print("No hay más páginas. Finalizando el script.")
        break  # Salir del bucle si no hay más páginas


    #----------------------------------------

# VOLVER AL MENÚ DE BASES DE DATOS

try:
    print("Regresando a la página de la biblioteca...")
    driver.get("https://library.uniquindio.edu.co/")

    # Esperar y hacer clic en 'BASES DATOS x FACULTAD' de nuevo
    bases_facultad_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'BASES DATOS x FACULTAD')]")))
    bases_facultad_button.click()
    print("Se volvió a hacer clic en 'BASES DATOS x FACULTAD'.")
    
    # Esperar a que desaparezca el div de carga
    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "onload-background")))

    # Clic en 'Fac. Ingeniería' nuevamente
    fac_ingenieria_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//summary[@role='button'][.//div[@data-content-listing-item='fac-ingenier-a']]")))
    driver.execute_script("arguments[0].click();", fac_ingenieria_button)
    print("Se volvió a desplegar las bases de datos de 'Fac. Ingeniería'.")

except Exception as e:
    print(f"Error al regresar al menú de bases de datos: {e}")

# Obtener todos los enlaces de bases de datos
database_links = driver.find_elements(By.XPATH, "//h3[@class='result-title']/a")

# Buscar el enlace de IEEE Xplore
ieee_link = None
for link in database_links:
    if "ieeexplore" in link.get_attribute("href").lower():
        ieee_link = link
        break

# Si se encuentra el enlace, hacer clic en él
if ieee_link:
    driver.execute_script("arguments[0].click();", ieee_link)
    print("Se hizo clic en 'IEEE Xplore'.")
else:
    print("No se encontró el enlace de IEEE Xplore.")
    driver.quit()
    exit()

# Esperar unos segundos para que cargue la página
time.sleep(3)

# Esperar a que la barra de búsqueda esté visible
search_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input.Typeahead-input"))
)

# Ingresar el término de búsqueda
search_input.send_keys('"Computational Thinking"') 
print("Término de búsqueda ingresado correctamente.")

# Esperar un momento y hacer clic en el botón de búsqueda
time.sleep(1)
search_button = driver.find_element(By.CSS_SELECTOR, "button.fa-search")
search_button.click()
print("Búsqueda realizada correctamente.")

# Esperar unos segundos para que carguen los resultados
time.sleep(3)

while True:
    try:
        # Esperar a que aparezca la casilla de "Select All on Page"
        select_all_checkbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.results-actions-selectall-checkbox"))
        )

        # Verificar si la casilla ya está marcada antes de hacer clic
        if not select_all_checkbox.is_selected():
            driver.execute_script("arguments[0].click();", select_all_checkbox)
            print("Se seleccionaron todos los artículos.")
        else:
            print("Los artículos ya estaban seleccionados.")

        # Esperar a que el botón "Export" esté presente y sea interactuable
        export_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Export')]"))
        )
        driver.execute_script("arguments[0].click();", export_button)
        print("Se hizo clic en el botón de Export.")

        # Esperar a que el botón "Citations" esté presente y sea interactuable
        citations_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Citations')]"))
        )
        driver.execute_script("arguments[0].click();", citations_button)
        print("Se hizo clic en el botón de Citations.")

        # Esperar a que el input de BibTeX esté presente
        bibtex_radio = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//label[@for='download-bibtex']/input[@type='radio']"))
        )

        driver.execute_script("arguments[0].scrollIntoView(true);", bibtex_radio)
        time.sleep(1)  # Espera breve

        driver.execute_script("arguments[0].click();", bibtex_radio)
        print("Se seleccionó el formato BibTeX correctamente.")

        time.sleep(2)

        # Esperar a que el botón "Download" esté presente y sea clickeable
        download_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'stats-SearchResults_Citation_Download')]"))
        )

        time.sleep(2)  # Ajustar tiempo si es necesario
        driver.execute_script("arguments[0].click();", download_button)
        print("Se hizo clic en el botón 'Download'.")

        time.sleep(2)

        # Intentar cerrar el cuadro de diálogo presionando "Cancel" si aparece
        try:
            cancel_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'stats-download-citations-button-cancel')]"))
            )
            driver.execute_script("arguments[0].click();", cancel_button)
            print("Se hizo clic en el botón 'Cancel'.")
        except Exception:
            print("No se encontró el botón 'Cancel', continuando...")

        # Intentar hacer clic en el botón "Next" para pasar a la siguiente página
        try:
            next_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'stats-Pagination_arrow_next')]"))
            )

            # Verificar que el botón está habilitado antes de hacer clic
            if next_button.is_enabled():
                driver.execute_script("arguments[0].scrollIntoView();", next_button)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", next_button)
                print("Avanzando a la siguiente página...")

                # Esperar que la nueva página cargue completamente
                time.sleep(5)
            else:
                print("El botón 'Next' está deshabilitado. Finalizando el proceso.")
                break

        except Exception:
            print("No se encontró el botón 'Next'. Terminando...")
            break

    except Exception as e:
        print("Error general en el proceso:", e)
        break  # Salir del bucle si ocurre un error crítico

print("Descarga completada.")

# Cerrar el navegador cuando el usuario lo decida
input("Presiona Enter para cerrar el navegador...")
driver.quit()