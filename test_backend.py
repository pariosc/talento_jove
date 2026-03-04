import requests
import random
import json
import time

# Asegúrate de que tu servidor esté corriendo en este puerto
BASE_URL = "http://localhost:8000"

def print_step(step, message):
    print(f"\n[{step}] {message}")

def assert_status(response, expected_code=200, context=""):
    if response.status_code != expected_code:
        print(f"   ❌ FALLÓ {context}: Código {response.status_code} - {response.text}")
        return False
    return True

def run_tests():
    print("🚀 Iniciando pruebas COMPLETAS del CRUD Talento Joven...\n")
    
    rand_suffix = random.randint(1000, 9999)
    ids = {} # Diccionario para guardar los IDs generados

    # ---------------------------------------------------------
    # 1. ROLES (CRUD)
    # ---------------------------------------------------------
    print_step("1", "Gestión de ROLES")
    
    # A. Crear un Rol de prueba para borrarlo luego
    res = requests.post(f"{BASE_URL}/roles/", json={"nombre_rol": f"RolTest_{rand_suffix}"})
    if assert_status(res, 200, "Crear Rol Test"):
        ids["rol_test"] = res.json()["id_rol"]
        print(f"   ✅ Rol creado (ID: {ids['rol_test']})")

    # B. Leer Rol
    if assert_status(requests.get(f"{BASE_URL}/roles/{ids['rol_test']}"), 200, "Leer Rol"):
        print(f"   ✅ Rol leído correctamente")

    # C. Actualizar Rol
    if assert_status(requests.put(f"{BASE_URL}/roles/{ids['rol_test']}", json={"nombre_rol": f"RolUpd_{rand_suffix}"}), 200, "Actualizar Rol"):
        print(f"   ✅ Rol actualizado")

    # D. Obtener/Crear Roles necesarios para el flujo (Postulante/Empresa)
    # (No borramos estos al final porque son estructurales)
    def get_or_create_rol(name):
        # Intentar crear, si falla asumimos que existe y buscamos su ID (simplificado)
        res = requests.post(f"{BASE_URL}/roles/", json={"nombre_rol": name})
        if res.status_code == 200:
            return res.json()["id_rol"]
        # Si ya existe, listamos para buscarlo
        all_roles = requests.get(f"{BASE_URL}/roles/").json()
        for r in all_roles:
            if r["nombre_rol"].lower() == name.lower():
                return r["PK_id_rol"]
        return 1 # Fallback

    ids["rol_postulante"] = get_or_create_rol("Postulante")
    ids["rol_empresa"] = get_or_create_rol("Empresa")
    print(f"   ℹ️  Roles base: Postulante={ids['rol_postulante']}, Empresa={ids['rol_empresa']}")

    # ---------------------------------------------------------
    # 2. SECTORES Y CARRERAS (CRUD)
    # ---------------------------------------------------------
    print_step("2", "Gestión de SECTORES y CARRERAS")

    # --- SECTOR ---
    res = requests.post(f"{BASE_URL}/sectores/", json={"nombre_sector": f"Tecnología {rand_suffix}"})
    if assert_status(res, 200, "Crear Sector"):
        ids["sector"] = res.json()["id_sector"]
        print(f"   ✅ Sector creado (ID: {ids['sector']})")
    
    requests.put(f"{BASE_URL}/sectores/{ids['sector']}", json={"nombre_sector": f"Tecnología Avanzada {rand_suffix}"})
    print("   ✅ Sector actualizado")

    # --- CARRERA ---
    res = requests.post(f"{BASE_URL}/carreras/", json={"nombre_carrera": f"Ing. Sistemas {rand_suffix}"})
    if assert_status(res, 200, "Crear Carrera"):
        ids["carrera"] = res.json()["id_carrera"]
        print(f"   ✅ Carrera creada (ID: {ids['carrera']})")

    requests.put(f"{BASE_URL}/carreras/{ids['carrera']}", json={"nombre_carrera": f"Ing. Software {rand_suffix}"})
    print("   ✅ Carrera actualizada")

    # ---------------------------------------------------------
    # 3. USUARIOS (CRUD)
    # ---------------------------------------------------------
    print_step("3", "Gestión de USUARIOS")
    
    # Usuario Postulante
    u_p_data = {"FK_id_rol": ids["rol_postulante"], "email": f"est_{rand_suffix}@test.com", "password": "123", "estado": True}
    res = requests.post(f"{BASE_URL}/usuarios/", json=u_p_data)
    if assert_status(res, 200, "Crear Usuario P"):
        ids["user_p"] = res.json()["id_usuario"]
        print(f"   ✅ Usuario Postulante creado (ID: {ids['user_p']})")

    # Usuario Empresa
    u_e_data = {"FK_id_rol": ids["rol_empresa"], "email": f"emp_{rand_suffix}@test.com", "password": "123", "estado": True}
    res = requests.post(f"{BASE_URL}/usuarios/", json=u_e_data)
    if assert_status(res, 200, "Crear Usuario E"):
        ids["user_e"] = res.json()["id_usuario"]
        print(f"   ✅ Usuario Empresa creado (ID: {ids['user_e']})")

    # Actualizar Usuario
    requests.put(f"{BASE_URL}/usuarios/{ids['user_p']}", json={**u_p_data, "password": "456"})
    print("   ✅ Usuario actualizado (password)")

    # ---------------------------------------------------------
    # 4. PERFILES (PERSONA Y EMPRESA)
    # ---------------------------------------------------------
    print_step("4", "Gestión de PERFILES")

    # --- PERSONA ---
    p_data = {"FK_id_usuario": ids["user_p"], "nombres": "Juan", "apellidos": f"Perez {rand_suffix}", 
              "ci": f"100{rand_suffix}", "telefono": "700123", "semestre": 5, "habilidades": "Python", "experiencia_prev": "Ninguna"}
    res = requests.post(f"{BASE_URL}/personas/", json=p_data)
    if assert_status(res, 200, "Crear Persona"):
        ids["persona"] = res.json()["id_persona"]
        print(f"   ✅ Perfil Persona creado (ID: {ids['persona']})")
    
    requests.put(f"{BASE_URL}/personas/{ids['persona']}", json={**p_data, "nombres": "Juan Actualizado"})
    print("   ✅ Perfil Persona actualizado")

    # --- EMPRESA ---
    e_data = {"FK_id_usuario": ids["user_e"], "FK_id_sector": ids["sector"], "nombre_comercial": f"Tech {rand_suffix}", 
              "nit": f"900{rand_suffix}", "persona_contacto": "Maria", "ubicacion": "Centro", "descripcion_empresa": "Dev"}
    res = requests.post(f"{BASE_URL}/empresas/", json=e_data)
    if assert_status(res, 200, "Crear Empresa"):
        ids["empresa"] = res.json()["id_empresa"]
        print(f"   ✅ Perfil Empresa creado (ID: {ids['empresa']})")

    requests.put(f"{BASE_URL}/empresas/{ids['empresa']}", json={**e_data, "nombre_comercial": f"Tech {rand_suffix} Inc."})
    print("   ✅ Perfil Empresa actualizado")

    # ---------------------------------------------------------
    # 5. VINCULACIÓN PERSONA-CARRERA
    # ---------------------------------------------------------
    print_step("5", "Vinculación ACADÉMICA")
    
    pc_data = {"FK_id_persona": ids["persona"], "FK_id_carrera": ids["carrera"], "estado_academico": "Estudiante"}
    if assert_status(requests.post(f"{BASE_URL}/persona-carrera/", json=pc_data), 200, "Vincular Carrera"):
        print("   ✅ Carrera vinculada al estudiante")

    pc_data["estado_academico"] = "Egresado"
    if assert_status(requests.put(f"{BASE_URL}/persona-carrera/{ids['persona']}/{ids['carrera']}", json=pc_data), 200, "Actualizar Vinculación"):
        print("   ✅ Estado académico actualizado")

    # ---------------------------------------------------------
    # 6. OFERTAS
    # ---------------------------------------------------------
    print_step("6", "Gestión de OFERTAS")
    
    o_data = {"FK_id_empresa": ids["empresa"], "titulo": "Dev Junior", "descripcion": "Backend", 
              "requisitos": "FastAPI", "fecha_limite": "2026-12-31", "estado": True}
    res = requests.post(f"{BASE_URL}/ofertas/", json=o_data)
    if assert_status(res, 200, "Crear Oferta"):
        ids["oferta"] = res.json()["id_oferta"]
        print(f"   ✅ Oferta publicada (ID: {ids['oferta']})")

    o_data["titulo"] = "Dev Junior Avanzado"
    requests.put(f"{BASE_URL}/ofertas/{ids['oferta']}", json=o_data)
    print("   ✅ Oferta actualizada")

    # ---------------------------------------------------------
    # 7. POSTULACIONES
    # ---------------------------------------------------------
    print_step("7", "Gestión de POSTULACIONES")
    
    post_data = {"FK_id_persona": ids["persona"], "FK_id_oferta": ids["oferta"], 
                 "mensaje_solicitud": "Hola", "estado_proceso": "Enviada"}
    res = requests.post(f"{BASE_URL}/postulaciones/", json=post_data)
    if assert_status(res, 200, "Crear Postulación"):
        ids["postulacion"] = res.json()["id_postulacion"]
        print(f"   ✅ Postulación realizada (ID: {ids['postulacion']})")

    # Actualizar estado (Endpoint especial con query param)
    if assert_status(requests.put(f"{BASE_URL}/postulaciones/{ids['postulacion']}/estado?nuevo_estado=Visto"), 200, "Actualizar Estado"):
        print("   ✅ Estado de postulación actualizado a 'Visto'")

    # ---------------------------------------------------------
    # 8. ELIMINACIÓN (CLEANUP)
    # ---------------------------------------------------------
    print_step("8", "ELIMINACIÓN (Limpieza de BD)")
    
    # El orden importa por las llaves foráneas
    if assert_status(requests.delete(f"{BASE_URL}/postulaciones/{ids['postulacion']}"), 200, "Del Postulación"):
        print("   🗑️  Postulación eliminada")
    
    if assert_status(requests.delete(f"{BASE_URL}/ofertas/{ids['oferta']}"), 200, "Del Oferta"):
        print("   🗑️  Oferta eliminada")

    if assert_status(requests.delete(f"{BASE_URL}/persona-carrera/{ids['persona']}/{ids['carrera']}"), 200, "Del Vinculación"):
        print("   🗑️  Vinculación eliminada")

    if assert_status(requests.delete(f"{BASE_URL}/empresas/{ids['empresa']}"), 200, "Del Empresa"):
        print("   🗑️  Empresa eliminada")

    if assert_status(requests.delete(f"{BASE_URL}/personas/{ids['persona']}"), 200, "Del Persona"):
        print("   🗑️  Persona eliminada")

    if assert_status(requests.delete(f"{BASE_URL}/usuarios/{ids['user_e']}"), 200, "Del Usuario E"):
        print("   🗑️  Usuario Empresa eliminado")

    if assert_status(requests.delete(f"{BASE_URL}/usuarios/{ids['user_p']}"), 200, "Del Usuario P"):
        print("   🗑️  Usuario Postulante eliminado")

    if assert_status(requests.delete(f"{BASE_URL}/carreras/{ids['carrera']}"), 200, "Del Carrera"):
        print("   🗑️  Carrera eliminada")

    if assert_status(requests.delete(f"{BASE_URL}/sectores/{ids['sector']}"), 200, "Del Sector"):
        print("   🗑️  Sector eliminado")

    if assert_status(requests.delete(f"{BASE_URL}/roles/{ids['rol_test']}"), 200, "Del Rol Test"):
        print("   🗑️  Rol de prueba eliminado")

    print("\n🎉 --- TEST COMPLETO FINALIZADO CON ÉXITO --- 🎉")

if __name__ == "__main__":
    try:
        run_tests()
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor. Asegúrate de que 'main.py' esté corriendo (uvicorn main:app --reload).")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
