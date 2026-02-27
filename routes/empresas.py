from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from config.conexionDB import get_conexion 

router = APIRouter()

# Modelo adaptado a la tabla EMPRESAS
class Empresa(BaseModel):
    PK_id_empresa: int
    FK_id_usuario: int
    FK_id_sector: int
    nombre_comercial: str
    nit: str
    persona_contacto: str
    logo_empresa: Optional[str] = None
    ubicacion: str
    descripcion_empresa: Optional[str] = None

@router.get("/")
async def listar_empresas(conn = Depends(get_conexion)):
    # Usamos comillas dobles para respetar las mayúsculas de tu esquema SQL
    consulta = """SELECT "PK_id_empresa", "FK_id_usuario", "FK_id_sector", "nombre_comercial", 
                         "nit", "persona_contacto", "ubicacion" FROM "EMPRESAS" """
    try:            
        async with conn.cursor() as cursor:
            await cursor.execute(consulta)
            return await cursor.fetchall()
    except Exception as e:
        print(f"Error listado empresas: {e}")
        raise HTTPException(status_code=400, detail="Error al obtener la lista de empresas")

@router.get("/{id_empresa}")
async def get_empresa(id_empresa: int, conn = Depends(get_conexion)):     
    consulta = 'SELECT * FROM "EMPRESAS" WHERE "PK_id_empresa" = %s'
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, (id_empresa,))
            resultado = await cursor.fetchone()
            if not resultado:
                raise HTTPException(status_code=404, detail="Empresa no encontrada")
            return resultado
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/")
async def insert_empresa(empresa: Empresa, conn = Depends(get_conexion)):
    consulta = """INSERT INTO "EMPRESAS" ("PK_id_empresa", "FK_id_usuario", "FK_id_sector", 
                  "nombre_comercial", "nit", "persona_contacto", "ubicacion", "descripcion_empresa") 
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    parametros = (empresa.PK_id_empresa, empresa.FK_id_usuario, empresa.FK_id_sector, 
                  empresa.nombre_comercial, empresa.nit, empresa.persona_contacto, 
                  empresa.ubicacion, empresa.descripcion_empresa)
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            await conn.commit()
            return {"mensaje": "Empresa registrada exitosamente"}
    except Exception as e:
        print(f"Error al registrar: {e}")
        raise HTTPException(status_code=400, detail="Error en el registro, verifique los IDs de usuario y sector")

@router.put("/{id_empresa}")
async def update_empresa(id_empresa: int, empresa: Empresa, conn = Depends(get_conexion)):
    consulta = """UPDATE "EMPRESAS" SET "FK_id_sector"=%s, "nombre_comercial"=%s, "nit"=%s, 
                  "persona_contacto"=%s, "ubicacion"=%s, "descripcion_empresa"=%s 
                  WHERE "PK_id_empresa" = %s"""
    parametros = (empresa.FK_id_sector, empresa.nombre_comercial, empresa.nit, 
                  empresa.persona_contacto, empresa.ubicacion, empresa.descripcion_empresa, id_empresa)
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Empresa no encontrada")
            await conn.commit()
            return {"mensaje": "Datos de empresa actualizados"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id_empresa}")
async def delete_empresa(id_empresa: int, conn = Depends(get_conexion)):
    consulta = 'DELETE FROM "EMPRESAS" WHERE "PK_id_empresa" = %s'
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, (id_empresa,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Empresa no encontrada")
            await conn.commit()
            return {"mensaje": "Empresa eliminada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="No se puede eliminar la empresa (puede tener ofertas activas)")