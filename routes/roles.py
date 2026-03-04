from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from config.conexionDB import get_conexion

router = APIRouter()

class RolCreate(BaseModel):
    nombre_rol: str

class Rol(RolCreate):
    PK_id_rol: int

    class Config:
        from_attributes = True

@router.get("/")
async def listar_roles(conn = Depends(get_conexion)):
    # Usamos comillas dobles para respetar el esquema SQL
    consulta = 'SELECT "PK_id_rol", "nombre_rol" FROM "ROLES"'
    try:            
        async with conn.cursor() as cursor:
            await cursor.execute(consulta)
            return await cursor.fetchall()
    except Exception as e:
        print(f"Error listado roles: {e}")
        raise HTTPException(status_code=400, detail="Error al consultar los roles del sistema")

@router.get("/{id_rol}")
async def get_rol(id_rol: int, conn = Depends(get_conexion)):     
    consulta = 'SELECT "PK_id_rol", "nombre_rol" FROM "ROLES" WHERE "PK_id_rol" = %s'
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, (id_rol,))
            result = await cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Rol no encontrado")
            return result
    except Exception as e:
        print(f"Error al obtener rol: {e}")
        raise HTTPException(status_code=400, detail="Error en la consulta")

@router.post("/")
async def insert_rol(rol: RolCreate, conn = Depends(get_conexion)):
    consulta = 'INSERT INTO "ROLES"("nombre_rol") VALUES(%s) RETURNING "PK_id_rol"'
    parametros = (rol.nombre_rol,)
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            row = await cursor.fetchone()
            await conn.commit()
            return {"mensaje": "Nuevo rol registrado exitosamente", "id_rol": row["PK_id_rol"]}
    except Exception as e:
        print(f"Error al registrar rol: {e}")
        raise HTTPException(status_code=400, detail="No se pudo crear el rol (posible ID duplicado)")

@router.put("/{id_rol}")
async def update_rol(id_rol: int, rol: RolCreate, conn = Depends(get_conexion)):
    consulta = 'UPDATE "ROLES" SET "nombre_rol"=%s WHERE "PK_id_rol" = %s'
    parametros = (rol.nombre_rol, id_rol)
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Rol no encontrado")
            await conn.commit()
            return {"mensaje": "Rol actualizado correctamente"}
    except Exception as e:
        print(f"Error al actualizar rol: {e}")
        raise HTTPException(status_code=400, detail="Error al procesar la actualización")

@router.delete("/{id_rol}")
async def delete_rol(id_rol: int, conn = Depends(get_conexion)):
    consulta = 'DELETE FROM "ROLES" WHERE "PK_id_rol" = %s'
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, (id_rol,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Rol no encontrado")
            await conn.commit()
            return {"mensaje": "Rol eliminado exitosamente"}
    except Exception as e:
        print(f"Error al eliminar rol: {e}")
        # Error común: No se puede borrar si hay usuarios asignados a este rol
        raise HTTPException(status_code=400, detail="No se puede eliminar el rol porque tiene usuarios asociados")