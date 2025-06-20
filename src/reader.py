import json
from curso import Curso
from unidade import UnidadeUSP
from disciplina import Disciplina

# Caminho para o arquivo JSON exportado
CAMINHO_JSON = "dados_extraidos.json"

# Carrega os dados e reconstrói os objetos

def carregar_dados():
    with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
        dados = json.load(f)

    unidades = {}
    disciplinas_por_codigo = {}

    for unidade_nome, unidade_info in dados.items():
        unidade_obj = UnidadeUSP(unidade_nome)

        for curso_info in unidade_info["cursos"]:
            curso_obj = Curso(
                nome=curso_info["nome"],
                unidade=unidade_nome,
                duracao_ideal=curso_info["duracao_ideal"],
                duracao_min=curso_info["duracao_min"],
                duracao_max=curso_info["duracao_max"]
            )

            # Reconstruir disciplinas a partir dos códigos
            for tipo in ["obrigatorias", "optativas_eletivas", "optativas_livres"]:
                for codigo in curso_info[tipo]:
                    if codigo not in disciplinas_por_codigo:
                        disciplina = Disciplina(codigo, "", 0, 0, "")
                        disciplinas_por_codigo[codigo] = disciplina
                    else:
                        disciplina = disciplinas_por_codigo[codigo]
                    getattr(curso_obj, tipo).append(disciplina)

            unidade_obj.cursos.append(curso_obj)

        unidades[unidade_nome] = unidade_obj

    return unidades, disciplinas_por_codigo


# Menu interativo para testar as funcionalidades
def menu():
    unidades, disciplinas_por_codigo = carregar_dados()

    while True:
        print("\n=== MENU ===")
        print("1. Listar cursos por unidade")
        print("2. Mostrar dados de um curso")
        print("3. Mostrar dados de todos os cursos")
        print("4. Dados de uma disciplina e onde ela aparece")
        print("5. Disciplinas que aparecem em mais de um curso")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            for unidade in unidades.values():
                print(f"\n📚 {unidade.nome}")
                for curso in unidade.cursos:
                    print(f"  - {curso.nome}")

        elif opcao == "2":
            nome_curso = input("Digite o nome (ou parte) do curso: ").lower()
            for unidade in unidades.values():
                for curso in unidade.cursos:
                    if nome_curso in curso.nome.lower():
                        print(f"\n🎓 {curso.nome} - Unidade: {curso.unidade}")
                        print(f"  Duração: ideal {curso.duracao_ideal}, min {curso.duracao_min}, max {curso.duracao_max}")
                        print(f"  Obrigatórias: {len(curso.obrigatorias)} | Eletivas: {len(curso.optativas_eletivas)} | Livres: {len(curso.optativas_livres)}")

        elif opcao == "3":
            for unidade in unidades.values():
                for curso in unidade.cursos:
                    print(f"\n🎓 {curso.nome} - Unidade: {curso.unidade}")
                    print(f"  Duração: ideal {curso.duracao_ideal}, min {curso.duracao_min}, max {curso.duracao_max}")
                    print(f"  Obrigatórias: {len(curso.obrigatorias)} | Eletivas: {len(curso.optativas_eletivas)} | Livres: {len(curso.optativas_livres)}")

        elif opcao == "4":
            codigo = input("Digite o código da disciplina: ").upper()
            disciplina = disciplinas_por_codigo.get(codigo)
            if disciplina:
                print(f"\n📘 {disciplina.codigo} - {disciplina.nome} ({disciplina.creditos_aula} CH, {disciplina.creditos_trabalho} CT)")
                print("Presente nos cursos:")
                for unidade in unidades.values():
                    for curso in unidade.cursos:
                        if disciplina in curso.obrigatorias or disciplina in curso.optativas_eletivas or disciplina in curso.optativas_livres:
                            print(f"  - {curso.nome} ({curso.unidade})")
            else:
                print("❌ Disciplina não encontrada.")

        elif opcao == "5":
            aparicoes = {}
            for unidade in unidades.values():
                for curso in unidade.cursos:
                    for d in (curso.obrigatorias + curso.optativas_eletivas + curso.optativas_livres):
                        aparicoes.setdefault(d.codigo, set()).add(curso.nome)
            print("\n📌 Disciplinas presentes em mais de um curso:")
            for codigo, cursos in aparicoes.items():
                if len(cursos) > 1:
                    nome = disciplinas_por_codigo[codigo].nome
                    print(f"- {codigo}: {nome} [em {len(cursos)} cursos]")

        elif opcao == "0":
            break
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    menu()
