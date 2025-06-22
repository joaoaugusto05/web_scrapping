class Curso:
    """
    Representa um curso de graduação.
    Atributos:
        nome (str): nome do curso.
        unidade (str): nome da unidade (filiada).
        duracao_ideal (int): duração ideal em semestres.
        duracao_min (int): duração mínima.
        duracao_max (int): duração máxima.
        obrigatorias (list): lista de Disciplinas obrigatórias.
        optativas_livres (list): lista de Disciplinas optativas livres.
        optativas_eletivas (list): lista de Disciplinas optativas eletivas.
    """
    def __init__(self, nome, unidade, duracao_ideal=None, duracao_min=None, duracao_max=None):
        self.nome = nome
        self.unidade = unidade
        self.duracao_ideal = duracao_ideal
        self.duracao_min = duracao_min
        self.duracao_max = duracao_max
        self.obrigatorias = []
        self.optativas_livres = []
        self.optativas_eletivas = []

    def adicionar_disciplina(self, disciplina, tipo):
        if tipo.lower() in ["obrigatória", "obrigatoria"]:
            self.obrigatorias.append(disciplina)
        elif "livre" in tipo.lower():
            self.optativas_livres.append(disciplina)
        elif "eletiva" in tipo.lower():
            self.optativas_eletivas.append(disciplina)
        else:
            self.obrigatorias.append(disciplina)  # fallback

    def __str__(self):
        return f"Curso: {self.nome} ({self.unidade}), Durações - ideal: {self.duracao_ideal}, min: {self.duracao_min}, max: {self.duracao_max}"
