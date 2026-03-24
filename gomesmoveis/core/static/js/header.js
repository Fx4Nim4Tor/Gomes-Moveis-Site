// botao para abrir alerta
const botao = document.getElementsByClassName("btn-whatsapp-header")[0];
botao.addEventListener("click",abrirAlerta)
// botao para fechar alerta
const fecha_alerta = document.getElementsByClassName("fechar")[0];
fecha_alerta.addEventListener("click",fecharAlerta)

// direciona botoes para whats dependendo de onde mora
document.getElementsByClassName("smo")[0].addEventListener("click", function(){
    window.location.href = "";
});
document.getElementsByClassName("pinhalzinho")[0].addEventListener("click", function(){
    window.location.href = "";
});


// funcao que os botoes que abre e fecha o alerta puxa 
function fecharAlerta(){
    document.getElementById("alerta").style.display = "none";
}
function abrirAlerta(){
    document.getElementById("alerta").style.display = "flex";
}


//menu overlay
const overlay = document.getElementsByClassName("menu-header-1100px")[0];
overlay.addEventListener("click", abreMenu)

function abreMenu(){
    document.getElementsByClassName("menu-lateral-container")[0].style.display = "flex";
    requestAnimationFrame(() => {
        requestAnimationFrame(() => {
            document.getElementsByClassName("overlay-header")[0].classList.add("aberto");
        });
    });

}

const drawer = document.getElementsByClassName("drawer-header")[0];
drawer.addEventListener("click", fecharMenu)

function fecharMenu(){
    const overlayHeader = document.getElementsByClassName("overlay-header")[0];
    const container = document.getElementsByClassName("menu-lateral-container")[0];
    
    overlayHeader.classList.remove("aberto");
    
    setTimeout(() => {
        container.style.display = "none";
    }, 300);
}


//busca
const inputBusca = document.getElementById('input-busca');
const dropdown = document.getElementById('dropdown-busca');

let timer = null; // para não disparar a cada letra digitada

inputBusca.addEventListener('input', function () {
    const query = this.value.trim();

    clearTimeout(timer); // cancela a requisição anterior

    if (query.length < 2) {
        dropdown.classList.remove('ativo');
        dropdown.innerHTML = '';
        return;
    }

    // Espera 300ms depois que o usuário parar de digitar
    timer = setTimeout(() => {
        fetch(`/buscar/?q=${encodeURIComponent(query)}`)
            .then(res => res.json())
            .then(data => {
                dropdown.innerHTML = '';

                if (data.resultados.length === 0) {
                    dropdown.innerHTML = '<p class="busca-vazia">Nenhum produto encontrado</p>';
                } else {
                    data.resultados.forEach(p => {
                        const item = document.createElement('a');
                        item.href = `/produto/${p.slug}/`;
                        item.classList.add('item-busca');
                        item.innerHTML = `
                            ${p.imagem ? `<img src="${p.imagem}" alt="${p.nome}">` : ''}
                            <span>${p.nome}</span>
                        `;
                        dropdown.appendChild(item);
                    });
                }

                dropdown.classList.add('ativo');
            });
    }, 300);
});

// Fecha o dropdown ao clicar fora
document.addEventListener('click', function (e) {
    if (!inputBusca.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.classList.remove('ativo');
    }
});