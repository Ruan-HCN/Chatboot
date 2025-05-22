async function enviarComentario() {
  const nome = document.getElementById('nome').value.trim();
  const mensagem = document.getElementById('mensagem').value.trim();

  if (!nome || !mensagem) {
    alert("Por favor, preencha todos os campos.");
    return;
  }

  const dados = {
    nome: nome,
    mensagem: mensagem
  };

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

    // Exibir no front
    document.getElementById('comentarioFiltrado').innerHTML =
      `<strong>${resultado.nome}</strong>: ${resultado.mensagem}`;

    // Limpa os campos
    document.getElementById('nome').value = '';
    document.getElementById('mensagem').value = '';

  } catch (erro) {
    console.error("Erro ao enviar comentário:", erro);
    alert("Erro ao enviar comentário. Verifique se a API está rodando.");
  }
}
