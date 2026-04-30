document.addEventListener("DOMContentLoaded", function() {
    const principal = document.getElementById("img-principal");
    const miniaturas = document.querySelectorAll(".miniatura");

    if (principal && miniaturas.length) {
        miniaturas.forEach(img => {
            img.addEventListener("click", function() {
                principal.src = this.src;
            });
        });
    }

    const botao = document.querySelector(".btn-whats");
    if (botao) {
        botao.addEventListener("click", abrirAlerta);
    }

    const fecha_alerta = document.querySelector(".fechar");
    if (fecha_alerta) {
        fecha_alerta.addEventListener("click", fecharAlerta);
    }
});

function fecharAlerta(){
    document.getElementById("alerta").style.display = "none";
}
function abrirAlerta(){
    document.getElementsByClassName("alerta")[0].style.display = "flex";
}

function fecharAlertaComp(){
    document.getElementById("alertacomp").style.display = "none";
}

function abrirAlertaComp(){
    document.getElementById("link-compartilhar").value = window.location.href;
    document.getElementById("alertacomp").style.display = "flex";
}

function copiarLink(){
    const input = document.getElementById("link-compartilhar");
    navigator.clipboard.writeText(input.value).then(() => {
        const btn = document.querySelector(".btn-copiar");
        btn.textContent = "Copiado!";
        setTimeout(() => btn.textContent = "Copiar", 2000);
    });
}

document.getElementsByClassName("feitopor")[0].addEventListener("click", function(){
    window.location.href = this.dataset.url;
});

document.querySelectorAll('img').forEach(img => {
    if (img.complete) {
        img.classList.add('carregada');
    } else {
        img.addEventListener('load', () => img.classList.add('carregada'));
    }
});

document.querySelectorAll(".smo").forEach(function(btn) {
    btn.addEventListener("click", function() {
        window.location.href = this.dataset.url;
    });
});

document.querySelectorAll(".pinhalzinho").forEach(function(btn) {
    btn.addEventListener("click", function() {
        window.location.href = this.dataset.url;
    });
});