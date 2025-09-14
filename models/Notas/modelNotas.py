import sqlite3 as sql
import os
from datetime import date
from pprint import pprint

class ModeloNotas:
    def __init__(self):
       self.db_ruta = os.path.join('db', 'sistema_academico.db')

    def is_assigned_pnf(self, estudiante_id):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute('''
                            SELECT pnf_id, trayecto_actual FROM estudiante_pnf WHERE estudiante_id = ?
                            ''',(estudiante_id,))
            resultado = cursor.fetchone()
            con.close()
            if resultado:
                return resultado
            else:
                return False
        except Exception as e:
            print(f"Error al realizar la consulta: {e}") 
            return False
        finally:
            if con is not None:
                con.close()
        
    def bring_project(self, estudiante_id, pnf_id, trayecto_actual_id):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            """
            1. Obtener todas la Unidades Curriculares de tipo Proyecto del PNF y Trayecto actual
            2. Verificar si el estudiante tiene notas en la tabla notas correcpondiente a esa unidad curricular

            """
            cursor.execute('''
                            SELECT id, nombre FROM unidades_curriculares 
                            WHERE pnf_id = ? AND trayecto_id = ? AND tipo = 'Proyecto'
                            ''',(pnf_id, trayecto_actual_id))

            resultado = cursor.fetchall()
            
            # Usar una list comprehension es más eficiente y conciso.
            lisDicProyectos = [{"id": proyecto[0], "nombre": proyecto[1]} for proyecto in resultado]
            
            """ Ahora necesitamos obtner el id inscripcion del estudiante """
            cursor.execute('''
                            SELECT id FROM inscripciones WHERE estudiante_id = ?
                            ''',(estudiante_id,))
            resultado = cursor.fetchone()
            if resultado:
                inscripcion_id = resultado[0]
                for dicProyecto in lisDicProyectos:
                    cursor.execute('''
                                    SELECT valor FROM notas 
                                    WHERE inscripcion_id = ? AND unidad_curricular_id = ?
                                    ''',(inscripcion_id, dicProyecto["id"]))
                    resultado = cursor.fetchone()
                    if resultado:
                        dicProyecto["nota"] = resultado[0]
                    else:
                        dicProyecto["nota"] = None

            return lisDicProyectos                    

        except Exception as e:
            print(f"Error al realizar la consulta: {e}") 
            return False
        finally:
            if con is not None:
                con.close()

    def esTrayectoInicial(self, trayecto_id):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute('''
                            SELECT tipo FROM trayectos WHERE id = ?
                            ''',(trayecto_id,))
            resultado = cursor.fetchone()
            con.close()
            if resultado and resultado[0] == "Inicial":
                return True
            else:
                return False
        except Exception as e:
            print(f"Error al realizar la consulta: {e}") 
            return False
        finally:
            if con is not None:
                con.close()

    def estudiantes_por_uc(self, unidad_curricular_id, periodo_academico_id):
        """
        Obtiene una lista de diccionarios con la información de los estudiantes
        inscritos en una unidad curricular y período académico específicos.
        """
        con = None
        try:
            con = sql.connect(self.db_ruta)
            # Configurar para que devuelva diccionarios
            con.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
            cursor = con.cursor()

            # Consulta unificada para obtener los datos de los estudiantes directamente
            cursor.execute('''
                SELECT
                    e.id AS estudiante_id,
                    e.persona_id,
                    ip.documento_identidad,
                    ip.nombres,
                    ip.apellidos,
                    i.id AS inscripcion_id,
                    s.id AS seccion_id,
                    s.codigo_seccion AS nombre_seccion
                FROM
                    unidades_curriculares uc
                JOIN
                    secciones s ON uc.trayecto_id = s.trayecto_id
                                AND uc.tramo_id = s.tramo_id
                                AND uc.pnf_id = s.pnf_id
                JOIN
                    inscripciones i ON s.id = i.seccion_id
                JOIN
                    estudiantes e ON i.estudiante_id = e.id
                JOIN
                    informacion_personal ip ON e.persona_id = ip.id
                WHERE
                    uc.id = ? AND s.periodo_academico_id = ?
                ORDER BY
                    ip.apellidos, ip.nombres;
            ''', (unidad_curricular_id, periodo_academico_id))

            estudiantes = cursor.fetchall()
            return estudiantes if estudiantes else []

        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}") 
            return []
        
        finally:
            if con is not None:
                con.close()


#pprint(ModeloNotas().estudiantes_por_uc(8,1))