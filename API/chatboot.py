from flask import Flask, request, jsonify
import json
import openai
import os
from dotenv import load_dotenv
from flask_cors import CORS


load_dotenv(dotenv_path="chave.env")

# Recebe chave da API
openai.api_key = os.getenv("OPENAI_API_KEY")
print(f"Chave carregada: {openai.api_key}")


# Inicializa o Flask
app = Flask(__name__)
CORS(app)

'''
#função teste
palavroes = [
    "palavrao1", "palavrao2", "palavrao3",
    "idiota", "burro", "besta", "tolo", "otario",
    "palavraofensiva", "xingar", "chato"
]

def censurar_mensagem(mensagem):
    palavras = mensagem.split()

    mensagem_censurada = []

    for palavra in palavras:
        # Remove caracteres não alfanuméricos temporariamente para comparar
        palavra_limpa = ''.join(filter(str.isalnum, palavra)).lower()
        if palavra_limpa in palavroes:
            censurada = '*' * len(palavra_limpa)
            # Substitui apenas a parte da palavra que é ofensiva
            palavra_censurada = palavra.replace(palavra_limpa, censurada)
            mensagem_censurada.append(palavra_censurada)
        else:
            mensagem_censurada.append(palavra)

    return ' '.join(mensagem_censurada)
'''


#prompt do chat
def censurar_mensagem(mensagem):
  prompt = f"Censure qualquer palavrão, racismo, preconceito etc. na frase abaixo. Substitua as letras ofensivas por '*'.\nFrase: \"{mensagem}\""

  resposta = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "Você é um filtro de linguagem ofensiva."},
      {"role": "user", "content": prompt}
      ],
      temperature=0.5,
      max_tokens=10
      )

  return resposta['choices'][0]['text'].strip()


#deixa essa boma aqui
def salvar_em_arquivo(nome, mensagem):
   dados = {"nome": nome, "mensagem": mensagem}

   # Cria o diretório 'dados' se não existir
   if not os.path.exists('dados'):
      os.makedirs('dados')
   # Cria um arquivo JSON com o nome da pessoa
   caminho_arquivo = os.path.join('dados', f'{nome}.json')

   with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
      json.dump(dados, arquivo, ensure_ascii=False, indent=4)
      

@app.route('/mensagem', methods=['POST'])
def processar_mensagem():
  dados = request.get_json()

  nome = dados['nome']
  mensagem = dados['mensagem']

  if not nome or not mensagem:
    return jsonify({'erro': 'Nome e mensagem são obrigatórios'}), 400

  mensagem_censurada = censurar_mensagem(mensagem)

  salvar_em_arquivo(nome, mensagem_censurada)

  return jsonify({'nome': nome, 'mensagem': mensagem_censurada}), 200


if __name__ == '__main__':
  app.run(debug=True)
