from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from config.conexionDB import get_conexion

router = APIRouter()

class CarreraCreate(BaseModel):
    nombre_carrera: str

class Carrera(CarreraCreate):
    PK_id_persona_carrera: int

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
async def insert_carrera(carrera: CarreraCreate, conn = Depends(get_conexion)):
    consulta = 'INSERT INTO "CARRERAS"("nombre_carrera") VALUES(%s) RETURNING "PK_id_persona_carrera"'
    parametros = (carrera.nombre_carrera,)
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            row = await cursor.fetchone()
            await conn.commit()
            return {"mensaje": "Carrera registrada exitosamente", "id_carrera": row["PK_id_persona_carrera"]}
    except Exception as e:
        print(f"Error al registrar carrera: {e}")
        raise HTTPException(status_code=400, detail="No se pudo registrar la carrera")

@router.put("/{id_carrera}")
async def update_carrera(id_carrera: int, carrera: CarreraCreate, conn = Depends(get_conexion)):
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