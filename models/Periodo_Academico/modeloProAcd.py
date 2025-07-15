import sqlite3 as sql
import os
from pprint import pprint

class ModeloProAcademico:
    def __init__(self):
       self.db_ruta = os.path.join('db', 'sistema_academico.db')
    
    def registrar_periodo_academico(self,datos_periodo):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute(
                """
                INSERT INTO periodos_academicos
                (codigo, nombre, tipo, fecha_inicio, fecha_fin, fecha_inicio_inscripcion, fecha_fin_inscripcion, 
                fecha_inicio_clases, fecha_fin_clases, fecha_inicio_evaluaciones, fecha_fin_evaluaciones, duracion_semanas,
                estado, observaciones)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                 
                """,(
                    datos_periodo["codigo"],
                    datos_periodo["nombre"],
                    datos_periodo["tipo"],
                    datos_periodo["fecha_inicio"],
                    datos_periodo["fecha_fin"],
                    datos_periodo["fecha_inicio_inscripcion"],
                    datos_periodo["fecha_fin_inscripcion"],
                    datos_periodo["fecha_inicio_clases"],
                    datos_periodo["fecha_fin_clases"],
                    datos_periodo["fecha_inicio_evaluaciones"],
                    datos_periodo["fecha_fin_evaluaciones"],
                    datos_periodo["duracion_semanas"],
                    datos_periodo["estado"],
                    datos_periodo["observaciones"]
                    )
                )
            con.commit()
            con.close()
            return True
        except Exception as e:
            print(f"Error al registrar el periodo academico: {e}") 
            return False
        finally:
            if con is not None:
                con.close()

    def obtener_periodos_academicos(self):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute('SELECT id, nombre, codigo FROM periodos_academicos ORDER BY nombre')
            return [{
                "id": row[0],
                "nombre": row[1],
                "codigo": row[2]
            } for row in cursor.fetchall()]
                
        except Exception as e:
            print(f"Error al obtener los periodos academicos: {e}") 
            return []
        finally:
            if con is not None:
                con.close()


