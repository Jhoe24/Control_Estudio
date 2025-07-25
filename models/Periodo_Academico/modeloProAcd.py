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
            cursor.execute('SELECT id, nombre, codigo, estado FROM periodos_academicos ORDER BY nombre')
            return [{
                "id": row[0],
                "nombre": row[1],
                "codigo": row[2],
                "estado": row[3]
            } for row in cursor.fetchall()]
                
        except Exception as e:
            print(f"Error al obtener los periodos academicos: {e}") 
            return []
        finally:
            if con is not None:
                con.close()

    def obtener_periodo_academico_datos(self, id_periodo):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute(
                """
                SELECT id, codigo, nombre, tipo, fecha_inicio, fecha_fin, fecha_inicio_inscripcion, 
                fecha_fin_inscripcion, fecha_inicio_clases, fecha_fin_clases, fecha_inicio_evaluaciones, 
                fecha_fin_evaluaciones, duracion_semanas, estado, observaciones FROM periodos_academicos 
                WHERE id=?""", (id_periodo,))
            return [{
                "id": row[0],
                "codigo": row[1],
                "nombre": row[2],
                "tipo": row[3],
                "fecha_inicio": row[4],
                "fecha_fin": row[5],
                "fecha_inicio_inscripcion": row[6],
                "fecha_fin_inscripcion": row[7],
                "fecha_inicio_clases": row[8],
                "fecha_fin_clases": row[9],
                "fecha_inicio_evaluaciones": row[10],
                "fecha_fin_evaluaciones": row[11],
                "duracion_semanas": row[12],
                "estado": row[13],
                "observaciones": row[14]
            } for row in cursor.fetchall()]
        
        except Exception as e:
            print(f"Error al obtener los periodos academicos: {e}") 
            return []
        finally:
            if con is not None:
                con.close()

#=======================================================================================================================================================

    def actualizar_periodo_academico(self, id_periodo, datos):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute("""
                    UPDATE periodos_academicos
                    SET codigo=?, nombre=?, tipo=?, fecha_inicio=?, fecha_fin=?, fecha_inicio_inscripcion=?, fecha_fin_inscripcion=?,
                        fecha_inicio_clases=?, fecha_fin_clases=?, fecha_inicio_evaluaciones=?, fecha_fin_evaluaciones=?,
                        duracion_semanas=?, estado=?, observaciones=?
                    WHERE id=?
                """, (
                    datos["codigo"], 
                    datos["nombre"], 
                    datos["tipo"],
                    datos["fecha_inicio"], 
                    datos["fecha_fin"],
                    datos["fecha_inicio_inscripcion"], 
                    datos["fecha_fin_inscripcion"],
                    datos["fecha_inicio_clases"], 
                    datos["fecha_fin_clases"],
                    datos["fecha_inicio_evaluaciones"], 
                    datos["fecha_fin_evaluaciones"],
                    datos["duracion_semanas"], 
                    datos["estado"], 
                    datos["observaciones"],
                    id_periodo
                )
                )
            con.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar período académico: {e}")
            return False

    def obtener_codigos(self):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute('SELECT codigo FROM periodos_academicos')
            return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error al obtener los códigos: {e}")
            return []
        finally:
            if con is not None:
                con.close()


    def obtener_id_por_codigo(self, codigo):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute('SELECT id FROM periodos_academicos WHERE codigo=?', (codigo,))
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error al obtener el ID por código: {e}")
            return None
        finally:
            if con is not None:
                con.close()

# ModeloProAcademico = ModeloProAcademico()

# pprint(ModeloProAcademico.obtener_codigos())

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

# db = ModeloProAcademico()
# print(db.obtener_nombres_por_id("periodos_academicos", 1))

