import sqlite3 as sql
import os
from pprint import pprint

class ModeloSedes:
    def __init__(self):
       self.db_ruta = os.path.join('db', 'sistema_academico.db')
    
    def registrar_sede(self,datos_sede,fecha_actual):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()

            cursor.execute("""
                            INSERT INTO sedes (codigo, nombre, nombre_corto, tipo, direccion,
                           telefono, correo, director, coordinador_academico, fecha_creacion, 
                           fecha_actualizacion, estado, observaciob)
                           VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?) 
                           """,
                            (
                            datos_sede["codigo"],
                            datos_sede["nombre"],
                            datos_sede["nombre_corto"],
                            datos_sede["tipo"],
                            datos_sede["direccion"],
                            datos_sede["telefono"],
                            datos_sede["correo"],
                            datos_sede["director"],
                            datos_sede["coordinador_academico"],
                            fecha_actual,
                            fecha_actual,
                            datos_sede["estado"],
                            datos_sede["observaciones"]
                            )
                           )
            con.commit()
            con.close()
            return True
        except Exception as e:
            print(f"Error al registrar la sede: {e}") 
            return False
        finally:
            if con is not None:
                con.close()

    def listar_sedes(self):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            con.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
            cursor = con.cursor()
            cursor.execute("SELECT * FROM sedes")
            sedes = cursor.fetchall()
            return sedes
        except Exception as e:
            print(f"Error al listar las sedes: {e}")
            return []
        finally:
            if con is not None:
                con.close()

    def actualizar_sede(self, sede_id, datos_actualizados,fecha_actualizacion):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute("""
                            UPDATE sedes
                            SET codigo = ?, nombre = ?, nombre_corto = ?, tipo = ?, direccion = ?,
                                telefono = ?, correo = ?, director = ?, coordinador_academico = ?,
                                fecha_actualizacion = ?, estado = ?, observaciones = ?
                            WHERE id = ?
                            """,(
                            datos_actualizados["codigo"],
                            datos_actualizados["nombre"],
                            datos_actualizados["nombre_corto"],
                            datos_actualizados["tipo"],
                            datos_actualizados["direccion"],
                            datos_actualizados["telefono"],
                            datos_actualizados["correo"],
                            datos_actualizados["director"],
                            datos_actualizados["coordinador_academico"],
                            fecha_actualizacion,
                            datos_actualizados["estado"],
                            datos_actualizados["observaciones"],
                            sede_id
                            ))
            
            con.commit()
            con.close()
            return True
           
        except Exception as e:
            print(f"Error al actualizar datos de la sede: {e}")
            return False
        finally:
            if con is not None:
                con.close()


    def obtener_codigos(self):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute('SELECT codigo FROM sedes')
            return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error al obtener los códigos: {e}")
            return []
    
    def obtener_id_por_codigo(self, codigo):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute('SELECT id FROM sedes WHERE codigo=?', (codigo,))
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error al obtener el ID por código: {e}")
            return None
        finally:
            if con is not None:
                con.close()

    def obtener_nombres_por_id(self, tabla, id):
            con = None
            try:
                con = sql.connect(self.db_ruta)
                cursor = con.cursor()
                cursor.execute(
                    f"""
                    SELECT nombre FROM {tabla} WHERE id = ?
                    """, (id,)
                )
                return cursor.fetchone()
            except Exception as e:
                print(f"Error al obtener el nombre por ID: {e}")
                return None
            finally:
                if con is not None:
                    con.close()

    def obtener_codigo_por_id(self, id):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute('SELECT codigo FROM sedes WHERE id=?', (id,))
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error al obtener el código por id: {e}")
            return None
        finally:
            if con is not None:
                con.close()

# bd = ModeloSedes()
# print(bd.obtener_codigo_por_id(1))

