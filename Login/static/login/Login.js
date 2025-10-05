// Login/static/login/Login.js
document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector("form");
    const carnetInput = document.getElementById("carnet");
    const contrasenaInput = document.getElementById("contrasena");

    // Contenedor para errores
    const errorContainer = document.createElement("p");
    errorContainer.style.color = "red";
    errorContainer.style.textAlign = "center"; 
    form.appendChild(errorContainer);

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        try {
            const response = await fetch("/login_usuario/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ 
                    carnet: carnetInput.value, 
                    contrasena: contrasenaInput.value 
                })
            });

            const data = await response.json();

            if (data.success) { // Redirigir según rol
                
                switch(data.rol) {
                    case "alumno": window.location.href = "/vista_alumno/"; break;
                    case "maestro": window.location.href = "/vista_maestro/"; break; 
                    case "admin": window.location.href = "/vista_admin/"; break;
                }
                
            } else {
               errorContainer.innerHTML = "<br> Carnet o contraseña incorrectos.<br>Intenta nuevamente.";
            }

        } catch (error) {
            console.error("Error al hacer login:", error);
            errorContainer.textContent = "Ocurrió un error al conectarse con el servidor.";
        }
    });

});
