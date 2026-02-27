from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from config.conexionDB import get_conexion

router = APIRouter()

# Modelo adaptado a la tabla PERSONAS de Talento Joven
class Persona(BaseModel):
    PK_id_persona: int
    FK_id_usuario: int
    nombres: str
    apellidos: str
    ci: str
    telefono: str
    foto_perfil: Optional[str] = None
    semestre: int
    habilidades: Optional[str] = None
    experiencia_prev: Optional[str] = None

    class Config:
        from_attributes = True

@router.get("/")
async def listar(conn = Depends(get_conexion)):
    print("Listando personas")
    # Ajustado a los nombres de columna de tu nueva BD
    consulta = """SELECT "PK_id_persona", "FK_id_usuario", "nombres", "apellidos", "ci", 
                         "telefono", "foto_perfil", "semestre", "habilidades", "experiencia_prev" 
                  FROM "PERSONAS" """
    try:            
        async with conn.cursor() as cursor:
            await cursor.execute(consulta)
            return await cursor.fetchall()
    except Exception as e:
        print(f"Error listado: {e}")
        raise HTTPException(status_code=400, detail="Error al consultar la lista de personas")

@router.get("/{id_persona}")
async def get_persona(id_persona: int, conn = Depends(get_conexion)):     
    consulta = 'SELECT * FROM "PERSONAS" WHERE "PK_id_persona" = %s'
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, (id_persona,))
            result = await cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Persona no encontrada")
            return result
    except Exception as e:
        print(f"Error al obtener persona: {e}")
        raise HTTPException(status_code=400, detail="Error en la consulta")

@router.post("/")
async def insert_persona(persona: Persona, conn = Depends(get_conexion)):
    consulta = """INSERT INTO "PERSONAS" ("PK_id_persona", "FK_id_usuario", "nombres", "apellidos", "ci", 
                                       "telefono", "foto_perfil", "semestre", "habilidades", "experiencia_prev") 
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    parametros = (persona.PK_id_persona, persona.FK_id_usuario, persona.nombres, persona.apellidos, 
                  persona.ci, persona.telefono, persona.foto_perfil, persona.semestre, 
                  persona.habilidades, persona.experiencia_prev)
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            await conn.commit()
            return {"mensaje": "Registro en Talento Joven exitoso"}
    except Exception as e:
        print(f"Error al registrar: {e}")
        raise HTTPException(status_code=400, detail="No se pudo completar el registro")

@router.put("/{id_persona}")
async def update_persona(id_persona: int, persona: Persona, conn = Depends(get_conexion)):
    consulta = """UPDATE "PERSONAS" SET "nombres"=%s, "apellidos"=%s, "ci"=%s, "telefono"=%s, 
                         "foto_perfil"=%s, "semestre"=%s, "habilidades"=%s, "experiencia_prev"=%s 
                  WHERE "PK_id_persona" = %s"""
    parametros = (persona.nombres, persona.apellidos, persona.ci, persona.telefono, 
                  persona.foto_perfil, persona.semestre, persona.habilidades, 
                  persona.experiencia_prev, id_persona)
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Persona no encontrada")
            await conn.commit()
            return {"mensaje": "Perfil actualizado correctamente"}
    except Exception as e:
        print(f"Error al actualizar: {e}")
        raise HTTPException(status_code=400, detail="Error al actualizar datos")

@router.delete("/{id_persona}")
async def delete_persona(id_persona: int, conn = Depends(get_conexion)):
    consulta = 'DELETE FROM "PERSONAS" WHERE "PK_id_persona" = %s'
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, (id_persona,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Persona no encontrada")
            await conn.commit()
            return {"mensaje": "Registro eliminado"}
    except Exception as e:
        print(f"Error al eliminar: {e}")
        raise HTTPException(status_code=400, detail="No se pudo eliminar el registro")