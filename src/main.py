import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from curso import Curso
from disciplina import Disciplina
from unidade import UnidadeUSP
#from utils import exportar_para_json
from reader import iniciar_menu_interativo
from bs4 import BeautifulSoup

import time
def main():
    parser = argparse.ArgumentParser(description="Extrator de cursos do Júpiter da USP.")
    parser.add_argument("quantidade_unidades", type=int, help="Quantidade de unidades a serem processadas")
    args = parser.parse_args()
    limite_unidades = args.quantidade_unidades

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
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

        print(f"[DEBUG] Unidade selecionada: {unidade_name}")
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

            print(f"[DEBUG] → Curso: {curso_name}")
            curso_select = driver.find_element(By.ID, "comboCurso")
            curso_select.find_element(By.CSS_SELECTOR, f"option[value='{curso_value}']").click()

            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "enviar"))).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "step4-tab"))).click()
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

                    elif colunas and colunas[0].select_one(".disciplina"):
                        link_element = colunas[0].select_one(".disciplina")
                        codigo = link_element.get_text(strip=True)
                        nome = colunas[1].get_text(strip=True)

                        selenium_link = driver.find_element(By.LINK_TEXT, codigo)
                        driver.execute_script("arguments[0].click();", selenium_link)
                        try:
                            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "disciplinaDialog")))
                        except:
                            print(f"[ERRO] Disciplina inválida ou não ativada: {codigo} - {nome}")
                            fechar_erro = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Fechar']]")))
                            fechar_erro.click()
                            driver.execute_script("""document.querySelectorAll('.blockUI, .blockOverlay, .blockMsg').forEach(el => el.remove());""")
                            continue
                        dialog = driver.find_element(By.ID, "disciplinaDialog")

                        def safe_text(cls):
                            try:
                                return dialog.find_element(By.CLASS_NAME, cls).text.strip()
                            except:
                                return ""

                        creditos_aula = int(safe_text("creditosAula") or 0)
                        creditos_trabalho = int(safe_text("creditosTrabalho") or 0)
                        carga_horaria = safe_text("cargaHorariaTotal")
                        objetivos = safe_text("objetivos")
                        programa = safe_text("programa")

                        if codigo not in disciplinas_por_codigo:
                            disciplina_obj = Disciplina(codigo, nome, creditos_aula, creditos_trabalho, carga_horaria, objetivos, programa)
                            disciplinas_por_codigo[codigo] = disciplina_obj
                        else:
                            disciplina_obj = disciplinas_por_codigo[codigo]

                        if "eletiv" in tipo_atual:
                            curso_obj.optativas_eletivas.append(disciplina_obj)
                        elif "livre" in tipo_atual:
                            curso_obj.optativas_livres.append(disciplina_obj)
                        else:
                            curso_obj.obrigatorias.append(disciplina_obj)

                        print(f"    → {disciplina_obj}")

                        fechar_botao = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.ui-dialog-titlebar-close"))
                        )
                        fechar_botao.click()

            except Exception as e:
                print(f"[ERRO ao coletar info do curso '{curso_name}' da unidade '{unidade_name}']: {e}")
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "step1-tab"))).click()

        unidades_processadas += 1

    # print("\n✅ Finalizou com sucesso.")
    # print("\n🧪 Teste de estrutura de dados:")
    # for unidade_nome, unidade in unidades_data.items():
    #     print(f"\n📚 Unidade: {unidade.nome}")
    #     for curso in unidade.cursos:
    #         print(f"  🎓 Curso: {curso.nome}")
    #         print(f"    - Duração: ideal {curso.duracao_ideal}, min {curso.duracao_min}, max {curso.duracao_max}")
    #         print(f"    - Disciplinas obrigatórias: {len(curso.obrigatorias)}")
    #         print(f"    - Disciplinas optativas eletivas: {len(curso.optativas_eletivas)}")
    #         print(f"    - Disciplinas optativas livres: {len(curso.optativas_livres)}")

    #         for d in curso.obrigatorias:
    #             print(f"      → [OB] {d}")

    #         for d in curso.optativas_eletivas:
    #             print(f"      → [EL] {d}")

    #         for d in curso.optativas_livres:
    #             print(f"      → [LV] {d}")
    
    #exportar_para_json(unidades_data)
    iniciar_menu_interativo(unidades_data, disciplinas_por_codigo)
    driver.quit()

if __name__ == "__main__":
    main()
