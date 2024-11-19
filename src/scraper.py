from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def iniciar_sesion(usuario, clave):
    url = 'http://extranet.unsa.edu.pe/sisacad/parciales18/index.php'
    driver = webdriver.Chrome()  # Asegúrate de tener el driver de Chrome instalado y en tu PATH
    driver.get(url)

    # Esperar a que el campo de usuario esté presente
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'usuario')))

    # Ingresar usuario y clave
    driver.find_element(By.NAME, 'usuario').send_keys(usuario)
    driver.find_element(By.NAME, 'clave').send_keys(clave)

    # Resolver el captcha manualmente
    print("Por favor, resuelve el captcha manualmente y presiona Enter...")
    input()

    # Enviar el formulario
    driver.find_element(By.NAME, 'consulta').submit()

    # Esperar a que la tabla de resultados esté presente
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'resul_tab')))

    # Obtener el HTML de la página
    html = driver.page_source
    driver.quit()
    return html

def obtener_notas(html):
    soup = BeautifulSoup(html, 'html.parser')
    notas = []

    # Ajustar el selector según la estructura HTML de la página
    tabla = soup.find('table', {'id': 'resul_tab'})
    if not tabla:
        print("No se encontró la tabla de resultados.")
        return []

    for row in tabla.find_all('tr')[1:]:  # Omitir la fila de encabezado
        cols = row.find_all('td')
        if len(cols) > 4:  # Asegurarse de que hay suficientes columnas
            asignatura = cols[1].text.strip()
            nota = float(cols[4].text.strip())
            peso = float(cols[5].text.strip().replace('%', '')) / 100
            acumulado = nota * peso
            notas.append({
                'asignatura': asignatura,
                'nota': nota,
                'peso': peso,
                'acumulado': acumulado
            })

    return notas

def agrupar_acumulados(notas):
    acumulados_por_curso = {}
    for nota in notas:
        asignatura = nota['asignatura']
        if asignatura not in acumulados_por_curso:
            acumulados_por_curso[asignatura] = 0
        acumulados_por_curso[asignatura] += nota['acumulado']
    return acumulados_por_curso

def main():
    usuario = input("Ingrese su usuario: ")
    clave = input("Ingrese su clave: ")
    html = iniciar_sesion(usuario, clave)
    if html:
        print("HTML obtenido correctamente.")
    else:
        print("No se pudo obtener el HTML.")
        return

    notas = obtener_notas(html)
    if notas:
        print("Notas y acumulados por curso:")
        print(f"{'Asignatura':<40} {'Acumulado':<10} {'Falta para 10.5':<15} {'Estado':<10}")
        print("="*75)
        acumulados_por_curso = agrupar_acumulados(notas)
        for asignatura, acumulado in acumulados_por_curso.items():
            falta_para_aprobar = max(0, 10.5 - acumulado)
            estado = "Aprobado" if acumulado >= 10.5 else "Desaprobado"
            print(f"{asignatura:<40} {acumulado:<10.2f} {falta_para_aprobar:<15.2f} {estado:<10}")
        total_acumulado = sum(acumulados_por_curso.values())
        print("="*75)
        print(f"{'Total Acumulado':<40} {total_acumulado:<10.2f}")
    else:
        print("No se pudieron obtener las notas.")

if __name__ == "__main__":
    main()