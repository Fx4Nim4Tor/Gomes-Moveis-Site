document.addEventListener('DOMContentLoaded', function () {
    const btnAbrir = document.getElementById('btn-abrir-filtro');
    const btnFechar = document.getElementById('btn-fechar-filtro');
    const overlay = document.getElementById('filtro-overlay');
    const painel = document.getElementById('painel-filtro');

    function abrirFiltro() {
        painel.classList.add('aberto');
        overlay.classList.add('aberto');
        document.body.style.overflow = 'hidden';
    }

    function fecharFiltro() {
        painel.classList.remove('aberto');
        overlay.classList.remove('aberto');
        document.body.style.overflow = '';
    }

    btnAbrir.addEventListener('click', abrirFiltro);
    btnFechar.addEventListener('click', fecharFiltro);
    overlay.addEventListener('click', fecharFiltro);
});

document.addEventListener('DOMContentLoaded', function () {
    const listaProdutos = document.getElementById('lista-produtos');
    const containerBotao = document.getElementById('container-carregar-mais');

    // Se não tiver o botão na página, para por aqui
    if (!containerBotao) return;

    const botao = document.getElementById('btn-carregar-mais');

    botao.addEventListener('click', function () {
        const proximaPagina = botao.dataset.proximaPagina;

        // Pega os filtros ativos da URL atual para manter na requisição
        const params = new URLSearchParams(window.location.search);
        params.set('page', proximaPagina);

        botao.textContent = 'Carregando...';
        botao.disabled = true;

        fetch(`/produtos/?${params.toString()}`, {
            headers: { 'x-requested-with': 'XMLHttpRequest' }
        })
        .then(res => res.json())
        .then(data => {
            // Adiciona os novos cards no final da lista
            listaProdutos.insertAdjacentHTML('beforeend', data.html);

            if (data.tem_proxima) {
                // Atualiza o botão para buscar a próxima página
                botao.dataset.proximaPagina = data.proxima_pagina;
                botao.textContent = 'Carregar mais';
                botao.disabled = false;
            } else {
                // Sem mais páginas, esconde o botão
                containerBotao.remove();
            }
        })
        .catch(() => {
            botao.textContent = 'Erro ao carregar. Tente novamente.';
            botao.disabled = false;
        });
    });
});



document.getElementsByClassName("feitopor")[0].addEventListener("click", function(){
    window.location.href = this.dataset.url;
});