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
            print(datos_trayecto["numero"])
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute(
                """
                UPDATE trayectos SET
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
#==================================================================================================================
    def obtener_lista_trayecto(self, id_pnf):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            
            cursor.execute(
                """
                SELECT id, nombre FROM trayectos WHERE pnf_id = ?
                """, (id_pnf,)
            )

            return cursor.fetchall()   

        except Exception as e:
            print(f"Error al obtener la lista: {e}") 
            return False
        finally:
            if con is not None:
                con.close()

    def obtener_lista_tramo(self, id_trayecto):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            
            cursor.execute(
                """
                SELECT id, nombre FROM tramos WHERE trayecto_id = ?
                """, (id_trayecto,)
            )

            return cursor.fetchall()   

        except Exception as e:
            print(f"Error al obtener la lista: {e}") 
            return False
        finally:
            if con is not None:
                con.close()
    
    def registrar_unidad_curricular(self, datos_uc,fecha_actual):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            
            cursor.execute(

                """
                INSERT INTO unidades_curriculares
                (codigo, nombre, nombre_corto, pnf_id, trayecto_id, tramo_id, area, subarea, eje_formativo, horas_teoricas, horas_practicas,
                horas_laboratorio, horas_trabajo_independiente, horas_totales, unidades_credito, tipo, caracter, modalidad, complejidad,
                prelaciones, competencias_genericas, competencias_especificas, saberes_cognitivos, saberes_procedimentales, saberes_actitudinales,
                estrategias_ensenanza, recursos_didacticos, evaluacion, bibliografia, homologacion_clave, clave_especial,
                estado, fecha_creacion, fecha_actualizacion)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    datos_uc["codigo"],
                    datos_uc["nombre"],
                    datos_uc["nombre_corto"],
                    datos_uc["id_pnf"],
                    datos_uc["id_trayecto"],
                    datos_uc["id_tramo"],
                    datos_uc["area"],
                    datos_uc["subarea"],
                    datos_uc["eje_formativo"],
                    datos_uc["horas_teoricas"],
                    datos_uc["horas_practicas"],
                    datos_uc["horas_laboratorio"],
                    datos_uc["horas_trabajo_independiente"],
                    datos_uc["horas_totales"],
                    datos_uc["unidades_credito"],
                    datos_uc["tipo"],
                    datos_uc["caracter"],
                    datos_uc["modalidad"],
                    datos_uc["complejidad"],
                    datos_uc["prelaciones"],
                    datos_uc["competencias_genericas"],
                    datos_uc["competencias_especificas"],
                    datos_uc["saberes_cognitivos"],
                    datos_uc["saberes_procedimentales"],
                    datos_uc["saberes_actitudinales"],
                    datos_uc["estrategias_ensenanza"],
                    datos_uc["recursos_didacticos"],
                    datos_uc["evaluacion"],
                    datos_uc["bibliografia"],
                    datos_uc["homologacion_clave"],
                    datos_uc["clave_especial"],
                    datos_uc["estado"],
                    fecha_actual,
                    fecha_actual,
                    
                )
            )
            con.commit()
            return True
        except Exception as e:
            print(f"Error al registrar la unidad curricular: {e}")
            return False
        finally:
            if con is not None:
                con.close()
    
    def existe_campo(self,campo, valor):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute(
                f"""
                SELECT * FROM pnf WHERE {campo} = ?
                """, (valor,)
            )
            row = cursor.fetchone()
            return row is not None  # Retorna True si existe, False si no
        except Exception as e:
            print(f"Error al verificar el campo {campo} del PNF: {e}")
            return False
        finally:
            if con is not None:
                con.close()

