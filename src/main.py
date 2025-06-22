import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from curso import Curso
from disciplina import Disciplina
from unidade import UnidadeUSP
from reader import iniciar_menu_interativo
from bs4 import BeautifulSoup

import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.by import By


def wait_until_not_obstructed(driver, timeout=15):
    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            overlays = driver.find_elements(By.CSS_SELECTOR, ".ui-widget-overlay, .blockOverlay, .modal, .loading")
            if all(not overlay.is_displayed() for overlay in overlays):
                return True
        except StaleElementReferenceException:
            pass
        time.sleep(0.1)
    return False

def safe_click(driver, by, value, timeout=15):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        element.click()

    except ElementClickInterceptedException:
        print("[CARREGANDO] Aguardo o carregamento dos elementos do site.")
        if wait_until_not_obstructed(driver, timeout=timeout):
            element.click()
        else:
            raise

def main():
    parser = argparse.ArgumentParser(description="Extrator de cursos do Júpiter da USP.")
    parser.add_argument("quantidade_unidades", type=int, help="Quantidade de unidades a serem processadas")
    parser.add_argument(
            "--default-timeout",       
            type=float,
            default=0.15,             
            help="Tempo de espera do carregamento (padrão: 0.15 segundos)"
        )
    args = parser.parse_args()
    limite_unidades = args.quantidade_unidades


    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)

    driver.get("https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275")

    WebDriverWait(driver, 15).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, "#comboUnidade option")) > 1
    )

    unidade_select = driver.find_element(By.ID, "comboUnidade")
    unidades = unidade_select.find_elements(By.TAG_NAME, "option")

    unidades_data = {}
    disciplinas_por_codigo = {} 
    unidades_processadas = 0

    for unidade in unidades:
        
        unidade_value = unidade.get_attribute("value")
        unidade_name = unidade.text.strip()

        if not unidade_value:
            continue
        if unidades_processadas >= limite_unidades:
            break

        print(f"[CARREGANDO] Unidade selecionada: {unidade_name}")
        unidade_select = driver.find_element(By.ID, "comboUnidade")
        unidade_select.find_element(By.CSS_SELECTOR, f"option[value='{unidade_value}']").click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "comboCurso")))

        unidade_obj = UnidadeUSP(unidade_name)
        unidades_data[unidade_name] = unidade_obj

        WebDriverWait(driver, 10).until(
            lambda d: len(d.find_elements(By.CSS_SELECTOR, "#comboCurso option")) > 1
        )

        curso_select = driver.find_element(By.ID, "comboCurso")
        cursos_options = curso_select.find_elements(By.TAG_NAME, "option")

        for curso in cursos_options:
            curso_value = curso.get_attribute("value")
            curso_name = curso.text.strip()
            if not curso_value:
                continue

            print(f"[CARREGANDO] → Curso: {curso_name}")
            curso_select = driver.find_element(By.ID, "comboCurso")
            curso_select.find_element(By.CSS_SELECTOR, f"option[value='{curso_value}']").click()

            safe_click(driver, By.ID, "enviar")
            wait_until_not_obstructed(driver)

            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            dialog = soup.select_one("div.ui-dialog[style*='display: block']")
            if dialog:
                try:
                    wait = WebDriverWait(driver, 10)
                    fechar_button = wait.until(EC.element_to_be_clickable(
                        (By.XPATH, "//button[./span[text()='Fechar']]")
                    ))
                    fechar_button.click()
                    print(f"[WARNING] → Sem dados para {curso_name}.")
                    time.sleep(0.5)
                    continue
                except TimeoutException:
                    pass
                
            safe_click(driver, By.ID, "step4-tab")
            
            try:
                duracao_ideal = driver.find_elements(By.CSS_SELECTOR, "span.duridlhab")[1].text.strip()
                duracao_minima = driver.find_element(By.CSS_SELECTOR, "span.durminhab").text.strip()
                duracao_max = driver.find_element(By.CSS_SELECTOR, "span.durmaxhab").text.strip()

                curso_obj = Curso(
                    nome=curso_name,
                    unidade=unidade_name,
                    duracao_ideal=duracao_ideal,
                    duracao_min=duracao_minima,
                    duracao_max=duracao_max
                )
                unidade_obj.cursos.append(curso_obj)
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "gradeCurricular"))
                    )
                except:
                    time.sleep(1)
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "gradeCurricular"))
                    )
                    
                    
                tipo_atual = ""
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#gradeCurricular tr"))
                )

                html_grade = driver.find_element(By.ID, "gradeCurricular").get_attribute("outerHTML")
                soup = BeautifulSoup(html_grade, "html.parser")
                linhas = soup.select("tr")

                for linha in linhas:
                    colunas = linha.find_all("td")

                    if len(colunas) == 1:
                        tipo_atual = colunas[0].get_text(strip=True).lower()

                    elif len(colunas) >= 8 and colunas[0].select_one(".disciplina"):
                        link_element = colunas[0].select_one(".disciplina")
                        codigo = link_element.get_text(strip=True)
                        nome = colunas[1].get_text(strip=True)

                        def col_int(idx):
                            try:
                                return int(colunas[idx].get_text(strip=True))
                            except:
                                return 0

                        creditos_aula = col_int(2)
                        creditos_trabalho = col_int(3)
                        carga_horaria = col_int(4)
                        carga_estagio = col_int(5)
                        carga_praticas = col_int(6)
                        carga_atpa = col_int(7)

                        if codigo not in disciplinas_por_codigo:
                            disciplina_obj = Disciplina(
                                codigo,
                                nome,
                                creditos_aula,
                                creditos_trabalho,
                                carga_horaria,
                                carga_estagio,
                                carga_praticas,
                                carga_atpa
                            )
                            disciplinas_por_codigo[codigo] = disciplina_obj
                        else:
                            disciplina_obj = disciplinas_por_codigo[codigo]

                        if "eletiv" in tipo_atual:
                            curso_obj.optativas_eletivas.append(disciplina_obj)
                        elif "livre" in tipo_atual:
                            curso_obj.optativas_livres.append(disciplina_obj)
                        else:
                            curso_obj.obrigatorias.append(disciplina_obj)
            except Exception as e:
                print(f"[ERRO ao coletar info do curso '{curso_name}' da unidade '{unidade_name}']: {e}")
            safe_click(driver, By.ID, "step1-tab")

        unidades_processadas += 1
        
    iniciar_menu_interativo(unidades_data, disciplinas_por_codigo)
    driver.quit()

if __name__ == "__main__":
    main()
