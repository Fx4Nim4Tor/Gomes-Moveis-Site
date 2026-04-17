document.getElementsByClassName("subit-form-categoria-adm")[0].addEventListener("click", function(){
    window.location.href = this.dataset.url;
});

document.querySelectorAll(".btn-edit-adm").forEach(btn => {
    btn.addEventListener("click", function () {
        window.location.href = this.dataset.url;
    });
});

document.querySelectorAll(".btn-delet-adm").forEach(btn => {
    btn.addEventListener("click", function () {
        window.location.href = this.dataset.url;
    });
});