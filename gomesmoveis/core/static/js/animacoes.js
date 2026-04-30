const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visivel');
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.animar').forEach(el => observer.observe(el));

document.querySelectorAll('img').forEach(img => {
    if (img.complete) {
        img.classList.add('carregada');
    } else {
        img.addEventListener('load', () => img.classList.add('carregada'));
    }
});