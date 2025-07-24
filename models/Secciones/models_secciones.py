import sqlite3 as sql
import os
from pprint import pprint

class ModeloSecciones:
    def __init__(self):
       self.db_ruta = os.path.join('db', 'sistema_academico.db')
    
    def registrar_sede(self,datos_secciones):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()

            cursor.execute("""
                            INSERT INTO secciones (sede_id, periodo_academico_id, pnf_id, 
                            trayecto_id, tramo_id, codigo_seccion, docente_titular_id, 
                            cupo_maximo, turno, modalidad, aula, estado)
                            VALUES(?,?,?,?,?,?,?,?,?,?,?,?) 
                           """,
                            (
                            datos_secciones["sede_id"],
                            datos_secciones["periodo_academico_id"],
                            datos_secciones["pnf_id"],
                            datos_secciones["trayecto_id"],
                            datos_secciones["tramo_id"],
                            datos_secciones["codigo_seccion"],
                            datos_secciones["docente_titular_id"],
                            datos_secciones["cupo_maximo"],
                            datos_secciones["turno"],
                            datos_secciones["modalidad"],
                            datos_secciones["aula"],
                            datos_secciones["estado"],
                            )
                           )
            con.commit()
            con.close()
            return True
        except Exception as e:
            print(f"Error al registrar la seccion: {e}") 
            return False
        finally:
            if con is not None:
                con.close()

    def listar_secciones(self,pnf_id):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            con.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
            cursor = con.cursor()
            cursor.execute("SELECT * FROM secciones WHERE pnf_id = ? ORDER BY codigo_seccion ASC", (pnf_id,))
            secciones = cursor.fetchall()
            return secciones
        except Exception as e:
            print(f"Error al listar las secciones: {e}")
            return []
        finally:
            if con is not None:
                con.close()
    
    def actualizar_seccion(self, seccion_id, datos_actualizados,fecha_actualizacion):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute("""
                UPDATE secciones
                SET 
                    codigo = ?, 
                    docente_nombre = ?, 
                    cupo_maximo = ?, 
                    turno = ?, 
                    modalidad = ?, 
                    aula = ?, 
                    estado = ?, 
                    sede = ?, 
                    periodo_academico = ?, 
                    pnf = ?, 
                    trayecto = ?, 
                    tramo = ?, 
                    fecha_actualizacion = ?
                WHERE id = ?
            """, (
                datos_actualizados["codigo"],
                datos_actualizados["docente_nombre"],
                datos_actualizados["cupo_maximo"],
                datos_actualizados["turno"],
                datos_actualizados["modalidad"],
                datos_actualizados["aula"],
                datos_actualizados["estado"],
                datos_actualizados["sede"],
                datos_actualizados["periodo_academico"],
                datos_actualizados["pnf"],
                datos_actualizados["trayecto"],
                datos_actualizados["tramo"],
                fecha_actualizacion,
                seccion_id
            ))

            con.commit()
            return True

        except Exception as e:
            print(f"Error al actualizar datos de la sección: {e}")
            return False

        finally:
            if con is not None:
                con.close()
