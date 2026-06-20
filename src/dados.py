import json
import os

PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
CAMINHO_RANKING = os.path.join(PASTA_ATUAL, "..", "ranking.json")


def salvar_recorde(caminho_arquivo, pontuacao):
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(str(pontuacao))


def carregar_recorde(caminho_arquivo):
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read().strip()
            if conteudo == "":
                return 0
            return int(conteudo)
    except FileNotFoundError:
        return 0


def carregar_ranking():
    if not os.path.exists(CAMINHO_RANKING):
        return []
    with open(CAMINHO_RANKING, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_ranking(vencedor, pontos):
    ranking = carregar_ranking()
    
    for entrada in ranking:
        if entrada["jogador"] == vencedor:
            if pontos > entrada["pontos"]:
                entrada["pontos"] = pontos
            with open(CAMINHO_RANKING, "w", encoding="utf-8") as f:
                json.dump(ranking, f)
            return
    
    ranking.append({"jogador": vencedor, "pontos": pontos})
    ranking.sort(key=lambda x: x["pontos"], reverse=True)
    ranking = ranking[:5]
    with open(CAMINHO_RANKING, "w", encoding="utf-8") as f:
        json.dump(ranking, f)