// logica troca de imagens miniatura e principal
const principal = document.getElementById("img-principal");
const miniaturas = document.querySelectorAll(".miniatura");

miniaturas.forEach(img => {
    img.addEventListener("click", function(){
        principal.src = this.src;
    });
});



// botao para abrir alerta
const botao = document.getElementsByClassName("btn-whats")[0];
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