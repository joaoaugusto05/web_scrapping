# web_scrapping

Projeto de captura automatizada de dados do **JupiterWeb**, sistema oficial de graduação da USP.  
Este projeto foi desenvolvido para a disciplina **Teste e Validação de Software** e tem como objetivo extrair informações detalhadas das disciplinas dos cursos de graduação da USP.

## Descrição

O script realiza scraping da grade curricular e detalhes das disciplinas diretamente do site JupiterWeb, navegando pelas unidades e cursos, coletando informações relevantes como créditos, carga horária, objetivos e programas das disciplinas.

## Tecnologias Utilizadas

- Python 3
- Selenium WebDriver (para automação do navegador)
- BeautifulSoup (para parsing do HTML)

## Como Rodar

No terminal, execute o script principal passando como argumento o número de unidades que deseja processar.

```bash
python3 src/main.py <numero_de_unidades>
