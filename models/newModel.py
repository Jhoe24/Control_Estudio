import sqlite3

conn = sqlite3.connect('Control_Academico.db')
cursor = conn.cursor()


# Tabla SEDES
cursor.execute('''
CREATE TABLE IF NOT EXISTS sedes (
    id_sede INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    ubicacion TEXT NOT NULL,
    fecha_creacion DATE NOT NULL,
    estado TEXT NOT NULL
)
''')

# Tabla ROLES
cursor.execute('''
CREATE TABLE IF NOT EXISTS roles (
    id_rol INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    permisos TEXT,
    fecha_creacion DATE NOT NULL
)
''')

# Tabla PROGRAMAS
cursor.execute('''
CREATE TABLE IF NOT EXISTS programas (
    id_programa INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL,
    nombre TEXT NOT NULL,
    nivel TEXT,
    duracion TEXT,
    modalidad TEXT,
    tipo_periodo TEXT,
    id_sede INTEGER,
    fecha_creacion DATE NOT NULL,
    estado TEXT NOT NULL,
    FOREIGN KEY (id_sede) REFERENCES sedes(id_sede)
)
''')

# Tabla DIRECCIONES
cursor.execute('''
CREATE TABLE IF NOT EXISTS direcciones (
    id_direccion INTEGER PRIMARY KEY AUTOINCREMENT,
    estado TEXT NOT NULL,
    municipio TEXT NOT NULL,
    parroquia TEXT,
    sector TEXT,
    calle TEXT,
    casa_apto TEXT,
    detalles TEXT,
    codigo_postal TEXT,
    tipo_direccion TEXT,
    principal BOOLEAN,
    referencia_ubicacion TEXT,
    coordenadas TEXT,
    fecha_registro DATE NOT NULL,
    fecha_actualizacion DATE
)
''')

# Tabla TELEFONOS
cursor.execute('''
CREATE TABLE IF NOT EXISTS telefonos (
    id_telefono INTEGER PRIMARY KEY AUTOINCREMENT,
    numero TEXT NOT NULL,
    codigo_pais TEXT,
    codigo_area TEXT,
    tipo TEXT NOT NULL,
    operadora TEXT,
    principal BOOLEAN,
    id_estudiante INTEGER,
    id_docente INTEGER,
    estado TEXT NOT NULL,
    fecha_registro DATE NOT NULL,
    fecha_actualizacion DATE,
    FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante),
    FOREIGN KEY (id_docente) REFERENCES docentes(id_docente)
)
''')

# Tabla ESTUDIANTES
cursor.execute('''
CREATE TABLE IF NOT EXISTS estudiantes (
    id_estudiante INTEGER PRIMARY KEY AUTOINCREMENT,
    cedula TEXT NOT NULL,
    pasaporte TEXT,
    nombres TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    lugar_nacimiento TEXT,
    sexo TEXT,
    estado_civil TEXT,
    nacionalidad TEXT,
    correo TEXT,
    id_direccion INTEGER,
    fecha_ingreso DATE NOT NULL,
    condicion TEXT,
    situacion TEXT,
    foto_url TEXT,
    codigo_sni TEXT,
    fecha_registro DATE NOT NULL,
    fecha_actualizacion DATE,
    FOREIGN KEY (id_direccion) REFERENCES direcciones(id_direccion)
)
''')

# Tabla INFORMACION_ACADEMICA_PRECEDENTE
cursor.execute('''
CREATE TABLE IF NOT EXISTS informacion_academica_precedente (
    id_info_academica INTEGER PRIMARY KEY AUTOINCREMENT,
    id_estudiante INTEGER NOT NULL,
    institucion_procedencia TEXT NOT NULL,
    tipo_institucion TEXT,
    ubicacion_institucion TEXT,
    titulo_previo TEXT,
    mencion_bachillerato TEXT,
    fecha_graduacion_previa DATE,
    promedio_bachillerato REAL,
    codigo_sni TEXT,
    indice_academico_ingreso REAL,
    proceso_ingreso TEXT,
    documentos_consignados TEXT,
    fecha_registro DATE NOT NULL,
    fecha_actualizacion DATE,
    FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante)
)
''')

# Tabla DOCENTES
cursor.execute('''
CREATE TABLE IF NOT EXISTS docentes (
    id_docente INTEGER PRIMARY KEY AUTOINCREMENT,
    cedula TEXT NOT NULL,
    pasaporte TEXT,
    nombres TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    titulo_academico TEXT,
    especialidad TEXT,
    fecha_nacimiento DATE NOT NULL,
    sexo TEXT,
    correo TEXT,
    id_direccion INTEGER,
    fecha_ingreso DATE NOT NULL,
    dedicacion TEXT,
    categoria TEXT,
    estado TEXT NOT NULL,
    foto_url TEXT,
    fecha_registro DATE NOT NULL,
    fecha_actualizacion DATE,
    FOREIGN KEY (id_direccion) REFERENCES direcciones(id_direccion)
)
''')

# Tabla PERIODOS_ACADEMICOS
cursor.execute('''
CREATE TABLE IF NOT EXISTS periodos_academicos (
    id_periodo INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL,
    nombre TEXT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    tipo TEXT NOT NULL,
    id_programa INTEGER,
    estado TEXT NOT NULL,
    fecha_creacion DATE NOT NULL,
    FOREIGN KEY (id_programa) REFERENCES programas(id_programa)
)
''')

# Tabla MATERIAS
cursor.execute('''
CREATE TABLE IF NOT EXISTS materias (
    id_materia INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    creditos INTEGER,
    horas_teoricas INTEGER,
    horas_practicas INTEGER,
    requisitos TEXT,
    id_programa INTEGER,
    trayecto TEXT,
    tramo TEXT,
    tipo TEXT,
    estado TEXT NOT NULL,
    fecha_creacion DATE NOT NULL,
    FOREIGN KEY (id_programa) REFERENCES programas(id_programa)
)
''')

# Tabla SECCIONES
cursor.execute('''
CREATE TABLE IF NOT EXISTS secciones (
    id_seccion INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL,
    id_materia INTEGER NOT NULL,
    id_periodo INTEGER NOT NULL,
    id_docente INTEGER,
    cupo_maximo INTEGER,
    inscritos INTEGER,
    turno TEXT,
    aula TEXT,
    horario TEXT,
    fecha_inicio DATE,
    fecha_fin DATE,
    estado TEXT NOT NULL,
    fecha_creacion DATE NOT NULL,
    FOREIGN KEY (id_materia) REFERENCES materias(id_materia),
    FOREIGN KEY (id_periodo) REFERENCES periodos_academicos(id_periodo),
    FOREIGN KEY (id_docente) REFERENCES docentes(id_docente)
)
''')

# Tabla INSCRIPCIONES
cursor.execute('''
CREATE TABLE IF NOT EXISTS inscripciones (
    id_inscripcion INTEGER PRIMARY KEY AUTOINCREMENT,
    id_estudiante INTEGER NOT NULL,
    id_seccion INTEGER NOT NULL,
    fecha_inscripcion DATE NOT NULL,
    tipo_inscripcion TEXT,
    nota_final REAL,
    porcentaje_asistencia REAL,
    observaciones TEXT,
    estado TEXT NOT NULL,
    fecha_actualizacion DATE,
    FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante),
    FOREIGN KEY (id_seccion) REFERENCES secciones(id_seccion)
)
''')

# Tabla NOTAS_PARCIALES
cursor.execute('''
CREATE TABLE IF NOT EXISTS notas_parciales (
    id_nota_parcial INTEGER PRIMARY KEY AUTOINCREMENT,
    id_inscripcion INTEGER NOT NULL,
    descripcion TEXT NOT NULL,
    ponderacion REAL,
    nota REAL,
    fecha_evaluacion DATE,
    observaciones TEXT,
    fecha_registro DATE NOT NULL,
    FOREIGN KEY (id_inscripcion) REFERENCES inscripciones(id_inscripcion)
)
''')

# Tabla ASISTENCIAS
cursor.execute('''
CREATE TABLE IF NOT EXISTS asistencias (
    id_asistencia INTEGER PRIMARY KEY AUTOINCREMENT,
    id_inscripcion INTEGER NOT NULL,
    fecha DATE NOT NULL,
    estado TEXT NOT NULL,
    observaciones TEXT,
    fecha_registro DATE NOT NULL,
    FOREIGN KEY (id_inscripcion) REFERENCES inscripciones(id_inscripcion)
)
''')

# Tabla HISTORICO_ACADEMICO
cursor.execute('''
CREATE TABLE IF NOT EXISTS historico_academico (
    id_historico INTEGER PRIMARY KEY AUTOINCREMENT,
    id_estudiante INTEGER NOT NULL,
    id_programa INTEGER NOT NULL,
    promedio_general REAL,
    creditos_aprobados INTEGER,
    creditos_cursados INTEGER,
    fecha_ultimo_periodo DATE,
    estado TEXT NOT NULL,
    fecha_actualizacion DATE,
    FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante),
    FOREIGN KEY (id_programa) REFERENCES programas(id_programa)
)
''')

# Tabla USUARIOS
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_usuario TEXT NOT NULL UNIQUE,
    contrasena_hash TEXT NOT NULL,
    id_estudiante INTEGER,
    id_docente INTEGER,
    id_administrativo INTEGER,
    FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante),
    FOREIGN KEY (id_docente) REFERENCES docentes(id_docente)
)
''')

# Tabla USUARIO_ROLES
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuario_roles (
    id_usuario INTEGER NOT NULL,
    id_rol INTEGER NOT NULL,
    fecha_asignacion DATE NOT NULL,
    asignado_por INTEGER,
    activo BOOLEAN,
    PRIMARY KEY (id_usuario, id_rol),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_rol) REFERENCES roles(id_rol)
)
''')

conn.commit()
conn.close()

print("Base de datos creada exitosamente.")
