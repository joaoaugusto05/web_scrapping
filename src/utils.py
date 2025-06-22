import json

def exportar_para_json(unidades_data, caminho="dados_extraidos.json"):
    print("[DEBUG] Exportando dados para JSON...")
    dados = {}

    for unidade_nome, unidade in unidades_data.items():
        cursos_data = []
        for curso in unidade.cursos:
            cursos_data.append({
                "nome": curso.nome,
                "duracao_ideal": curso.duracao_ideal,
                "duracao_min": curso.duracao_min,
                "duracao_max": curso.duracao_max,
                "obrigatorias": [
                    {
                        "codigo": d.codigo,
                        "nome": d.nome,
                        "creditos_aula": d.creditos_aula,
                        "creditos_trabalho": d.creditos_trabalho,
                        "carga_horaria": d.carga_horaria
                    } for d in curso.obrigatorias
                ],
                "optativas_eletivas": [
                    {
                        "codigo": d.codigo,
                        "nome": d.nome,
                        "creditos_aula": d.creditos_aula,
                        "creditos_trabalho": d.creditos_trabalho,
                        "carga_horaria": d.carga_horaria
                    } for d in curso.optativas_eletivas
                ],
                "optativas_livres": [
                    {
                        "codigo": d.codigo,
                        "nome": d.nome,
                        "creditos_aula": d.creditos_aula,
                        "creditos_trabalho": d.creditos_trabalho,
                        "carga_horaria": d.carga_horaria
                    } for d in curso.optativas_livres
                ]
            })
        dados[unidade_nome] = {"cursos": cursos_data}

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    print(f"📁 Dados exportados para: {caminho}")
    print("[DEBUG] Exportação concluída com sucesso.")

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
