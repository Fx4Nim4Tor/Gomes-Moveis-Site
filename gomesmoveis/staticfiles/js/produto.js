document.addEventListener("DOMContentLoaded", function() {
    const principal = document.getElementById("img-principal");
    const miniaturasContainer = document.querySelector('.mini-img-produto');

    if (principal && miniaturasContainer) {
        miniaturasContainer.addEventListener('click', function(event) {
            const thumb = event.target.closest('.miniatura');
            if (!thumb) return;

            principal.src = thumb.src;
            miniaturasContainer.querySelectorAll('.miniatura').forEach(function(img) {
                img.classList.remove('miniatura--active');
            });
            thumb.classList.add('miniatura--active');
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

function fecharAlerta(){
    const alerta = document.getElementById('alerta');
    if (alerta) alerta.style.display = 'none';
}

function abrirAlerta(){
    const alerta = document.getElementById('alerta');
    if (alerta) alerta.style.display = 'flex';
}

function fecharAlertaComp(){
    const alertaComp = document.getElementById('alertacomp');
    if (alertaComp) alertaComp.style.display = 'none';
}

function abrirAlertaComp(){
    const linkInput = document.getElementById('link-compartilhar');
    const alertaComp = document.getElementById('alertacomp');
    if (linkInput) linkInput.value = window.location.href;
    if (alertaComp) alertaComp.style.display = 'flex';
}

function copiarLink(){
    const input = document.getElementById('link-compartilhar');
    if (!input) return;

    navigator.clipboard.writeText(input.value).then(() => {
        const btn = document.querySelector('.btn-copiar');
        if (btn) {
            btn.textContent = 'Copiado!';
            setTimeout(() => btn.textContent = 'Copiar', 2000);
        }
    }).catch(() => {
        input.select();
        document.execCommand('copy');
    });
}

const botaoFeitoPor = document.getElementsByClassName("feitopor")[0];
if (botaoFeitoPor) {
    botaoFeitoPor.addEventListener("click", function() {
        window.location.href = this.dataset.url;
    });
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

function fecharAlertaComp(){
    document.getElementById("alertacomp").style.display = "none";
}
// function abrirAlertaComp(){
//     document.getElementsByClassName("alertacomp")[0].style.display = "flex";
// }

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


const botaoFeitoPor = document.getElementsByClassName("feitopor")[0];
if (botaoFeitoPor) {
    botaoFeitoPor.addEventListener("click", function(){
        window.location.href = this.dataset.url;
    });
}