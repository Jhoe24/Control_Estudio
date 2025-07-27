# archivo cargar_docentes.py - Carga masiva de datos de docentes
import sqlite3
import os

# --- DATOS DE EJEMPLO PARA 10 DOCENTES ---
docentes_data = [
    {
        "personal": {
            "documento_identidad": "10123456", "nombres": "Juan Carlos", "apellidos": "Pérez Gómez",
            "fecha_nacimiento": "1980-03-20", "sexo": "M", "estado_civil": "Casado",
            "correo_electronico": "juan.perez.g@email.com", "correo_institucional": "jperez@uptrjf.edu.ve"
        },
        "telefonos": [
            {"tipo_telefono": "movil", "numero": "04129876543", "principal": True}
        ],
        "direcciones": [{
            "estado": "Barinas", "municipio": "Barinas", "parroquia": "Alto Barinas", "sector": "La Floresta",
            "calle": "Avenida 5", "casa_edificio": "Edif. Los Profesores, Apto 1A", "direccion_completa": "Urb. La Floresta, Av. 5, Edif. Los Profesores, Apto 1A, Barinas",
            "tipo_direccion": "residencia", "principal": True
        }],
        "academico": {
            "codigo_docente": "D1980001", "abreviatura_titulo": "Ing.", "titulo_pregrado": "Ingeniero en Informática",
            "institucion_pregrado": "UNET", "titulo_postgrado": "Magister en Ciencias de la Computación", "institucion_postgrado": "ULA",
            "especialidad": "Bases de Datos", "area_conocimiento": "Informática", "fecha_ingreso_uptrjf": "2010-09-15",
            "tipo_contrato": "Tiempo completo", "categoria": "Agregado", "dedicacion": "Exclusiva", "estado": "Activo"
        }
    },
    {
        "personal": {
            "documento_identidad": "12345678", "nombres": "María Elena", "apellidos": "Rodríguez López",
            "fecha_nacimiento": "1975-11-05", "sexo": "F", "estado_civil": "Soltero",
            "correo_electronico": "maria.r.lopez@email.com", "correo_institucional": "mrodriguez@uptrjf.edu.ve"
        },
        "telefonos": [
            {"tipo_telefono": "movil", "numero": "04141112233", "principal": True}
        ],
        "direcciones": [{
            "estado": "Barinas", "municipio": "Barinas", "parroquia": "Corazón de Jesús", "sector": "Centro",
            "calle": "Av. Sucre", "casa_edificio": "Casa 25-B", "direccion_completa": "Av. Sucre, Casa 25-B, Barinas",
            "tipo_direccion": "residencia", "principal": True
        }],
        "academico": {
            "codigo_docente": "D1975002", "abreviatura_titulo": "Lic.", "titulo_pregrado": "Licenciada en Educación, mención Matemática",
            "institucion_pregrado": "UPEL", "titulo_postgrado": "Especialista en Planificación Educativa", "institucion_postgrado": "UCV",
            "especialidad": "Matemática", "area_conocimiento": "Ciencias Básicas", "fecha_ingreso_uptrjf": "2005-02-01",
            "tipo_contrato": "Tiempo completo", "categoria": "Asociado", "dedicacion": "Tiempo completo", "estado": "Activo"
        }
    },
    # Puedes agregar los 8 docentes restantes aquí con una estructura similar
    {"personal": {"documento_identidad": "9876543", "nombres": "Pedro José", "apellidos": "Martínez Salas", "fecha_nacimiento": "1968-07-12", "sexo": "M", "estado_civil": "Divorciado", "correo_electronico": "pedro.martinez@email.com", "correo_institucional": "pmartinez@uptrjf.edu.ve"}, "telefonos": [{"tipo_telefono": "movil", "numero": "04265554433", "principal": True}], "direcciones": [{"estado": "Barinas", "municipio": "Barinitas", "parroquia": "Alto Barinas", "sector": "El Centro", "calle": "Calle 4", "casa_edificio": "Casa 1-1", "direccion_completa": "Calle 4, Casa 1-1, Barinitas", "tipo_direccion": "residencia", "principal": True}], "academico": {"codigo_docente": "D1968003", "abreviatura_titulo": "Dr.", "titulo_pregrado": "Licenciado en Física", "institucion_pregrado": "ULA", "titulo_postgrado": "Doctor en Física", "institucion_postgrado": "IVIC", "especialidad": "Física de Partículas", "area_conocimiento": "Ciencias Básicas", "fecha_ingreso_uptrjf": "2000-01-10", "tipo_contrato": "Tiempo completo", "categoria": "Titular", "dedicacion": "Exclusiva", "estado": "Activo"}},
    {"personal": {"documento_identidad": "11223344", "nombres": "Ana Sofía", "apellidos": "González Rivas", "fecha_nacimiento": "1985-01-30", "sexo": "F", "estado_civil": "Casado", "correo_electronico": "ana.gonzalez@email.com", "correo_institucional": "agonzalez@uptrjf.edu.ve"}, "telefonos": [{"tipo_telefono": "movil", "numero": "04161237890", "principal": True}], "direcciones": [{"estado": "Barinas", "municipio": "Socopó","parroquia": "Alto Barinas", "sector": "Las Flores", "calle": "Principal", "casa_edificio": "Quinta Ana", "direccion_completa": "Sector Las Flores, Quinta Ana, Socopó", "tipo_direccion": "residencia", "principal": True}], "academico": {"codigo_docente": "D1985004", "abreviatura_titulo": "Ing.", "titulo_pregrado": "Ingeniero Civil", "institucion_pregrado": "UCLA", "titulo_postgrado": None, "institucion_postgrado": None, "especialidad": "Estructuras", "area_conocimiento": "Ingeniería Civil", "fecha_ingreso_uptrjf": "2015-05-20", "tipo_contrato": "Contratado", "categoria": "Instructor", "dedicacion": "Medio tiempo", "estado": "Activo"}},
    {"personal": {"documento_identidad": "15987654", "nombres": "Luis Alberto", "apellidos": "Hernández", "fecha_nacimiento": "1990-09-09", "sexo": "M", "estado_civil": "Soltero", "correo_electronico": "luis.h@email.com", "correo_institucional": "lhernandez@uptrjf.edu.ve"}, "telefonos": [{"tipo_telefono": "movil", "numero": "04247654321", "principal": True}], "direcciones": [{"estado": "Barinas", "municipio": "Barinas", "parroquia": "Rómulo Betancourt", "sector": "Ciudad Varyna", "calle": "Manzana 12", "casa_edificio": "Casa 3", "direccion_completa": "Ciudad Varyna, Manzana 12, Casa 3, Barinas", "tipo_direccion": "residencia", "principal": True}], "academico": {"codigo_docente": "D1990005", "abreviatura_titulo": "Lic.", "titulo_pregrado": "Licenciado en Química", "institucion_pregrado": "UC", "titulo_postgrado": "Magister en Química Orgánica", "institucion_postgrado": "UC", "especialidad": "Química", "area_conocimiento": "Ciencias Básicas", "fecha_ingreso_uptrjf": "2018-03-12", "tipo_contrato": "Por horas", "categoria": "Asistente", "dedicacion": "Tiempo convencional", "estado": "Activo"}},
    {"personal": {"documento_identidad": "14785236", "nombres": "Laura Patricia", "apellidos": "Ramírez", "fecha_nacimiento": "1982-04-15", "sexo": "F", "estado_civil": "Viudo", "correo_electronico": "laura.r@email.com", "correo_institucional": "lramirez@uptrjf.edu.ve"}, "telefonos": [{"tipo_telefono": "movil", "numero": "04122583691", "principal": True}], "direcciones": [{"estado": "Barinas", "municipio": "Barinas", "parroquia": "Alto Barinas", "sector": "Los Pomelos", "calle": "Avenida 3", "casa_edificio": "Casa 12-B", "direccion_completa": "Urb. Los Pomelos, Av. 3, Casa 12-B, Barinas", "tipo_direccion": "residencia", "principal": True}], "academico": {"codigo_docente": "D1982006", "abreviatura_titulo": "Ing.", "titulo_pregrado": "Ingeniero Agroindustrial", "institucion_pregrado": "UNELLEZ", "titulo_postgrado": "Especialista en Tecnología de Alimentos", "institucion_postgrado": "UNELLEZ", "especialidad": "Procesamiento de Alimentos", "area_conocimiento": "Agroalimentaria", "fecha_ingreso_uptrjf": "2012-11-01", "tipo_contrato": "Tiempo completo", "categoria": "Agregado", "dedicacion": "Tiempo completo", "estado": "Activo"}},
    {"personal": {"documento_identidad": "13579246", "nombres": "David Antonio", "apellidos": "Torres", "fecha_nacimiento": "1979-12-25", "sexo": "M", "estado_civil": "Casado", "correo_electronico": "david.t@email.com", "correo_institucional": "dtorres@uptrjf.edu.ve"}, "telefonos": [{"tipo_telefono": "movil", "numero": "04147896541", "principal": True}], "direcciones": [{"estado": "Barinas", "municipio": "Barinas", "parroquia": "El Carmen", "sector": "Centro", "calle": "Av. 23 de Enero", "casa_edificio": "Edif. El Sol, Apto 5C", "direccion_completa": "Av. 23 de Enero, Edif. El Sol, Apto 5C, Barinas", "tipo_direccion": "residencia", "principal": True}], "academico": {"codigo_docente": "D1979007", "abreviatura_titulo": "Lic.", "titulo_pregrado": "Licenciado en Contaduría Pública", "institucion_pregrado": "ULA", "titulo_postgrado": "Magister en Finanzas", "institucion_postgrado": "UCAB", "especialidad": "Auditoría", "area_conocimiento": "Ciencias Sociales", "fecha_ingreso_uptrjf": "2008-09-15", "tipo_contrato": "Tiempo completo", "categoria": "Asociado", "dedicacion": "Exclusiva", "estado": "Activo"}},
    {"personal": {"documento_identidad": "16123789", "nombres": "Isabel Cristina", "apellidos": "Flores", "fecha_nacimiento": "1988-06-18", "sexo": "F", "estado_civil": "Soltero", "correo_electronico": "isabel.f@email.com", "correo_institucional": "iflores@uptrjf.edu.ve"}, "telefonos": [{"tipo_telefono": "movil", "numero": "04269871234", "principal": True}], "direcciones": [{"estado": "Barinas", "municipio": "Barinas", "parroquia": "Alto Barinas", "sector": "Ciudad Tavacare", "calle": "Manzana F", "casa_edificio": "Casa 1", "direccion_completa": "Ciudad Tavacare, Manzana F, Casa 1, Barinas", "tipo_direccion": "residencia", "principal": True}], "academico": {"codigo_docente": "D1988008", "abreviatura_titulo": "M.Sc.", "titulo_pregrado": "Ingeniero Industrial", "institucion_pregrado": "UNEXPO", "titulo_postgrado": "Magister en Gerencia Empresarial", "institucion_postgrado": "UNET", "especialidad": "Gerencia de Proyectos", "area_conocimiento": "Ciencias Sociales", "fecha_ingreso_uptrjf": "2019-01-20", "tipo_contrato": "Contratado", "categoria": "Asistente", "dedicacion": "Medio tiempo", "estado": "Activo"}},
    {"personal": {"documento_identidad": "8765432", "nombres": "Ricardo", "apellidos": "Méndez", "fecha_nacimiento": "1965-02-10", "sexo": "M", "estado_civil": "Casado", "correo_electronico": "ricardo.m@email.com", "correo_institucional": "rmendez@uptrjf.edu.ve"}, "telefonos": [{"tipo_telefono": "movil", "numero": "04143219876", "principal": True}], "direcciones": [{"estado": "Barinas", "municipio": "Barinas", "parroquia": "Corazón de Jesús", "sector": "La Carolina", "calle": "Av. Los Llanos", "casa_edificio": "Casa 88", "direccion_completa": "La Carolina, Av. Los Llanos, Casa 88, Barinas", "tipo_direccion": "residencia", "principal": True}], "academico": {"codigo_docente": "D1965009", "abreviatura_titulo": "TSU", "titulo_pregrado": "TSU en Informática", "institucion_pregrado": "IUTEMBI", "titulo_postgrado": None, "institucion_postgrado": None, "especialidad": "Soporte Técnico", "area_conocimiento": "Informática", "fecha_ingreso_uptrjf": "2002-06-01", "tipo_contrato": "Tiempo completo", "categoria": "Técnico III", "dedicacion": "Tiempo completo", "estado": "Jubilado Activo"}},
    {"personal": {"documento_identidad": "17543210", "nombres": "Valentina", "apellidos": "Rojas", "fecha_nacimiento": "1992-08-22", "sexo": "F", "estado_civil": "Soltero", "correo_electronico": "valentina.r@email.com", "correo_institucional": "vrojas@uptrjf.edu.ve"}, "telefonos": [{"tipo_telefono": "movil", "numero": "04241020304", "principal": True}], "direcciones": [{"estado": "Barinas", "municipio": "Barinas", "parroquia": "Alto Barinas", "sector": "El Milagro", "calle": "Calle Ciega", "casa_edificio": "Casa S/N", "direccion_completa": "Sector El Milagro, Calle Ciega, Casa S/N, Barinas", "tipo_direccion": "residencia", "principal": True}], "academico": {"codigo_docente": "D1992010", "abreviatura_titulo": "Abg.", "titulo_pregrado": "Abogado", "institucion_pregrado": "UCAT", "titulo_postgrado": "Especialista en Derecho Administrativo", "institucion_postgrado": "UCV", "especialidad": "Leyes y Regulaciones", "area_conocimiento": "Ciencias Sociales", "fecha_ingreso_uptrjf": "2020-09-01", "tipo_contrato": "Contratado", "categoria": "Instructor", "dedicacion": "Tiempo convencional", "estado": "Activo"}}
]

class CargadorDocentes:
    def __init__(self, docentes_data, db_path=None):
        self.docentes_data = docentes_data
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

    def insertar_docente(self, docente_data):
        """Inserta los datos completos de un solo docente en una transacción."""
        if not self.con:
            raise ConnectionError("La conexión a la base de datos no está establecida.")

        cursor = self.con.cursor()
        personal = docente_data['personal']
        
        try:
            # 1. Insertar en informacion_personal
            cursor.execute('''
                INSERT INTO informacion_personal (
                    documento_identidad, nombres, apellidos, fecha_nacimiento, sexo,
                    estado_civil, correo_electronico, correo_institucional, tipo
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'docente')
            ''', (
                personal['documento_identidad'], personal['nombres'], personal['apellidos'],
                personal['fecha_nacimiento'], personal['sexo'], personal['estado_civil'],
                personal['correo_electronico'], personal.get('correo_institucional')
            ))
            persona_id = cursor.lastrowid
            print(f"  -> Persona '{personal['nombres']} {personal['apellidos']}' insertada con ID: {persona_id}")

            # 2. Insertar en docentes
            academico = docente_data['academico']
            cursor.execute('''
                INSERT INTO docentes (
                    persona_id, codigo_docente, abreviatura_titulo, titulo_pregrado, institucion_pregrado,
                    titulo_postgrado, institucion_postgrado, especialidad, area_conocimiento,
                    fecha_ingreso_uptrjf, tipo_contrato, categoria, dedicacion, estado
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                persona_id, academico['codigo_docente'], academico.get('abreviatura_titulo'),
                academico.get('titulo_pregrado'), academico.get('institucion_pregrado'),
                academico.get('titulo_postgrado'), academico.get('institucion_postgrado'),
                academico.get('especialidad'), academico.get('area_conocimiento'),
                academico.get('fecha_ingreso_uptrjf'), academico.get('tipo_contrato'),
                academico.get('categoria'), academico.get('dedicacion'), academico.get('estado')
            ))
            docente_id = cursor.lastrowid
            print(f"  -> Datos académicos para '{academico['codigo_docente']}' insertados con ID: {docente_id}")

            # 3. Insertar en telefonos
            for telefono in docente_data.get('telefonos', []):
                cursor.execute('''
                    INSERT INTO telefonos (persona_id, tipo_telefono, numero, principal) 
                    VALUES (?, ?, ?, ?)
                ''', (persona_id, telefono['tipo_telefono'], telefono['numero'], telefono.get('principal', False)))
            print(f"  -> {len(docente_data.get('telefonos', []))} teléfono(s) insertado(s).")

            # 4. Insertar en direcciones
            for direccion in docente_data.get('direcciones', []):
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
            print(f"  -> {len(docente_data.get('direcciones', []))} dirección(es) insertada(s).")

            self.con.commit()
            print(f"Docente '{personal['nombres']}' cargado exitosamente.\n")

        except sqlite3.IntegrityError as e:
            print(f"Error de integridad al insertar a '{personal['nombres']} {personal['apellidos']}' (CI: {personal['documento_identidad']}): {e}.")
            print("El registro ya podría existir. Saltando...\n")
            self.con.rollback()
        except Exception as e:
            print(f"Error catastrófico insertando docente '{personal['nombres']}': {e}")
            self.con.rollback()
            raise

    def cargar(self):
        """Carga todos los docentes de la lista de datos a la base de datos."""
        if not os.path.exists(self.db_path):
            print(f"Error: La base de datos en '{self.db_path}' no existe.")
            print("Por favor, ejecute primero el script 'creacion_db.py'.")
            return

        try:
            self.conectar()
            print("="*50)
            print("Iniciando carga masiva de datos de docentes...")
            print("="*50)
            for docente in self.docentes_data:
                self.insertar_docente(docente)
            print("\nCarga masiva de docentes finalizada.")
            print("="*50)
        finally:
            self.cerrar()

if __name__ == "__main__":
    cargador = CargadorDocentes(docentes_data)
    cargador.cargar()