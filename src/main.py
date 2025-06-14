from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from curso import Curso
from disciplina import Disciplina
from unidade import UnidadeUSP

def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)

    driver.get("https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275")
    time.sleep(2)

    unidade_select = driver.find_element(By.ID, "comboUnidade")
    unidades = unidade_select.find_elements(By.TAG_NAME, "option")

    unidades_data = {}
    cursos_data = {}
    
    for unidade in unidades:
        unidade_value = unidade.get_attribute("value")
        unidade_name = unidade.text.strip()
        if not unidade_value:
            continue

        unidade_select = driver.find_element(By.ID, "comboUnidade")
        unidade_select.find_element(By.CSS_SELECTOR, f"option[value='{unidade_value}']").click()
        time.sleep(1)

        unidade_obj = UnidadeUSP(unidade_name)
        unidades_data[unidade_name] = unidade_obj

        curso_select = driver.find_element(By.ID, "comboCurso")
        cursos_options = curso_select.find_elements(By.TAG_NAME, "option")

        for curso in cursos_options:
            curso_value = curso.get_attribute("value")
            curso_name = curso.text.strip()
            if not curso_value:
                continue

            curso_select = driver.find_element(By.ID, "comboCurso")
            curso_select.find_element(By.CSS_SELECTOR, f"option[value='{curso_value}']").click()
            time.sleep(0.3)

            driver.find_element(By.ID, "enviar").click()
            time.sleep(0.3)
            driver.find_element(By.ID, "step4-tab").click()
            try:
                unidade = driver.find_element(By.CSS_SELECTOR, "span.unidade").text.strip()
                curso = driver.find_element(By.CSS_SELECTOR, "span.curso").text.strip()
                duracao_ideal = driver.find_element(By.CSS_SELECTOR, "span.duridlhab").text.strip()
                duracao_minima = driver.find_element(By.CSS_SELECTOR, "span.durminhab").text.strip()
                duracao_max = driver.find_element(By.CSS_SELECTOR, "span.durmaxhab").text.strip()
                cursos_data[curso_name] = Curso(nome = curso_name, unidade = unidade_name, duracao_ideal = duracao_ideal, duracao_min = duracao_minima, duracao_max = duracao_max)
                print(f"Unidade: {unidade_name}")
                print(f"Curso: {curso_name}")
                print(f"Duração Ideal: {duracao_ideal} semestres")
                print(f"Duração Mínima: {duracao_minima} semestres")
                
                # Aguarda aba carregar
                time.sleep(0.3)

                grade = driver.find_element(By.ID, "gradeCurricular")
                linhas = grade.find_elements(By.TAG_NAME, "tr")

                tipo_atual = ""
                for linha in linhas:
                    colunas = linha.find_elements(By.TAG_NAME, "td")
                    if len(colunas) == 1:
                        tipo_atual = colunas[0].text.strip()
                    elif colunas and colunas[0].find_elements(By.CLASS_NAME, "disciplina"):
                        link = colunas[0].find_element(By.CLASS_NAME, "disciplina")
                        codigo = link.text.strip()
                        nome = colunas[1].text.strip()
                                             
                        driver.execute_script("arguments[0].click();", link)
                        time.sleep(0.3)

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

                        print(codigo)
                
            except Exception as e:
                print(f"[Erro ao coletar info do curso]: {e}")

            fechar_botao = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.ui-dialog-titlebar-close"))
            )
            fechar_botao.click()
            driver.find_element(By.ID, "step1-tab").click()
            time.sleep(1)

    driver.quit()

if __name__ == "__main__":
    main()
