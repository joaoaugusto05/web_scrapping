class UnidadeUSP:
    """
    Representa uma unidade da USP com seus cursos.
    Atributos:
        nome (str): nome da unidade (ex: 'Fá. de Filosofia e Ciências Humanas').
        cursos (list): lista de objetos Curso pertencentes a esta unidade.
    """
    def __init__(self, nome):
        self.nome = nome
        self.cursos = []

    def adicionar_curso(self, curso):
        self.cursos.append(curso)

    def __str__(self):
        return f"Unidade: {self.nome} - {len(self.cursos)} curso(s)"
