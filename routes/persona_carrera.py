from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from datetime import date
from typing import Optional
from config.conexionDB import get_conexion

router = APIRouter()

# Modelo para la relación PERSONAS_CARRERAS
class PersonaCarrera(BaseModel):
    FK_id_persona: int
    FK_id_carrera: int
    fecha_vinculacion: Optional[date] = None
    estado_academico: str # Ejemplo: 'Regular', 'Egresado', 'Graduado'

    class Config:
        from_attributes = True

@router.get("/")
async def listar_vinculaciones(conn = Depends(get_conexion)):
    # Traemos los datos cruzados para que sea más informativo
    consulta = """
        SELECT pc."FK_id_persona", p."nombres", p."apellidos", 
               c."nombre_carrera", pc."estado_academico"
        FROM "PERSONAS_CARRERAS" pc
        JOIN "PERSONAS" p ON pc."FK_id_persona" = p."PK_id_persona"
        JOIN "CARRERAS" c ON pc."FK_id_carrera" = c."PK_id_persona_carrera"
    """
    try:            
        async with conn.cursor() as cursor:
            await cursor.execute(consulta)
            return await cursor.fetchall()
    except Exception as e:
        print(f"Error listado vinculaciones: {e}")
        raise HTTPException(status_code=400, detail="Error al consultar las carreras de los estudiantes")

@router.post("/")
async def vincular_persona_carrera(pc: PersonaCarrera, conn = Depends(get_conexion)):
    consulta = """
        INSERT INTO "PERSONAS_CARRERAS"("FK_id_persona", "FK_id_carrera", "fecha_vinculacion", "estado_academico") 
        VALUES(%s, %s, %s, %s)
    """
    parametros = (pc.FK_id_persona, pc.FK_id_carrera, pc.fecha_vinculacion or date.today(), pc.estado_academico)
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            await conn.commit()
            return {"mensaje": "Carrera vinculada exitosamente al estudiante"}
    except Exception as e:
        print(f"Error al vincular: {e}")
        raise HTTPException(status_code=400, detail="No se pudo realizar la vinculación (verifique si el ID de persona o carrera existen)")

@router.delete("/{id_persona}/{id_carrera}")
async def eliminar_vinculacion(id_persona: int, id_carrera: int, conn = Depends(get_conexion)):
    consulta = 'DELETE FROM "PERSONAS_CARRERAS" WHERE "FK_id_persona" = %s AND "FK_id_carrera" = %s'
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, (id_persona, id_carrera))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Vinculación no encontrada")
            await conn.commit()
            return {"mensaje": "Vinculación eliminada"}
    except Exception as e:
        print(f"Error al eliminar vinculación: {e}")
        raise HTTPException(status_code=400, detail="Error al procesar la eliminación")