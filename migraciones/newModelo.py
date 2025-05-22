# archivo newmodelo.py creamos las base de datos y tablas necesarias para el sistema académico
import sqlite3 as sql
import os
import datetime

class SistemaAcademicoDB:
    def __init__(self):
        self.crear_base_datos()

    def ejecutar_consulta(self, instruccion):
        # Conexión a la base de datos, si no encuentra el archivo lo crea
        db_ruta = os.path.join('db', 'sistema_academico.db')
        con = sql.connect(db_ruta, isolation_level=None)
        cursor = con.cursor()
        # Ejecutamos la consulta
        cursor.execute(instruccion)
        # Guardamos los cambios
        con.commit()
        # Cerramos la conexión
        con.close()

    def crear_tablas_base(self):
        instruccion1 = '''
        CREATE TABLE IF NOT EXISTS informacion_personal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            documento_identidad TEXT NOT NULL UNIQUE,
            tipo_documento TEXT NOT NULL DEFAULT 'cedula',
            nombres TEXT NOT NULL,
            apellidos TEXT,
            fecha_nacimiento DATE,
            sexo CHAR(1) CHECK (sexo IN ('M', 'F')),
            estado_civil TEXT CHECK (estado_civil IN ('Soltero', 'Casado', 'Divorciado', 'Viudo', 'Otro')),
            nacionalidad TEXT,
            lugar_nacimiento TEXT,
            correo_electronico TEXT,
            fecha_registro DATE DEFAULT CURRENT_DATE,
            tipo TEXT NOT NULL CHECK (tipo IN ('estudiante', 'docente')),
            pasaporte TEXT,
            estado TEXT DEFAULT 'activo' CHECK (estado IN ('activo', 'inactivo', 'retirado', 'graduado', 'suspendido')),
            UNIQUE(documento_identidad, tipo_documento)
        );'''
        self.ejecutar_consulta(instruccion1)
        
        instruccion2 = '''
        CREATE TABLE IF NOT EXISTS telefonos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            persona_id INTEGER NOT NULL,
            tipo_telefono TEXT NOT NULL CHECK (tipo_telefono IN ('movil', 'casa', 'trabajo', 'otro')),
            numero TEXT NOT NULL,
            principal BOOLEAN DEFAULT 0,
            FOREIGN KEY (persona_id) REFERENCES informacion_personal(id) ON DELETE CASCADE
        );'''
        self.ejecutar_consulta(instruccion2)
        
        instruccion3 = '''
        CREATE TABLE IF NOT EXISTS direcciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            persona_id INTEGER NOT NULL,
            estado TEXT NOT NULL,
            municipio TEXT NOT NULL,
            parroquia TEXT,
            sector TEXT,
            calle TEXT,
            casa_edificio TEXT,
            piso_apartamento TEXT,
            direccion_completa TEXT NOT NULL,
            tipo_direccion TEXT NOT NULL CHECK (tipo_direccion IN ('residencia', 'trabajo', 'otro')),
            principal BOOLEAN DEFAULT 0,
            FOREIGN KEY (persona_id) REFERENCES informacion_personal(id) ON DELETE CASCADE
        );'''
        self.ejecutar_consulta(instruccion3)

    def crear_tablas_catalogo(self):
        instruccion1 = '''
        CREATE TABLE IF NOT EXISTS sedes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL UNIQUE,
            nombre TEXT NOT NULL,
            direccion TEXT NOT NULL,
            telefono TEXT,
            correo TEXT,
            director TEXT,
            fecha_creacion DATE,
            estado TEXT DEFAULT 'activa' CHECK (estado IN ('activa', 'inactiva'))
        );'''
        self.ejecutar_consulta(instruccion1)

        instruccion2 = '''
        CREATE TABLE IF NOT EXISTS pnf (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL UNIQUE,
            nombre TEXT NOT NULL,
            nivel TEXT NOT NULL CHECK (nivel IN ('TSU', 'Ingeniería', 'Licenciatura', 'Medicina')),
            duracion_semestres INTEGER,
            coordinador TEXT,
            fecha_creacion DATE,
            estado TEXT DEFAULT 'activo' CHECK (estado IN ('activo', 'inactivo'))
        );'''
        self.ejecutar_consulta(instruccion2)

        instruccion3 = '''
        CREATE TABLE IF NOT EXISTS sede_pnf (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sede_id INTEGER NOT NULL,
            pnf_id INTEGER NOT NULL,
            fecha_inicio DATE,
            estado TEXT DEFAULT 'activo' CHECK (estado IN ('activo', 'inactivo')),
            FOREIGN KEY (sede_id) REFERENCES sedes(id),
            FOREIGN KEY (pnf_id) REFERENCES pnf(id),
            UNIQUE(sede_id, pnf_id)
        );'''
        self.ejecutar_consulta(instruccion3)

        instruccion4 = '''
        CREATE TABLE IF NOT EXISTS unidades_curriculares (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL,
            nombre TEXT NOT NULL,
            pnf_id INTEGER NOT NULL,
            trayecto INTEGER NOT NULL,
            tramo INTEGER NOT NULL,
            horas_teoricas INTEGER,
            horas_practicas INTEGER,
            unidades_credito INTEGER,
            prelacion TEXT,
            tipo TEXT CHECK (tipo IN ('Obligatoria', 'Electiva', 'Proyecto', 'Pasantía')),
            estado TEXT DEFAULT 'activa' CHECK (estado IN ('activa', 'inactiva')),
            homologacion_clave TEXT,
            clave_especial TEXT,
            FOREIGN KEY (pnf_id) REFERENCES pnf(id),
            UNIQUE(codigo, pnf_id)
        );'''
        self.ejecutar_consulta(instruccion4)

        instruccion5 = '''
        CREATE TABLE IF NOT EXISTS periodos_academicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL UNIQUE,
            nombre TEXT NOT NULL,
            fecha_inicio DATE NOT NULL,
            fecha_fin DATE NOT NULL,
            estado TEXT DEFAULT 'planificacion'
                CHECK (estado IN ('planificacion', 'inscripcion', 'en_curso', 'finalizado', 'cerrado')),
            observaciones TEXT
        );'''
        self.ejecutar_consulta(instruccion5)

    def crear_tablas_academicas(self):
        instruccion1 = '''
        CREATE TABLE IF NOT EXISTS estudiantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            persona_id INTEGER NOT NULL UNIQUE,
            codigo_unico TEXT UNIQUE,
            institucion_procedencia TEXT,
            mencion_bachiller TEXT,
            fecha_grado_bachiller DATE,
            profesion TEXT,
            fecha_grado_profesional DATE,
            fecha_ingreso DATE,
            condicion TEXT CHECK (condicion IN ('Regular', 'Repitente', 'Reingreso', 'Transferencia')),
            oyente BOOLEAN DEFAULT 0,
            situacion_academica TEXT DEFAULT 'Activo'
                CHECK (situacion_academica IN ('Activo', 'Inactivo', 'Graduado', 'Retirado', 'Egresado')),
            FOREIGN KEY (persona_id) REFERENCES informacion_personal(id) ON DELETE CASCADE
        );'''
        self.ejecutar_consulta(instruccion1)

        instruccion2 = '''
        CREATE TABLE IF NOT EXISTS docentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            persona_id INTEGER NOT NULL UNIQUE,
            abreviatura_titulo TEXT,
            especialidad TEXT,
            fecha_ingreso DATE,
            tipo_contrato TEXT DEFAULT 'Tiempo completo' CHECK (tipo_contrato IN ('Tiempo completo', 'Medio tiempo', 'Por horas', 'Contratado')),
            categoria TEXT,
            auxiliar BOOLEAN DEFAULT 0,
            dedicacion TEXT DEFAULT 'Tiempo completo' CHECK (dedicacion IN ('Exclusiva', 'Tiempo completo', 'Medio tiempo', 'Tiempo convencional')),
            estado TEXT DEFAULT 'Activo' CHECK (estado IN ('Activo', 'Inactivo', 'Jubilado', 'Permiso')),
            FOREIGN KEY (persona_id) REFERENCES informacion_personal(id) ON DELETE CASCADE
        );'''
        self.ejecutar_consulta(instruccion2)

        instruccion3 = '''
        CREATE TABLE IF NOT EXISTS estudiante_pnf (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estudiante_id INTEGER NOT NULL,
            pnf_id INTEGER NOT NULL,
            sede_id INTEGER NOT NULL,
            fecha_inicio DATE NOT NULL,
            fecha_fin DATE,
            estado TEXT DEFAULT 'Activo' CHECK (estado IN ('Activo', 'Inactivo', 'Graduado', 'Retirado')),
            turno TEXT CHECK (turno IN ('Diurno', 'Nocturno', 'Fin de semana')),
            FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id),
            FOREIGN KEY (pnf_id) REFERENCES pnf(id),
            FOREIGN KEY (sede_id) REFERENCES sedes(id),
            UNIQUE(estudiante_id, pnf_id, sede_id)
        );'''
        self.ejecutar_consulta(instruccion3)

    def crear_tablas_operativas(self):
        instruccion1 = '''
        CREATE TABLE IF NOT EXISTS secciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unidad_curricular_id INTEGER NOT NULL,
            periodo_academico_id INTEGER NOT NULL,
            sede_id INTEGER NOT NULL,
            codigo_seccion TEXT NOT NULL,
            docente_id INTEGER,
            cupo_maximo INTEGER NOT NULL DEFAULT 40,
            inscritos INTEGER DEFAULT 0,
            turno TEXT CHECK (turno IN ('Diurno', 'Nocturno', 'Fin de semana')),
            aula TEXT,
            horario TEXT,
            fecha_inicio DATE,
            fecha_fin DATE,
            estado TEXT DEFAULT 'Planificada'
                CHECK (estado IN ('Planificada', 'Abierta', 'En curso', 'Finalizada', 'Cancelada')),
            FOREIGN KEY (unidad_curricular_id) REFERENCES unidades_curriculares(id),
            FOREIGN KEY (periodo_academico_id) REFERENCES periodos_academicos(id),
            FOREIGN KEY (sede_id) REFERENCES sedes(id),
            FOREIGN KEY (docente_id) REFERENCES docentes(id),
            UNIQUE(unidad_curricular_id, periodo_academico_id, sede_id, codigo_seccion)
        );'''
        self.ejecutar_consulta(instruccion1)

        instruccion2 = '''
        CREATE TABLE IF NOT EXISTS inscripciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estudiante_id INTEGER NOT NULL,
            seccion_id INTEGER NOT NULL,
            fecha_inscripcion DATE NOT NULL DEFAULT CURRENT_DATE,
            condicion TEXT DEFAULT 'Regular' CHECK (condicion IN ('Regular', 'Repitente', 'Equivalencia', 'Especial')),
            estado TEXT DEFAULT 'Inscrito' CHECK (estado IN ('Inscrito', 'Retirado', 'Aprobado', 'Reprobado')),
            nota_final REAL,
            porcentaje_asistencia REAL,
            observaciones TEXT,
            FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id),
            FOREIGN KEY (seccion_id) REFERENCES secciones(id),
            UNIQUE(estudiante_id, seccion_id)
        );'''
        self.ejecutar_consulta(instruccion2)

        instruccion3 = '''
        CREATE TABLE IF NOT EXISTS evaluaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inscripcion_id INTEGER NOT NULL,
            tipo_evaluacion TEXT NOT NULL,
            fecha_evaluacion DATE,
            nota REAL,
            porcentaje_valor REAL,
            observaciones TEXT,
            FOREIGN KEY (inscripcion_id) REFERENCES inscripciones(id)
        );'''
        self.ejecutar_consulta(instruccion3)
        
        instruccion4 = '''
        CREATE TABLE IF NOT EXISTS historial_academico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estudiante_id INTEGER NOT NULL,
            pnf_id INTEGER NOT NULL,
            periodo_academico_id INTEGER NOT NULL,
            promedio_periodo REAL,
            total_creditos_periodo INTEGER,
            promedio_acumulado REAL,
            total_creditos_acumulados INTEGER,
            observaciones TEXT,
            FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id),
            FOREIGN KEY (pnf_id) REFERENCES pnf(id),
            FOREIGN KEY (periodo_academico_id) REFERENCES periodos_academicos(id),
            UNIQUE(estudiante_id, pnf_id, periodo_academico_id)
        );'''
        self.ejecutar_consulta(instruccion4)

    def crear_base_datos(self):
        # Verificar si el directorio 'db' existe, si no, crearlo
        if not os.path.exists('db'):
            os.makedirs('db')

        print(f"Creando base de datos en: {os.path.join('db', 'sistema_academico.db')}")
        print(f"Fecha y hora: {datetime.datetime.now()}")

        self.crear_tablas_base()
        self.crear_tablas_catalogo()
        self.crear_tablas_academicas()
        self.crear_tablas_operativas()

        self.verificar_tablas()

    def verificar_tablas(self):
        db_ruta = os.path.join('db', 'sistema_academico.db')
        con = sql.connect(db_ruta)
        cursor = con.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = cursor.fetchall()
        con.close()

        print("\nTablas creadas:")
        for tabla in tablas:
            print(f"- {tabla[0]}")

        print(f"\nTotal de tablas creadas: {len(tablas)}")

if __name__ == "__main__":
    sistema_academico = SistemaAcademicoDB()
