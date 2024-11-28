document.addEventListener("DOMContentLoaded", function () {
    // Selección de los botones y menús
    const menuButton = document.getElementById("menuButton");
    const menuDropdown = document.getElementById("menuDropdown");

    const formularioButton = document.getElementById("formularioButton");
    const formularioDropdown = document.getElementById("formularioDropdown");

    // Lógica para el botón y menú principal
    menuButton.addEventListener("click", function () {
        menuDropdown.classList.toggle("show");
        formularioDropdown.classList.remove("show"); // Cierra el formulario si está abierto
    });

    // Lógica para el botón y menú del formulario
    formularioButton.addEventListener("click", function () {
        formularioDropdown.classList.toggle("show");
        menuDropdown.classList.remove("show"); // Cierra el menú principal si está abierto
    });

    // Cerrar menús si se hace clic fuera de ellos
    window.addEventListener("click", function (event) {
        if (!event.target.matches("#menuButton") && !event.target.matches("#formularioButton")) {
            menuDropdown.classList.remove("show");
            formularioDropdown.classList.remove("show");
        }
    });
});
