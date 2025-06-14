class Disciplina:
    """
    Representa uma disciplina de curso.
    Atributos:
        codigo (str): código da disciplina (ex: 'MAP1234').
        nome (str): nome da disciplina.
        creditos_aula (int): créditos de aula.
        creditos_trabalho (int): créditos de trabalho.
        carga_horaria (int): carga horária total.
        carga_estagio (int): carga horária de estágio.
        carga_praticas (int): carga horária de Práticas como CC.
        atividades_aprofund (int): carga horária de Atividades Teórico-Práticas.
    """
    def __init__(self, codigo, nome, creditos_aula, creditos_trabalho, 
                 carga_horaria, carga_estagio, carga_praticas, atividades_aprofund):
        self.codigo = codigo
        self.nome = nome
        self.creditos_aula = creditos_aula
        self.creditos_trabalho = creditos_trabalho
        self.carga_horaria = carga_horaria
        self.carga_estagio = carga_estagio
        self.carga_praticas = carga_praticas
        self.atividades_aprofund = atividades_aprofund

    def __str__(self):
        return f"{self.codigo} - {self.nome} ({self.creditos_aula} C.H., {self.creditos_trabalho} C.T.)"
