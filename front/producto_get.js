// URL actualizada al endpoint de personas en tu FastAPI
const url = "http://localhost:8000/personas"; 

const contenedor = document.getElementById("data");

const cargaData = (datos) => {
    let resultado = '';
    for (let i = 0; i < datos.length; i++) {
        // Adaptamos los campos a la estructura de la tabla PERSONAS
        // Nota: En FastAPI con PostgreSQL, los nombres suelen venir como los definiste en el modelo
        resultado += `
            <li class="persona-card">
                <div class="info">
                    <h3>${datos[i].nombres} ${datos[i].apellidos}</h3>
                    <p><strong>CI:</strong> ${datos[i].ci}</p>
                    <p><strong>Teléfono:</strong> ${datos[i].telefono}</p>
                    <p><strong>Semestre:</strong> ${datos[i].semestre}°</p>
                    <p><strong>Habilidades:</strong> ${datos[i].habilidades || 'No registradas'}</p>
                    <p><strong>Experiencia:</strong> ${datos[i].experiencia_prev || 'Sin experiencia'}</p>
                </div>
            </li><hr>`;
    }
    contenedor.innerHTML = resultado;
}

fetch(url, {
    method: "GET",
    headers: {
        "Content-Type": "application/json"
    }
})
.then(response => {
    if (!response.ok) {
        throw new Error(`Error en la red: ${response.status}`);
    }
    return response.json();
})
.then(data => {
    console.log("Datos recibidos de Talento Joven:", data);
    cargaData(data);
})
.catch(error => {
    console.error("Error al obtener los perfiles:", error);
});