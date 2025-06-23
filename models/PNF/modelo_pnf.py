import sqlite3 as sql
import os
from pprint import pprint

class ModeloPNF:
    def __init__(self):
       self.db_ruta = os.path.join('db', 'sistema_academico.db')

    def registrar_pnf(self, datos_tramo,fecha_cracion):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            
            cursor.execute(
                """
                INSERT INTO pnf 
                (codigo, codigo_nacional, nombre, nombre_corto, nivel,area_conocimiento, duracion_trayectos,
                duracion_semanas, total_horas, titulo_otorga, perfil_egreso, resolucion_creacion,
                fecha_resolucion, version_pensum, coordinador_nacional, fecha_actualizacion, estado) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    datos_tramo["codigo"],
                    datos_tramo["codigo_nacional"],
                    datos_tramo["nombre_pnf"],
                    datos_tramo["siglas"],
                    datos_tramo["tipo_pnf"],
                    datos_tramo["area_conocimiento"],
                    datos_tramo["cantidad_trayectos"],
                    datos_tramo["duracion_semanas"],
                    datos_tramo["duracion_horas"],
                    datos_tramo["titulo_otorga"],
                    datos_tramo["titulo_egreso"],
                    datos_tramo["resolucion"],
                    datos_tramo["fecha_resolucion"],
                    datos_tramo["version_pensum"],
                    datos_tramo["coordinador_nacional"],
                    fecha_cracion,
                    datos_tramo["estado"]
                )
            )

            id_pnf = cursor.lastrowid
            con.commit()
            con.close()
            return id_pnf   

        except Exception as e:
            print(f"Error al registrar los datos del pnf: {e}") 
            return False
        finally:
            if con is not None:
                con.close()
    
    def registrar_trayecto(self,datos_tramo,id_pnf):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            
            cursor.execute(
                """
                INSERT INTO trayectos 
                (pnf_id, numero, nombre, tipo, duracion_semanas, duracion_horas, creditos_minimos,
                creditos_maximos, numeros_tramos, objectivos, perfil_egreso, obligatorio, secuencial, estado) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    id_pnf,
                    datos_tramo["numero"],
                    datos_tramo["nombre"],
                    datos_tramo["tipo"],
                    datos_tramo["duracion_semanas"],
                    datos_tramo["duracion_horas"],
                    datos_tramo["creditos_minimos"],
                    datos_tramo["creditos_maximos"],
                    datos_tramo["numero_tramos"],
                    datos_tramo["objetivos"],
                    datos_tramo["perfil_egreso"],
                    datos_tramo["obligatorio"],
                    datos_tramo["secuencial"],
                    datos_tramo["estado"]
                )
            )

            id_trayecto = cursor.lastrowid
            con.commit()
            con.close()
            return id_trayecto   

        except Exception as e:
            print(f"Error al registrar los datos del trayecto {datos_tramo["tipo"]}: {e}") 
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
                INSERT INTO trayectos 
                (trayecto_id, numero, nombre, duracion_semanas, duracion_horas, creditos,
                objectivos, estado) 
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
            con.close()
            return True   

        except Exception as e:
            print(f"Error al registrar los datos del tramo {datos_tramo["nombre"]}: {e}") 
            return False
        finally:
            if con is not None:
                con.close()