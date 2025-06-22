# web_scrapping

Projeto de captura automatizada de dados do **JupiterWeb**, sistema oficial de graduação da USP.  
Este projeto foi desenvolvido para a disciplina **Teste e Validação de Software** e tem como objetivo extrair informações detalhadas das disciplinas dos cursos de graduação da USP.

## Membros
Danielle Pereira (11918539), Henrique Carobolante Parro (11917987), Joao Augusto Fernandes Barbosa (11953348)

## Descrição

O script realiza scraping da grade curricular e detalhes das disciplinas diretamente do site JupiterWeb, navegando pelas unidades e cursos, coletando informações relevantes como créditos, carga horária, objetivos e programas das disciplinas.

## Tecnologias Utilizadas

- Python 3
- Selenium WebDriver (para automação do navegador)
- BeautifulSoup (para parsing do HTML). O processo foi optimizado usando selenium para interacao com o JS, uma vez que o site não eh estatico e BS4 para parser em dialogs e semelhantes

## Como Rodar
Garanta a instalacao das bibliotecas necessarias.
```bash
pip install -r requirements.txt

No terminal, execute o script principal passando como argumento o número de unidades que deseja processar.

```bash
python3 src/main.py <numero_de_unidades>
