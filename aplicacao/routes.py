from flask import Blueprint, render_template, request, jsonify, send_from_directory, current_app
from .filtros import censurar_mensagem, salvar_em_arquivo
import os
import logging

bp = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

@bp.route('/')
def index():
    logger.info("Pagina inicial acessada.")
    return render_template('index.html')

@bp.route('/<path:filename>')
def static_files(filename):
    logger.info(f"Arquivo estático acessado: {filename}")
    static_folder = os.path.join(current_app.root_path, 'static')
    return send_from_directory(static_folder, filename)

@bp.route('/mensagem', methods=['POST'])
def processar_mensagem():
    try:
        dados = request.get_json()
        nome = dados.get('nome')
        mensagem = dados.get('mensagem')

        if not nome or not mensagem:
            logger.warning("Requisição sem nome ou mensagem.")
            return jsonify({'erro': 'Nome e mensagem são obrigatórios'}), 400

        mensagem_censurada = censurar_mensagem(mensagem)

        salvar_em_arquivo(nome, mensagem, mensagem_censurada)
        
        logger.info(f"Mensagem processada com sucesso para {nome}")
        return jsonify({'nome': nome, 'mensagem': mensagem_censurada}), 200

    except Exception as e:
        logger.exception(f"Erro no processamento da mensagem: {e}")
        return jsonify({'erro': 'Erro interno no servidor'}), 500