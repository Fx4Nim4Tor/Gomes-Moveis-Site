// const loadButton = document.getElementById("load-more");
// const container = document.getElementById("produtos-container");
// const filtroForm = document.getElementById("filtro-form");

// function getCategoriasSelecionadas() {
//     const checked = filtroForm.querySelectorAll('input[name="categoria"]:checked');
//     return Array.from(checked).map(c => c.value);
// }

// // Função para carregar produtos via AJAX
// function carregarProdutos(page = 1, append = true) {
//     const categorias = getCategoriasSelecionadas();
//     const params = new URLSearchParams();
//     params.append("page", page);
//     categorias.forEach(c => params.append("categoria", c));

//     fetch(`/produtos/?${params.toString()}`, {
//         headers: { "X-Requested-With": "XMLHttpRequest" }
//     })
//     .then(res => res.json())
//     .then(data => {
//         if (append) {
//             container.insertAdjacentHTML('beforeend', data.html);
//         } else {
//             container.innerHTML = data.html;
//         }

//         if (data.has_next) {
//             loadButton.dataset.nextPage = data.next_page;
//             loadButton.style.display = "inline-block";
//         } else {
//             loadButton.style.display = "none";
//         }
//     });
// }

// // Evento do botão "Carregar mais"
// if (loadButton) {
//     loadButton.addEventListener("click", () => {
//         const nextPage = loadButton.dataset.nextPage;
//         carregarProdutos(nextPage, true);
//     });
// }

// // Evento do filtro
// filtroForm.addEventListener("change", () => {
//     carregarProdutos(1, false);  // pagina 1, substituindo os produtos
// });