from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from config.conexionDB import get_conexion 

router = APIRouter()

class EmpresaCreate(BaseModel):
    FK_id_usuario: int
    FK_id_sector: int
    nombre_comercial: str
    nit: str
    persona_contacto: str
    logo_empresa: Optional[str] = None
    ubicacion: str
    descripcion_empresa: Optional[str] = None

class Empresa(EmpresaCreate):
    PK_id_empresa: int

@router.get("/")
async def listar_empresas(conn = Depends(get_conexion)):
    # Usamos comillas dobles para respetar las mayúsculas de tu esquema SQL
    consulta = """SELECT "PK_id_empresa", "FK_id_usuario", "FK_id_sector", "nombre_comercial", 
                         "nit", "persona_contacto", "logo_empresa", "ubicacion", "descripcion_empresa" FROM "EMPRESAS" """
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
async def insert_empresa(empresa: EmpresaCreate, conn = Depends(get_conexion)):
    consulta = """INSERT INTO "EMPRESAS" ("FK_id_usuario", "FK_id_sector", 
                  "nombre_comercial", "nit", "persona_contacto", "logo_empresa", "ubicacion", "descripcion_empresa") 
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING "PK_id_empresa" """
    parametros = (empresa.FK_id_usuario, empresa.FK_id_sector, 
                  empresa.nombre_comercial, empresa.nit, empresa.persona_contacto, 
                  empresa.logo_empresa, empresa.ubicacion, empresa.descripcion_empresa)
    try:
        async with conn.cursor() as cursor:
            # 1. Validar el rol del usuario
            await cursor.execute("""
                SELECT r."nombre_rol" FROM "USUARIOS" u 
                JOIN "ROLES" r ON u."FK_id_rol" = r."PK_id_rol" 
                WHERE u."PK_id_usuario" = %s
            """, (empresa.FK_id_usuario,))
            
            rol_res = await cursor.fetchone()
            
            if not rol_res:
                raise HTTPException(status_code=404, detail=f"El usuario con ID {empresa.FK_id_usuario} no existe.")
            
            # ¡CORRECCIÓN 1! Usamos la llave del diccionario en lugar de [0]
            if rol_res["nombre_rol"].strip().lower() != "empresa":
                raise HTTPException(status_code=400, detail=f"El usuario tiene rol '{rol_res['nombre_rol']}', no puede crear un perfil de Empresa.")

            # 2. Insertar la empresa
            await cursor.execute(consulta, parametros)
            row = await cursor.fetchone()
            await conn.commit()
            
            # ¡CORRECCIÓN 2! Obtenemos el ID usando la llave de la columna
            return {"mensaje": "Empresa registrada exitosamente", "id_empresa": row["PK_id_empresa"]}
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error técnico de BD: {repr(e)}") # Agregué repr() para que en consola se vea el error real si vuelve a fallar
        raise HTTPException(status_code=400, detail=f"Error en la base de datos: {str(e)}")  
@router.put("/{id_empresa}")
async def update_empresa(id_empresa: int, empresa: EmpresaCreate, conn = Depends(get_conexion)):
    consulta = """UPDATE "EMPRESAS" SET "FK_id_sector"=%s, "nombre_comercial"=%s, "nit"=%s, 
                  "persona_contacto"=%s, "logo_empresa"=%s, "ubicacion"=%s, "descripcion_empresa"=%s 
                  WHERE "PK_id_empresa" = %s"""
    parametros = (empresa.FK_id_sector, empresa.nombre_comercial, empresa.nit, 
                  empresa.persona_contacto, empresa.logo_empresa, empresa.ubicacion, empresa.descripcion_empresa, id_empresa)
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