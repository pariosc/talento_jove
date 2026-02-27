from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from config.conexionDB import get_conexion

router = APIRouter()

# Modelo adaptado a la tabla CARRERAS
class Carrera(BaseModel):
    PK_id_persona_carrera: int
    nombre_carrera: str

    class Config:
        from_attributes = True

@router.get("/")
async def listar_carreras(conn = Depends(get_conexion)):
    # Usamos comillas dobles para respetar las mayúsculas de tu script SQL
    consulta = 'SELECT "PK_id_persona_carrera", "nombre_carrera" FROM "CARRERAS"'
    try:            
        async with conn.cursor() as cursor:
            await cursor.execute(consulta)
            return await cursor.fetchall()
    except Exception as e:
        print(f"Error listado carreras: {e}")
        raise HTTPException(status_code=400, detail="Ocurrio un error al listar las carreras")

@router.get("/{id_carrera}")
async def get_carrera(id_carrera: int, conn = Depends(get_conexion)):     
    consulta = 'SELECT "PK_id_persona_carrera", "nombre_carrera" FROM "CARRERAS" WHERE "PK_id_persona_carrera" = %s'
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, (id_carrera,))
            result = await cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Carrera no encontrada")
            return result
    except Exception as e:
        print(f"Error al obtener carrera: {e}")
        raise HTTPException(status_code=400, detail="Error en la consulta de carrera")

@router.post("/")
async def insert_carrera(carrera: Carrera, conn = Depends(get_conexion)):
    consulta = 'INSERT INTO "CARRERAS"("PK_id_persona_carrera", "nombre_carrera") VALUES(%s, %s)'
    parametros = (carrera.PK_id_persona_carrera, carrera.nombre_carrera)
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            await conn.commit()
            return {"mensaje": "Carrera registrada exitosamente"}
    except Exception as e:
        print(f"Error al registrar carrera: {e}")
        raise HTTPException(status_code=400, detail="No se pudo registrar la carrera")

@router.put("/{id_carrera}")
async def update_carrera(id_carrera: int, carrera: Carrera, conn = Depends(get_conexion)):
    consulta = 'UPDATE "CARRERAS" SET "nombre_carrera"=%s WHERE "PK_id_persona_carrera" = %s'
    parametros = (carrera.nombre_carrera, id_carrera)
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Carrera no encontrada")
            await conn.commit()
            return {"mensaje": "Carrera actualizada exitosamente"}
    except Exception as e:
        print(f"Error al actualizar carrera: {e}")
        raise HTTPException(status_code=400, detail="Error al actualizar los datos")

@router.delete("/{id_carrera}")
async def delete_carrera(id_carrera: int, conn = Depends(get_conexion)):
    consulta = 'DELETE FROM "CARRERAS" WHERE "PK_id_persona_carrera" = %s'
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, (id_carrera,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Carrera no encontrada")
            await conn.commit()
            return {"mensaje": "Carrera eliminada exitosamente"}
    except Exception as e:
        print(f"Error al eliminar carrera: {e}")
        raise HTTPException(status_code=400, detail="No se pudo eliminar la carrera")