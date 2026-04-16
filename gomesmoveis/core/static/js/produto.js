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

    const smoBtn = document.querySelector(".smo");
    if (smoBtn) {
        smoBtn.addEventListener("click", function() {
            window.location.href = "";
        });
    }

    const pinhalzinhoBtn = document.querySelector(".pinhalzinho");
    if (pinhalzinhoBtn) {
        pinhalzinhoBtn.addEventListener("click", function() {
            window.location.href = "";
        });
    }
});

// funcao que os botoes que abre e fecha o alerta puxa 
function fecharAlerta(){
    document.getElementById("alerta").style.display = "none";
}
function abrirAlerta(){
    document.getElementsByClassName("alerta")[0].style.display = "flex";
}