# web_scrapping

Projeto de captura automatizada de dados do **JupiterWeb**, sistema oficial de graduação da USP.  
Este projeto foi desenvolvido para a disciplina **Teste e Validação de Software** e tem como objetivo extrair informações detalhadas das disciplinas dos cursos de graduação da USP.
Membros: Joao Augusto Fernandes Barbosa (11953348), Daniele, Henrique Carobolante Parro (11917987)
## Descrição

O script realiza scraping da grade curricular e detalhes das disciplinas diretamente do site JupiterWeb, navegando pelas unidades e cursos, coletando informações relevantes como créditos, carga horária, objetivos e programas das disciplinas.

## Tecnologias Utilizadas

- Python 3
- Selenium WebDriver (para automação do navegador)
- BeautifulSoup (para parsing do HTML). O processo foi optimizado usando selenium para interacao com o JS, uma vez que o site não eh estatico e BS4 para parser em dialogs e semelhantes

## Como Rodar

No terminal, execute o script principal passando como argumento o número de unidades que deseja processar.

```bash
python3 src/main.py <numero_de_unidades>
