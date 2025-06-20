import json

def exportar_para_json(unidades_data, caminho="dados_extraidos.json"):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump({
            unidade: {
                "cursos": [
                    {
                        "nome": curso.nome,
                        "duracao_ideal": curso.duracao_ideal,
                        "duracao_min": curso.duracao_min,
                        "duracao_max": curso.duracao_max,
                        "obrigatorias": [d.codigo for d in curso.obrigatorias],
                        "optativas_eletivas": [d.codigo for d in curso.optativas_eletivas],
                        "optativas_livres": [d.codigo for d in curso.optativas_livres]
                    }
                    for curso in unidade_obj.cursos
                ]
            }
            for unidade, unidade_obj in unidades_data.items()
        }, f, ensure_ascii=False, indent=2)
    print(f"📁 Dados exportados para: {caminho}")

def listar_cursos_por_unidade(unidades_data):
    print("\n📚 Unidades e seus cursos:")
    for nome_unidade, unidade in unidades_data.items():
        print(f"- {nome_unidade} ({len(unidade.cursos)} cursos)")
        for curso in unidade.cursos:
            print(f"   → {curso.nome}")

def mostrar_dados_curso(curso):
    print(f"\n🎓 {curso.nome} ({len(curso.obrigatorias)} obrigatórias, {len(curso.optativas_eletivas)} eletivas, {len(curso.optativas_livres)} livres)")

def mostrar_dados_disciplina(disciplina):
    print(f"→ {disciplina.codigo} - {disciplina.nome} ({disciplina.creditos_aula} CH, {disciplina.creditos_trabalho} CT)")
