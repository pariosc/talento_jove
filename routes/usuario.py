from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional
from config.conexionDB import get_conexion

router = APIRouter()

# Modelo adaptado a la tabla USUARIOS
class Usuario(BaseModel):
    PK_id_usuario: int
    FK_id_rol: int
    email: str
    password: str
    estado: bool
    fecha_registro: Optional[date] = None

    class Config:
        from_attributes = True

@router.get("/")
async def listar_usuarios(conn = Depends(get_conexion)):
    # Usamos comillas dobles para que PostgreSQL reconozca las mayúsculas
    consulta = 'SELECT "PK_id_usuario", "FK_id_rol", "email", "estado", "fecha_registro" FROM "USUARIOS"'
    try:            
        async with conn.cursor() as cursor:
            await cursor.execute(consulta)
            return await cursor.fetchall()
    except Exception as e:
        print(f"Error listado usuarios: {e}")
        raise HTTPException(status_code=400, detail="Error al consultar la lista de usuarios")

@router.get("/{id_usuario}")
async def get_usuario(id_usuario: int, conn = Depends(get_conexion)):     
    consulta = 'SELECT "PK_id_usuario", "FK_id_rol", "email", "estado", "fecha_registro" FROM "USUARIOS" WHERE "PK_id_usuario" = %s'
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, (id_usuario,))
            result = await cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            return result
    except Exception as e:
        print(f"Error al obtener usuario: {e}")
        raise HTTPException(status_code=400, detail="Error en la consulta")

@router.post("/")
async def insert_usuario(usuario: Usuario, conn = Depends(get_conexion)):
    # Nota: En una app real, aquí deberías hashear el password antes de insertar
    consulta = """INSERT INTO "USUARIOS"("PK_id_usuario", "FK_id_rol", "email", "password", "estado", "fecha_registro") 
                  VALUES(%s, %s, %s, %s, %s, %s)"""
    parametros = (usuario.PK_id_usuario, usuario.FK_id_rol, usuario.email, 
                  usuario.password, usuario.estado, usuario.fecha_registro or date.today())
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            await conn.commit()
            return {"mensaje": "Usuario creado exitosamente"}
    except Exception as e:
        print(f"Error al registrar usuario: {e}")
        raise HTTPException(status_code=400, detail="El email ya existe o hay un error en los datos")

@router.put("/{id_usuario}")
async def update_usuario(id_usuario: int, usuario: Usuario, conn = Depends(get_conexion)):
    consulta = """UPDATE "USUARIOS" SET "FK_id_rol"=%s, "email"=%s, "password"=%s, "estado"=%s 
                  WHERE "PK_id_usuario" = %s"""
    parametros = (usuario.FK_id_rol, usuario.email, usuario.password, usuario.estado, id_usuario)
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            await conn.commit()
            return {"mensaje": "Usuario actualizado correctamente"}
    except Exception as e:
        print(f"Error al actualizar usuario: {e}")
        raise HTTPException(status_code=400, detail="No se pudo actualizar el usuario")

@router.delete("/{id_usuario}")
async def delete_usuario(id_usuario: int, conn = Depends(get_conexion)):
    consulta = 'DELETE FROM "USUARIOS" WHERE "PK_id_usuario" = %s'
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, (id_usuario,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            await conn.commit()
            return {"mensaje": "Usuario eliminado"}
    except Exception as e:
        print(f"Error al eliminar usuario: {e}")
        raise HTTPException(status_code=400, detail="No se puede eliminar el usuario (posiblemente tiene perfiles asociados)")