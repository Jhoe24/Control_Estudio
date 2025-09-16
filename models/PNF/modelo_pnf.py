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
                duracion_semanas, total_creditos,total_horas, titulo_otorga, perfil_egreso,
                fecha_resolucion, version_pensum, fecha_creacion,fecha_actualizacion, estado) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                    datos_pnf["fecha_resolucion"],
                    datos_pnf["version_pensum"],
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

    def obtner_lista_pnf(self, docente_id=None):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            if docente_id:
                cursor.execute(
                    """
                    SELECT pnf.id, pnf.codigo, pnf.nombre FROM pnf
                    JOIN docente_sede_pnf ON pnf.id = docente_sede_pnf.pnf_id
                    WHERE docente_sede_pnf.docente_id = ?
                    """, (docente_id,)
                )
            else:
                
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

    def obtener_pnf_id(self, id):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute(
                """
                SELECT id FROM pnf WHERE id = ?
                """, (id,)
            )
            # El método fetchone() retorna la primera fila, que es una tupla
            resultado = cursor.fetchone() 
            return resultado[0] if resultado else None # Devuelve el primer elemento de la tupla (el ID) o None
        except Exception as e:
            print(f"Error al obtener la lista: {e}") 
            return None
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
                    fecha_resolucion = ?,
                    version_pensum = ?,
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
                    datos_pnf["fecha_resolucion"],
                    datos_pnf["version_pensum"],
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
                (codigo, nombre, nombre_corto, pnf_id, trayecto_id, tramo_id, area, subarea, horas_teoricas, horas_practicas,
                horas_laboratorio, horas_trabajo_independiente, horas_totales, unidades_credito, tipo, caracter, modalidad, complejidad, 
                clave_especial,
                estado, fecha_creacion, fecha_actualizacion)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
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

    def obtener_UC(self):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute(
                f"""
                SELECT * FROM unidades_curriculares
                """
            )
            respuesta = cursor.fetchall()
            return respuesta
        except Exception as e:
            print(f"Error al obtener la lista de pnf : {e}")
            return False
        finally:
            if con is not None:
                con.close()
    
    def obtener_unidad_curricular(self, id_uc):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute(
                "SELECT * FROM unidades_curriculares WHERE id = ?", (id_uc,)
            )
            row = cursor.fetchone()
            if row:
                columnas = [column[0] for column in cursor.description]
                return dict(zip(columnas, row))
            else:
                return None
        except Exception as e:
            print(f"Error al obtener la unidad curricular: {e}")
            return None
        finally:
            if con is not None:
                con.close()

    def update_unidad_curricular(self, datos_uc, id_uc, fecha_actual):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute(
                """
                UPDATE unidades_curriculares SET
                    codigo = ?,
                    nombre = ?,
                    nombre_corto = ?,
                    area = ?,
                    subarea = ?,
                    horas_teoricas = ?,
                    horas_practicas = ?,
                    horas_laboratorio = ?,
                    horas_trabajo_independiente = ?,
                    horas_totales = ?,
                    unidades_credito = ?,
                    tipo = ?,
                    caracter = ?,
                    modalidad = ?,
                    complejidad = ?,
                    clave_especial = ?,
                    estado = ?,
                    pnf_id = ?,
                    trayecto_id = ?,
                    tramo_id = ?,
                    fecha_actualizacion = ?
                    
                WHERE id = ?
                """,
                (
                    datos_uc["codigo"],
                    datos_uc["nombre"],
                    datos_uc["nombre_corto"],
                    datos_uc["area"],
                    datos_uc["subarea"],
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
                    datos_uc["clave_especial"],
                    datos_uc["estado"],
                    datos_uc["pnf_id"],
                    datos_uc["trayecto_id"],
                    datos_uc["tramo_id"],
                    fecha_actual,
                    id_uc
                )
            )
            con.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar la Unidad Curricular: {e}")
            return False
        finally:
            if con is not None:
                con.close()
    
    def buscar_uc_por_pnf(self, sentencia_sql, tuple_id,es_dic = False):
        """
        Busca las Unidades Curriculares asociadas a un PNF específico.
        """
        con = None
        try:
            con = sql.connect(self.db_ruta)
            if es_dic:
                con.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
            cursor = con.cursor()
            
            cursor.execute(sentencia_sql, tuple_id)
            return cursor.fetchall()  # Retorna una lista de diccionarios
        except Exception as e:
            print(f"Error al buscar UC por PNF: {e}")
            return []
        finally:
            if con is not None:
                con.close()

    #==========================================================================================

    def registrar_asignacion_estudiante_pnf(self, datos_asignacion):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            
            cursor.execute(
                """
                INSERT INTO estudiante_pnf 
                (estudiante_id, pnf_id, fecha_inicio, fecha_fin, trayecto_actual, tramo_actual, cohorte, turno, 
                creditos_aprobados, creditos_cursados, promedio_general, estado, observaciones) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    datos_asignacion["estudiante_id"],
                    datos_asignacion["pnf_id"],
                    datos_asignacion["fecha_inicio"],
                    datos_asignacion["fecha_fin"],
                    datos_asignacion["trayecto_actual"],
                    datos_asignacion["tramo_actual"],
                    datos_asignacion["cohorte"],
                    datos_asignacion["turno"],
                    datos_asignacion["creditos_aprobados"],
                    datos_asignacion["creditos_cursados"],
                    datos_asignacion["promedio_general"],
                    datos_asignacion["estado"],
                    datos_asignacion["observaciones"]
                )
            )
            con.commit()
            return True
        except Exception as e:
            print(f"Error al registrar la asignación del PNF: {e}")
            return False
        finally:
            if con is not None:
                con.close()

    def registrar_asignacion_docente_pnf(self, datos):
        """
        Registra una asignación de PNF para un docente en la tabla docente_sede_pnf.
        """
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute(
                """
                INSERT INTO docente_sede_pnf 
                (docente_id, pnf_id, fecha_asignacion, fecha_desasignacion, coordinador, activo, observaciones)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    datos["docente_id"],
                    datos["pnf_id"],
                    datos["fecha_asignacion"],
                    datos["fecha_desasignacion"],
                    int(datos["coordinador"]),  # Asegúrate de que sea 0 o 1
                    int(datos["activo"]),       # Asegúrate de que sea 0 o 1
                    datos["observaciones"]
                )
            )
            con.commit()
            return True
        except Exception as e:
            print(f"Error al registrar la asignación del PNF al docente: {e}")
            return False
        finally:
            if con is not None:
                con.close()


    def tiene_pnf_asignado(self, id_estudiante,tabla="estudiante_pnf"):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            if tabla != "estudiante_pnf":
                columna = "docente_id"
            else:
                columna = "estudiante_id"
            cursor.execute(
                f"""
                SELECT * FROM {tabla} WHERE {columna} = ?
                """, (id_estudiante,)
            )
            row = cursor.fetchone()
            return row is not None  # Retorna True si tiene PNF asignado, False si no
        except Exception as e:
            print(f"Error al verificar si el estudiante tiene PNF asignado: {e}")
            return False
        finally:
            if con is not None:
                con.close()


    def obtener_pnf_asignado(self, id_estudiante):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            con.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
            cursor = con.cursor()
            cursor.execute(
                """
                SELECT * FROM estudiante_pnf WHERE estudiante_id = ?
                """, (id_estudiante,)
            )
            return cursor.fetchone()  # Retorna un diccionario o None
        except Exception as e:
            print(f"Error al obtener el PNF asignado: {e}")
            return None
        finally:
            if con is not None:
                con.close()
        
    def obtener_pnf_asignado_docente(self, docente_id):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            con.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
            cursor = con.cursor()
            cursor.execute(
                """
                SELECT * FROM docente_sede_pnf WHERE docente_id = ?
                """, (docente_id,)
            )
            return cursor.fetchall()  # Retorna un diccionario o None
        except Exception as e:
            print(f"Error al obtener el PNF asignado: {e}")
            return None
        finally:
            if con is not None:
                con.close()

    def update_pnf_asignado(self, estudiante_id, datos_asignacion):
        """
        Actualiza la asignación de PNF de un estudiante en la tabla estudiante_pnf.
        """
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute(
                """
                UPDATE estudiante_pnf SET
                    pnf_id = ?,
                    fecha_inicio = ?,
                    fecha_fin = ?,
                    trayecto_actual = ?,
                    tramo_actual = ?,
                    cohorte = ?,
                    turno = ?,
                    creditos_aprobados = ?,
                    creditos_cursados = ?,
                    promedio_general = ?,
                    estado = ?,
                    observaciones = ?
                WHERE estudiante_id = ?
                """,
                (
                    datos_asignacion["pnf_id"],
                    datos_asignacion["fecha_inicio"],
                    datos_asignacion["fecha_fin"],
                    datos_asignacion["trayecto_actual"],
                    datos_asignacion["tramo_actual"],
                    datos_asignacion["cohorte"],
                    datos_asignacion["turno"],
                    datos_asignacion["creditos_aprobados"],
                    datos_asignacion["creditos_cursados"],
                    datos_asignacion["promedio_general"],
                    datos_asignacion["estado"],
                    datos_asignacion["observaciones"],
                    estudiante_id
                )
            )
            con.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar la asignación del PNF: {e}")
            return False
        finally:
            if con is not None:
                con.close()
            
    def update_pnf_asignado_docente(self, docente_id, datos,id_asignacion):
        """
        Actualiza la asignación de PNF de un docente en la tabla docente_sede_pnf.
        """
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute(
                """
                UPDATE docente_sede_pnf SET
                    pnf_id = ?,
                    fecha_asignacion = ?,
                    fecha_desasignacion = ?,
                    coordinador = ?,
                    activo = ?,
                    observaciones = ?
                WHERE id =? AND docente_id = ?
                """,
                (
                    datos["pnf_id"],
                    datos["fecha_asignacion"],
                    datos["fecha_desasignacion"],
                    int(datos["coordinador"]),
                    int(datos["activo"]),
                    datos["observaciones"],
                    id_asignacion,
                    docente_id
                )
            )
            con.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar la asignación del PNF al docente: {e}")
            return False
        finally:
            if con is not None:
                con.close()

    def obtener_nombre_pnf_asignado_docente(self, docente_id):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            con.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
            cursor = con.cursor()
            cursor.execute(
                """
                SELECT dsp.*, pnf.nombre AS nombre_pnf
                FROM docente_sede_pnf dsp
                JOIN pnf ON dsp.pnf_id = pnf.id
                WHERE dsp.docente_id = ?
                """, (docente_id,)
            )
            return cursor.fetchall()  # Lista de diccionarios con nombre_pnf incluido
        except Exception as e:
            print(f"Error al obtener el PNF asignado: {e}")
            return None
        finally:
            if con is not None:
                con.close()


    def obtener_nombres_por_id(self, tabla, id ):
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

    def buscar_uc_por_pnf_trayecto_tramo(self, id_pnf, id_trayecto=None, id_tramo=None):
        """
        Busca las Unidades Curriculares asociadas a un PNF específico.
        """
        if id_trayecto is not None and id_tramo is not None:
            sentencia_sql = """
            SELECT * FROM unidades_curriculares
            WHERE pnf_id = ? AND trayecto_id = ? AND tramo_id = ?
            """
            respuesta = self.buscar_uc_por_pnf(sentencia_sql,(id_pnf, id_trayecto, id_tramo))
        elif id_trayecto is not None:
            sentencia_sql = """
            SELECT * FROM unidades_curriculares
            WHERE pnf_id = ? AND trayecto_id = ?
            """
            respuesta = self.buscar_uc_por_pnf(sentencia_sql, (id_pnf, id_trayecto))
        else:
            sentencia_sql = """
            SELECT * FROM unidades_curriculares
            WHERE pnf_id = ?
            """
            respuesta = self.buscar_uc_por_pnf(sentencia_sql, (id_pnf,))
        return respuesta
    
    #=============================================================================================================================
    
    def uc_asignada_a_docente(self, docente_pnf_id, uc_id, periodo_id):
        """
        Verifica si una Unidad Curricular (UC) ya está asignada a un docente en un período académico.
        """
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute("""
                SELECT * 
                FROM docente_uc
                WHERE docente_pnf_id = ? 
                AND unidad_curricular_id = ? 
                AND periodo_academico_id = ? 
                AND activo = 1
            """, (docente_pnf_id, uc_id, periodo_id))

            return cursor.fetchone() is not None

        except Exception as e:
            print(f"Error al verificar asignación de UC: {e}")
            return False

        finally:
            if con is not None:
                con.close()

    def asignar_uc_a_docente(self, docente_pnf_id, uc_id, periodo_id):
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()

            # Insertar o reemplazar directamente la asignación
            cursor.execute("""
                INSERT OR REPLACE INTO docente_uc (id, docente_pnf_id, unidad_curricular_id, periodo_academico_id, fecha_asignacion, activo)
                VALUES (
                    (SELECT id FROM docente_uc 
                    WHERE docente_pnf_id = ? AND unidad_curricular_id = ? AND periodo_academico_id = ?),
                    ?, ?, ?, DATE('now'), 1
                )
            """, (docente_pnf_id, uc_id, periodo_id, docente_pnf_id, uc_id, periodo_id))

            con.commit()
            return True
        except Exception as e:
            print(f"Error al asignar UC a docente: {e}")
            return False
        finally:
            if con:
                con.close()

    def desasignar_uc_de_docente(self, docente_pnf_id, uc_id, periodo_id):
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            
            cursor.execute("""
                UPDATE docente_uc
                SET activo = 0
                WHERE docente_pnf_id = ? AND unidad_curricular_id = ? AND periodo_academico_id = ?
            """, (docente_pnf_id, uc_id, periodo_id))

            con.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al desasignar UC de docente: {e}")
            return False
        finally:
            if con:
                con.close()
        
    def obtener_docente_asignado_uc(self, uc_id, periodo_id):
        """
        Retorna el docente_id al que está asignada la UC en el periodo dado, o None si no está asignada.
        """
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute("""
                SELECT docente_pnf_id
                FROM docente_uc
                WHERE unidad_curricular_id = ? AND periodo_academico_id = ? AND activo = 1
                LIMIT 1
            """, (uc_id, periodo_id))
            resultado = cursor.fetchone()
            if resultado:
                return resultado[0]  # docente_id
            return None
        except Exception as e:
            print(f"Error al obtener el docente asignado a la UC: {e}")
            return None
        finally:
            if con:
                con.close()

    def obtener_periodos_disponibles(self):
        """
        Devuelve una lista de tuplas (id, nombre) de los periodos académicos activos.
        """
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()

            cursor.execute("""
                SELECT id, nombre 
                FROM periodos_academicos
                WHERE estado IN ('planificacion','en_curso', 'inscripcion')
                ORDER BY fecha_inicio
            """)
            resultados = cursor.fetchall()

            if con is not None:
                con.close()
            return resultados if resultados else []
        except Exception as e:
            print("Error al obtener periodos académicos:", e)
            return []

    def obtener_periodo_id_por_nombre(self, nombre_periodo):
        """
        Devuelve el ID de un periodo a partir de su nombre.
        """
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()

            cursor.execute("""
                SELECT id 
                FROM periodos_academicos
                WHERE nombre = ?
            """, (nombre_periodo,))
            resultado = cursor.fetchone()

            if con is not None:
                con.close()
            return resultado[0] if resultado else None
        except Exception as e:
            print("Error al obtener ID del periodo por nombre:", e)
            return None
        
    def existe_coordinador(self, pnf_id):
        """Verifica si ya existe un coordinador asignado para un PNF específico.""" 
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute(
                """
                SELECT * FROM docente_sede_pnf WHERE pnf_id = ? AND coordinador = 1 AND activo = 1
                """, (pnf_id,)
            )
            row = cursor.fetchone()
            return row is not None  # Retorna True si existe, False si no
        except Exception as e:
            print(f"Error al verificar si existe coordinador para el PNF: {e}")
            return False
        finally:
            if con is not None:
                con.close()
    
    def contar_pnf(self):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute("SELECT COUNT(*) FROM pnf")
            resultado = cursor.fetchone()
            return resultado[0] if resultado else 0
        except Exception as e:
            print(f"Error al contar los PNF: {e}")
            return 0
        finally:
            if con is not None:
                con.close()

    def contar_uc_por_pnf(self, pnf_id):
        """Cuenta el número de unidades curriculares para un PNF específico."""
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute("SELECT COUNT(*) FROM unidades_curriculares WHERE pnf_id = ?", (pnf_id,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else 0
        except Exception as e:
            print(f"Error al contar las Unidades Curriculares por PNF: {e}")
            return 0
        finally:
            if con is not None:
                con.close()

    def obtener_id_por_nombre_y_pnf(self, tabla, nombre, pnf_id):
        """
        Obtiene el ID de un registro en una tabla (ej. trayectos, tramos)
        filtrando por su nombre y el pnf_id asociado.
        """
        con = None
        # Lista blanca de tablas permitidas para evitar inyección SQL
        tablas_permitidas = ["trayectos", "tramos"]
        if tabla not in tablas_permitidas:
            print(f"Error: La tabla '{tabla}' no está permitida para esta consulta.")
            return None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute(f"SELECT id FROM {tabla} WHERE nombre = ? AND pnf_id = ?", (nombre, pnf_id))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
        except Exception as e:
            print(f"Error al obtener ID por nombre y PNF: {e}")
            return None
        finally:
            if con:
                con.close()


    
