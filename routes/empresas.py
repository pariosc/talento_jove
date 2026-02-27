
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from config.conexionDB import get_conexion # Importamos desde config

router = APIRouter()

class Producto(BaseModel):
    id_producto: int
    id_tipo: int
    descripcion: str
    precio_compra: float
    precio_venta: float
    cantidad: int
    activo: bool

@router.get("/")
async def listar(conn = Depends(get_conexion)):
    consulta = "Select id_producto, id_tipo, descripcion, precio_compra, precio_venta, cantidad, activo from tproducto"
    try:            
        async with conn.cursor() as cursor:
            await cursor.execute(consulta)
            return await cursor.fetchall()
    except Exception as e:
        print(f"Error listado gral de Psycopg: {e}")
        raise HTTPException(status_code=400, detail="Ocurrio un error, consulte con su Administrador")
    
@router.get("/{id_producto}")
async def get_producto(id_producto: int, conn = Depends(get_conexion)):     
    consulta = "SELECT id_producto, id_tipo, descripcion, precio_compra, precio_venta, cantidad, activo FROM tproducto WHERE id_producto = %s"
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, (id_producto,))
            return await cursor.fetchone()
    except Exception as e:
        print(f"Error al obtener producto de Psycopg: {e}")
        raise HTTPException(status_code=400, detail="Ocurrio un error, consulte con su Administrador")

@router.post("/")
async def insert_producto(producto: Producto, conn = Depends(get_conexion)):
    consulta = """INSERT INTO tproducto(id_producto, id_tipo, descripcion, precio_compra, precio_venta, cantidad) VALUES(%s, %s, %s, %s, %s, %s)"""
    parametros = (producto.id_producto, producto.id_tipo, producto.descripcion, 
                  producto.precio_compra, producto.precio_venta, producto.cantidad)
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            await conn.commit()
            return {"mensaje": "Producto registrado exitosamente"}
    except Exception as e:
        print(f"Error al registrar producto de Psycopg: {e}")
        raise HTTPException(status_code=400, detail="Ocurrio un error, consulte con su Administrador")

@router.put("/{id_producto}")
async def update_producto(id_producto: int, producto: Producto, conn = Depends(get_conexion)):
    consulta = "UPDATE tproducto SET id_tipo=%s, descripcion=%s, precio_compra=%s, precio_venta=%s, cantidad=%s WHERE id_producto = %s"
    parametros = (producto.id_tipo, producto.descripcion, producto.precio_compra, producto.precio_venta, producto.cantidad, id_producto)
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, parametros)
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Producto no encontrado")
            await conn.commit()
            return {"mensaje": "Producto actualizado exitosamente"}
    except HTTPException:
        raise # Re-raise HTTP exceptions (like the 404 above)
    except Exception as e:
        print(f"Error al actualizar producto de Psycopg: {e}")
        raise HTTPException(status_code=400, detail="Ocurrio un error, consulte con su Administrador")

@router.delete("/{id_producto}")
async def delete_producto(id_producto: int, conn = Depends(get_conexion)):
    consulta = "DELETE FROM tproducto WHERE id_producto = %s"
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta, (id_producto,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Producto no encontrado")
            await conn.commit()
            return {"mensaje": "Producto eliminado exitosamente"}
    except HTTPException:
        raise  # Re-raise HTTP exceptions (like the 404 above)
    except Exception as e:
        print(f"Error al eliminar producto de Psycopg: {e}")
        raise HTTPException(status_code=400, detail="Ocurrio un error, consulte con su Administrador")