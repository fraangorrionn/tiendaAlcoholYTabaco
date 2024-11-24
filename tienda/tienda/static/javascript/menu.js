document.addEventListener("DOMContentLoaded", function () {
    const menuButton = document.getElementById("menuButton");
    const menuDropdown = document.getElementById("menuDropdown");

    // Alternar visibilidad del menú al hacer clic en el botón
    menuButton.addEventListener("click", function () {
        menuDropdown.classList.toggle("show");
    });

    // Cerrar el menú si se hace clic fuera de él
    window.addEventListener("click", function (e) {
        if (!menuButton.contains(e.target) && !menuDropdown.contains(e.target)) {
            menuDropdown.classList.remove("show");
        }
    });
});
