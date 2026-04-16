document.addEventListener('DOMContentLoaded', function() {
    const nomeInput = document.getElementById('nome');
    const descricaoInput = document.getElementById('descricao');
    const imagensInput = document.getElementById('imagens');
    const previewNome = document.getElementById('preview-nome');
    const previewDescricao = document.getElementById('preview-descricao');
    const previewImgPrincipal = document.getElementById('preview-img-principal');
    const miniaturas = document.querySelectorAll('.miniatura');

    function updatePreview() {
        const nome = nomeInput.value || 'Nome do Produto';
        const desc = descricaoInput.value || 'Descrição do produto aparecerá aqui.';
        previewNome.textContent = nome;
        // Converte \n em <br> para o preview
        previewDescricao.innerHTML = desc
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/\n/g, '<br>');
    }

    let arquivosAcumulados = new DataTransfer();
    let shouldProcessNewFiles = false;

    function syncFileInput() {
        try {
            imagensInput.files = arquivosAcumulados.files;
        } catch (error) {
            console.warn('Não foi possível sincronizar imagensInput.files:', error);
        }
    }

    function removeAccumulatedFile(index) {
        const files = Array.from(arquivosAcumulados.files);
        arquivosAcumulados = new DataTransfer();
        files.forEach((file, fileIndex) => {
            if (fileIndex !== index) {
                arquivosAcumulados.items.add(file);
            }
        });
        syncFileInput();
        updateImagePreview();
    }

    function setMainAccumulatedFile(index) {
        const files = Array.from(arquivosAcumulados.files);
        if (index < 0 || index >= files.length) return;
        const selectedFile = files.splice(index, 1)[0];
        arquivosAcumulados = new DataTransfer();
        arquivosAcumulados.items.add(selectedFile);
        files.forEach(file => arquivosAcumulados.items.add(file));
        syncFileInput();
        updateImagePreview();
    }

    function renderSelectedFiles(existingCount, totalAllowed, accumulatedFiles) {
        const lista = document.getElementById('imagens-lista');
        let html = `<p style="margin-top: 0; font-size: 12px; color: #666;">Imagens novas (${accumulatedFiles.length}/` + (totalAllowed - existingCount) + `), total ${existingCount + accumulatedFiles.length}/${totalAllowed}:</p><ul style="list-style: none; padding: 0; margin: 5px 0;">`;
        accumulatedFiles.forEach((file, index) => {
            html += `<li class="imagem-nova-item" style="display:flex; align-items:center; justify-content:space-between; padding: 8px 0; border-bottom: 1px solid #eee; gap:10px;">
                <span style="flex:1; min-width:0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${index + 1}. ${file.name}</span>
                <div style="display:flex; gap:6px;">
                    <button type="button" class="btn-remove-image" data-index="${index}" style="padding:5px 8px; font-size:12px; border:1px solid #D32F2F; background:white; color:#D32F2F; border-radius:8px;">✕</button>
                    <button type="button" class="btn-main-image" data-index="${index}" style="padding:5px 8px; font-size:12px; border:1px solid #4A4A4A; background:white; color:#4A4A4A; border-radius:8px;">Principal</button>
                </div>
            </li>`;
        });
        html += '</ul>';
        lista.innerHTML = html;
        lista.querySelectorAll('.btn-remove-image').forEach(button => {
            button.addEventListener('click', function() {
                removeAccumulatedFile(Number(this.dataset.index));
            });
        });
        lista.querySelectorAll('.btn-main-image').forEach(button => {
            button.addEventListener('click', function() {
                setMainAccumulatedFile(Number(this.dataset.index));
            });
        });
    }

    function getExistingImagesCount() {
        const checkboxes = document.querySelectorAll('input[name="deletar_imagem"]');
        let count = 0;
        checkboxes.forEach(checkbox => {
            if (!checkbox.checked) {
                count++;
            }
        });
        return count;
    }

    function buildFileKey(file) {
        return `${file.name}_${file.size}_${file.lastModified}`;
    }

    function addFilesFromInput(existingCount) {
        const totalAllowed = 3;
        const selectedFiles = Array.from(imagensInput.files);
        const currentFiles = Array.from(arquivosAcumulados.files);
        const remainingSlots = totalAllowed - existingCount - currentFiles.length;

        if (remainingSlots <= 0) {
            imagensInput.value = '';
            return;
        }

        selectedFiles.some(file => {
            const fileKey = buildFileKey(file);
            const isDuplicate = currentFiles.some(existing => buildFileKey(existing) === fileKey);
            if (!isDuplicate && arquivosAcumulados.files.length < totalAllowed - existingCount) {
                arquivosAcumulados.items.add(file);
            }
            return arquivosAcumulados.files.length >= totalAllowed - existingCount;
        });

        syncFileInput();
    }

    function updateImagePreview() {
        const lista = document.getElementById('imagens-lista');
        const existingCount = getExistingImagesCount();
        const totalAllowed = 3;

        lista.innerHTML = '';

        if (shouldProcessNewFiles) {
            addFilesFromInput(existingCount);
            shouldProcessNewFiles = false;
        }

        const accumulatedFiles = Array.from(arquivosAcumulados.files);
        const totalSelected = existingCount + accumulatedFiles.length;

        if (totalSelected > totalAllowed) {
            lista.innerHTML = '<p style="color: #D32F2F; font-weight: bold;">⚠️ Máximo de 3 imagens no total. Ajuste as imagens atuais ou novas.</p>';
            return;
        }

        if (accumulatedFiles.length > 0) {
            const imageUrls = [];
            let loadedCount = 0;

            accumulatedFiles.forEach((file, index) => {
                const reader = new FileReader();
                reader.onload = function(e) {
                    imageUrls[index] = e.target.result;
                    loadedCount++;

                    if (loadedCount === accumulatedFiles.length) {
                        previewImgPrincipal.src = imageUrls[0] || '{% static "images/img-visao.jpg" %}';
                        miniaturas.forEach((img, miniIndex) => {
                            img.src = imageUrls[miniIndex] || '{% static "images/img-visao.jpg" %}';
                        });
                    }
                };
                reader.readAsDataURL(file);
            });

            renderSelectedFiles(existingCount, totalAllowed, accumulatedFiles);
        } else if (existingCount > 0) {
            lista.innerHTML = `<p style="margin-top: 0; font-size: 12px; color: #666;">Imagens atuais não removidas: ${existingCount}/${totalAllowed}. Você pode adicionar até ${totalAllowed - existingCount} novas.</p>`;
            previewImgPrincipal.src = '{% static "images/img-visao.jpg" %}';
            miniaturas.forEach(img => img.src = '{% static "images/img-visao.jpg" %}');
        } else {
            lista.innerHTML = '<p style="margin-top: 0; font-size: 12px; color: #666;">Nenhuma imagem selecionada.</p>';
            previewImgPrincipal.src = '{% static "images/img-visao.jpg" %}';
            miniaturas.forEach(img => img.src = '{% static "images/img-visao.jpg" %}');
        }
    }

    nomeInput.addEventListener('input', updatePreview);
    descricaoInput.addEventListener('input', updatePreview);
    imagensInput.addEventListener('change', function() {
        shouldProcessNewFiles = true;
        updateImagePreview();
    });
    document.querySelectorAll('input[name="deletar_imagem"]').forEach(checkbox => {
        checkbox.addEventListener('change', updateImagePreview);
    });

    // Initial update
    updatePreview();
    updateImagePreview();
});

document.getElementsByClassName("voltar-categoria-voltar-categoria-inline")[0].addEventListener("click", function(){
    window.location.href = this.dataset.url;
});