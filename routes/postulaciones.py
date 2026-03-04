from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from datetime import date
from typing import Optional
from config.conexionDB import get_conexion

router = APIRouter()

class PostulacionCreate(BaseModel):
    FK_id_persona: int
    FK_id_oferta: int
    mensaje_solicitud: Optional[str] = None
    fecha_postulacion: Optional[date] = None
    estado_proceso: str # Ejemplo: 'Enviada', 'Visto', 'Rechazado', 'Seleccionado'

class Postulacion(PostulacionCreate):
    PK_id_postulacion: int

    class Config:
        from_attributes = True

@router.get("/")
async def listar_postulaciones(conn = Depends(get_conexion)):
    # Consulta con JOINs para ver quién postula a qué
    consulta = """
        SELECT pos."PK_id_postulacion", per."nombres", per."apellidos", 
               ofe."titulo" as oferta_titulo, emp."nombre_comercial" as empresa,
               pos."fecha_postulacion", pos."estado_proceso"
        FROM "POSTULACIONES" pos
        JOIN "PERSONAS" per ON pos."FK_id_persona" = per."PK_id_persona"
        JOIN "OFERTAS" ofe ON pos."FK_id_oferta" = ofe."PK_id_oferta"
        JOIN "EMPRESAS" emp ON ofe."FK_id_empresa" = emp."PK_id_empresa"
    """
    try:            
        async with conn.cursor() as cursor:
            await cursor.execute(consulta)
            return await cursor.fetchall()
    except Exception as e:
        print(f"Error al listar postulaciones: {e}")
        raise HTTPException(status_code=400, detail="Error al consultar las postulaciones")

@router.post("/")
async def crear_postulacion(postulacion: PostulacionCreate, conn = Depends(get_conexion)):
    consulta = """
        INSERT INTO "POSTULACIONES"("FK_id_persona", "FK_id_oferta", 
                                     "mensaje_solicitud", "fecha_postulacion", "estado_proceso") 
        VALUES(%s, %s, %s, %s, %s) RETURNING "PK_id_postulacion"
    """
    parametros = (
        postulacion.FK_id_persona, 
        postulacion.FK_id_oferta, 
        postulacion.mensaje_solicitud, 
        postulacion.fecha_postulacion or date.today(), 
        postulacion.estado_proceso
    )
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            row = await cursor.fetchone()
            await conn.commit()
            return {"mensaje": "Postulación enviada correctamente. ¡Mucho éxito!", "id_postulacion": row["PK_id_postulacion"]}
    except Exception as e:
        print(f"Error al postular: {e}")
        raise HTTPException(status_code=400, detail="No se pudo completar la postulación")

@router.put("/{id_postulacion}/estado")
async def actualizar_estado_postulacion(id_postulacion: int, nuevo_estado: str, conn = Depends(get_conexion)):
    # Este endpoint es útil para que la empresa cambie el estado (ej. de 'Enviada' a 'Visto')
    consulta = 'UPDATE "POSTULACIONES" SET "estado_proceso" = %s WHERE "PK_id_postulacion" = %s'
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, (nuevo_estado, id_postulacion))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Postulación no encontrada")
            await conn.commit()
            return {"mensaje": "Estado de postulación actualizado"}
    except Exception as e:
        print(f"Error al actualizar estado: {e}")
        raise HTTPException(status_code=400, detail="Error al actualizar el estado de la postulación")

@router.delete("/{id_postulacion}")
async def cancelar_postulacion(id_postulacion: int, conn = Depends(get_conexion)):
    consulta = 'DELETE FROM "POSTULACIONES" WHERE "PK_id_postulacion" = %s'
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, (id_postulacion,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Postulación no encontrada")
            await conn.commit()
            return {"mensaje": "Postulación retirada correctamente"}
    except Exception as e:
        print(f"Error al eliminar postulación: {e}")
        raise HTTPException(status_code=400, detail="Error al procesar la solicitud")