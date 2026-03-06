// front/js/usuario_get.js
const API_URL = "http://127.0.0.1:8000/usuarios"; 

// Variable global para controlar el Modal de Bootstrap
let modalUsuario;

document.addEventListener("DOMContentLoaded", () => {
    // Inicializamos el modal de Bootstrap para poder abrirlo/cerrarlo con JS
    modalUsuario = new bootstrap.Modal(document.getElementById('modalUsuario'));
    cargarUsuarios(); // Cargamos la tabla al iniciar
});

// ==========================================
// 1. LEER (GET) - Lista todos los usuarios
// ==========================================
async function cargarUsuarios() {
    try {
        const respuesta = await fetch(API_URL);
        const usuarios = await respuesta.json();
        const tablaBody = document.getElementById("tabla-usuarios");
        tablaBody.innerHTML = ""; 

        usuarios.forEach(usuario => {
            const fila = document.createElement("tr");
            const textoEstado = usuario.estado ? "Activo" : "Inactivo";
            const claseEstado = usuario.estado ? "bg-success" : "bg-danger";
            
            fila.innerHTML = `
                <td>${usuario.PK_id_usuario}</td>
                <td class="fw-bold">${usuario.email}</td>
                <td><span class="badge bg-secondary">Rol: ${usuario.FK_id_rol}</span></td>
                <td><span class="badge ${claseEstado}">${textoEstado}</span></td>
                <td>
                    <button class="btn btn-sm btn-outline-primary" title="Editar" onclick="abrirModalEditar(${usuario.PK_id_usuario})">
                        <i class="bi bi-pencil-square"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" title="Eliminar" onclick="eliminarUsuario(${usuario.PK_id_usuario})">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            `;
            tablaBody.appendChild(fila);
        });
    } catch (error) {
        console.error("Error al cargar:", error);
    }
}

// ==========================================
// 2. CREAR / ACTUALIZAR (POST / PUT)
// ==========================================

// Prepara el formulario vacío para crear uno nuevo
function abrirModalCrear() {
    document.getElementById("formUsuario").reset(); // Limpia los campos
    document.getElementById("usuario_id").value = ""; // Borra el ID oculto
    document.getElementById("modalUsuarioLabel").innerText = "Nuevo Usuario";
    modalUsuario.show();
}

// Guarda los datos (sirve para Crear y para Editar)
async function guardarUsuario(event) {
    event.preventDefault(); // Evita que la página se recargue al enviar el formulario

    const id = document.getElementById("usuario_id").value;
    
    // Armamos el objeto con los datos del formulario (Igual a tu Pydantic 'UsuarioCreate')
    const datosUsuario = {
        FK_id_rol: parseInt(document.getElementById("rol").value),
        email: document.getElementById("email").value,
        password: document.getElementById("password").value,
        estado: document.getElementById("estado").checked
        // Nota: No enviamos fecha_registro porque en tu backend pusiste que se ponga por defecto (date.today())
    };

    // Si hay un ID, es un PUT (Actualizar). Si no hay ID, es un POST (Crear).
    const metodo = id ? "PUT" : "POST";
    const urlFina = id ? `${API_URL}/${id}` : API_URL;

    try {
        const respuesta = await fetch(urlFina, {
            method: metodo,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(datosUsuario)
        });

        if (respuesta.ok) {
            modalUsuario.hide(); // Cerramos el modal
            cargarUsuarios();    // Recargamos la tabla para ver los cambios
            alert(id ? "Usuario actualizado correctamente" : "Usuario creado exitosamente");
        } else {
            const error = await respuesta.json();
            alert("Error: " + error.detail);
        }
    } catch (error) {
        console.error("Error al guardar:", error);
        alert("Error de conexión con el servidor");
    }
}

// ==========================================
// 3. EDITAR - Obtiene 1 usuario y llena el modal
// ==========================================
async function abrirModalEditar(id) {
    try {
        const respuesta = await fetch(`${API_URL}/${id}`);
        const usuario = await respuesta.json();

        // Llenamos el formulario con los datos de la base de datos
        document.getElementById("usuario_id").value = usuario.PK_id_usuario;
        document.getElementById("email").value = usuario.email;
        document.getElementById("rol").value = usuario.FK_id_rol;
        document.getElementById("estado").checked = usuario.estado;
        
        // La contraseña por seguridad no suele devolverse, pero la dejamos vacía o requerimos que la vuelva a escribir
        document.getElementById("password").value = ""; 

        document.getElementById("modalUsuarioLabel").innerText = "Editar Usuario";
        modalUsuario.show(); // Mostramos el modal
    } catch (error) {
        console.error("Error al obtener usuario:", error);
    }
}

// ==========================================
// 4. ELIMINAR (DELETE)
// ==========================================
async function eliminarUsuario(id) {
    // Pedimos confirmación antes de borrar
    if (confirm("¿Estás seguro de que deseas eliminar este usuario? Esta acción no se puede deshacer.")) {
        try {
            const respuesta = await fetch(`${API_URL}/${id}`, {
                method: "DELETE"
            });

            if (respuesta.ok) {
                cargarUsuarios(); // Recargamos la tabla
            } else {
                const error = await respuesta.json();
                alert("Error al eliminar: " + error.detail);
            }
        } catch (error) {
            console.error("Error al eliminar:", error);
        }
    }
}