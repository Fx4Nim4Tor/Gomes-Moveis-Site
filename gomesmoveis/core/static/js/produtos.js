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

    if (!containerBotao) return;

    const botao = document.getElementById('btn-carregar-mais');

    botao.addEventListener('click', function () {
        const proximaPagina = botao.dataset.proximaPagina;

        const params = new URLSearchParams(window.location.search);
        params.set('page', proximaPagina);

        botao.textContent = 'Carregando...';
        botao.disabled = true;

        fetch(`/produtos/?${params.toString()}`, {
            headers: { 'x-requested-with': 'XMLHttpRequest' }
        })
        .then(res => res.json())
        .then(data => {
            listaProdutos.insertAdjacentHTML('beforeend', data.html);

            // Registra as novas imagens inseridas no observer de carregamento
            listaProdutos.querySelectorAll('img:not(.carregada)').forEach(img => {
                if (img.complete) {
                    img.classList.add('carregada');
                } else {
                    img.addEventListener('load', () => img.classList.add('carregada'));
                }
            });

            // Registra os novos cards no IntersectionObserver de animação
            listaProdutos.querySelectorAll('.animar:not(.visivel)').forEach(el => {
                observer.observe(el);
            });

            if (data.tem_proxima) {
                botao.dataset.proximaPagina = data.proxima_pagina;
                botao.textContent = 'Carregar mais';
                botao.disabled = false;
            } else {
                containerBotao.remove();
            }
        })
        .catch(() => {
            botao.textContent = 'Erro ao carregar. Tente novamente.';
            botao.disabled = false;
        });
    });
});

document.getElementsByClassName("feitopor")[0].addEventListener("click", function () {
    window.location.href = this.dataset.url;
});