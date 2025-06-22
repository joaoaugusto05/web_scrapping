class Disciplina:
    """
    Representa uma disciplina de curso.
    Atributos:
        codigo (str): código da disciplina (ex: 'MAP1234').
        nome (str): nome da disciplina.
        creditos_aula (int): créditos de aula.
        creditos_trabalho (int): créditos de trabalho.
    """
    def __init__(self, codigo, nome, creditos_aula, creditos_trabalho, carga_horaria, objetivos, programa):
        self.codigo = codigo
        self.nome = nome
        self.creditos_aula = creditos_aula
        self.creditos_trabalho = creditos_trabalho
        self.carga_horaria = carga_horaria
        self.objetivos = objetivos
        self.programa = programa
    def __str__(self):
        return f"{self.codigo} - {self.nome} ({self.creditos_aula} CA, {self.creditos_trabalho} CT)"
