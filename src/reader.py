from curso import Curso
from unidade import UnidadeUSP
from disciplina import Disciplina

# Menu interativo para testar as funcionalidades

def iniciar_menu_interativo(unidades, disciplinas_por_codigo):
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
                print(f"\n📚 {unidade}")
                for curso in unidade.cursos:
                    print(f"  - {curso}")

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
