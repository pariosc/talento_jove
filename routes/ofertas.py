from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from datetime import date
from typing import Optional
from config.conexionDB import get_conexion

router = APIRouter()

class OfertaCreate(BaseModel):
    FK_id_empresa: int
    titulo: str
    descripcion: str
    requisitos: Optional[str] = None
    fecha_limite: date
    estado: bool

class Oferta(OfertaCreate):
    PK_id_oferta: int

    class Config:
        from_attributes = True

@router.get("/")
async def listar_ofertas(conn = Depends(get_conexion)):
    consulta = """
        SELECT o."PK_id_oferta", e."nombre_comercial", o."titulo", 
               o."descripcion", o."requisitos", o."fecha_limite", o."estado"
        FROM "OFERTAS" o
        JOIN "EMPRESAS" e ON o."FK_id_empresa" = e."PK_id_empresa"
        WHERE o."estado" = true
    """
    try:            
        async with conn.cursor() as cursor:
            await cursor.execute(consulta)
            return await cursor.fetchall()
    except Exception as e:
        print(f"Error listado ofertas: {e}")
        raise HTTPException(status_code=400, detail="Error al consultar vacantes")

@router.get("/{id_oferta}")
async def get_oferta(id_oferta: int, conn = Depends(get_conexion)):
    consulta = 'SELECT * FROM "OFERTAS" WHERE "PK_id_oferta" = %s'
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, (id_oferta,))
            result = await cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Oferta no encontrada")
            return result
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error al obtener la oferta")

@router.post("/")
async def crear_oferta(oferta: OfertaCreate, conn = Depends(get_conexion)):
    consulta = """
        INSERT INTO "OFERTAS"("FK_id_empresa", "titulo", 
                             "descripcion", "requisitos", "fecha_limite", "estado") 
        VALUES(%s, %s, %s, %s, %s, %s) RETURNING "PK_id_oferta"
    """
    parametros = (oferta.FK_id_empresa, oferta.titulo, 
                  oferta.descripcion, oferta.requisitos, oferta.fecha_limite, oferta.estado)
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            row = await cursor.fetchone()
            await conn.commit()
            return {"mensaje": "Oferta laboral publicada exitosamente", "id_oferta": row["PK_id_oferta"]}
    except Exception as e:
        print(f"Error al crear oferta: {e}")
        raise HTTPException(status_code=400, detail="No se pudo publicar la oferta")

@router.put("/{id_oferta}")
async def update_oferta(id_oferta: int, oferta: OfertaCreate, conn = Depends(get_conexion)):
    consulta = """UPDATE "OFERTAS" SET "FK_id_empresa"=%s, "titulo"=%s, 
                  "descripcion"=%s, "requisitos"=%s, "fecha_limite"=%s, "estado"=%s 
                  WHERE "PK_id_oferta" = %s"""
    parametros = (oferta.FK_id_empresa, oferta.titulo, 
                  oferta.descripcion, oferta.requisitos, oferta.fecha_limite, oferta.estado, id_oferta)
    print(f"ACTUALIZANDO OFERTA")

    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Oferta no encontrada")
            await conn.commit()
            return {"mensaje": "Oferta actualizada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error al actualizar la oferta")

@router.delete("/{id_oferta}")
async def eliminar_oferta(id_oferta: int, conn = Depends(get_conexion)):
    consulta = 'DELETE FROM "OFERTAS" WHERE "PK_id_oferta" = %s'
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, (id_oferta,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Oferta no encontrada")
            await conn.commit()
            return {"mensaje": "Oferta eliminada correctamente"}
    except Exception as e:
        print(f"Error al eliminar: {e}")
        raise HTTPException(status_code=400, detail="Error al procesar la solicitud")