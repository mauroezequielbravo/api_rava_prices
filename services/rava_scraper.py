from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd


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

    # # Mostrar las primeras filas del DataFrame
    # print(df.head())

    # print(df.to_dict(orient='records'))  # Convertir a lista de diccionarios
    return df.to_dict(orient='records')  # Convertir a lista de diccionarios
