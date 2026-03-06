from fastapi import FastAPI
from routes import (
    persona, 
    empresas, 
    carrera,
    sector, 
    usuario, 
    ofertas, 
    roles, 
    persona_carrera, 
    postulaciones,
    reportes
)
from config.conexionDB import lifespan
from fastapi.middleware.cors import CORSMiddleware

# Inicialización de la API
app = FastAPI(
    title="Talento Joven - Backend API",
    description="Servicios backend para el portal de empleo UPDS",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configurado para permitir pruebas locales de la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- REGISTRO DE RUTAS EXCLUSIVAS DEL BACKEND ---

# Seguridad y Cuentas
app.include_router(roles.router, prefix="/roles", tags=["Seguridad"])
app.include_router(usuario.router, prefix="/usuarios", tags=["Seguridad"])

# Gestión de Perfiles
app.include_router(persona.router, prefix="/personas", tags=["Perfiles"])
app.include_router(empresas.router, prefix="/empresas", tags=["Perfiles"])

# Estructura Académica y Relaciones
app.include_router(carrera.router, prefix="/carreras", tags=["Académico"])
app.include_router(persona_carrera.router, prefix="/persona_carrera", tags=["Académico"])
app.include_router(sector.router, prefix="/sectores", tags=["Sectores"])

# Procesos de Selección
app.include_router(postulaciones.router, prefix="/postulaciones", tags=["Procesos"])
app.include_router(ofertas.router, prefix="/ofertas", tags=["Procesos"]) # <-- Cambié el tag a "Procesos"

# Reportes y Estadísticas
app.include_router(reportes.router, prefix="/reportes", tags=["Reportes"])


@app.get("/", tags=["Inicio"])
async def root():
    return {
        "proyecto": "Talento Joven",
        "estado": "Backend Operativo",
        "documentacion": "/docs"
    }