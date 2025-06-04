from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time


def get_cedear() -> list:
    # Configurar opciones para Selenium
    options = Options()
    options.add_argument('--headless')  # Ejecutar en modo headless
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    # Inicializar el navegador
    driver = webdriver.Chrome(options=options)

    # Navegar a la página de Rava
    url = 'https://www.rava.com/cotizaciones/cedears'
    driver.get(url)

    # Esperar a que la tabla se cargue
    driver.implicitly_wait(10)  # Esperar hasta 10 segundos

    # Obtener el contenido de la página
    html = driver.page_source

    # Cerrar el navegador
    driver.quit()

    # Parsear el HTML con BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Encontrar la tabla por su ID
    tabla_div = soup.find('div', id='tabla')

    # Extraer las filas de la tabla
    filas = tabla_div.find_all('tr')

    # Procesar las filas y extraer los datos
    datos = []
    for fila in filas:
        columnas = fila.find_all(['th', 'td'])
        datos.append([columna.get_text(strip=True) for columna in columnas])

    # Crear un DataFrame de pandas
    df = pd.DataFrame(datos, columns=[
        'especie', 'ultimo_precio', 'porcentaje_diario', 'porcentaje_mes', 'porcentaje_anio', 
        'precio_anterior', 'precio_apertura', 'precio_minimo', 'precio_maximo', 'hora', 'vol_nominal', 
        'vol_efectivo', 'ratio', 'ccl'
    ])  # Saltar la primera fila si es el encabezado

    df = df.iloc[1:].reset_index(drop=True)  # Eliminar la primera fila si es el encabezado

    df = df.applymap(lambda x: x.replace('.', '').replace(',', '.') if isinstance(x, str) else x)  # Reemplazar puntos y comas
    df = df.applymap(lambda x: float(x) if isinstance(x, str) and x.replace('.', '', 1).isdigit() else x)  # Convertir a float

    # remplaza los guiones por none
    df = df.replace('-', None)

    # # Mostrar las primeras filas del DataFrame
    # print(df.head())

    # print(df.to_dict(orient='records'))  # Convertir a lista de diccionarios
    return df.to_dict(orient='records')  # Convertir a lista de diccionarios


def get_bonos() -> list:
    # Configurar opciones para Selenium
    options = Options()
    options.add_argument('--headless')  # Ejecutar en modo headless
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    # Inicializar el navegador
    driver = webdriver.Chrome(options=options)

    # Navegar a la página de Rava
    url = 'https://www.rava.com/cotizaciones/bonos'
    driver.get(url)

    # Esperar a que la tabla se cargue
    driver.implicitly_wait(10)  # Esperar hasta 10 segundos

    # Obtener el contenido de la página
    html = driver.page_source

    # Cerrar el navegador
    driver.quit()

    # Parsear el HTML con BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Encontrar la tabla por su ID
    tabla_div = soup.find('div', id='tabla')

    # Extraer las filas de la tabla
    filas = tabla_div.find_all('tr')

    # Procesar las filas y extraer los datos
    datos = []
    for fila in filas:
        columnas = fila.find_all(['th', 'td'])
        datos.append([columna.get_text(strip=True) for columna in columnas])

    # Crear un DataFrame de pandas
    df = pd.DataFrame(datos, columns=[
        'especie', 'ultimo_precio', 'porcentaje_diario', 'porcentaje_mes', 'porcentaje_anio', 
        'precio_anterior', 'precio_apertura', 'precio_minimo', 'precio_maximo', 'hora', 'vol_nominal', 
        'vol_efectivo'
    ])  # Saltar la primera fila si es el encabezado

    df = df.iloc[1:].reset_index(drop=True)  # Eliminar la primera fila si es el encabezado

    df = df.applymap(lambda x: x.replace('.', '').replace(',', '.') if isinstance(x, str) else x)  # Reemplazar puntos y comas
    df = df.applymap(lambda x: float(x) if isinstance(x, str) and x.replace('.', '', 1).isdigit() else x)  # Convertir a float

    # remplaza los guiones por none
    df = df.replace('-', None)

    # # Mostrar las primeras filas del DataFrame
    # print(df.head())

    # print(df.to_dict(orient='records'))  # Convertir a lista de diccionarios
    return df.to_dict(orient='records')  # Convertir a lista de diccionarios


def get_acciones() -> list:
    # Configurar opciones para Chrome en modo headless
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Inicializar el driver de Chrome
    driver = webdriver.Chrome(options=options)

    try:
        # Ir a la página
        driver.get("https://www.rava.com/cotizaciones/acciones-argentinas")

        # Esperar a que se cargue la primera tabla
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "tabla"))
        )

        # Obtener HTML de la tabla inicial (Panel Líder)
        tabla_lider = driver.find_element(By.ID, "tabla")
        html_lider = tabla_lider.get_attribute('outerHTML')
        df_lider = pd.read_html(html_lider)[0]

        df_lider.columns = [
            'especie', 'ultimo_precio', 'porcentaje_diario', 'porcentaje_mes', 'porcentaje_anio', 
            'precio_anterior', 'precio_apertura', 'precio_minimo', 'precio_maximo', 'hora', 'vol_nominal', 
            'vol_efectivo'
        ]

        # df_lider = df_lider.iloc[1:].reset_index(drop=True)  # Eliminar la primera fila si es el encabezado
        df_lider = df_lider.applymap(lambda x: x.replace('.', '').replace(',', '.') if isinstance(x, str) else x)  # Reemplazar puntos y comas
        df_lider = df_lider.applymap(lambda x: float(x) if isinstance(x, str) and x.replace('.', '', 1).isdigit() else x)  # Convertir a float

        # remplaza los guiones por none
        df_lider = df_lider.replace('-', None)

        # Hacer clic en el botón del Panel General
        boton_general_xpath = '//*[@id="tabla"]/div/div/ul/li[2]/a'
        boton_general = driver.find_element(By.XPATH, boton_general_xpath)
        boton_general.click()

        # Esperar a que se cargue la nueva tabla
        # WebDriverWait(driver, 10).until(
        #     EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#tabla .nav-item.active"), "General")
        # )
        time.sleep(2)  # Esperar un poco para que la tabla se cargue completamente

        # Volver a obtener la tabla del Panel General
        tabla_general = driver.find_element(By.ID, "tabla")
        html_general = tabla_general.get_attribute('outerHTML')
        df_general = pd.read_html(html_general)[0]

        df_general.columns = [
            'especie', 'ultimo_precio', 'porcentaje_diario', 'porcentaje_mes', 'porcentaje_anio', 
            'precio_anterior', 'precio_apertura', 'precio_minimo', 'precio_maximo', 'hora', 'vol_nominal', 
            'vol_efectivo'
        ]

        # df_general = df_general.iloc[1:].reset_index(drop=True)  # Eliminar la primera fila si es el encabezado
        df_general = df_general.applymap(lambda x: x.replace('.', '').replace(',', '.') if isinstance(x, str) else x)  # Reemplazar puntos y comas
        df_general = df_general.applymap(lambda x: float(x) if isinstance(x, str) and x.replace('.', '', 1).isdigit() else x)  # Convertir a float

        # remplaza los guiones por none
        df_general = df_general.replace('-', None)

        # Unir los dos DataFrames
        df_total = pd.concat([df_lider, df_general], ignore_index=True)

        return df_total.to_dict(orient='records')  # Convertir a lista de diccionarios
    except Exception as e:
        print(f"Error al obtener las acciones: {e}")
        return []

    finally:
        driver.quit() 


