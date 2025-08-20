import sqlite3 as sql
import os
from pprint import pprint

class ModelRegistroEstudiantes:
    def guardar_nota(self, inscripcion_id, unidad_curricular_id, valor):
        """
        Guarda o actualiza la nota de un estudiante para una unidad curricular específica.
        """
        db_ruta = self.db_ruta
        con = sql.connect(db_ruta)
        cursor = con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        try:
            # Verificar si ya existe una nota para esta inscripcion y unidad curricular
            cursor.execute("SELECT id FROM notas WHERE inscripcion_id = ? AND unidad_curricular_id = ?", (inscripcion_id, unidad_curricular_id))
            existe = cursor.fetchone()
            if existe:
                # Actualizar nota existente
                cursor.execute("UPDATE notas SET valor = ? WHERE id = ?", (valor, existe[0]))
            else:
                # Insertar nueva nota
                cursor.execute("INSERT INTO notas (inscripcion_id, unidad_curricular_id, valor) VALUES (?, ?, ?)", (inscripcion_id, unidad_curricular_id, valor))
            con.commit()
            return True
        except Exception as e:
            print(f"Error al guardar la nota: {e}")
            raise
        finally:
            con.close()

    def obtener_nota(self, inscripcion_id, unidad_curricular_id):
        """
        Guarda o actualiza la nota de un estudiante para una unidad curricular específica.
        """
        db_ruta = self.db_ruta
        con = sql.connect(db_ruta)
        cursor = con.cursor()
        try:
            # Verificar si ya existe una nota para esta inscripcion y unidad curricular
            cursor.execute("SELECT valor FROM notas WHERE inscripcion_id = ? AND unidad_curricular_id = ?", (inscripcion_id, unidad_curricular_id))
            resultado =  cursor.fetchone()
            return resultado[0] if resultado else None
        
        except Exception as e:
            print(f"Error al obtener la nota: {e}")
            raise
        finally:
            con.close()
    
    def __init__(self):
        self.db_ruta = os.path.join('db', 'sistema_academico.db')
    
    def registrar_estudiante(self, datos_estudiantes):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            # insertar datos en la tabla de informacion_personal
            cursor.execute(''' INSERT INTO informacion_personal
                           (documento_identidad, tipo_documento, nombres, apellidos, fecha_nacimiento, sexo, estado_civil, nacionalidad, lugar_nacimiento, correo_electronico, tipo)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                           ''',(
                               datos_estudiantes['nro_documento'],
                               datos_estudiantes['tipo_documento'],
                               datos_estudiantes['nombre'],
                               datos_estudiantes['apellido'],
                               datos_estudiantes['f_nacimiento'],
                               datos_estudiantes['genero'],
                               datos_estudiantes['edo_civil'],
                               datos_estudiantes['nacionalidad'],
                               datos_estudiantes['lugar_nacimiento'],
                               datos_estudiantes['correo_electronico'],
                               'estudiante'
                           ))
            persona_id = cursor.lastrowid

            
            # Insertar datos en la tabla estudiante
            
            cursor.execute('''
                           INSERT INTO estudiantes
                           (persona_id, codigo_unico, institucion_procedencia, mencion_bachiller, fecha_grado_bachiller, fecha_ingreso, condicion)
                           VALUES (?, ?, ?, ?, ?, ?, ?)
                           ''', (
                            persona_id,
                            datos_estudiantes['codigo_sni'],
                            datos_estudiantes['institucion'],
                            datos_estudiantes['titulo_obtenido'],
                            datos_estudiantes['f_grado'],
                            datos_estudiantes['f_ingreso'],
                            datos_estudiantes['condicion']
                           ))
            
            # Insertar datos en la tabla telefonos

            telefonos = datos_estudiantes.get('lista_telefonos', [])

            for idx, (tipo, numero) in enumerate(telefonos):
                cursor.execute('''
                    INSERT INTO telefonos
                    (persona_id, tipo_telefono, numero, principal)
                    VALUES (?, ?, ?, ?)
                ''', (
                    persona_id,
                    tipo,
                    numero,
                    1 if idx == 0 else 0  # El primero es principal, los demás secundarios
                ))
            
            # cursor.execute('''
            #                 INSERT INTO telefonos
            #                 (persona_id, tipo_telefono, numero, principal)
            #                 VALUES (?,?,?,?)
            #                 ''',(
            #                     persona_id,
            #                     datos_estudiantes['tipo_telefono_p'],
            #                     datos_estudiantes['telefono_principal'],
            #                     1 # true
            #                 ))
            

            # cursor.execute('''
            #                 INSERT INTO telefonos
            #                 (persona_id, tipo_telefono, numero, principal)
            #                 VALUES (?,?,?,?)
            #                 ''',(
            #                     persona_id,
            #                     datos_estudiantes['tipo_telefono_s'],
            #                     datos_estudiantes['telefono_secundario'],
            #                     0 # false
            #                 ))
            
            # Insertar datos en la tabla de direcciones

            cursor.execute('''
                            INSERT INTO direcciones
                            (persona_id, estado, municipio, parroquia, sector, calle, casa_edificio, direccion_completa, tipo_direccion, principal)
                            VALUES (?,?,?,?,?,?,?,?,?,?)
                           ''',(
                               persona_id,
                               datos_estudiantes['estado'],
                               datos_estudiantes['municipio'],
                               datos_estudiantes['parroquia'],
                               datos_estudiantes['sector'],
                               datos_estudiantes['calle'],
                               datos_estudiantes['casa_apart'],
                               f"{datos_estudiantes['estado']}, {datos_estudiantes['municipio']}, {datos_estudiantes['parroquia']},{datos_estudiantes['sector']},{datos_estudiantes['calle']},{datos_estudiantes['casa_apart']}",
                               datos_estudiantes['tipo_direccion'],
                               1 #True
                           ))

            con.commit()
            con.close()
            return True   

        except Exception as e:
            print(f"Error al registrar estudiantes: {e}") 
            return False
        finally:
            if con is not None:
                con.close()
    
    def lista_Estudiantes(self, registro_inicio = 0):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()

            #Extraer de la tabla informacion personal y estudiantes
            cursor.execute('''
                            SELECT ip.id AS persona_id, ip.*, e.*
                            FROM informacion_personal ip
                            LEFT JOIN estudiantes e ON ip.id = e.persona_id
                            WHERE ip.tipo='estudiante'
                            LIMIT 11
                            OFFSET ?
                            ''',(registro_inicio,))
            resultados = cursor.fetchall()
                            
            nombres_columnas = [descripcion[0] for descripcion in cursor.description]
            
            # Telefonos
            cursor.execute('''
                SELECT persona_id, tipo_telefono, numero, principal
                FROM telefonos
            ''')
            telefonos = cursor.fetchall()

            # Agrupa todos los teléfonos por persona_id
            telefonos_dict = {}
            for persona_id, tipo_telefono, numero, principal in telefonos:
                if persona_id not in telefonos_dict:
                    telefonos_dict[persona_id] = {
                        "todos": []  # Aquí guardaremos todos los teléfonos
                    }
                # Agrega cada teléfono a la lista 'todos'
                telefonos_dict[persona_id]["todos"].append((tipo_telefono, numero, principal))
                # (Opcional) sigue guardando principal/secundario si lo necesitas
                if principal == 1:
                    telefonos_dict[persona_id]['telefono_principal'] = numero
                    telefonos_dict[persona_id]['tipo_telefono_p'] = tipo_telefono
                else:
                    telefonos_dict[persona_id]['telefono_secundario'] = numero
                    telefonos_dict[persona_id]['tipo_telefono_s'] = tipo_telefono


            # direcciones
            cursor.execute('''
                                SELECT persona_id, estado, municipio, parroquia, sector, calle, casa_edificio, tipo_direccion
                                FROM direcciones
                            ''')
            direcciones = cursor.fetchall()

            direcciones_dict = {
                                d[0]: {
                                    "estado": d[1],
                                    "municipio": d[2],
                                    "parroquia": d[3],
                                    "sector": d[4],
                                    "calle": d[5],
                                    "casa_edificio": d[6],
                                    "tipo_direccion": d[7]
                                }
                                for d in direcciones
                            }                
            con.close()
            
            informacion_estudiantes = []
            
            for resultado in resultados:
                
                estudiante = dict(zip(nombres_columnas, resultado))
                
                # Asegurarse de que persona_id siempre sea el id de informacion_personal
                persona_id = estudiante.get('persona_id')
                estudiante['id'] = estudiante.get('id')
                

                tel_info = telefonos_dict.get(persona_id, {})
                # Agrega todos los teléfonos como array de tuplas según el id_persona
                estudiante['telefonos'] = [
                    (tipo_telefono, numero, principal)
                    for tipo_telefono, numero, principal in [
                        (t[0], t[1], t[2]) for t in tel_info.get('todos', [])
                    ]
                ]
                
                direccion_info = direcciones_dict.get(persona_id, {})
                estudiante['estado'] = direccion_info.get('estado', '')
                estudiante['municipio'] = direccion_info.get('municipio', '')
                estudiante['parroquia'] = direccion_info.get('parroquia', '')
                estudiante['sector'] = direccion_info.get('sector', '')
                estudiante['calle'] = direccion_info.get('calle', '')
                estudiante['casa_apart'] = direccion_info.get('casa_edificio', '')
                estudiante['tipo_direccion'] = direccion_info.get('tipo_direccion', '')
                    
                
                informacion_estudiantes.append(estudiante)

            return informacion_estudiantes
            
        except Exception as e:
            print(f"Error al realizar la consulta: {e}") 
            return False
        finally:
            if con is not None:
                con.close()
    
    def buscar_estudiante(self, tipo_documento, nro_documento):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()

            # Buscar estudiante, usando alias para los IDs
            cursor.execute('''
                SELECT ip.id AS persona_id, ip.*, e.id AS estudiante_id, e.*
                FROM informacion_personal ip
                LEFT JOIN estudiantes e ON ip.id= e.persona_id
                WHERE ip.tipo='estudiante' AND ip.tipo_documento = ? AND ip.documento_identidad = ?
                LIMIT 1
            ''', (tipo_documento, nro_documento))
            resultado = cursor.fetchone()
            if not resultado:
                con.close()
                return None  # No encontrado

            nombres_columnas = [desc[0] for desc in cursor.description]
            estudiante = dict(zip(nombres_columnas, resultado))
            persona_id = estudiante['persona_id']  

            # Telefonos del estudiante
            cursor.execute('''
                SELECT tipo_telefono, numero, principal FROM telefonos
                WHERE persona_id = ?
            ''', (persona_id,))
            telefonos = cursor.fetchall()
            estudiante['telefonos'] = [(tipo_telefono, numero, principal) for tipo_telefono, numero, principal in telefonos]

            # Direccion del estudiante
            print("persona_id:", persona_id)
            cursor.execute('''
                SELECT estado, municipio, parroquia, sector, calle, casa_edificio, tipo_direccion
                FROM direcciones
                WHERE persona_id = ? AND principal=1
                LIMIT 1
            ''', (persona_id,))
            dir_row = cursor.fetchone()
            if dir_row:
                estudiante['estado'] = dir_row[0]
                estudiante['municipio'] = dir_row[1]
                estudiante['parroquia'] = dir_row[2]
                estudiante['sector'] = dir_row[3]
                estudiante['calle'] = dir_row[4]
                estudiante['casa_apart'] = dir_row[5]
                estudiante['tipo_direccion'] = dir_row[6]
            else:
                estudiante['estado'] = ''
                estudiante['municipio'] = ''
                estudiante['parroquia'] = ''
                estudiante['sector'] = ''
                estudiante['calle'] = ''
                estudiante['casa_apart'] = ''
                estudiante['tipo_direccion'] = ''

            con.close()
            return estudiante

        except Exception as e:
            print(f"Error al realizar la consulta: {e}")
            return False
        finally:
            if con is not None:
                con.close()

    def obtener_id_ultimo(self):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()

            cursor.execute('''
                            SELECT id FROM informacion_personal 
                            WHERE tipo = 'estudiante'
                            ''')
            resultado = cursor.fetchall()
            con.close()
            dato = resultado[-1]
            return dato[0]
        
        except Exception as e:
             print(f"Error al realizar la ultima consulta: {e}") 
             return False
        finally:
            if con is not None:
                con.close()
        
    def obtener_primer_id(self):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute('''
                            SELECT id FROM informacion_personal
                            WHERE tipo = 'estudiante'
                            ORDER BY id ASC
                            LIMIT 1;
                            ''')
            resultado = cursor.fetchall()
            con.close()
            if resultado:
                dato = resultado[0]
                return dato[0]
            else:
                return None
        except Exception as e:
            print(f"Error al realizar la consulta: {e}") 
            return False
        finally:
            if con is not None:
                con.close()
            
    def obtener_cantidad_estudiantes(self):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute('''
                            SELECT COUNT(*) FROM informacion_personal
                            WHERE tipo = 'estudiante'
                            ''')
            resultado = cursor.fetchone()
            con.close()
            return resultado[0]
        except Exception as e:
            print(f"Error al realizar la consulta: {e}") 
            return False
        finally:
            if con is not None:
                con.close()
        

    def update_estudiante(self, id, datos_estudiantes):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()

            # Actualizar datos en la tabla de informacion_personal
            cursor.execute('''
                           UPDATE informacion_personal
                           SET nombres = ?, apellidos = ?, fecha_nacimiento = ?, sexo = ?, estado_civil = ?, nacionalidad = ?, lugar_nacimiento = ?, correo_electronico = ?
                           WHERE id = ?
                           ''',(
                               datos_estudiantes['nombre'],
                               datos_estudiantes['apellido'],
                               datos_estudiantes['f_nacimiento'],
                               datos_estudiantes['genero'],
                               datos_estudiantes['edo_civil'],
                               datos_estudiantes['nacionalidad'],
                               datos_estudiantes['lugar_nacimiento'],
                               datos_estudiantes['correo_electronico'],
                               id
                           ))
            
            # Actualizar datos en la tabla estudiantes
            cursor.execute('''
                           UPDATE estudiantes
                           SET codigo_unico = ?, institucion_procedencia = ?, mencion_bachiller = ?, fecha_grado_bachiller = ?, fecha_ingreso = ?, condicion = ?
                           WHERE persona_id = ?
                           ''', (
                            datos_estudiantes['codigo_sni'],
                            datos_estudiantes['institucion'],
                            datos_estudiantes['titulo_obtenido'],
                            datos_estudiantes['f_grado'],
                            datos_estudiantes['f_ingreso'],
                            datos_estudiantes['condicion'],
                            id
                           ))
            
            # Actualizar telefonos
            # cursor.execute('''
            #                 UPDATE telefonos
            #                 SET tipo_telefono = ?, numero = ?
            #                 WHERE persona_id = ? AND principal=1
            #                 ''',(
            #                     datos_estudiantes['tipo_telefono_p'],
            #                     datos_estudiantes['telefono_principal'],
            #                     id
            #                 ))
            
            # cursor.execute('''
            #                 UPDATE telefonos
            #                 SET tipo_telefono = ?, numero = ?
            #                 WHERE persona_id = ? AND principal=0
            #                 ''',(
            #                     datos_estudiantes['tipo_telefono_s'],
            #                     datos_estudiantes['telefono_secundario'],
            #                     id
            #                 ))

            # Actualizar telefonos: eliminar los existentes y volver a insertar los nuevos
            print(id)
            cursor.execute('DELETE FROM telefonos WHERE persona_id = ?', (id,))
            telefonos = datos_estudiantes.get('lista_telefonos', [])
            for idx, (tipo, numero) in enumerate(telefonos):
                cursor.execute('''
                    INSERT INTO telefonos (persona_id, tipo_telefono, numero, principal)
                    VALUES (?, ?, ?, ?)
                ''', (
                    id,
                    tipo,
                    numero,
                    1 if idx == 0 else 0  # El primero es principal, los demás secundarios
                ))

            print("id:", id)
            # Actualizar direcciones
            cursor.execute('''
                           UPDATE direcciones
                           SET estado=?, municipio=?, parroquia=?, sector=?, calle=?, casa_edificio=?, direccion_completa=?, tipo_direccion=?
                            WHERE persona_id = ? AND principal=1
                            ''',(
                                 datos_estudiantes['estado'],
                                 datos_estudiantes['municipio'],
                                 datos_estudiantes['parroquia'],
                                 datos_estudiantes['sector'],
                                 datos_estudiantes['calle'],
                                 datos_estudiantes['casa_apart'],
                                 f"{datos_estudiantes['estado']}, {datos_estudiantes['municipio']}, {datos_estudiantes['parroquia']},{datos_estudiantes['sector']},{datos_estudiantes['calle']},{datos_estudiantes['casa_apart']}",
                                 datos_estudiantes['tipo_direccion'],
                                 id
                            ))
            con.commit()
            con.close()
            return True
        except Exception as e:
            print(f"Error al actualizar estudiante: {e}") 
            return False
        finally:
            if con is not None:
                con.close()
    

    #==========Asignacion del pnf a estudiantes=======================

    # def obtener_estudiantes_pnf(self,tupla_datos):
    #     con = None
    #     try:
    #         con = sql.connect(self.db_ruta)
    #         con.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
    #         cursor = con.cursor()
    #         cursor.execute(
    #             """
    #             SELECT * FROM estudiante_pnf WHERE pnf_id = ? AND trayecto_actual = ? AND tramo_actual = ?
    #             """, tupla_datos
    #         )
    #         return cursor.fetchall()  # Retorna un diccionario o None
    #     except Exception as e:
    #         print(f"Error al obtener el PNF asignado: {e}")
    #         return None
    #     finally:
    #         if con is not None:
    #             con.close()


                           
    # def obtener_campo(self, table, columna, value):
    #     try:
    #         con = sql.connect(self.db_ruta)
    #         cursor = con.cursor()

    #         #Estraer los datos de informacion perosonal
    #         cursor.execute('''
    #                         SELECT FROM {table} 
    #                         WHERE {columna} = ?
    #                        ''',(value))
    #         resultado = cursor.fetchone()
    #         con.close()
    #         return resultado   

    #     except Exception as e:
    #         print(f"Error en la consulta {table}: {e}") 
    #         return False

    def obtener_estudiantes_pnf(self, pnf_id, trayecto_actual, tramo_actual):
        """
        Obtiene información detallada de estudiantes inscritos en un PNF, trayecto y tramo específicos.
        Los resultados se devuelven como una lista de diccionarios.
        """
        instruccion = '''
        SELECT
            epnf.id, epnf.estudiante_id, epnf.pnf_id, epnf.sede_id, epnf.fecha_inicio,
            epnf.fecha_fin, epnf.cohorte, epnf.turno, epnf.trayecto_actual,
            epnf.tramo_actual, epnf.creditos_aprobados, epnf.promedio_general,
            epnf.estado,
            est.codigo_unico, est.codigo_estudiantil, est.tipo_ingreso,
            est.fecha_ingreso, est.situacion_academica,
            ip.documento_identidad, ip.nombres, ip.apellidos, ip.fecha_nacimiento,
            ip.correo_electronico, ip.correo_institucional, ip.sexo, ip.nacionalidad
        FROM
            estudiante_pnf AS epnf
        JOIN
            estudiantes AS est ON epnf.estudiante_id = est.id
        JOIN
            informacion_personal AS ip ON est.persona_id = ip.id
        WHERE
            epnf.pnf_id = ? AND epnf.trayecto_actual = ? AND epnf.tramo_actual = ?;
        '''
        parametros = (pnf_id, trayecto_actual, tramo_actual)
        
        db_ruta = os.path.join('db', 'sistema_academico.db')
        con = sql.connect(db_ruta)
        cursor = con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        try:
            cursor.execute(instruccion, parametros)
            
            # Obtener los nombres de las columnas para usarlos como claves del diccionario
            column_names = [description[0] for description in cursor.description]
            
            resultados_diccionarios = []
            for fila in cursor.fetchall():
                resultados_diccionarios.append(dict(zip(column_names, fila)))
            
            return resultados_diccionarios
        except Exception as e:
            print(f"Error al obtener estudiantes con detalle: {e}")
            raise
        finally:
            con.close()

    def obtener_estudiantes_por_seccion(self, seccion_id):
        """
        Devuelve una lista de estudiantes inscritos en una sección específica.
        """
        instruccion = '''
        SELECT e.id, ip.documento_identidad, ip.nombres, ip.apellidos
        FROM inscripciones i
        JOIN estudiantes e ON i.estudiante_id = e.id
        JOIN informacion_personal ip ON e.persona_id = ip.id
        WHERE i.seccion_id = ?
        '''
        db_ruta = self.db_ruta
        con = sql.connect(db_ruta)
        con.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
        cursor = con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        try:
            cursor.execute(instruccion, (seccion_id,))
            resultados = cursor.fetchall()
            return resultados
        except Exception as e:
            print(f"Error al obtener estudiantes por sección: {e}")
            return []
        finally:
            con.close()
    
    def obtener_inscripcion_id(self, estudiante_id, seccion_id):
        instruccion = "SELECT id FROM inscripciones WHERE estudiante_id = ? AND seccion_id = ?"
        db_ruta = self.db_ruta
        con = sql.connect(db_ruta)
        cursor = con.cursor()
        try:
            cursor.execute(instruccion, (estudiante_id, seccion_id))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
        except Exception as e:
            print(f"Error al obtener inscripcion_id: {e}")
            return None
        finally:
            con.close()
            
    def obtener_id_por_nro_doc(self,nro_doc):
        con = None
        
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute("SELECT id FROM informacion_personal WHERE documento_identidad = ?",(nro_doc,))
            resultado = cursor.fetchone()
            con.close()
            return resultado[0]
           
            
        except Exception as e:
            print(f"Error al obtener el id: {e}") 
            return False
        finally:
            if con is not None:
                con.close()
    

