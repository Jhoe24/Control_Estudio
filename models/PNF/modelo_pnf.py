import sqlite3 as sql
import os
from pprint import pprint

class ModeloPNF:
    def __init__(self):
       self.db_ruta = os.path.join('db', 'sistema_academico.db')

    def registrar_pnf(self, datos_pnf,fecha_creacion):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            
            cursor.execute(
                """
                INSERT INTO pnf 
                (codigo, codigo_nacional, nombre, nombre_corto, nivel,area_conocimiento, duracion_trayectos,
                duracion_semanas, total_creditos,total_horas, titulo_otorga, perfil_egreso, resolucion_creacion,
                fecha_resolucion, version_pensum, coordinador_nacional, fecha_creacion,fecha_actualizacion, estado) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    datos_pnf["codigo"],
                    datos_pnf["codigo_nacional"],
                    datos_pnf["nombre_pnf"],
                    datos_pnf["siglas"],
                    datos_pnf["tipo_pnf"],
                    datos_pnf["area_conocimiento"],
                    datos_pnf["cantidad_trayectos"],
                    datos_pnf["duracion_semana"],
                    datos_pnf["duracion_creditos"],
                    datos_pnf["duracion_horas"],
                    datos_pnf["titulo_otorga"],
                    datos_pnf["perfil_egreso"],
                    datos_pnf["resolucion"],
                    datos_pnf["fecha_resolucion"],
                    datos_pnf["version_pensum"],
                    datos_pnf["coordinador_nacional"],
                    fecha_creacion,
                    fecha_creacion,
                    datos_pnf["estado"]
                )
            )

            id_pnf = cursor.lastrowid
            con.commit()
            return id_pnf   

        except Exception as e:
            print(f"Error al registrar los datos del pnf: {e}") 
            return False
        finally:
            if con is not None:
                con.close()
    
    def registrar_trayecto(self,datos_trayecto,id_pnf):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            
            cursor.execute(
                """
                INSERT INTO trayectos 
                (pnf_id, numero, nombre, tipo, duracion_semanas, duracion_horas, creditos_minimos,
                creditos_maximos, numero_tramos, objetivos, perfil_egreso, obligatorio, secuencial, estado) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    id_pnf,
                    datos_trayecto["numero"],
                    datos_trayecto["nombre"],
                    "Inicial",
                    datos_trayecto["duracion_semanas"],
                    datos_trayecto["duracion_horas"],
                    datos_trayecto["creditos_minimos"],
                    datos_trayecto["creditos_maximos"],
                    datos_trayecto["numero_tramos"],
                    datos_trayecto["objetivos"],
                    datos_trayecto["perfil_egreso"],
                    datos_trayecto["obligatorio"],
                    datos_trayecto["secuencial"],
                    datos_trayecto["estado"]
                )
            )

            id_trayecto = cursor.lastrowid
            con.commit()
            return id_trayecto   

        except Exception as e:
            print(f"Error al registrar los datos del trayecto {datos_trayecto["tipo"]}: {e}") 
            return False
        finally:
            if con is not None:
                con.close()
    
    def registrar_tramos(self,datos_tramo,id_tramo):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            
            cursor.execute(
                """
                INSERT INTO tramos 
                (trayecto_id, numero, nombre, duracion_semanas, duracion_horas, creditos,
                objetivos, estado) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    id_tramo,
                    datos_tramo["numero"],
                    datos_tramo["nombre"],
                    datos_tramo["duracion_semanas"],
                    datos_tramo["duracion_horas"],
                    datos_tramo["creditos"],
                    datos_tramo["objetivos"],
                    datos_tramo["estado"]
                )
            )

           #id_trayecto = cursor.lastrowid
            con.commit()
            return True   

        except Exception as e:
            print(f"Error al registrar los datos del tramo {datos_tramo["nombre"]}: {e}") 
            return False
        finally:
            if con is not None:
                con.close()

    def obtner_lista_pnf(self):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            
            cursor.execute(
                """
                SELECT id, codigo, nombre FROM pnf
                """
            )

            return cursor.fetchall()   

        except Exception as e:
            print(f"Error al obtener la lista: {e}") 
            return False
        finally:
            if con is not None:
                con.close()

    def obtener_pnf(self,id):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            con.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
            cursor = con.cursor()
            cursor.execute(
                """
                SELECT * FROM pnf WHERE id = ?
                """, (id,)
            )
            return cursor.fetchone()   # Un solo diccionario o None
        except Exception as e:
            print(f"Error al obtener la lista: {e}") 
            return False
        finally:
            if con is not None:
                con.close()

    def obtener_trayecto(self, id):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            con.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
            cursor = con.cursor()
            cursor.execute(
                """
                SELECT * FROM trayectos WHERE pnf_id = ?
                """, (id,)
            )
            return cursor.fetchall()   # Lista de diccionarios
        except Exception as e:
            print(f"Error al obtener el trayecto: {e}") 
            return False
        finally:
            if con is not None:
                con.close()

    def obtener_tramo(self, id):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            con.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
            cursor = con.cursor()
            cursor.execute(
                """
                SELECT * FROM tramos WHERE trayecto_id = ?
                """, (id,)
            )
            return cursor.fetchall()  # Ahora retorna una lista de diccionarios
        except Exception as e:
            print(f"Error al obtener tramo: {e}") 
            return False
        finally:
            if con is not None:
                con.close()

    def update_pnf(self, datos_pnf, id):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute(
                """
                UPDATE pnf SET
                    codigo = ?,
                    codigo_nacional = ?,
                    nombre = ?,
                    nombre_corto = ?,
                    nivel = ?,
                    area_conocimiento = ?,
                    duracion_trayectos = ?,
                    duracion_semanas = ?,
                    total_creditos = ?,
                    total_horas = ?,
                    titulo_otorga = ?,
                    perfil_egreso = ?,
                    resolucion_creacion = ?,
                    fecha_resolucion = ?,
                    version_pensum = ?,
                    coordinador_nacional = ?,
                    estado = ?
                WHERE id = ?
                """,
                (
                    datos_pnf["codigo"],
                    datos_pnf["codigo_nacional"],
                    datos_pnf["nombre_pnf"],
                    datos_pnf["siglas"],
                    datos_pnf["tipo_pnf"],
                    datos_pnf["area_conocimiento"],
                    datos_pnf["cantidad_trayectos"],
                    datos_pnf["duracion_semana"],
                    datos_pnf["duracion_creditos"],
                    datos_pnf["duracion_horas"],
                    datos_pnf["titulo_otorga"],
                    datos_pnf["perfil_egreso"],
                    datos_pnf["resolucion"],
                    datos_pnf["fecha_resolucion"],
                    datos_pnf["version_pensum"],
                    datos_pnf["coordinador_nacional"],
                    datos_pnf["estado"],
                    id
                )
            )
            con.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar el PNF: {e}")
            return False
        finally:
            if con is not None:
                con.close()

    def update_trayecto(self, datos_trayecto, id):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute(
                """
                UPDATE trayectos SET
                    numero = ?,
                    nombre = ?,
                    tipo = ?,
                    duracion_semanas = ?,
                    duracion_horas = ?,
                    creditos_minimos = ?,
                    creditos_maximos = ?,
                    numero_tramos = ?,
                    objetivos = ?,
                    perfil_egreso = ?,
                    obligatorio = ?,
                    secuencial = ?,
                    estado = ?
                WHERE id = ?
                """,
                (
                    datos_trayecto["numero"],
                    datos_trayecto["nombre"],
                    "Inicial",  # Si siempre es "Inicial" como en el registro
                    datos_trayecto["duracion_semanas"],
                    datos_trayecto["duracion_horas"],
                    datos_trayecto["creditos_minimos"],
                    datos_trayecto["creditos_maximos"],
                    datos_trayecto["numero_tramos"],
                    datos_trayecto["objetivos"],
                    datos_trayecto["perfil_egreso"],
                    datos_trayecto["obligatorio"],
                    datos_trayecto["secuencial"],
                    datos_trayecto["estado"],
                    id
                )
            )
            con.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar el trayecto: {e}")
            return False
        finally:
            if con is not None:
                con.close()

    def update_tramo(self, datos_tramo, id):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute(
                """
                UPDATE tramos SET
                    numero = ?,
                    nombre = ?,
                    duracion_semanas = ?,
                    duracion_horas = ?,
                    creditos = ?,
                    objetivos = ?,
                    estado = ?
                WHERE id = ?
                """,
                (
                    datos_tramo["numero"],
                    datos_tramo["nombre"],
                    datos_tramo["duracion_semanas"],
                    datos_tramo["duracion_horas"],
                    datos_tramo["creditos"],
                    datos_tramo["objetivos"],
                    datos_tramo["estado"],
                    id
                )
            )
            con.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar el tramo: {e}")
            return False
        finally:
            if con is not None:
                con.close()