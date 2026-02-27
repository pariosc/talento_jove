from psycopg_pool import AsyncConnectionPool
from psycopg.rows import dict_row
from contextlib import asynccontextmanager

# URL de tu base de datos local
DB_URL = "postgresql://postgres:12345678@localhost:5432/talento_joven"

# Instanciamos el pool (sin abrirlo todavía)
async_pool = AsyncConnectionPool(conninfo=DB_URL, open=False)

@asynccontextmanager
async def lifespan(app):
    # Se abre el pool al iniciar la app
    await async_pool.open()
    print("✅ Pool de conexiones abierto exitosamente")
    try:
        yield
    finally:
        # Se cierra al apagar la app
        await async_pool.close()
        print("🛑 Pool de conexiones cerrado")

# Dependencia para inyectar la conexión
async def get_conexion():
    async with async_pool.connection() as conn:
        conn.row_factory = dict_row
        yield conn