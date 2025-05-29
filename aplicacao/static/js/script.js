const nomeInput = document.getElementById('nome');
const mensagemInput = document.getElementById('mensagem');
const contadorNome = document.getElementById('contadorNome');
const contadorMensagem = document.getElementById('contadorMensagem');
const botaoEnviar = document.getElementById('botaoEnviar')


// === Restrição e contador para o NOME ===
nomeInput.addEventListener('input', function () {
  this.value = this.value
    .replace(/[^a-zA-ZÀ-ÿ\s]/g, '')   // Remove números e caracteres especiais
    .replace(/\s{2,}/g, ' ')          // Remove múltiplos espaços
    .trimStart();                     // Remove espaço no início

  // Limita a 50 caracteres
  if (this.value.length > 50) {
    this.value = this.value.slice(0, 50);
  }

  // Atualiza contador
  contadorNome.textContent = `${this.value.length}/50`;
});

// === Restrição e contador para o COMENTÁRIO ===
mensagemInput.addEventListener('input', function () {
  this.value = this.value
    .replace(/\s{2,}/g, ' ')          // Remove múltiplos espaços
    .trimStart();                     // Remove espaço no início

  // Limita a 200 caracteres
  if (this.value.length > 200) {
    this.value = this.value.slice(0, 200);
  }

  // Atualiza contador
  contadorMensagem.textContent = `${this.value.length}/200`;
});


document.getElementById('botaoEnviar').addEventListener('click', async function() {
    const nome = document.getElementById('nome').value.trim();
    const mensagem = document.getElementById('mensagem').value.trim();

    if (!nome || !mensagem) {
        alert("Por favor, preencha todos os campos.");
        return;
    }

    const dados = { nome, mensagem };

    try {
        const resposta = await fetch('http://127.0.0.1:5000/mensagem', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dados)
        });

        if (!resposta.ok) {
            throw new Error(`Erro HTTP: ${resposta.status}`);
        }

        const resultado = await resposta.json();

        // Exibir comentário no front
        const comentarioDiv = document.getElementById('comentarioFiltrado');
        comentarioDiv.innerHTML += `<p><strong>${resultado.nome}</strong>: ${resultado.mensagem}</p>`;

        // Limpa os campos
        // Limpa os campos
        nomeInput.value = '';
        mensagemInput.value = '';
        contadorNome.textContent = '0/50';
        contadorMensagem.textContent = '0/200';

    } catch (erro) {
        console.error("Erro ao enviar comentário:", erro);
        alert("Erro ao enviar comentário. Verifique se a API está rodando.");
    }
});