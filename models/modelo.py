#importamos la libreria para la base de datos
import sqlite3 as sql

# declaramos mi clase para mi modelo principal
class Modelo():
    
    def __init__(self):
        
        self.crear_tablas()
    
    def ejecutar_consulta(self, instruccion):
        # Conexion a la base de datos, si no encuentra el archivo lo crea
        con = sql.connect('base_de_datos.db', isolation_level=None )
        cursor = con.cursor()
        # Ejecutamos la consulta
        cursor.execute(instruccion)
        # Guardamos los cambios 
        con.commit()
        # cerramos la conexión
        con.close()

    def crear_tabla_preguntas(self):
        instruccion = '''CREATE TABLE IF NOT EXISTS "preguntas" (
                            "id_pregunta"	INTEGER,
                            "pregunta_1"	TEXT,
                            "pregunta_2"	TEXT,
                            "pregunta_3"	TEXT,
                            PRIMARY KEY("id_pregunta" AUTOINCREMENT)
                        );'''
        self.ejecutar_consulta(instruccion)
    
    def crear_tabla_usuario(self):
        instruccion = '''CREATE TABLE IF NOT EXISTS "usuario" (
                            "id_usuario"	INTEGER,
                            "usuario"	TEXT UNIQUE,
                            "cedula" INTEGER,
                            "contraseña"	BLOB,
                            "id_pregunta"	INTEGER,                            
                            PRIMARY KEY("id_usuario" AUTOINCREMENT),
                            FOREIGN KEY("id_pregunta") REFERENCES "preguntas"("id_pregunta")
                        );'''
        self.ejecutar_consulta(instruccion)
    
    def crear_tabla_historial(self):
        instruccion = '''CREATE TABLE IF NOT EXISTS "historial" (
                            "id_historial" INTEGER,
                            "funcion" TEXT,
                            "posicion" TEXT,
                            "palabra" TEXT,
                            "fecha" TEXT,
                            "hora" TEXT,
                            "id_usuario"	INTEGER,
                            PRIMARY KEY("id_historial" AUTOINCREMENT),
                            FOREIGN KEY("id_usuario") REFERENCES "usuario"("id_usuario")
                        );'''
        self.ejecutar_consulta(instruccion)
    
    def crear_tabla_imagen(self):
        instruccion = '''CREATE TABLE IF NOT EXISTS "imagen" (
                            "id_imagen"	INTEGER,
                            "destino"	TEXT,
                            "id_usuario" INTEGER,                           
                            PRIMARY KEY("id_imagen" AUTOINCREMENT)
                            FOREIGN KEY("id_usuario") REFERENCES "usuario"("id_usuario")
                        );'''
        self.ejecutar_consulta(instruccion)
    
    def crear_tablas(self):
        self.crear_tabla_preguntas()
        self.crear_tabla_usuario()
        self.crear_tabla_historial()
        self.crear_tabla_imagen()
