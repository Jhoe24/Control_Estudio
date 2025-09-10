import sqlite3 as sql
import os
from pprint import pprint

class ModeloDocente:
    
    def __init__(self):
        self.db_ruta = os.path.join('db', 'sistema_academico.db')
    
    def registrar_docente(self, datos_docentes):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            
            # insertar datos en la tabla de informacion_personal
            cursor.execute(''' INSERT INTO informacion_personal
                           (documento_identidad, tipo_documento, nombres, apellidos, fecha_nacimiento, sexo, estado_civil, nacionalidad, lugar_nacimiento, correo_electronico, tipo)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                           ''',(
                               datos_docentes['nro_documento'],
                               datos_docentes['tipo_documento'],
                               datos_docentes['nombre'],
                               datos_docentes['apellido'],
                               datos_docentes['f_nacimiento'],
                               datos_docentes['genero'],
                               datos_docentes['edo_civil'],
                               datos_docentes['nacionalidad'],
                               datos_docentes['lugar_nacimiento'],
                               datos_docentes['correo_electronico'],
                               'docente'
                           ))
            persona_id = cursor.lastrowid
            
            # Insertar datos en la tabla estudiante
            
            cursor.execute('''
                           INSERT INTO docentes
                           (persona_id, abreviatura_titulo, especialidad, fecha_ingreso,fecha_ingreso_uptrjf ,tipo_contrato, categoria, auxiliar, dedicacion, estado)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                           ''', (
                            persona_id,
                            datos_docentes.get('abreviatura_titulo', ''),
                            datos_docentes.get('especialidad', ''),
                            datos_docentes.get('fecha_ingreso', ''),
                            datos_docentes.get('fecha_ingreso_uptrjf'),
                            datos_docentes.get('tipo_contrato', ''),
                            datos_docentes.get('categoria', ''),
                            datos_docentes.get('auxiliar', ''),
                            datos_docentes.get('dedicacion', ''),
                            datos_docentes.get('estado_doc', '')
                           ))
            
            # Insertar datos en la tabla telefonos

            telefonos = datos_docentes.get('lista_telefonos', [])

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
            #                     datos_docentes['tipo_telefono_p'],
            #                     datos_docentes['telefono_principal'],
            #                     1 # true
            #                 ))
            

            # cursor.execute('''
            #                 INSERT INTO telefonos
            #                 (persona_id, tipo_telefono, numero, principal)
            #                 VALUES (?,?,?,?)
            #                 ''',(
            #                     persona_id,
            #                     datos_docentes['tipo_telefono_s'],
            #                     datos_docentes['telefono_secundario'],
            #                     0 # false
            #                 ))
            
            # Insertar datos en la tabla de direcciones

            cursor.execute('''
                            INSERT INTO direcciones
                            (persona_id, estado, municipio, parroquia, sector, calle, casa_edificio, direccion_completa, tipo_direccion, principal)
                            VALUES (?,?,?,?,?,?,?,?,?,?)
                           ''',(
                               persona_id,
                               datos_docentes['estado'],
                               datos_docentes['municipio'],
                               datos_docentes['parroquia'],
                               datos_docentes['sector'],
                               datos_docentes['calle'],
                               datos_docentes['casa_apart'],
                               f"{datos_docentes['estado']}, {datos_docentes['municipio']}, {datos_docentes['parroquia']},{datos_docentes['sector']},{datos_docentes['calle']},{datos_docentes['casa_apart']}",
                               datos_docentes['tipo_direccion'],
                               1 #True
                           ))

            con.commit()
            if con is not None:
                con.close()
            return True   

        except Exception as e:
             print(f"Error al registrar docente: {e}") 
        finally:
            if con is not None:
                con.close()
    
    def lista_Docentes(self, registro_inicio = 0, pnf_id = None):
        
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()

            #Estraer los datos de informacion personal
            # cursor.execute('''
            #                 SELECT * FROM informacion 
            #                 WHERE tipo = 'estudiante'
            #                 LIMIT 10
            #                 OFFSET {registro_inicio}
            #                ''')


            #Extraer de la tabla informacion personal y esrudiantes
            if pnf_id:
                cursor.execute('''
                               SELECT ip.*, e.id as docente_id, e.persona_id, e.abreviatura_titulo, e.especialidad, e.fecha_ingreso, e.fecha_ingreso_uptrjf, e.tipo_contrato, e.categoria, e.auxiliar, e.dedicacion, e.estado as estado_docente
                               FROM informacion_personal ip
                               JOIN docentes e ON ip.id = e.persona_id
                               JOIN docente_sede_pnf dsp ON e.id = dsp.docente_id
                               WHERE ip.tipo='docente' AND dsp.pnf_id = ?
                               LIMIT 13
                               OFFSET ?
                               ''', (pnf_id, registro_inicio))
            else:   
                cursor.execute('''
                            SELECT ip.*, e.*
                            FROM informacion_personal ip
                            JOIN docentes e ON ip.id = e.persona_id
                            WHERE ip.tipo='docente'
                            LIMIT 13
                            OFFSET ?
                            ''',(registro_inicio,))
            resultados = cursor.fetchall()
                        
            nombres_columnas = [descripcion[0] for descripcion in cursor.description]
            
            # Telefonos
            
            # cursor.execute('''
            #                 SELECT persona_id, tipo_telefono, numero, principal
            #                 FROM telefonos
            #                 ''')
            # telefonos = cursor.fetchall()
            
            # telefonos_dict = {}
            # for persona_id, tipo_telefono, numero, principal in telefonos:
            #     if persona_id not in telefonos_dict:
            #         telefonos_dict[persona_id] = {}
            #     if principal == 1:
            #         telefonos_dict[persona_id]['telefono_principal'] = numero
            #         telefonos_dict[persona_id]['tipo_telefono_p'] = tipo_telefono
            #     else:
            #         telefonos_dict[persona_id]['telefono_secundario'] = numero
            #         telefonos_dict[persona_id]['tipo_telefono_s'] = tipo_telefono

            # Después de obtener los teléfonos:
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
                
                persona_id = estudiante['persona_id']

                tel_info = telefonos_dict.get(persona_id, {})
                # estudiante['telefono_principal'] = tel_info.get('telefono_principal', '')
                # estudiante['tipo_telefono_p'] = tel_info.get('tipo_telefono_p', '')
                # estudiante['telefono_secundario'] = tel_info.get('telefono_secundario', '')
                # estudiante['tipo_telefono_s'] = tel_info.get('tipo_telefono_s', '')
                # Agrega todos los teléfonos como array de tuplas según el id_persona
                estudiante['telefonos'] = [
                    (tipo_telefono, numero, principal)
                    for tipo_telefono, numero, principal in [
                        (t[0], t[1], t[2]) for t in tel_info.get('todos', [])
                    ]
                ]
                
                direccion_info = direcciones_dict.get(persona_id, {})
                estudiante['estado_direccion'] = direccion_info.get('estado', '')
                estudiante['municipio'] = direccion_info.get('municipio', '')
                estudiante['parroquia'] = direccion_info.get('parroquia', '')
                estudiante['sector'] = direccion_info.get('sector', '')
                estudiante['calle'] = direccion_info.get('calle', '')
                estudiante['casa_apart'] = direccion_info.get('casa_edificio', '') # Aquí estaba el error
                estudiante['tipo_direccion'] = direccion_info.get('tipo_direccion', '')
                    
                
                informacion_estudiantes.append(estudiante)
           # return tel_info
            return informacion_estudiantes
            
           
        except Exception as e:
            print(f"Error al realizar la consulta: {e}") 
            return False
       
    def obtener_nombres_docentes(self, id_pnf=None):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute("""
                           SELECT ip.nombres, ip.apellidos, d.id
                           FROM informacion_personal ip
                           JOIN docentes d ON ip.id= d.persona_id
                           JOIN docente_sede_pnf dsp ON d.id = dsp.docente_id
                           WHERE ip.tipo='docente' AND dsp.pnf_id = ?
                           ORDER BY ip.nombres, ip.apellidos                        
                            """,(id_pnf,))
            return [{
                'nombres': row[0],
                'apellidos': row[1],
                'id': row[2]
            } for row in cursor.fetchall()]
        
        except Exception as e:
            print(f"Error al obtener los nombres de los docentes: {e}") 
            return []
        finally:
            if con is not None:
                con.close()


    
    def buscar_estudiante(self, tipo_documento, nro_documento, id_pnf=None):
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()

            # Buscar estudiante
            if id_pnf:
                cursor.execute('''
                    SELECT ip.*, e.id as docente_id, e.persona_id, e.abreviatura_titulo, e.especialidad, e.fecha_ingreso, e.fecha_ingreso_uptrjf, e.tipo_contrato, e.categoria, e.auxiliar, e.dedicacion, e.estado as estado_docente, dsp.pnf_id
                    FROM informacion_personal ip
                    JOIN docentes e ON ip.id= e.persona_id
                    JOIN docente_sede_pnf dsp ON e.id = dsp.docente_id
                    WHERE ip.tipo='docente' AND ip.tipo_documento = ? AND ip.documento_identidad = ? AND dsp.pnf_id = ?
                    LIMIT 1
                ''', (tipo_documento, nro_documento, id_pnf))
            else:

                cursor.execute('''
                    SELECT ip.*, e.*
                    FROM informacion_personal ip
                    JOIN docentes e ON ip.id= e.persona_id
                    WHERE ip.tipo='docente' AND ip.tipo_documento = ? AND ip.documento_identidad = ?
                    LIMIT 1
                ''', (tipo_documento, nro_documento))

            resultado = cursor.fetchone()
            if not resultado:
                con.close()
                return None  # No encontrado

            nombres_columnas = [desc[0] for desc in cursor.description]
            docentes = dict(zip(nombres_columnas, resultado))
            persona_id = docentes['persona_id']

            # Telefonos del estudiante
            
            cursor.execute('''
                SELECT tipo_telefono, numero, principal FROM telefonos
                WHERE persona_id = ?
            ''', (persona_id,))
            telefonos = cursor.fetchall()
            docentes['telefonos'] = [(tipo_telefono, numero, principal) for tipo_telefono, numero, principal in telefonos]

            # Direccion del estudiante
            cursor.execute('''
                SELECT estado, municipio, parroquia, sector, calle, casa_edificio, tipo_direccion
                FROM direcciones
                WHERE persona_id = ? AND principal=1
                LIMIT 1
            ''', (persona_id,))
            dir_row = cursor.fetchone()

            if dir_row:
                docentes['estado_direccion'] = dir_row[0]
                docentes['municipio'] = dir_row[1]
                docentes['parroquia'] = dir_row[2]
                docentes['sector'] = dir_row[3]
                docentes['calle'] = dir_row[4]
                docentes['casa_apart'] = dir_row[5]
                docentes['tipo_direccion'] = dir_row[6]
            else:
                docentes['estado_direccion'] = ''
                docentes['municipio'] = ''
                docentes['parroquia'] = ''
                docentes['sector'] = ''
                docentes['calle'] = ''
                docentes['casa_apart'] = ''
                docentes['tipo_direccion'] = ''
                
            
            con.close()
            return docentes

        except Exception as e:
            print(f"Error al realizar la consulta: {e}")
            return False
        finally:
            con.close()

    def obtener_id_ultimo(self):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()

            cursor.execute('''
                            SELECT id FROM informacion_personal 
                            WHERE tipo = 'docente'
                            ORDER BY id DESC
                            LIMIT 1
                            ''')
            resultado = cursor.fetchone()
            if con is not None:
                con.close()
            if resultado:
                return resultado[0]
            else:
                return None
        
        except Exception as e:
            if con is not None:
                con.close()
            print(f"Error al realizar la ultima consulta: {e}") 
            return False

                
        
    def obtener_primer_id(self):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute('''
                            SELECT id FROM informacion_personal
                            WHERE tipo = 'docente'
                            ORDER BY id ASC
                            LIMIT 1;
                            ''')
            resultado = cursor.fetchall()
            if con is not None:
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
            
    def obtener_cantidad_docente(self):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute('''
                            SELECT COUNT(*) FROM informacion_personal
                            WHERE tipo = 'docente'
                            ''')
            resultado = cursor.fetchone()
            if con is not None:
                con.close()
            if resultado and resultado[0] is not None:
                return resultado[0]
            else:
                return 0
        except Exception as e:
            print(f"Error al realizar la consulta: {e}") 
            return 0
        finally:
            if con is not None:
                con.close()
        

    def update_docente(self, id, datos_docentes):
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
                               datos_docentes['nombre'],
                               datos_docentes['apellido'],
                               datos_docentes['f_nacimiento'],
                               datos_docentes['genero'],
                               datos_docentes['edo_civil'],
                               datos_docentes['nacionalidad'],
                               datos_docentes['lugar_nacimiento'],
                               datos_docentes['correo_electronico'],
                               id
                           ))

            # Actualizar datos en la tabla estudiantes
            print( datos_docentes['estado_doc'])
            cursor.execute('''
                           UPDATE docentes
                           SET abreviatura_titulo = ?, especialidad = ?, fecha_ingreso = ?, tipo_contrato = ?, categoria = ?, auxiliar = ?, dedicacion = ?, estado = ?
                           WHERE persona_id = ?
                           ''', (
                            datos_docentes['abreviatura_titulo'],
                            datos_docentes['especialidad'],
                            datos_docentes['fecha_ingreso_uptrjf'],
                            datos_docentes['tipo_contrato'],
                            datos_docentes['categoria'],
                            datos_docentes['auxiliar'],
                            datos_docentes['dedicacion'],
                            datos_docentes['estado_doc'],
                            id
                           ))
            
            # Actualizar telefonos
            # cursor.execute('''
            #                 UPDATE telefonos
            #                 SET tipo_telefono = ?, numero = ?
            #                 WHERE persona_id = ? AND principal=1
            #                 ''',(
            #                     datos_docentes['tipo_telefono_p'],
            #                     datos_docentes['telefono_principal'],
            #                     id
            #                 ))
            
            # cursor.execute('''
            #                 UPDATE telefonos
            #                 SET tipo_telefono = ?, numero = ?
            #                 WHERE persona_id = ? AND principal=0
            #                 ''',(
            #                     datos_docentes['tipo_telefono_s'],
            #                     datos_docentes['telefono_secundario'],
            #                     id
            #                 ))

            # Actualizar telefonos: eliminar los existentes y volver a insertar los nuevos
            cursor.execute('DELETE FROM telefonos WHERE persona_id = ?', (id,))
            telefonos = datos_docentes.get('lista_telefonos', [])
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

            
            # Actualizar direcciones
            cursor.execute('''
                           UPDATE direcciones
                           SET estado=?, municipio=?, parroquia=?, sector=?, calle=?, casa_edificio=?, direccion_completa=?, tipo_direccion=?
                            WHERE persona_id = ? AND principal=1
                            ''',(
                                 datos_docentes['estado'],
                                 datos_docentes['municipio'],
                                 datos_docentes['parroquia'],
                                 datos_docentes['sector'],
                                 datos_docentes['calle'],
                                 datos_docentes['casa_apart'],
                                 f"{datos_docentes['estado']}, {datos_docentes['municipio']}, {datos_docentes['parroquia']},{datos_docentes['sector']},{datos_docentes['calle']},{datos_docentes['casa_apart']}",
                                 datos_docentes['tipo_direccion'],
                                 id
                            ))
            con.commit()
            if con is not None:
                con.close()
            return True
        except Exception as e:
            print(f"Error al actualizar docente: {e}") 
            return False
        finally:
            if con is not None:
                con.close()

    def obtener_id_docente(self, persona_id):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()

            cursor.execute('''
                            SELECT id FROM docentes 
                            WHERE persona_id = ?
                            ''',(persona_id,))
            resultado = cursor.fetchone()
            if con is not None:
                con.close()
            if resultado:
                return resultado[0]
            else:
                return None
        
        except Exception as e:
            if con is not None:
                con.close()
            print(f"Error al realizar la consulta: {e}") 
            return False
    
    def obtener_pnf_id(self, docente_id):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()

            cursor.execute('''
                            SELECT pnf_id FROM docente_sede_pnf 
                            WHERE docente_id = ?
                            ''',(docente_id,))
            resultado = cursor.fetchone()
            if con is not None:
                con.close()
            if resultado:
                return resultado[0]
            else:
                return None
        
        except Exception as e:
            if con is not None:
                con.close()
            print(f"Error al realizar la consulta: {e}") 
            return False
        
    def contar_docentes_activos(self):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()

            cursor.execute('''
                            SELECT COUNT(*) FROM docentes 
                            WHERE estado = 'Activo'
                            ''')
            resultado = cursor.fetchone()
            if con is not None:
                con.close()
            if resultado and resultado[0] is not None:
                return resultado[0]
            else:
                return 0
        except Exception as e:
            print(f"Error al realizar la consulta: {e}") 
            return 0
        finally:
            if con is not None:
                con.close()
        
                           
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
        
              
