import os
import re
import json
import logging
from datetime import datetime
from flask import current_app

logger = logging.getLogger(__name__)

def carregar_palavroes():
    try:
        caminho = os.path.join(current_app.instance_path, 'palavroes.txt')
        with open(caminho, "r", encoding="utf-8") as arquivo:
            palavroes = [linha.strip().lower() for linha in arquivo if linha.strip()]
        logger.info("Palavrões carregados com sucesso.")
        return palavroes
    except Exception as e:
        logger.error(f"Erro ao carregar palavrões: {e}")
        return []


def gerar_regex_palavrao(palavrao):
    mapa = {
        'a': '[aáàâã4@]',
        'i': '[iíìî1!]',
        'e': '[eéèê3]',
        'o': '[oóòôõ0]',
        'u': '[uúùû]',
        's': '[s$5]',
        'c': '[cç]',
        'd': '[d]',
        'f': '[f]',
        'p': '[p]',
        't': '[t]',
        'l': '[l]',
        'h': '[h]',
        'm': '[m]',
        'r': '[r]',
        'n': '[n]',
        'b': '[b]',
        'g': '[g]',
        'j': '[j]',
        'q': '[q]',
        'v': '[v]',
        'w': '[w]',
        'x': '[x]',
        'y': '[y]',
        'z': '[z]'
    }

    partes = palavrao.strip().split()

    regex_partes = []
    for parte in partes:
        regex_parte = ''
        for i, letra in enumerate(parte):
            if letra.lower() in mapa:
                regex_parte += mapa[letra.lower()]
            else:
                regex_parte += re.escape(letra)

            # Adiciona caracteres não alfanuméricos apenas se não for o último caractere da parte
            if i < len(parte) - 1:
                regex_parte += r'[\W_]*'
        regex_partes.append(regex_parte)

    separador = r'[\W_]+' # Alterado para + para garantir pelo menos um separador não alfanumérico

    regex_final = separador.join(regex_partes)

    # Limites de palavra
    regex_final = r'(?<!\w)' + regex_final + r'(?!\w)'

    return regex_final

# Função para censurar mensagens com leetspeak
def censurar_mensagem(mensagem):
    palavroes = carregar_palavroes()
    mensagem_censurada = mensagem

    for palavrao in palavroes:
        regex = gerar_regex_palavrao(palavrao)

        mensagem_censurada = re.sub(
            regex,
            lambda m: '*' * len(m.group()),
            mensagem_censurada,
            flags=re.IGNORECASE
        )

    return mensagem_censurada

def salvar_em_arquivo(nome, comentario_original, comentario_final):
    foi_censurado = comentario_original != comentario_final

    dados = {
        "nome": nome,
        "comentario_original": comentario_original,
        "foi_censurado": foi_censurado,
        "comentario_final": comentario_final
    }

    dados_dir = os.path.join(current_app.instance_path, 'dados')
    os.makedirs(dados_dir, exist_ok=True)

    try:
        timestap = datetime.now().strftime("%Y%m%d_%H%M%S")
        caminho_arquivo = os.path.join(dados_dir, f'{nome}_{timestap}.json')

        with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)

        logger.info(f"Comentário salvo com sucesso: {caminho_arquivo}")

    except Exception as e:
        logger.error(f"Erro ao salvar arquivo {nome}: {e}")