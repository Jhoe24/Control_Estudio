# archivo newmodelo.py - Sistema Académico Mejorado
# Control de Estudios - Universidad Politécnica Territorial "José Félix Ribas"
import sqlite3 as sql
import os
import datetime
import hashlib
import secrets

class SistemaAcademicoDB:
    def __init__(self):
        self.crear_base_datos()

    def ejecutar_consulta(self, instruccion, parametros=None):
        """Ejecuta una consulta SQL con parámetros opcionales para mayor seguridad"""
        db_ruta = os.path.join('db', 'sistema_academico.db')
        con = sql.connect(db_ruta, isolation_level=None)
        cursor = con.cursor()
        
        # Habilitar foreign keys
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        try:
            if parametros:
                cursor.execute(instruccion, parametros)
            else:
                cursor.execute(instruccion)
            con.commit()
        except Exception as e:
            print(f"Error ejecutando consulta: {e}")
            con.rollback()
            raise
        finally:
            con.close()

    def crear_tablas_base(self):
        """Tablas base para información personal y contacto"""
        
        # Tabla principal de personas (base para estudiantes, docentes y usuarios del sistema)
        instruccion1 = '''
        CREATE TABLE IF NOT EXISTS informacion_personal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            documento_identidad TEXT,
            tipo_documento TEXT DEFAULT 'cedula' 
                CHECK (tipo_documento IN ('cedula', 'pasaporte', 'extranjeria')),
            nombres TEXT,
            apellidos TEXT,
            fecha_nacimiento DATE,
            sexo CHAR(1) CHECK (sexo IN ('M', 'F')),
            estado_civil TEXT CHECK (estado_civil IN ('Soltero', 'Casado', 'Divorciado', 'Viudo', 'Unión Libre')),
            nacionalidad TEXT DEFAULT 'Venezolana',
            lugar_nacimiento TEXT,
            correo_electronico TEXT,
            correo_institucional TEXT,
            fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
            fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            tipo TEXT CHECK (tipo IN ('estudiante', 'docente')),
            estado TEXT DEFAULT 'activo' 
                CHECK (estado IN ('activo', 'inactivo', 'suspendido')),
            UNIQUE(documento_identidad, tipo_documento)
        );'''
        self.ejecutar_consulta(instruccion1)
        
        # Tabla de teléfonos con mejor estructura
        instruccion2 = '''
        CREATE TABLE IF NOT EXISTS telefonos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            persona_id INTEGER,
            tipo_telefono TEXT 
                CHECK (tipo_telefono IN ('movil', 'casa', 'trabajo', 'emergencia')),
            codigo_pais TEXT DEFAULT '+58',
            numero TEXT,
            extension TEXT,
            principal BOOLEAN DEFAULT 0,
            fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (persona_id) REFERENCES informacion_personal(id) ON DELETE CASCADE
        );'''
        self.ejecutar_consulta(instruccion2)
        
        # Tabla de direcciones mejorada
        instruccion3 = '''
        CREATE TABLE IF NOT EXISTS direcciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            persona_id INTEGER,
            estado TEXT,
            municipio TEXT,
            parroquia TEXT,
            sector TEXT,
            calle TEXT,
            casa_edificio TEXT,
            piso_apartamento TEXT,
            codigo_postal TEXT,
            direccion_completa TEXT,
            tipo_direccion TEXT 
                CHECK (tipo_direccion IN ('residencia', 'trabajo', 'emergencia')),
            principal BOOLEAN DEFAULT 0,
            fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (persona_id) REFERENCES informacion_personal(id) ON DELETE CASCADE
        );'''
        self.ejecutar_consulta(instruccion3)

    def crear_tablas_usuarios_roles(self):
        """Sistema de usuarios, roles y permisos"""
        
        # Tabla de roles del sistema
        instruccion1 = '''
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE,
            nombre TEXT,
            descripcion TEXT,
            nivel_acceso INTEGER DEFAULT 1,
            estado TEXT DEFAULT 'activo' CHECK (estado IN ('activo', 'inactivo')),
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
        );'''
        self.ejecutar_consulta(instruccion1)
        
        # Tabla de permisos
        instruccion2 = '''
        CREATE TABLE IF NOT EXISTS permisos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE,
            nombre TEXT,
            descripcion TEXT,
            modulo TEXT,
            accion TEXT,
            estado TEXT DEFAULT 'activo' CHECK (estado IN ('activo', 'inactivo'))
        );'''
        self.ejecutar_consulta(instruccion2)
        
        # Tabla de relación roles-permisos
        instruccion3 = '''
        CREATE TABLE IF NOT EXISTS roles_permisos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rol_id INTEGER,
            permiso_id INTEGER,
            concedido BOOLEAN DEFAULT 1,
            fecha_asignacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (rol_id) REFERENCES roles(id) ON DELETE CASCADE,
            FOREIGN KEY (permiso_id) REFERENCES permisos(id) ON DELETE CASCADE,
            UNIQUE(rol_id, permiso_id)
        );'''
        self.ejecutar_consulta(instruccion3)
        
        # Tabla de usuarios del sistema
        instruccion4 = '''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            persona_id INTEGER,
            nombre_usuario TEXT UNIQUE,
            password_hash TEXT,
            salt TEXT,
            ultimo_acceso DATETIME,
            intentos_fallidos INTEGER DEFAULT 0,
            bloqueado BOOLEAN DEFAULT 0,
            fecha_bloqueo DATETIME,
            cambiar_password BOOLEAN DEFAULT 1,
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            fecha_expiracion DATETIME,
            estado TEXT DEFAULT 'activo' 
                CHECK (estado IN ('activo', 'inactivo', 'bloqueado', 'expirado')),
            token_recuperacion TEXT,
            fecha_token DATETIME,
            FOREIGN KEY (persona_id) REFERENCES informacion_personal(id) ON DELETE CASCADE
        );'''
        self.ejecutar_consulta(instruccion4)
        
        # Tabla de asignación de roles a usuarios
        instruccion5 = '''
        CREATE TABLE IF NOT EXISTS usuarios_roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            rol_id INTEGER,
            sede_id INTEGER,
            pnf_id INTEGER,
            fecha_asignacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            fecha_expiracion DATETIME,
            activo BOOLEAN DEFAULT 1,
            asignado_por INTEGER,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
            FOREIGN KEY (rol_id) REFERENCES roles(id),
            FOREIGN KEY (sede_id) REFERENCES sedes(id),
            FOREIGN KEY (pnf_id) REFERENCES pnf(id),
            FOREIGN KEY (asignado_por) REFERENCES usuarios(id),
            UNIQUE(usuario_id, rol_id, sede_id, pnf_id)
        );'''
        self.ejecutar_consulta(instruccion5)
        
        # Tabla de sesiones de usuario
        instruccion6 = '''
        CREATE TABLE IF NOT EXISTS sesiones_usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            token_sesion TEXT UNIQUE,
            ip_address TEXT,
            user_agent TEXT,
            fecha_inicio DATETIME DEFAULT CURRENT_TIMESTAMP,
            fecha_expiracion DATETIME,
            activa BOOLEAN DEFAULT 1,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        );'''
        self.ejecutar_consulta(instruccion6)

    def crear_tablas_catalogo(self):
        """Tablas de catálogos institucionales"""
        
        # Tabla de sedes mejorada
        instruccion1 = '''
        CREATE TABLE IF NOT EXISTS sedes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE,
            nombre TEXT,
            nombre_corto TEXT,
            tipo TEXT DEFAULT 'sede' CHECK (tipo IN ('sede', 'extension', 'nucleo')),
            direccion TEXT,
            telefono TEXT,
            correo TEXT,
            director TEXT,
            coordinador_academico TEXT,
            fecha_creacion DATE,
            fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            estado TEXT DEFAULT 'activa' CHECK (estado IN ('activa', 'inactiva', 'mantenimiento')),
            observaciones TEXT
        );'''
        self.ejecutar_consulta(instruccion1)

        # Tabla de PNF mejorada con más campos académicos
        instruccion2 = '''
        CREATE TABLE IF NOT EXISTS pnf (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE,
            codigo_nacional TEXT UNIQUE,
            nombre TEXT,
            nombre_corto TEXT,
            nivel TEXT  
                CHECK (nivel IN ('TSU', 'Ingeniería', 'Licenciatura', 'Medicina', 'Especialización')),
            area_conocimiento TEXT,
            duracion_trayectos INTEGER,
            duracion_semanas INTEGER,
            total_creditos INTEGER,
            total_horas INTEGER DEFAULT 0,
            modalidad TEXT DEFAULT 'Presencial' 
                CHECK (modalidad IN ('Presencial', 'Semipresencial', 'Virtual', 'Mixta')),
            titulo_otorga TEXT,
            perfil_egreso TEXT,
            campo_ocupacional TEXT,
            resolucion_creacion TEXT,
            fecha_resolucion DATE,
            version_pensum TEXT,
            coordinador_nacional TEXT,
            fecha_creacion DATE,
            fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            estado TEXT DEFAULT 'activo' CHECK (estado IN ('activo', 'inactivo', 'revision'))
        );'''
        self.ejecutar_consulta(instruccion2)

        # Tabla de relación sede-PNF con coordinador por sede
        instruccion3 = '''
        CREATE TABLE IF NOT EXISTS sede_pnf (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sede_id INTEGER,
            pnf_id INTEGER,
            coordinador_pnf TEXT,
            coordinador_usuario_id INTEGER,
            fecha_inicio DATE,
            fecha_fin DATE,
            turno_disponible TEXT CHECK (turno_disponible IN ('Diurno', 'Nocturno', 'Ambos', 'Fin de semana')),
            cupo_maximo INTEGER,
            estado TEXT DEFAULT 'activo' CHECK (estado IN ('activo', 'inactivo', 'suspendido')),
            observaciones TEXT,
            FOREIGN KEY (sede_id) REFERENCES sedes(id),
            FOREIGN KEY (pnf_id) REFERENCES pnf(id),
            FOREIGN KEY (coordinador_usuario_id) REFERENCES usuarios(id),
            UNIQUE(sede_id, pnf_id)
        );'''
        self.ejecutar_consulta(instruccion3)

        # Tabla de trayectos de formación
        instruccion4 = '''
        CREATE TABLE IF NOT EXISTS trayectos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pnf_id INTEGER,
            numero INTEGER,
            nombre TEXT,
            tipo TEXT CHECK (tipo IN ('Inicial', 'Profesional', 'Especialización', 'Investigación')),
            duracion_semanas INTEGER DEFAULT 0,
            duracion_horas INTEGER DEFAULT 0,
            creditos_minimos INTEGER DEFAULT 0,
            creditos_maximos INTEGER DEFAULT 0,
            numero_tramos INTEGER DEFAULT 0,
            objetivos TEXT,
            competencias TEXT,
            perfil_egreso TEXT,
            obligatorio BOOLEAN DEFAULT 1,
            secuencial BOOLEAN DEFAULT 1,
            estado TEXT DEFAULT 'activo' CHECK (estado IN ('activo', 'inactivo')),
            FOREIGN KEY (pnf_id) REFERENCES pnf(id),
            UNIQUE(pnf_id, numero)
        );'''
        self.ejecutar_consulta(instruccion4)

        # Tabla de tramos
        instruccion5 = '''
        CREATE TABLE IF NOT EXISTS tramos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trayecto_id INTEGER,
            numero INTEGER,
            nombre TEXT,
            duracion_semanas INTEGER DEFAULT 0,
            duracion_horas INTEGER DEFAULT 0,
            creditos INTEGER DEFAULT 0,
            objetivos TEXT,
            competencias TEXT,
            estado TEXT DEFAULT 'activo' CHECK (estado IN ('activo', 'inactivo')),
            FOREIGN KEY (trayecto_id) REFERENCES trayectos(id),
            UNIQUE(trayecto_id, numero)
        );'''
        self.ejecutar_consulta(instruccion5)

        # Tabla de unidades curriculares mejorada
        instruccion6 = '''
        CREATE TABLE IF NOT EXISTS unidades_curriculares (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT,
            nombre TEXT,
            nombre_corto TEXT,
            pnf_id INTEGER,
            trayecto_id INTEGER,
            tramo_id INTEGER,
            area TEXT,
            subarea TEXT,
            eje_formativo TEXT,
            horas_teoricas REAL DEFAULT 0,
            horas_practicas REAL DEFAULT 0,
            horas_laboratorio REAL DEFAULT 0,
            horas_trabajo_independiente REAL DEFAULT 0,
            horas_totales REAL DEFAULT 0,
            unidades_credito INTEGER,
            tipo TEXT DEFAULT 'Obligatoria' 
                CHECK (tipo IN ('Obligatoria', 'Electiva', 'Proyecto', 'Pasantía', 'Trabajo Especial')),
            caracter TEXT DEFAULT 'Teórica'
                CHECK (caracter IN ('Teórica', 'Práctica', 'Teórico-Práctica', 'Laboratorio')),
            modalidad TEXT DEFAULT 'Presencial' 
                CHECK (modalidad IN ('Presencial', 'Semipresencial', 'Virtual')),
            complejidad TEXT DEFAULT 'Básica'
                CHECK (complejidad IN ('Básica', 'Intermedia', 'Avanzada')),
            prelaciones TEXT,
            competencias_genericas TEXT,
            competencias_especificas TEXT,
            saberes_cognitivos TEXT,
            saberes_procedimentales TEXT,
            saberes_actitudinales TEXT,
            estrategias_ensenanza TEXT,
            recursos_didacticos TEXT,
            evaluacion TEXT,
            bibliografia TEXT,
            homologacion_clave TEXT,
            clave_especial TEXT,
            estado TEXT DEFAULT 'activa' CHECK (estado IN ('activa', 'inactiva', 'revision')),
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (pnf_id) REFERENCES pnf(id),
            FOREIGN KEY (trayecto_id) REFERENCES trayectos(id),
            FOREIGN KEY (tramo_id) REFERENCES tramos(id),
            UNIQUE(codigo, pnf_id, tramo_id)
        );'''
        self.ejecutar_consulta(instruccion6)

        # Tabla de periodos académicos
        instruccion7 = '''
        CREATE TABLE IF NOT EXISTS periodos_academicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE,
            nombre TEXT,
            tipo TEXT DEFAULT 'Regular' CHECK (tipo IN ('Regular', 'Intensivo', 'Intersemestral', 'Especial')),
            fecha_inicio DATE,
            fecha_fin DATE,
            fecha_inicio_inscripcion DATE,
            fecha_fin_inscripcion DATE,
            fecha_inicio_clases DATE,
            fecha_fin_clases DATE,
            fecha_inicio_evaluaciones DATE,
            fecha_fin_evaluaciones DATE,
            duracion_semanas INTEGER,
            estado TEXT DEFAULT 'planificacion'
                CHECK (estado IN ('planificacion', 'inscripcion', 'en_curso', 'evaluaciones', 'finalizado', 'cerrado')),
            observaciones TEXT
        );'''
        self.ejecutar_consulta(instruccion7)

    def crear_tablas_academicas(self):
        """Tablas específicas para estudiantes y docentes"""
        
        # Tabla de estudiantes mejorada
        instruccion1 = '''
        CREATE TABLE IF NOT EXISTS estudiantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            persona_id INTEGER UNIQUE,
            codigo_unico TEXT UNIQUE,
            codigo_estudiantil TEXT,
            tipo_ingreso TEXT CHECK (tipo_ingreso IN ('Nuevo', 'Transferencia', 'Reingreso', 'Equivalencia')),
            institucion_procedencia TEXT,
            tipo_bachiller TEXT,
            mencion_bachiller TEXT,
            fecha_grado_bachiller DATE,
            nota_bachiller REAL,
            profesion_anterior TEXT,
            institucion_profesional TEXT,
            fecha_grado_profesional DATE,
            fecha_ingreso DATE,
            cohorte TEXT,
            condicion TEXT DEFAULT 'Regular' 
                CHECK (condicion IN ('Regular', 'Repitente', 'Reingreso', 'Transferencia', 'Convalidación')),
            oyente BOOLEAN DEFAULT 0,
            beca BOOLEAN DEFAULT 0,
            tipo_beca TEXT,
            situacion_academica TEXT DEFAULT 'Activo'
                CHECK (situacion_academica IN ('Activo', 'Inactivo', 'Graduado', 'Retirado', 'Egresado', 'Suspendido')),
            fecha_cambio_situacion DATE,
            observaciones TEXT,
            FOREIGN KEY (persona_id) REFERENCES informacion_personal(id) ON DELETE CASCADE
        );'''
        self.ejecutar_consulta(instruccion1)

        # Tabla de docentes mejorada
        instruccion2 = '''
        CREATE TABLE IF NOT EXISTS docentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            persona_id INTEGER UNIQUE,
            codigo_docente TEXT UNIQUE,
            abreviatura_titulo TEXT,
            titulo_pregrado TEXT,
            institucion_pregrado TEXT,
            titulo_postgrado TEXT,
            institucion_postgrado TEXT,
            especialidad TEXT,
            area_conocimiento TEXT,
            fecha_ingreso DATE,
            fecha_ingreso_uptrjf DATE,
            tipo_contrato TEXT DEFAULT 'Tiempo completo' 
                CHECK (tipo_contrato IN ('Tiempo completo', 'Medio tiempo', 'Por horas', 'Contratado', 'Jubilado Activo')),
            categoria TEXT,
            escalafon TEXT,
            auxiliar BOOLEAN DEFAULT 0,
            coordinador BOOLEAN DEFAULT 0,
            dedicacion TEXT DEFAULT 'Tiempo completo' 
                CHECK (dedicacion IN ('Exclusiva', 'Tiempo completo', 'Medio tiempo', 'Tiempo convencional')),
            carga_horaria INTEGER,
            experiencia_anos INTEGER,
            investigador BOOLEAN DEFAULT 0,
            tutor BOOLEAN DEFAULT 0,
            estado TEXT DEFAULT 'Activo' 
                CHECK (estado IN ('Activo', 'Inactivo', 'Jubilado', 'Permiso', 'Comision')),
            fecha_cambio_estado DATE,
            observaciones TEXT,
            FOREIGN KEY (persona_id) REFERENCES informacion_personal(id) ON DELETE CASCADE
        );'''
        self.ejecutar_consulta(instruccion2)

        # Tabla de inscripción de estudiantes en PNF por sede
        instruccion3 = '''
        CREATE TABLE IF NOT EXISTS estudiante_pnf (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estudiante_id INTEGER,
            pnf_id INTEGER,
            sede_id INTEGER,
            fecha_inicio DATE,
            fecha_fin DATE,
            cohorte TEXT,
            turno TEXT CHECK (turno IN ('Diurno', 'Nocturno', 'Fin de semana')),
            trayecto_actual INTEGER DEFAULT 1,
            tramo_actual INTEGER DEFAULT 1,
            creditos_aprobados INTEGER DEFAULT 0,
            creditos_cursados INTEGER DEFAULT 0,
            promedio_general REAL DEFAULT 0.0,
            estado TEXT DEFAULT 'Activo' 
                CHECK (estado IN ('Activo', 'Inactivo', 'Graduado', 'Retirado', 'Suspendido', 'Transferido')),
            fecha_cambio_estado DATE,
            observaciones TEXT,
            FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id),
            FOREIGN KEY (pnf_id) REFERENCES pnf(id),
            FOREIGN KEY (sede_id) REFERENCES sedes(id),
            UNIQUE(estudiante_id, pnf_id, sede_id)
        );'''
        self.ejecutar_consulta(instruccion3)

        # Tabla de asignación de docentes a sedes y PNF
        instruccion4 = '''
        CREATE TABLE IF NOT EXISTS docente_sede_pnf (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            docente_id INTEGER,
            sede_id INTEGER,
            pnf_id INTEGER,
            fecha_asignacion DATE,
            fecha_desasignacion DATE,
            coordinador BOOLEAN DEFAULT 0,
            activo BOOLEAN DEFAULT 1,
            observaciones TEXT,
            FOREIGN KEY (docente_id) REFERENCES docentes(id),
            FOREIGN KEY (sede_id) REFERENCES sedes(id),
            FOREIGN KEY (pnf_id) REFERENCES pnf(id)
        );'''
        self.ejecutar_consulta(instruccion4)

    def crear_tablas_operativas(self):
        """Tablas operativas del sistema académico"""
        
        # Tabla de secciones mejorada
        instruccion1 = '''
        CREATE TABLE IF NOT EXISTS secciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sede_id INTEGER,
            periodo_academico_id INTEGER,
            pnf_id INTEGER,
            trayecto_id INTEGER,
            tramo_id INTEGER,
            codigo_seccion TEXT,
            docente_titular_id INTEGER,
            docente_auxiliar_id INTEGER,
            cupo_maximo INTEGER DEFAULT 40,
            cupo_minimo INTEGER DEFAULT 15,
            inscritos INTEGER DEFAULT 0,
            aprobados INTEGER DEFAULT 0,
            reprobados INTEGER DEFAULT 0,
            retirados INTEGER DEFAULT 0,
            turno TEXT CHECK (turno IN ('Diurno', 'Nocturno', 'Fin de semana')),
            modalidad TEXT DEFAULT 'Presencial' 
                CHECK (modalidad IN ('Presencial', 'Semipresencial', 'Virtual')),
            aula TEXT,
            horario TEXT,
            dias_semana TEXT,
            fecha_inicio DATE,
            fecha_fin DATE,
            horas_programadas INTEGER,
            horas_ejecutadas INTEGER DEFAULT 0,
            porcentaje_avance REAL DEFAULT 0.0,
            estado TEXT DEFAULT 'Planificada'
                CHECK (estado IN ('Planificada', 'Abierta', 'En curso', 'Finalizada', 'Cancelada', 'Suspendida')),
            fecha_cambio_estado DATE,
            observaciones TEXT,
            FOREIGN KEY (pnf_id) REFERENCES pnf(id),
            FOREIGN KEY (trayecto_id) REFERENCES trayectos(id),
            FOREIGN KEY (tramo_id) REFERENCES tramos(id),
            FOREIGN KEY (periodo_academico_id) REFERENCES periodos_academicos(id),
            FOREIGN KEY (sede_id) REFERENCES sedes(id),
            FOREIGN KEY (docente_titular_id) REFERENCES docentes(id),
            FOREIGN KEY (docente_auxiliar_id) REFERENCES docentes(id)
        );'''
        self.ejecutar_consulta(instruccion1)

        # Tabla de inscripciones mejorada
        instruccion2 = '''
        CREATE TABLE IF NOT EXISTS inscripciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estudiante_id INTEGER,
            seccion_id INTEGER,
            fecha_inscripcion DATETIME DEFAULT CURRENT_TIMESTAMP,
            condicion TEXT DEFAULT 'Regular' 
                CHECK (condicion IN ('Regular', 'Repitente', 'Equivalencia', 'Especial', 'Oyente')),
            estado TEXT DEFAULT 'Inscrito' 
                CHECK (estado IN ('Inscrito', 'Retirado', 'Aprobado', 'Reprobado', 'Sin Calificar')),
            fecha_cambio_estado DATE,
            nota_final REAL,
            nota_definitiva TEXT,
            porcentaje_asistencia REAL,
            numero_faltas INTEGER DEFAULT 0,
            perdio_por_faltas BOOLEAN DEFAULT 0,
            fecha_retiro DATE,
            motivo_retiro TEXT,
            observaciones TEXT,
            usuario_inscripcion INTEGER,
            FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id),
            FOREIGN KEY (seccion_id) REFERENCES secciones(id),
            FOREIGN KEY (usuario_inscripcion) REFERENCES usuarios(id),
            UNIQUE(estudiante_id, seccion_id)
        );'''
        self.ejecutar_consulta(instruccion2)

        # Tabla de evaluaciones mejorada
        instruccion3 = '''
        CREATE TABLE IF NOT EXISTS evaluaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inscripcion_id INTEGER,
            unidad_curricular_id INTEGER,
            tipo_evaluacion TEXT 
                CHECK (tipo_evaluacion IN ('Parcial', 'Final', 'Recuperativa', 'Extraordinaria', 'Proyecto', 'Práctica', 'Laboratorio')),
            numero_evaluacion INTEGER,
            descripcion TEXT,
            fecha_programada DATE,
            fecha_aplicada DATE,
            fecha_calificada DATE,
            nota REAL,
            nota_maxima REAL DEFAULT 20.0,
            porcentaje_valor REAL,
            peso_evaluacion REAL,
            aprobada BOOLEAN,
            observaciones TEXT,
            docente_califica INTEGER,
            fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (inscripcion_id) REFERENCES inscripciones(id),
            FOREIGN KEY (unidad_curricular_id) REFERENCES unidades_curriculares(id),
            FOREIGN KEY (docente_califica) REFERENCES docentes(id),
            UNIQUE(inscripcion_id, unidad_curricular_id, tipo_evaluacion)
        );'''
        self.ejecutar_consulta(instruccion3)
        
        # Tabla de historial académico mejorada
        instruccion4 = '''
        CREATE TABLE IF NOT EXISTS historial_academico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estudiante_id INTEGER,
            pnf_id INTEGER,
            periodo_academico_id INTEGER,
            sede_id INTEGER,
            trayecto INTEGER,
            tramo INTEGER,
            unidades_inscritas INTEGER DEFAULT 0,
            unidades_aprobadas INTEGER DEFAULT 0,
            unidades_reprobadas INTEGER DEFAULT 0,
            unidades_retiradas INTEGER DEFAULT 0,
            creditos_inscritos INTEGER DEFAULT 0,
            creditos_aprobados INTEGER DEFAULT 0,
            promedio_periodo REAL,
            promedio_acumulado REAL,
            total_creditos_acumulados INTEGER DEFAULT 0,
            eficiencia REAL,
            indice_academico REAL,
            situacion_periodo TEXT CHECK (situacion_periodo IN ('Regular', 'Condicionado', 'Probatorio', 'Excelente')),
            observaciones TEXT,
            fecha_calculo DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id),
            FOREIGN KEY (pnf_id) REFERENCES pnf(id),
            FOREIGN KEY (periodo_academico_id) REFERENCES periodos_academicos(id),
            FOREIGN KEY (sede_id) REFERENCES sedes(id),
            UNIQUE(estudiante_id, pnf_id, periodo_academico_id, sede_id)
        );'''
        self.ejecutar_consulta(instruccion4)

        # Tabla de asistencia
        instruccion5 = '''
        CREATE TABLE IF NOT EXISTS asistencia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inscripcion_id INTEGER,
            fecha DATE,
            presente BOOLEAN DEFAULT 0,
            tardanza BOOLEAN DEFAULT 0,
            minutos_tardanza INTEGER DEFAULT 0,
            justificada BOOLEAN DEFAULT 0,
            observaciones TEXT,
            docente_registro INTEGER,
            fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (inscripcion_id) REFERENCES inscripciones(id),
            FOREIGN KEY (docente_registro) REFERENCES docentes(id),
            UNIQUE(inscripcion_id, fecha)
        );'''
        self.ejecutar_consulta(instruccion5)
        
        # notas finales por unidad curricular
        instruccion_notas = '''
        CREATE TABLE IF NOT EXISTS notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inscripcion_id INTEGER NOT NULL,
            unidad_curricular_id INTEGER NOT NULL,
            valor REAL NOT NULL CHECK(valor BETWEEN 0 AND 20),
            fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (inscripcion_id)       REFERENCES inscripciones(id) ON DELETE CASCADE,
            FOREIGN KEY (unidad_curricular_id) REFERENCES unidades_curriculares(id),
            UNIQUE(inscripcion_id, unidad_curricular_id)
        );'''
        self.ejecutar_consulta(instruccion_notas)

    def crear_tablas_auditoria(self):
        """Tablas para auditoría y logs del sistema"""
        
        instruccion1 = '''
        CREATE TABLE IF NOT EXISTS auditoria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tabla_afectada TEXT,
            registro_id INTEGER,
            accion TEXT CHECK (accion IN ('INSERT', 'UPDATE', 'DELETE')),
            usuario_id INTEGER,
            fecha_accion DATETIME DEFAULT CURRENT_TIMESTAMP,
            valores_anteriores TEXT,
            valores_nuevos TEXT,
            ip_address TEXT,
            observaciones TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        );'''
        self.ejecutar_consulta(instruccion1)

    def insertar_datos_iniciales(self):
        """Inserta datos iniciales básicos del sistema"""
        
        # Insertar sedes
        sedes_datos = [
            ('BARINAS-01', 'Sede Barinas', 'Barinas'),
            ('BARINITAS-01', 'Sede Barinitas', 'Barinitas'),
            ('SOCOPO-01', 'Sede Socopó', 'Socopó')
        ]
        
        for codigo, nombre, nombre_corto in sedes_datos:
            try:
                self.ejecutar_consulta('''
                    INSERT OR IGNORE INTO sedes (codigo, nombre, nombre_corto, direccion, estado)
                    VALUES (?, ?, ?, ?, 'activa')
                ''', (codigo, nombre, nombre_corto, f'Dirección {nombre}'))
            except Exception as e:
                print(f"Error insertando sede {nombre}: {e}")
        
        # Insertar roles básicos del sistema
        roles_datos = [
            ('ADMIN', 'Administrador del Sistema', 'Control total del sistema', 10),
            ('COORD_GENERAL', 'Coordinador General de Control de Estudios', 'Gestión académica general', 9),
            ('COORD_PNF', 'Coordinador de PNF', 'Coordinación de Programa Nacional de Formación', 7),
            ('DOCENTE', 'Docente', 'Gestión de secciones y evaluaciones', 5),
            ('ESTUDIANTE', 'Estudiante', 'Consulta de información académica personal', 3),
            ('SECRETARIA', 'Personal de Secretaría', 'Gestión de inscripciones y registros', 6),
            ('DIRECTOR_SEDE', 'Director de Sede', 'Administración de sede específica', 8)
        ]
        
        for codigo, nombre, descripcion, nivel in roles_datos:
            try:
                self.ejecutar_consulta('''
                    INSERT OR IGNORE INTO roles (codigo, nombre, descripcion, nivel_acceso)
                    VALUES (?, ?, ?, ?)
                ''', (codigo, nombre, descripcion, nivel))
            except Exception as e:
                print(f"Error insertando rol {nombre}: {e}")
        
        # Insertar permisos básicos
        permisos_datos = [
            # Permisos de estudiantes
            ('EST_CONSULTAR_INFO', 'Consultar Información Personal', 'Ver información personal', 'estudiantes', 'read'),
            ('EST_ACTUALIZAR_INFO', 'Actualizar Información Personal', 'Modificar datos personales', 'estudiantes', 'update'),
            ('EST_CONSULTAR_NOTAS', 'Consultar Calificaciones', 'Ver notas y evaluaciones', 'evaluaciones', 'read'),
            ('EST_INSCRIBIRSE', 'Realizar Inscripciones', 'Inscribirse en secciones', 'inscripciones', 'create'),
            
            # Permisos de docentes
            ('DOC_GESTIONAR_SECCION', 'Gestionar Secciones', 'Administrar secciones asignadas', 'secciones', 'manage'),
            ('DOC_CALIFICAR', 'Registrar Calificaciones', 'Ingresar y modificar notas', 'evaluaciones', 'create_update'),
            ('DOC_TOMAR_ASISTENCIA', 'Tomar Asistencia', 'Registrar asistencia de estudiantes', 'asistencia', 'create_update'),
            ('DOC_CONSULTAR_ESTUDIANTES', 'Consultar Estudiantes', 'Ver información de estudiantes inscritos', 'estudiantes', 'read'),
            
            # Permisos de coordinadores PNF
            ('COORD_GESTIONAR_UC', 'Gestionar Unidades Curriculares', 'Administrar pensum y materias', 'unidades_curriculares', 'full'),
            ('COORD_GESTIONAR_INSCRIPCIONES', 'Gestionar Inscripciones', 'Administrar inscripciones del PNF', 'inscripciones', 'full'),
            ('COORD_ASIGNAR_DOCENTES', 'Asignar Docentes', 'Asignar docentes a secciones', 'secciones', 'assign'),
            ('COORD_REPORTES_PNF', 'Generar Reportes PNF', 'Crear reportes académicos del PNF', 'reportes', 'generate'),
            
            # Permisos administrativos
            ('ADMIN_USUARIOS', 'Administrar Usuarios', 'Gestionar usuarios del sistema', 'usuarios', 'full'),
            ('ADMIN_ROLES', 'Administrar Roles', 'Gestionar roles y permisos', 'roles', 'full'),
            ('ADMIN_SEDES', 'Administrar Sedes', 'Gestionar sedes de la universidad', 'sedes', 'full'),
            ('ADMIN_PNF', 'Administrar PNF', 'Gestionar Programas Nacionales de Formación', 'pnf', 'full'),
            ('ADMIN_PERIODOS', 'Administrar Períodos', 'Gestionar períodos académicos', 'periodos_academicos', 'full'),
            
            # Permisos de secretaría
            ('SEC_INSCRIPCIONES', 'Procesar Inscripciones', 'Realizar inscripciones de estudiantes', 'inscripciones', 'create_update'),
            ('SEC_CONSULTAR_ACADEMICO', 'Consultar Información Académica', 'Ver expedientes académicos', 'historial_academico', 'read'),
            ('SEC_GENERAR_CONSTANCIAS', 'Generar Constancias', 'Emitir constancias y certificados', 'constancias', 'generate')
        ]
        
        for codigo, nombre, descripcion, modulo, accion in permisos_datos:
            try:
                self.ejecutar_consulta('''
                    INSERT OR IGNORE INTO permisos (codigo, nombre, descripcion, modulo, accion)
                    VALUES (?, ?, ?, ?, ?)
                ''', (codigo, nombre, descripcion, modulo, accion))
            except Exception as e:
                print(f"Error insertando permiso {nombre}: {e}")
        
        # Asignar permisos a roles
        self.asignar_permisos_roles()
    
    def asignar_permisos_roles(self):
        """Asigna permisos específicos a cada rol"""
        
        # Obtener IDs de roles
        db_ruta = os.path.join('db', 'sistema_academico.db')
        con = sql.connect(db_ruta)
        cursor = con.cursor()
        
        try:
            # Rol ESTUDIANTE
            cursor.execute("SELECT id FROM roles WHERE codigo = 'ESTUDIANTE'")
            rol_estudiante = cursor.fetchone()
            if rol_estudiante:
                permisos_estudiante = ['EST_CONSULTAR_INFO', 'EST_ACTUALIZAR_INFO', 'EST_CONSULTAR_NOTAS', 'EST_INSCRIBIRSE']
                for permiso_codigo in permisos_estudiante:
                    cursor.execute("SELECT id FROM permisos WHERE codigo = ?", (permiso_codigo,))
                    permiso = cursor.fetchone()
                    if permiso:
                        cursor.execute('''
                            INSERT OR IGNORE INTO roles_permisos (rol_id, permiso_id)
                            VALUES (?, ?)
                        ''', (rol_estudiante[0], permiso[0]))
            
            # Rol DOCENTE
            cursor.execute("SELECT id FROM roles WHERE codigo = 'DOCENTE'")
            rol_docente = cursor.fetchone()
            if rol_docente:
                permisos_docente = [
                    'DOC_GESTIONAR_SECCION', 'DOC_CALIFICAR', 'DOC_TOMAR_ASISTENCIA', 
                    'DOC_CONSULTAR_ESTUDIANTES', 'EST_CONSULTAR_INFO'
                ]
                for permiso_codigo in permisos_docente:
                    cursor.execute("SELECT id FROM permisos WHERE codigo = ?", (permiso_codigo,))
                    permiso = cursor.fetchone()
                    if permiso:
                        cursor.execute('''
                            INSERT OR IGNORE INTO roles_permisos (rol_id, permiso_id)
                            VALUES (?, ?)
                        ''', (rol_docente[0], permiso[0]))
            
            # Rol COORDINADOR PNF
            cursor.execute("SELECT id FROM roles WHERE codigo = 'COORD_PNF'")
            rol_coord_pnf = cursor.fetchone()
            if rol_coord_pnf:
                permisos_coord_pnf = [
                    'COORD_GESTIONAR_UC', 'COORD_GESTIONAR_INSCRIPCIONES', 
                    'COORD_ASIGNAR_DOCENTES', 'COORD_REPORTES_PNF',
                    'DOC_GESTIONAR_SECCION', 'DOC_CONSULTAR_ESTUDIANTES', 'SEC_CONSULTAR_ACADEMICO'
                ]
                for permiso_codigo in permisos_coord_pnf:
                    cursor.execute("SELECT id FROM permisos WHERE codigo = ?", (permiso_codigo,))
                    permiso = cursor.fetchone()
                    if permiso:
                        cursor.execute('''
                            INSERT OR IGNORE INTO roles_permisos (rol_id, permiso_id)
                            VALUES (?, ?)
                        ''', (rol_coord_pnf[0], permiso[0]))
            
            # Rol ADMIN (todos los permisos)
            cursor.execute("SELECT id FROM roles WHERE codigo = 'ADMIN'")
            rol_admin = cursor.fetchone()
            if rol_admin:
                cursor.execute("SELECT id FROM permisos")
                todos_permisos = cursor.fetchall()
                for permiso in todos_permisos:
                    cursor.execute('''
                        INSERT OR IGNORE INTO roles_permisos (rol_id, permiso_id)
                        VALUES (?, ?)
                    ''', (rol_admin[0], permiso[0]))
            
            con.commit()
            
        except Exception as e:
            print(f"Error asignando permisos a roles: {e}")
            con.rollback()
        finally:
            con.close()

    def crear_usuario_admin_inicial(self):
        """Crea el usuario administrador inicial del sistema"""
        try:
            # Crear persona para admin
            self.ejecutar_consulta('''
                INSERT OR IGNORE INTO informacion_personal 
                (documento_identidad, tipo_documento, nombres, apellidos, correo_electronico, correo_institucional)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ('00000000', 'cedula', 'Administrador', 'del Sistema', 'admin@uptrjf.edu.ve', 'admin@uptrjf.edu.ve'))
            
            # Obtener ID de la persona creada
            db_ruta = os.path.join('db', 'sistema_academico.db')
            con = sql.connect(db_ruta)
            cursor = con.cursor()
            
            cursor.execute("SELECT id FROM informacion_personal WHERE documento_identidad = '00000000'")
            persona_id = cursor.fetchone()[0]
            
            # Generar hash de contraseña por defecto
            password_default = "admin123"
            salt = secrets.token_hex(32)
            password_hash = hashlib.sha256((password_default + salt).encode()).hexdigest()
            
            # Crear usuario admin
            cursor.execute('''
                INSERT OR IGNORE INTO usuarios 
                (persona_id, nombre_usuario, password_hash, salt, cambiar_password)
                VALUES (?, ?, ?, ?, ?)
            ''', (persona_id, 'admin', password_hash, salt, 1))
            
            # Obtener ID del usuario creado
            cursor.execute("SELECT id FROM usuarios WHERE nombre_usuario = 'admin'")
            usuario_id = cursor.fetchone()[0]
            
            # Asignar rol de administrador
            cursor.execute("SELECT id FROM roles WHERE codigo = 'ADMIN'")
            rol_admin_id = cursor.fetchone()[0]
            
            cursor.execute('''
                INSERT OR IGNORE INTO usuarios_roles (usuario_id, rol_id)
                VALUES (?, ?)
            ''', (usuario_id, rol_admin_id))
            
            con.commit()
            con.close()
            
            print("Usuario administrador creado:")
            print("Usuario: admin")
            print("Contraseña: admin123")
            print("IMPORTANTE: Cambiar la contraseña en el primer acceso")
            
        except Exception as e:
            print(f"Error creando usuario administrador: {e}")

    def crear_triggers_auditoria(self):
        """Crea triggers para auditoría automática"""
        
        tablas_auditoria = [
            'usuarios', 'estudiantes', 'docentes', 'inscripciones', 
            'evaluaciones', 'secciones', 'historial_academico'
        ]
        
        for tabla in tablas_auditoria:
            # Trigger para INSERT
            trigger_insert = f'''
            CREATE TRIGGER IF NOT EXISTS audit_{tabla}_insert
            AFTER INSERT ON {tabla}
            BEGIN
                INSERT INTO auditoria (tabla_afectada, registro_id, accion, valores_nuevos, fecha_accion)
                VALUES ('{tabla}', NEW.id, 'INSERT', 
                        json_object({self.get_columnas_json_new(tabla)}), 
                        datetime('now'));
            END;
            '''
            
            # Trigger para UPDATE
            trigger_update = f'''
            CREATE TRIGGER IF NOT EXISTS audit_{tabla}_update
            AFTER UPDATE ON {tabla}
            BEGIN
                INSERT INTO auditoria (tabla_afectada, registro_id, accion, valores_anteriores, valores_nuevos, fecha_accion)
                VALUES ('{tabla}', NEW.id, 'UPDATE',
                        json_object({self.get_columnas_json_old(tabla)}),
                        json_object({self.get_columnas_json_new(tabla)}),
                        datetime('now'));
            END;
            '''
            
            # Trigger para DELETE
            trigger_delete = f'''
            CREATE TRIGGER IF NOT EXISTS audit_{tabla}_delete
            AFTER DELETE ON {tabla}
            BEGIN
                INSERT INTO auditoria (tabla_afectada, registro_id, accion, valores_anteriores, fecha_accion)
                VALUES ('{tabla}', OLD.id, 'DELETE',
                        json_object({self.get_columnas_json_old(tabla)}),
                        datetime('now'));
            END;
            '''
            
            try:
                self.ejecutar_consulta(trigger_insert)
                self.ejecutar_consulta(trigger_update)
                self.ejecutar_consulta(trigger_delete)
            except Exception as e:
                print(f"Error creando triggers para {tabla}: {e}")

    def get_columnas_json_new(self, tabla):
        """Genera string de columnas para JSON en triggers (NEW)"""
        columnas_comunes = "'id', NEW.id"
        
        if tabla == 'usuarios':
            return f"{columnas_comunes}, 'nombre_usuario', NEW.nombre_usuario, 'estado', NEW.estado"
        elif tabla == 'estudiantes':
            return f"{columnas_comunes}, 'codigo_unico', NEW.codigo_unico, 'situacion_academica', NEW.situacion_academica"
        elif tabla == 'inscripciones':
            return f"{columnas_comunes}, 'estudiante_id', NEW.estudiante_id, 'seccion_id', NEW.seccion_id, 'estado', NEW.estado"
        else:
            return f"{columnas_comunes}"

    def get_columnas_json_old(self, tabla):
        """Genera string de columnas para JSON en triggers (OLD)"""
        columnas_comunes = "'id', OLD.id"
        
        if tabla == 'usuarios':
            return f"{columnas_comunes}, 'nombre_usuario', OLD.nombre_usuario, 'estado', OLD.estado"
        elif tabla == 'estudiantes':
            return f"{columnas_comunes}, 'codigo_unico', OLD.codigo_unico, 'situacion_academica', OLD.situacion_academica"
        elif tabla == 'inscripciones':
            return f"{columnas_comunes}, 'estudiante_id', OLD.estudiante_id, 'seccion_id', OLD.seccion_id, 'estado', OLD.estado"
        else:
            return f"{columnas_comunes}"

    def crear_indices_optimizacion(self):
        """Crea índices para optimizar consultas frecuentes"""
        
        indices = [
            # Índices para búsquedas frecuentes
            "CREATE INDEX IF NOT EXISTS idx_informacion_personal_documento ON informacion_personal(documento_identidad, tipo_documento);",
            "CREATE INDEX IF NOT EXISTS idx_informacion_personal_nombres ON informacion_personal(nombres, apellidos);",
            "CREATE INDEX IF NOT EXISTS idx_usuarios_nombre_usuario ON usuarios(nombre_usuario);",
            "CREATE INDEX IF NOT EXISTS idx_usuarios_persona ON usuarios(persona_id);",
            
            # Índices para relaciones académicas
            "CREATE INDEX IF NOT EXISTS idx_estudiantes_codigo ON estudiantes(codigo_unico);",
            "CREATE INDEX IF NOT EXISTS idx_estudiante_pnf_sede ON estudiante_pnf(estudiante_id, pnf_id, sede_id);",
            "CREATE INDEX IF NOT EXISTS idx_inscripciones_estudiante ON inscripciones(estudiante_id);",
            "CREATE INDEX IF NOT EXISTS idx_inscripciones_seccion ON inscripciones(seccion_id);",
            "CREATE INDEX IF NOT EXISTS idx_secciones_periodo ON secciones(periodo_academico_id, sede_id);",
            "CREATE INDEX IF NOT EXISTS idx_secciones_docente ON secciones(docente_titular_id);",
            
            # Índices para auditoría y logs
            "CREATE INDEX IF NOT EXISTS idx_auditoria_tabla_fecha ON auditoria(tabla_afectada, fecha_accion);",
            "CREATE INDEX IF NOT EXISTS idx_auditoria_usuario ON auditoria(usuario_id);",
            "CREATE INDEX IF NOT EXISTS idx_sesiones_usuario ON sesiones_usuario(usuario_id, activa);",
            
            # Índices para reportes
            "CREATE INDEX IF NOT EXISTS idx_historial_periodo ON historial_academico(periodo_academico_id, pnf_id);",
            "CREATE INDEX IF NOT EXISTS idx_evaluaciones_inscripcion ON evaluaciones(inscripcion_id);",
            "CREATE INDEX IF NOT EXISTS idx_asistencia_inscripcion_fecha ON asistencia(inscripcion_id, fecha);"
        ]
        
        for indice in indices:
            try:
                self.ejecutar_consulta(indice)
            except Exception as e:
                print(f"Error creando índice: {e}")

    def crear_vistas_consultas(self):
        """Crea vistas para consultas frecuentes y reportes"""
        
        # Vista de información completa de estudiantes
        vista_estudiantes = '''
        CREATE VIEW IF NOT EXISTS vista_estudiantes_completa AS
        SELECT 
            e.id,
            e.codigo_unico,
            p.documento_identidad,
            p.nombres || ' ' || p.apellidos as nombre_completo,
            p.correo_electronico,
            p.fecha_nacimiento,
            e.fecha_ingreso,
            e.situacion_academica,
            ep.pnf_id,
            pnf.nombre as pnf_nombre,
            ep.sede_id,
            s.nombre as sede_nombre,
            ep.trayecto_actual,
            ep.tramo_actual,
            ep.creditos_aprobados,
            ep.promedio_general
        FROM estudiantes e
        JOIN informacion_personal p ON e.persona_id = p.id
        LEFT JOIN estudiante_pnf ep ON e.id = ep.estudiante_id
        LEFT JOIN pnf ON ep.pnf_id = pnf.id
        LEFT JOIN sedes s ON ep.sede_id = s.id
        WHERE p.estado = 'activo';
        '''
        
        # Vista de información completa de docentes
        vista_docentes = '''
        CREATE VIEW IF NOT EXISTS vista_docentes_completa AS
        SELECT 
            d.id,
            d.codigo_docente,
            p.documento_identidad,
            p.nombres || ' ' || p.apellidos as nombre_completo,
            d.abreviatura_titulo,
            d.especialidad,
            d.tipo_contrato,
            d.dedicacion,
            d.estado,
            p.correo_electronico,
            p.telefono
        FROM docentes d
        JOIN informacion_personal p ON d.persona_id = p.id
        WHERE p.estado = 'activo';
        '''
        
        # Vista de secciones con información detallada
        vista_secciones = '''
        CREATE VIEW IF NOT EXISTS vista_secciones_detalle AS
        SELECT 
            sec.id,
            sec.codigo_seccion,
            uc.codigo as codigo_uc,
            uc.nombre as unidad_curricular,
            uc.unidades_credito,
            pnf.nombre as pnf_nombre,
            s.nombre as sede_nombre,
            pa.nombre as periodo_nombre,
            COALESCE(p.nombres || ' ' || p.apellidos, 'Sin Asignar') as docente_titular,
            sec.cupo_maximo,
            sec.inscritos,
            sec.turno,
            sec.estado
        FROM secciones sec
        JOIN unidades_curriculares uc ON sec.unidad_curricular_id = uc.id
        JOIN pnf ON uc.pnf_id = pnf.id
        JOIN sedes s ON sec.sede_id = s.id
        JOIN periodos_academicos pa ON sec.periodo_academico_id = pa.id
        LEFT JOIN docentes d ON sec.docente_titular_id = d.id
        LEFT JOIN informacion_personal p ON d.persona_id = p.id;
        '''
        
        vistas = [vista_estudiantes, vista_docentes, vista_secciones]
        
        for vista in vistas:
            try:
                self.ejecutar_consulta(vista)
            except Exception as e:
                print(f"Error creando vista: {e}")

    def crear_base_datos(self):
        """Método principal que orquesta la creación de toda la base de datos"""
        
        # Verificar si el directorio 'db' existe, si no, crearlo
        if not os.path.exists('db'):
            os.makedirs('db')

        print("="*60)
        print("SISTEMA ACADÉMICO - UNIVERSIDAD POLITÉCNICA TERRITORIAL")
        print('"José Félix Ribas" del estado Barinas')
        print("="*60)
        print(f"Creando base de datos en: {os.path.join('db', 'sistema_academico.db')}")
        print(f"Fecha y hora: {datetime.datetime.now()}")
        print("-"*60)

        try:
            print("Creando tablas base...")
            self.crear_tablas_base()
            
            print("Creando sistema de usuarios y roles...")
            self.crear_tablas_usuarios_roles()
            
            print("Creando tablas de catálogos...")
            self.crear_tablas_catalogo()
            
            print("Creando tablas académicas...")
            self.crear_tablas_academicas()
            
            print("Creando tablas operativas...")
            self.crear_tablas_operativas()
            
            print("Creando tablas de auditoría...")
            self.crear_tablas_auditoria()
            
            print("Insertando datos iniciales...")
            self.insertar_datos_iniciales()
            
            print("Creando usuario administrador...")
            self.crear_usuario_admin_inicial()
            
            print("Creando triggers de auditoría...")
            self.crear_triggers_auditoria()
            
            print("Creando índices de optimización...")
            self.crear_indices_optimizacion()
            
            print("Creando vistas de consulta...")
            self.crear_vistas_consultas()
            
            print("-"*60)
            self.verificar_tablas()
            
            print("="*60)
            print("BASE DE DATOS CREADA EXITOSAMENTE")
            print("="*60)
            
        except Exception as e:
            print(f"ERROR CRÍTICO: {e}")
            raise

    def verificar_tablas(self):
        """Verifica y muestra información sobre las tablas creadas"""
        db_ruta = os.path.join('db', 'sistema_academico.db')
        con = sql.connect(db_ruta)
        cursor = con.cursor()
        
        # Obtener todas las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tablas = cursor.fetchall()
        
        # Obtener todas las vistas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='view' ORDER BY name;")
        vistas = cursor.fetchall()
        
        # Obtener todos los índices
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%' ORDER BY name;")
        indices = cursor.fetchall()
        
        # Obtener todos los triggers
        cursor.execute("SELECT name FROM sqlite_master WHERE type='trigger' ORDER BY name;")
        triggers = cursor.fetchall()
        
        con.close()

        print(f"\n📊 RESUMEN DE LA BASE DE DATOS:")
        print(f"📋 Tablas creadas: {len(tablas)}")
        for tabla in tablas:
            print(f"   • {tabla[0]}")
            
        print(f"\n👁 Vistas creadas: {len(vistas)}")
        for vista in vistas:
            print(f"   • {vista[0]}")
            
        print(f"\n⚡ Índices creados: {len(indices)}")
        for indice in indices:
            print(f"   • {indice[0]}")
            
        print(f"\n🔄 Triggers creados: {len(triggers)}")
        for trigger in triggers:
            print(f"   • {trigger[0]}")

    def obtener_estadisticas_bd(self):
        """Obtiene estadísticas básicas de la base de datos"""
        db_ruta = os.path.join('db', 'sistema_academico.db')
        con = sql.connect(db_ruta)
        cursor = con.cursor()
        
        estadisticas = {}
        
        tablas_principales = [
            'informacion_personal', 'usuarios', 'estudiantes', 'docentes',
            'sedes', 'pnf', 'unidades_curriculares', 'secciones', 'inscripciones'
        ]
        
        for tabla in tablas_principales:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
                count = cursor.fetchone()[0]
                estadisticas[tabla] = count
            except:
                estadisticas[tabla] = 0
        
        con.close()
        return estadisticas

if __name__ == "__main__":
    try:
        sistema_academico = SistemaAcademicoDB()
        
        # Mostrar estadísticas finales
        print("\n📈 ESTADÍSTICAS INICIALES:")
        stats = sistema_academico.obtener_estadisticas_bd()
        for tabla, count in stats.items():
            print(f"   {tabla}: {count} registros")
            
    except Exception as e:
        print(f"❌ Error durante la creación del sistema: {e}")
        raise