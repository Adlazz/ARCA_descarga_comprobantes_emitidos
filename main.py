from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import os
import keyboard
from datetime import datetime

def get_random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15'
    ]
    return random.choice(user_agents)

def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%d/%m/%Y')
        return True
    except ValueError:
        return False

def get_valid_date(prompt):
    while True:
        date_str = input(prompt)
        if validate_date(date_str):
            return date_str
        print("Formato de fecha inválido. Por favor, use el formato DD/MM/YYYY")

def login_afip(cuit, password, fecha_desde, fecha_hasta):
    options = webdriver.ChromeOptions()
    user_agent = get_random_user_agent()
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    time.sleep(random.uniform(1, 3))
    
    try:
        driver.get("https://auth.afip.gob.ar/contribuyente_/login.xhtml")
        wait = WebDriverWait(driver, 10)

        # Ingresa el CUIT
        text_box = wait.until(EC.presence_of_element_located((By.ID, "F1:username")))
        text_box.clear()
        text_box.send_keys(cuit)
        print(f"CUIT ingresado: {cuit}")

        # Hace clic en el botón "Siguiente"
        siguiente_button = wait.until(EC.element_to_be_clickable((By.ID, "F1:btnSiguiente")))
        siguiente_button.click()
        print("Se hizo clic en el botón Siguiente")

        # Ingresa la contraseña
        password_field = wait.until(EC.presence_of_element_located((By.ID, "F1:password")))
        password_field.send_keys(password)
        print("Contraseña ingresada")

        # Hace clic en el botón "Ingresar"
        ingresar_button = wait.until(EC.element_to_be_clickable((By.ID, "F1:btnIngresar")))
        ingresar_button.click()
        print("Se hizo clic en el botón Ingresar")

        time.sleep(5)

        # Hace clic en "Ver Todos" en la página principal
        mis_comprobantes = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Ver todos")))
        mis_comprobantes.click()
        print("Se encontró y abrió 'Ver todos'")

        # Hacer clic en "Mis Comprobantes"
        comprobantes_link = wait.until(EC.presence_of_element_located((By.XPATH, "//h3[contains(text(),'MIS COMPROBANTES')]")))
        
        driver.execute_script("arguments[0].scrollIntoView(true);", comprobantes_link)
        time.sleep(1)
      
        try:
            comprobantes_link.click()
            print("Se hizo clic en Mis Comprobantes")
        except Exception as e:
            driver.execute_script("arguments[0].click();", comprobantes_link)
            print("Se hizo clic en Mis Comprobantes usando JavaScript")

        time.sleep(5)

        # Cambiar a la nueva pestaña
        handles = driver.window_handles
        driver.switch_to.window(handles[-1])
        print("Cambiado a la nueva pestaña")

        # Hacer clic en 'Emitidos'
        try:
            emitidos_button = wait.until(EC.element_to_be_clickable((
                By.XPATH, '//*[@id="btnEmitidos"]/div[2]/h3'
            )))
            
            driver.execute_script("arguments[0].scrollIntoView(true);", emitidos_button)
            time.sleep(1)
            
            try:
                emitidos_button.click()
                print("Se hizo clic en 'Emitidos'")
            except Exception as e:
                driver.execute_script("arguments[0].click();", emitidos_button)
                print("Se hizo clic en 'Emitidos' usando JavaScript")
                
            time.sleep(2)
                 
        except Exception as e:
            print(f"Error al hacer clic en 'Emitidos': {str(e)}")
            driver.save_screenshot("error_emitidos.png")

        # Manejar el campo de fecha
        try:
            fecha_input = wait.until(EC.presence_of_element_located((
                By.ID, "fechaEmision"
            )))
            
            driver.execute_script("arguments[0].value = '';", fecha_input)
            time.sleep(0.5)
            
            rango_fechas = f"{fecha_desde} - {fecha_hasta}"
            fecha_input.send_keys(rango_fechas)
            print(f"Se ingresó el rango de fechas: {rango_fechas}")
            
            valor_actual = fecha_input.get_attribute('value')
            if valor_actual == rango_fechas:
                print("Fechas ingresadas correctamente")
            else:
                print(f"Advertencia: El valor actual ({valor_actual}) no coincide con el esperado")
               
        except Exception as e:
            print(f"Error al manipular el campo de fecha: {str(e)}")
            driver.save_screenshot("error_fecha.png")

        # Hacer clic en el botón Buscar
        try:
            buscar_button = wait.until(EC.presence_of_element_located((
                By.ID, "buscarComprobantes"
            )))
            
            driver.execute_script("arguments[0].scrollIntoView(true);", buscar_button)
            time.sleep(1)
            
            try:
                buscar_button.click()
                print("Se hizo clic en el botón Buscar")
            except Exception as e:
                driver.execute_script("arguments[0].click();", buscar_button)
                print("Se hizo clic en el botón Buscar usando JavaScript")
            
            time.sleep(2)
            
        except Exception as e:
            print(f"Error al hacer clic en el botón Buscar: {str(e)}")
            driver.save_screenshot("error_buscar.png")

        # Descargar y procesar el CSV
        try:
            print("Esperando a que carguen los resultados...")
            time.sleep(3)

            # Esperar y hacer clic en el botón CSV
            excel_button = wait.until(EC.element_to_be_clickable((
                By.XPATH, '//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/button[1]/span'
            )))
            
            # Scroll hasta el botón CSV
            driver.execute_script("arguments[0].scrollIntoView(true);", excel_button)
            time.sleep(1)
            
            try:
                excel_button.click()
                print("Se hizo clic en el botón CSV")
                time.sleep(2)
                print("Archivo excel descargado")  

            except Exception as e:
                driver.execute_script("arguments[0].click();", excel_button)
                print("Se hizo clic en el botón CSV usando JavaScript")
                print("Archivo excel descargado")  
                time.sleep(2)
                
        except Exception as e:
            print(f"Error al intentar descargar/procesar el Excel: {str(e)}")
            driver.save_screenshot("error_excel.png")

        print("\nMantén la sesión abierta, presiona 'Esc' para cerrar.")
        while True:
            if keyboard.is_pressed('esc'):
                print("Tecla 'Esc' presionada. Cerrando sesión.")
                break

    except Exception as e:
        driver.save_screenshot(f"afip_login_error_{cuit}.png")
        print(f"Error durante el login: {str(e)}")
        return None

    finally:
        driver.quit()
        print("Sesión cerrada.")

# Ejemplo de uso
if __name__ == "__main__":
    cuit = "tu-cuit-aqui"
    password = "tu-contraseña-aqui"
    
    print("Por favor, ingrese el rango de fechas (formato DD/MM/YYYY)")
    fecha_desde = get_valid_date("Fecha desde: ")
    fecha_hasta = get_valid_date("Fecha hasta: ")
    
    login_afip(cuit, password, fecha_desde, fecha_hasta)