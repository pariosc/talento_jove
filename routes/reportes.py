from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from config.conexionDB import get_conexion

# Si en tu main.py no usas prefijo, puedes agregarlo aquí: router = APIRouter(prefix="/reportes")
router = APIRouter()

class ReporteSeguimiento(BaseModel):
    PK_id_postulacion: int
    nombre_estudiante: str
    semestre: Optional[int]
    habilidades: Optional[str]
    nombre_carrera: Optional[str]
    oferta_aplicada: str
    empresa: str
    sector_empresa: Optional[str]
    fecha_postulacion: Optional[date]
    estado_proceso: str
    
    class Config:
        from_attributes = True

class ReporteRendimientoOfertas(BaseModel):
    PK_id_empresa: int
    nombre_comercial: str
    PK_id_oferta: int
    titulo_oferta: str
    oferta_activa: bool
    fecha_limite: date
    total_postulantes: int
    pendientes: int
    en_entrevista: int
    seleccionados: int
    
    class Config:
        from_attributes = True

class ReporteEfectividadAcademica(BaseModel):
    nombre_carrera: Optional[str]
    total_estudiantes_registrados: int
    total_postulaciones_realizadas: int
    pasantias_conseguidas: int
    porcentaje_exito: float
    
    class Config:
        from_attributes = True

@router.get("/seguimiento_talento", response_model=List[ReporteSeguimiento])
async def obtener_seguimiento_talento(conn = Depends(get_conexion)):
    consulta = 'SELECT * FROM vw_seguimiento_talento'
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta)
            return await cursor.fetchall()
    except Exception as e:
        print(f"Error en reporte de seguimiento: {e}")
        raise HTTPException(status_code=400, detail="Error al generar el reporte de seguimiento")

@router.get("/rendimiento_ofertas", response_model=List[ReporteRendimientoOfertas])
async def obtener_rendimiento_ofertas(conn = Depends(get_conexion)):
    consulta = 'SELECT * FROM vw_rendimiento_ofertas'
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta)
            return await cursor.fetchall()
    except Exception as e:
        print(f"Error en reporte de rendimiento: {e}")
        raise HTTPException(status_code=400, detail="Error al generar el reporte de rendimiento")

@router.get("/efectividad_academica", response_model=List[ReporteEfectividadAcademica])
async def obtener_efectividad_academica(conn = Depends(get_conexion)):
    consulta = 'SELECT * FROM vw_efectividad_academica'
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(consulta)
            return await cursor.fetchall()
    except Exception as e:
        print(f"Error en reporte de efectividad: {e}")
        raise HTTPException(status_code=400, detail="Error al generar el reporte de efectividad")