from psycopg_pool import AsyncConnectionPool
from psycopg.rows import dict_row
from contextlib import asynccontextmanager
from .configuracion import config

DB_config = {
    "dbname": config.db_name,
    "user": config.db_user,
    "password": config.db_password,
    "host": config.db_host,
    "port": config.db_port
}

DB_URL = f"postgresql://{DB_config['user']}:{DB_config['password']}@{DB_config['host']}:{DB_config['port']}/{DB_config['dbname']}"
    
# 1. Declaramos la variable, pero NO creamos el pool todavía
async_pool = None

@asynccontextmanager
async def lifespan(app):
    global async_pool
    # 2. Creamos el pool AQUÍ ADENTRO. Esto lo ancla al motor correcto de FastAPI.
    async_pool = AsyncConnectionPool(conninfo=DB_URL, open=False)
    await async_pool.open()
    print("✅ Pool de conexiones abierto exitosamente (Motor sincronizado)")
    
    try:
        yield
    finally:
        # Se cierra al apagar la app
        if async_pool:
            await async_pool.close()
        print("🛑 Pool de conexiones cerrado")

# Dependencia para inyectar la conexión
async def get_conexion():
    try:
        if async_pool is None:
            raise Exception("El pool no está inicializado (lifespan no corrió)")
            
        async with async_pool.connection() as conn:
            conn.row_factory = dict_row
            yield conn
    except Exception as e:
        print(f"❌ Error al obtener conexión del pool: {e}")
        raise