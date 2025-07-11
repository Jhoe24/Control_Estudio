# archivo cargar_estudiantes.py - Carga masiva de datos de estudiantes
import sqlite3
import os

# --- DATOS DE EJEMPLO PARA 10 ESTUDIANTES ---
estudiantes_data = [
    {
        "personal": {
            "documento_identidad": "27123456", "nombres": "Ana María", "apellidos": "Pérez González",
            "fecha_nacimiento": "2002-05-15", "sexo": "F", "estado_civil": "Soltero",
            "correo_electronico": "ana.perez.g@email.com",
        },
        "telefonos": [
            {"tipo_telefono": "movil", "numero": "04141234567", "principal": True},
            {"tipo_telefono": "casa", "numero": "02735551234"},
        ],
        "direcciones": [{
            "estado": "Barinas", "municipio": "Barinas", "parroquia": "Alto Barinas", "sector": "Los Pomelos",
            "calle": "Avenida 2", "casa_edificio": "Casa 15-A", "direccion_completa": "Urb. Los Pomelos, Av. 2, Casa 15-A, Barinas",
            "tipo_direccion": "residencia", "principal": True
        }],
        "academico": {
            "codigo_unico": "E2022001", "codigo_estudiantil": "27123456-INF", "tipo_ingreso": "Nuevo",
            "cohorte": "2022-1", "situacion_academica": "Activo"
        }
    },
    {
        "personal": {
            "documento_identidad": "28789012", "nombres": "Carlos José", "apellidos": "Rodríguez Silva",
            "fecha_nacimiento": "2003-01-20", "sexo": "M", "estado_civil": "Soltero",
            "correo_electronico": "carlos.silva@email.com",
        },
        "telefonos": [{"tipo_telefono": "movil", "numero": "04247890123", "principal": True}],
        "direcciones": [{
            "estado": "Barinas", "municipio": "Barinas", "parroquia": "Corazón de Jesús", "sector": "Centro",
            "calle": "Calle Bolívar", "casa_edificio": "Edif. Central, Apto 3B", "direccion_completa": "Calle Bolívar, Edif. Central, Apto 3B, Barinas",
            "tipo_direccion": "residencia", "principal": True
        }],
        "academico": {
            "codigo_unico": "E2022002", "codigo_estudiantil": "28789012-INF", "tipo_ingreso": "Nuevo",
            "cohorte": "2022-1", "situacion_academica": "Activo"
        }
    },
    {
        "personal": {
            "documento_identidad": "26555888", "nombres": "Sofía Valentina", "apellidos": "García Márquez",
            "fecha_nacimiento": "2001-11-30", "sexo": "F", "estado_civil": "Soltero",
            "correo_electronico": "sofia.garcia@email.com",
        },
        "telefonos": [{"tipo_telefono": "movil", "numero": "04165558888", "principal": True}],
        "direcciones": [{
            "estado": "Barinas", "municipio": "Barinitas", "parroquia": "Barinitas", "sector": "La Cochinilla",
            "calle": "Principal", "casa_edificio": "Casa S/N", "direccion_completa": "Sector La Cochinilla, Barinitas",
            "tipo_direccion": "residencia", "principal": True
        }],
        "academico": {
            "codigo_unico": "E2021030", "codigo_estudiantil": "26555888-AGRO", "tipo_ingreso": "Reingreso",
            "cohorte": "2021-2", "situacion_academica": "Activo"
        }
    },
    # Agrega aquí los 7 estudiantes restantes con datos similares...
    {"personal": {"documento_identidad": "29111222", "nombres": "Luis Alberto", "apellidos": "Mendoza", "fecha_nacimiento": "2004-02-10", "sexo": "M", "estado_civil": "Soltero", "correo_electronico": "luis.m@email.com"}, "telefonos": [{"tipo_telefono": "movil", "numero": "04121112233", "principal": True}], "direcciones": [{"estado": "Barinas", "municipio": "Socopó", "parroquia": "Ticoporo", "sector": "Las Flores", "calle": "Calle 5", "casa_edificio": "Casa 10", "direccion_completa": "Las Flores, Calle 5, Casa 10, Socopó", "tipo_direccion": "residencia", "principal": True}], "academico": {"codigo_unico": "E2023003", "codigo_estudiantil": "29111222-INF", "tipo_ingreso": "Nuevo", "cohorte": "2023-1", "situacion_academica": "Activo"}},
    {"personal": {"documento_identidad": "28333444", "nombres": "Gabriela", "apellidos": "Hernández", "fecha_nacimiento": "2003-08-25", "sexo": "F", "estado_civil": "Soltero", "correo_electronico": "gaby.h@email.com"}, "telefonos": [{"tipo_telefono": "movil", "numero": "04263334455", "principal": True}], "direcciones": [{"estado": "Barinas", "municipio": "Barinas", "parroquia": "Rómulo Betancourt", "sector": "Corocito", "calle": "Avenida Principal", "casa_edificio": "Casa 22", "direccion_completa": "Corocito, Av. Principal, Casa 22, Barinas", "tipo_direccion": "residencia", "principal": True}], "academico": {"codigo_unico": "E2022004", "codigo_estudiantil": "28333444-CIV", "tipo_ingreso": "Nuevo", "cohorte": "2022-2", "situacion_academica": "Activo"}},
    {"personal": {"documento_identidad": "27555666", "nombres": "Diego Alejandro", "apellidos": "Castillo", "fecha_nacimiento": "2002-12-01", "sexo": "M", "estado_civil": "Soltero", "correo_electronico": "diego.c@email.com"}, "telefonos": [{"tipo_telefono": "movil", "numero": "04145556677", "principal": True}], "direcciones": [{"estado": "Portuguesa", "municipio": "Guanare", "parroquia": "Guanare", "sector": "Mesa de Cavacas", "calle": "Calle 1", "casa_edificio": "Casa 1", "direccion_completa": "Mesa de Cavacas, Guanare", "tipo_direccion": "residencia", "principal": True}], "academico": {"codigo_unico": "E2021050", "codigo_estudiantil": "27555666-MEC", "tipo_ingreso": "Transferencia", "cohorte": "2021-1", "situacion_academica": "Activo"}},
    {"personal": {"documento_identidad": "30123123", "nombres": "Valeria Isabel", "apellidos": "Rojas", "fecha_nacimiento": "2005-03-18", "sexo": "F", "estado_civil": "Soltero", "correo_electronico": "vale.r@email.com"}, "telefonos": [{"tipo_telefono": "movil", "numero": "04241231234", "principal": True}], "direcciones": [{"estado": "Barinas", "municipio": "Barinas", "parroquia": "Alto Barinas", "sector": "Ciudad Tavacare", "calle": "Manzana C", "casa_edificio": "Casa 8", "direccion_completa": "Ciudad Tavacare, Manzana C, Casa 8, Barinas", "tipo_direccion": "residencia", "principal": True}], "academico": {"codigo_unico": "E2023005", "codigo_estudiantil": "30123123-INF", "tipo_ingreso": "Nuevo", "cohorte": "2023-1", "situacion_academica": "Activo"}},
    {"personal": {"documento_identidad": "28999000", "nombres": "Ricardo Andrés", "apellidos": "Salazar", "fecha_nacimiento": "2003-07-07", "sexo": "M", "estado_civil": "Soltero", "correo_electronico": "ricardo.s@email.com"}, "telefonos": [{"tipo_telefono": "movil", "numero": "04169990001", "principal": True}], "direcciones": [{"estado": "Barinas", "municipio": "Barinas", "parroquia": "El Carmen", "sector": "El Centro", "calle": "Avenida Olmedilla", "casa_edificio": "Edif. Don Pepe, Apto 1", "direccion_completa": "Av. Olmedilla, Edif. Don Pepe, Apto 1, Barinas", "tipo_direccion": "residencia", "principal": True}], "academico": {"codigo_unico": "E2022006", "codigo_estudiantil": "28999000-INF", "tipo_ingreso": "Nuevo", "cohorte": "2022-2", "situacion_academica": "Activo"}},
    {"personal": {"documento_identidad": "27888777", "nombres": "Mariana Carolina", "apellidos": "Freites", "fecha_nacimiento": "2002-09-09", "sexo": "F", "estado_civil": "Soltero", "correo_electronico": "mariana.f@email.com"}, "telefonos": [{"tipo_telefono": "movil", "numero": "04148887766", "principal": True}], "direcciones": [{"estado": "Barinas", "municipio": "Barinitas", "parroquia": "Barinitas", "sector": "El Cacao", "calle": "Calle 3", "casa_edificio": "Casa 33", "direccion_completa": "El Cacao, Calle 3, Casa 33, Barinitas", "tipo_direccion": "residencia", "principal": True}], "academico": {"codigo_unico": "E2021080", "codigo_estudiantil": "27888777-TUR", "tipo_ingreso": "Equivalencia", "cohorte": "2021-2", "situacion_academica": "Activo"}},
    {"personal": {"documento_identidad": "29001002", "nombres": "Jesús David", "apellidos": "Paredes", "fecha_nacimiento": "2004-04-12", "sexo": "M", "estado_civil": "Soltero", "correo_electronico": "jesus.p@email.com"}, "telefonos": [{"tipo_telefono": "movil", "numero": "04240010022", "principal": True}], "direcciones": [{"estado": "Barinas", "municipio": "Barinas", "parroquia": "Corazón de Jesús", "sector": "La Carolina", "calle": "Avenida Industrial", "casa_edificio": "Casa 5-A", "direccion_completa": "La Carolina, Av. Industrial, Casa 5-A, Barinas", "tipo_direccion": "residencia", "principal": True}], "academico": {"codigo_unico": "E2023007", "codigo_estudiantil": "29001002-INF", "tipo_ingreso": "Nuevo", "cohorte": "2023-1", "situacion_academica": "Activo"}},
]

class CargadorEstudiantes:
    def __init__(self, estudiantes_data, db_path=None):
        self.estudiantes_data = estudiantes_data
        self.db_path = db_path or os.path.join(os.path.dirname(__file__), '..', 'db', 'sistema_academico.db')
        self.con = None

    def conectar(self):
        """Establece una conexión a la base de datos."""
        self.con = sqlite3.connect(self.db_path)
        self.con.execute("PRAGMA foreign_keys = ON;")

    def cerrar(self):
        """Cierra la conexión a la base de datos."""
        if self.con:
            self.con.close()

    def insertar_estudiante(self, estudiante_data):
        """Inserta los datos completos de un solo estudiante en una transacción."""
        if not self.con:
            raise ConnectionError("La conexión a la base de datos no está establecida.")

        cursor = self.con.cursor()
        personal = estudiante_data['personal']
        
        try:
            # 1. Insertar en informacion_personal
            cursor.execute('''
                INSERT INTO informacion_personal (
                    documento_identidad, nombres, apellidos, fecha_nacimiento, sexo,
                    estado_civil, correo_electronico, tipo
                ) VALUES (?, ?, ?, ?, ?, ?, ?, 'estudiante')
            ''', (
                personal['documento_identidad'], personal['nombres'], personal['apellidos'],
                personal['fecha_nacimiento'], personal['sexo'], personal['estado_civil'],
                personal['correo_electronico']
            ))
            persona_id = cursor.lastrowid
            print(f"  -> Persona '{personal['nombres']} {personal['apellidos']}' insertada con ID: {persona_id}")

            # 2. Insertar en estudiantes
            academico = estudiante_data['academico']
            cursor.execute('''
                INSERT INTO estudiantes (
                    persona_id, codigo_unico, codigo_estudiantil, tipo_ingreso,
                    cohorte, situacion_academica
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                persona_id, academico['codigo_unico'], academico['codigo_estudiantil'],
                academico['tipo_ingreso'], academico['cohorte'], academico['situacion_academica']
            ))
            estudiante_id = cursor.lastrowid
            print(f"  -> Datos académicos para '{academico['codigo_unico']}' insertados con ID: {estudiante_id}")

            # 3. Insertar en telefonos
            for telefono in estudiante_data.get('telefonos', []):
                cursor.execute('''
                    INSERT INTO telefonos (persona_id, tipo_telefono, numero, principal) 
                    VALUES (?, ?, ?, ?)
                ''', (persona_id, telefono['tipo_telefono'], telefono['numero'], telefono.get('principal', False)))
            print(f"  -> {len(estudiante_data.get('telefonos', []))} teléfono(s) insertado(s).")

            # 4. Insertar en direcciones
            for direccion in estudiante_data.get('direcciones', []):
                cursor.execute('''
                    INSERT INTO direcciones (
                        persona_id, estado, municipio, parroquia, sector, calle,
                        casa_edificio, direccion_completa, tipo_direccion, principal
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    persona_id, direccion['estado'], direccion['municipio'], direccion['parroquia'],
                    direccion['sector'], direccion['calle'], direccion['casa_edificio'],
                    direccion['direccion_completa'], direccion['tipo_direccion'], direccion.get('principal', False)
                ))
            print(f"  -> {len(estudiante_data.get('direcciones', []))} dirección(es) insertada(s).")

            self.con.commit()
            print(f"Estudiante '{personal['nombres']}' cargado exitosamente.\n")

        except sqlite3.IntegrityError as e:
            print(f"Error de integridad al insertar a '{personal['nombres']} {personal['apellidos']}' (CI: {personal['documento_identidad']}): {e}.")
            print("El registro ya podría existir. Saltando...\n")
            self.con.rollback()
        except Exception as e:
            print(f"Error catastrófico insertando estudiante '{personal['nombres']}': {e}")
            self.con.rollback()
            raise

    def cargar(self):
        """Carga todos los estudiantes de la lista de datos a la base de datos."""
        if not os.path.exists(self.db_path):
            print(f"Error: La base de datos en '{self.db_path}' no existe.")
            print("Por favor, ejecute primero el script 'creacion_db.py'.")
            return

        try:
            self.conectar()
            print("="*50)
            print("Iniciando carga masiva de datos de estudiantes...")
            print("="*50)
            for estudiante in self.estudiantes_data:
                self.insertar_estudiante(estudiante)
            print("\nCarga masiva de estudiantes finalizada.")
            print("="*50)
        finally:
            self.cerrar()

if __name__ == "__main__":
    cargador = CargadorEstudiantes(estudiantes_data)
    cargador.cargar()