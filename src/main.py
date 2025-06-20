import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from curso import Curso
from disciplina import Disciplina
from unidade import UnidadeUSP

def main():
    parser = argparse.ArgumentParser(description="Extrator de cursos do Júpiter da USP.")
    parser.add_argument("quantidade_unidades", type=int, help="Quantidade de unidades a serem processadas")
    args = parser.parse_args()
    limite_unidades = args.quantidade_unidades

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
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
    cursos_data = {}
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

        # Aguarda até que os cursos estejam carregados (pelo menos 2 opções)
        WebDriverWait(driver, 10).until(
            lambda d: len(d.find_elements(By.CSS_SELECTOR, "#comboCurso option")) > 1
        )

        curso_select = driver.find_element(By.ID, "comboCurso")
        cursos_options = curso_select.find_elements(By.TAG_NAME, "option")

        print(f"[DEBUG] Cursos encontrados na unidade '{unidade_name}': {len(cursos_options)}")
        for i, opt in enumerate(cursos_options):
            value = opt.get_attribute("value")
            text = opt.text.strip()
            print(f"  ↪ [{i}] value='{value}' | text='{text}'")


        for curso in cursos_options:
            curso_value = curso.get_attribute("value")
            curso_name = curso.text.strip()
            if not curso_value:
                continue

            print(f"[DEBUG] → Curso: {curso_name}")

            curso_select = driver.find_element(By.ID, "comboCurso")
            curso_select.find_element(By.CSS_SELECTOR, f"option[value='{curso_value}']").click()

            selected = driver.find_element(By.ID, "comboCurso").get_attribute("value")
            print(f"[DEBUG] Valor selecionado no comboCurso: {selected}")

            print("[DEBUG] Clicando em 'Buscar'...")
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "enviar"))).click()

            print("[DEBUG] Clicando na aba 'Grade Curricular'...")
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "step4-tab"))).click()

            try:
                duracao_ideal = driver.find_element(By.CSS_SELECTOR, "span.duridlhab").text.strip()
                duracao_minima = driver.find_element(By.CSS_SELECTOR, "span.durminhab").text.strip()
                duracao_max = driver.find_element(By.CSS_SELECTOR, "span.durmaxhab").text.strip()
                cursos_data[curso_name] = Curso(
                    nome=curso_name,
                    unidade=unidade_name,
                    duracao_ideal=duracao_ideal,
                    duracao_min=duracao_minima,
                    duracao_max=duracao_max
                )
                print(f"\n🎓 Curso: {curso_name} ({unidade_name})")
                print(f"  - Duração Ideal: {duracao_ideal} semestres")
                print(f"  - Duração Mínima: {duracao_minima} semestres")

                grade = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "gradeCurricular"))
                )

                tipo_atual = ""
                linhas = grade.find_elements(By.TAG_NAME, "tr")
                for linha in linhas:
                    colunas = linha.find_elements(By.TAG_NAME, "td")
                    if len(colunas) == 1:
                        tipo_atual = colunas[0].text.strip()
                    elif colunas and colunas[0].find_elements(By.CLASS_NAME, "disciplina"):
                        link = colunas[0].find_element(By.CLASS_NAME, "disciplina")
                        codigo = link.text.strip()
                        nome = colunas[1].text.strip()

                        driver.execute_script("arguments[0].click();", link)
                        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "disciplinaDialog")))

                        dialog = driver.find_element(By.ID, "disciplinaDialog")

                        def safe_text(cls_name):
                            try:
                                return dialog.find_element(By.CLASS_NAME, cls_name).text.strip()
                            except:
                                return ""

                        creditos_aula = int(safe_text("creditosAula") or 0)
                        creditos_trabalho = int(safe_text("creditosTrabalho") or 0)
                        carga_horaria = safe_text("cargaHorariaTotal")
                        modalidade = safe_text("tipo")
                        ativacao = safe_text("ativacao")
                        objetivos = safe_text("objetivos")
                        programa_resumido = safe_text("programaResumido")
                        programa = safe_text("programa")
                        metodo_avaliacao = safe_text("metodoAvaliacao")
                        criterio_avaliacao = safe_text("criterioAvaliacao")

                        docentes_elements = dialog.find_elements(By.CSS_SELECTOR, ".docentesResponsaveis li")
                        docentes = [d.text.strip() for d in docentes_elements]

                        print(f"    ↳ Disciplina: {codigo} - {nome}")

                        fechar_botao = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.ui-dialog-titlebar-close"))
                        )
                        fechar_botao.click()
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "step4-tab"))).click()

            except Exception as e:
                print(f"[ERRO ao coletar info do curso '{curso_name}' da unidade '{unidade_name}']: {e}")

            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "step1-tab"))).click()

        unidades_processadas += 1

    print("\n✅ Finalizou com sucesso.")
    driver.quit()

if __name__ == "__main__":
    main()