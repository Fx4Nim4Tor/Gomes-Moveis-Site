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
            // Cria um elemento temporário para parsear o HTML recebido
            const temp = document.createElement('div');
            temp.innerHTML = data.html;

            // Pega todos os novos cards
            const novosCards = Array.from(temp.children);

            // Para cada card, garante que a imagem carregue corretamente antes de exibir
            novosCards.forEach(card => {
                const img = card.querySelector('img');
                if (img) {
                    // Remove qualquer lazy loading que possa existir
                    img.removeAttribute('loading');

                    // Se a imagem já está em cache e carregada, força o reflow
                    if (img.complete && img.naturalHeight !== 0) {
                        img.style.display = 'none';
                        img.offsetHeight; // força reflow
                        img.style.display = '';
                    } else {
                        // Se ainda não carregou, aguarda o evento load
                        img.addEventListener('load', function () {
                            this.style.display = 'none';
                            this.offsetHeight; // força reflow
                            this.style.display = '';
                        });

                        // Força o browser a buscar a imagem novamente caso o src esteja travado
                        const src = img.getAttribute('src');
                        if (src) {
                            img.setAttribute('src', '');
                            img.setAttribute('src', src);
                        }
                    }
                }

                listaProdutos.appendChild(card);
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

document.addEventListener('DOMContentLoaded', function () {
    const principal = document.getElementById('img-principal');
    const miniaturas = document.querySelectorAll('.miniatura');

    if (principal && miniaturas.length) {
        miniaturas.forEach(function (thumb) {
            thumb.style.cursor = 'pointer';
            thumb.addEventListener('click', function () {
                principal.src = this.src;
                miniaturas.forEach(function (img) {
                    img.classList.remove('miniatura--active');
                });
                this.classList.add('miniatura--active');
            });
        });
    }
});

const botaoFeitoPor = document.getElementsByClassName('feitopor')[0];
if (botaoFeitoPor) {
    botaoFeitoPor.addEventListener('click', function () {
        window.location.href = this.dataset.url;
    });
}