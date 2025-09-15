import sqlite3 as sql
import os
from pprint import pprint
from datetime import datetime

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
    
    def actualizar_seccion(self, seccion_id, datos_actualizados,fecha_cambio_estado):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute("""
                UPDATE secciones
                SET 
                    codigo_seccion = ?, 
                    docente_titular_id = ?, 
                    cupo_maximo = ?, 
                    turno = ?, 
                    modalidad = ?, 
                    aula = ?, 
                    estado = ?, 
                    sede_id = ?, 
                    periodo_academico_id = ?, 
                    pnf_id = ?, 
                    trayecto_id = ?, 
                    tramo_id = ?, 
                    fecha_cambio_estado = ?
                WHERE id = ?
            """, (
                datos_actualizados["codigo_seccion"],
                datos_actualizados["docente_titular_id"],
                datos_actualizados["cupo_maximo"],
                datos_actualizados["turno"],
                datos_actualizados["modalidad"],
                datos_actualizados["aula"],
                datos_actualizados["estado"],
                datos_actualizados["sede_id"],
                datos_actualizados["periodo_academico_id"],
                datos_actualizados["pnf_id"],
                datos_actualizados["trayecto_id"],
                datos_actualizados["tramo_id"],
                fecha_cambio_estado,
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
                    
    def ejecutar_consulta_armada(self, sentencia, params=None,es_select=False):
            con = None
            try:
                con = sql.connect(self.db_ruta)
                con.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
                cursor = con.cursor()
                if params:
                    cursor.execute(sentencia, params)
                    con.commit()# si la sentencias es un insert o un update hacer modificacion en la base de datos
                    if es_select:
                        return cursor.fetchone()
                    else:
                        return True 
                else:
                    cursor.execute(sentencia)#si la sentencia es un select retornar resultado
                    return cursor.fetchone()
            except Exception as e:
                print(f"Error al ejecutar la consulta: {e}")
                return False
            finally:
                if con is not None:
                    con.close()

#===============================================================

    def actualizar_estado(self, seccion_id, nuevo_estado):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute("UPDATE secciones SET estado = ? WHERE id = ?", (nuevo_estado, seccion_id))
            con.commit()
            print("actualizacion exitosa")
            return True
        except Exception as e:
            print(f"Error al actualizar el estado de la sección: {e}")
            return False
        finally:
            if con is not None:
                con.close()
    
    def obtener_id_por_nombre(self, nombre_pnf):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute("SELECT id FROM pnf WHERE nombre = ?", (nombre_pnf,))
            row = cursor.fetchone()
            return row[0] if row else None
        except Exception as e:
            print(f"Error al obtener id por nombre: {e}")
            return None
        finally:
            if con is not None:
                con.close()

#print(ModeloSecciones().actualizar_estado(2, 'Abierta'))