from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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
        # Navegar a la página de cotizaciones
        driver.get("https://www.rava.com/cotizaciones/acciones-argentinas")
        time.sleep(5)  # Esperar a que la página cargue completamente

        # Obtener todas las tablas de cotizaciones
        tables = driver.find_elements(By.CSS_SELECTOR, "div.rava-box-shadow.table-a")

        # Verificar que se encontraron las tablas
        if len(tables) >= 2:
            # Extraer HTML de las tablas
            html_lider = tables[0].get_attribute('outerHTML')
            html_general = tables[1].get_attribute('outerHTML')

            # Convertir HTML a DataFrame
            df_lider = pd.read_html(html_lider)[0]
            df_general = pd.read_html(html_general)[0]

            df_todo = pd.concat([df_lider, df_general], ignore_index=True)
            return df_todo.to_dict(orient='records')
        else:
            print("No se encontraron las tablas esperadas.")
    finally:
        # Cerrar el navegador
        driver.quit()   


