from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from config.conexionDB import get_conexion

router = APIRouter()

# Modelos Pydantic para SECTORES
class SectorCreate(BaseModel):
    nombre_sector: str

class Sector(SectorCreate):
    PK_id_sector: int

    class Config:
        from_attributes = True

@router.get("/")
async def listar_sectores(conn = Depends(get_conexion)):
    consulta = 'SELECT "PK_id_sector", "nombre_sector" FROM "SECTORES"'
    try:            
        async with conn.cursor() as cursor:
            await cursor.execute(consulta)
            return await cursor.fetchall()
    except Exception as e:
        print(f"Error listado sectores: {e}")
        raise HTTPException(status_code=400, detail="Ocurrió un error al listar los sectores")

@router.get("/{id_sector}")
async def get_sector(id_sector: int, conn = Depends(get_conexion)):     
    consulta = 'SELECT "PK_id_sector", "nombre_sector" FROM "SECTORES" WHERE "PK_id_sector" = %s'
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, (id_sector,))
            result = await cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Sector no encontrado")
            return result
    except Exception as e:
        print(f"Error al obtener sector: {e}")
        raise HTTPException(status_code=400, detail="Error en la consulta de sector")

@router.post("/")
async def insert_sector(sector: SectorCreate, conn = Depends(get_conexion)):
    consulta = 'INSERT INTO "SECTORES"("nombre_sector") VALUES(%s) RETURNING "PK_id_sector"'
    parametros = (sector.nombre_sector,)
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            row = await cursor.fetchone()
            await conn.commit()
            return {"mensaje": "Sector registrado exitosamente", "id_sector": row["PK_id_sector"]}
    except Exception as e:
        print(f"Error al registrar sector: {e}")
        raise HTTPException(status_code=400, detail="No se pudo registrar el sector")

@router.put("/{id_sector}")
async def update_sector(id_sector: int, sector: SectorCreate, conn = Depends(get_conexion)):
    consulta = 'UPDATE "SECTORES" SET "nombre_sector"=%s WHERE "PK_id_sector" = %s'
    parametros = (sector.nombre_sector, id_sector)
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Sector no encontrado")
            await conn.commit()
            return {"mensaje": "Sector actualizado exitosamente"}
    except Exception as e:
        print(f"Error al actualizar sector: {e}")
        raise HTTPException(status_code=400, detail="Error al actualizar los datos")

@router.delete("/{id_sector}")
async def delete_sector(id_sector: int, conn = Depends(get_conexion)):
    consulta = 'DELETE FROM "SECTORES" WHERE "PK_id_sector" = %s'
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, (id_sector,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Sector no encontrado")
            await conn.commit()
            return {"mensaje": "Sector eliminado exitosamente"}
    except Exception as e:
        print(f"Error al eliminar sector: {e}")
        raise HTTPException(status_code=400, detail="No se pudo eliminar el sector")