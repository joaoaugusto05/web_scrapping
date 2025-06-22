class Disciplina:
    """
    Representa uma disciplina de curso.
    Atributos:
        codigo (str): código da disciplina (ex: 'MAP1234').
        nome (str): nome da disciplina.
        creditos_aula (int): créditos de aula.
        creditos_trabalho (int): créditos de trabalho.
    """
    def __init__(self, codigo, nome, creditos_aula, creditos_trabalho, carga_horaria,
                 carga_estagio, carga_praticas, carga_atpa):
        self.codigo = codigo
        self.nome = nome
        self.creditos_aula = creditos_aula
        self.creditos_trabalho = creditos_trabalho
        self.carga_horaria = carga_horaria
        self.carga_estagio = carga_estagio
        self.carga_praticas = carga_praticas
        self.carga_atpa = carga_atpa
        
    def __str__(self):
        return (
            f"{self.codigo} - {self.nome} "
            f"(CA: {self.creditos_aula}, CT: {self.creditos_trabalho}, "
            f"CH: {self.carga_horaria}, CE: {self.carga_estagio}, "
            f"CP: {self.carga_praticas}, ATPA: {self.carga_atpa})"
        )

