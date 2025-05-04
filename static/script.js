function enviarPergunta() {
    const input = document.getElementById('pergunta');
    const texto = input.value;
    if (!texto) return;

    adicionarMensagem('Você', texto);

    fetch('/mensagem', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pergunta: texto })
    })
    .then(response => response.json())
    .then(data => {
        adicionarMensagem('Salão', data.resposta);
        input.value = '';
    });
}

function adicionarMensagem(remetente, mensagem) {
    const chatbox = document.getElementById('chatbox');
    const p = document.createElement('p');
    p.innerHTML = `<strong>${remetente}:</strong> ${mensagem}`;
    chatbox.appendChild(p);
    chatbox.scrollTop = chatbox.scrollHeight;
}
