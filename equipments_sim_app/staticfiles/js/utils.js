document.addEventListener("DOMContentLoaded", function () {
    // Inicializar tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Mostrar el año actual en el footer
    const yearSpan = document.createElement("span");
    yearSpan.textContent = new Date().getFullYear();
    const aboutTitle = document.querySelector(".about-tittle p");
    if (aboutTitle) {
        aboutTitle.appendChild(yearSpan);
    }
});

