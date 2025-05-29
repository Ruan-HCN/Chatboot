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


# Função para censurar mensagens com leetspeak
def censurar_mensagem(mensagem):
    palavroes = carregar_palavroes()
    mensagem_censurada = mensagem

    for palavrao in palavroes:
        # Monta regex permitindo substituições comuns (leetspeak)
        regex = ''
        for letra in palavrao:
            if letra == 'a':
                regex += '[aáàâã4@]'
            elif letra == 'i':
                regex += '[iíìî1!]'
            elif letra == 'e':
                regex += '[eéèê3]'
            elif letra == 'o':
                regex += '[oóòôõ0]'
            elif letra == 'u':
                regex += '[uúùû]'
            elif letra == 's':
                regex += '[s$]'
            else:
                regex += letra

        # Considera a palavra inteira (delimitada)
        regex = r'\b' + regex + r'\b'

        # Substitui por asteriscos mantendo o tamanho da palavra
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