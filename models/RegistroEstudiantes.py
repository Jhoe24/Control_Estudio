import sqlite3 as sql
import os
from pprint import pprint

class RegistroEstudiantes:
    
    def __init__(self):
        self.db_ruta = os.path.join('db', 'sistema_academico.db')
    
    def registrar_estudiante(self, datos_estudiantes):
        
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
            
            cursor.execute('''
                            INSERT INTO telefonos
                            (persona_id, tipo_telefono, numero, principal)
                            VALUES (?,?,?,?)
                            ''',(
                                persona_id,
                                datos_estudiantes['tipo_telefono_p'],
                                datos_estudiantes['telefono_principal'],
                                1 # true
                            ))
            

            cursor.execute('''
                            INSERT INTO telefonos
                            (persona_id, tipo_telefono, numero, principal)
                            VALUES (?,?,?,?)
                            ''',(
                                persona_id,
                                datos_estudiantes['tipo_telefono_s'],
                                datos_estudiantes['telefono_secundario'],
                                0 # false
                            ))
            
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
    
    def lista_Estudiantes(self, registro_inicio = 0):
        
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
            cursor.execute('''
                           SELECT ip.*, e.*
                           FROM informacion_personal ip
                           JOIN estudiantes e ON ip.id= e.persona_id
                           WHERE ip.tipo='estudiante'
                           LIMIT 3
                           OFFSET ?
                           ''',(registro_inicio,))
            resultados = cursor.fetchall()
                        
            nombres_columnas = [descripcion[0] for descripcion in cursor.description]
            
            # Telefonos
            
            cursor.execute('''
                           SELECT persona_id, GROUP_CONCAT(numero, ',') as numeros
                           FROM telefonos
                           GROUP BY persona_id''')
            
            telefonos = cursor.fetchall()
            
            telefonos_dict = {t[0]: t[1].split(',') for t in telefonos}
         
            # direcciones
            cursor.execute('''
                           SELECT persona_id, direccion_completa,tipo_direccion
                           FROM direcciones
                           ''')
            direcciones = cursor.fetchall()

            direcciones_dict = {
                                    d[0]: {
                                        "direccion_completa": d[1],
                                        "tipo_direccion": d[2]
                                    }
                                    for d in direcciones
                                }
            
            
            con.close()
            
            informacion_estudiantes = []
            
            for resultado in resultados:
                
                estudiante = dict(zip(nombres_columnas, resultado))
                
                persona_id = estudiante['id']
                
                estudiante['telefonos'] = telefonos_dict.get(persona_id, [])
                direccion_info = direcciones_dict.get(persona_id, {})
                estudiante['direccion_completa'] = direccion_info.get('direccion_completa', '')
                estudiante['tipo_direccion'] = direccion_info.get('tipo_direccion', '')
                
                
                informacion_estudiantes.append(estudiante)

            return informacion_estudiantes
            
           
        except Exception as e:
             print(f"Error al realizar la consulta: {e}") 
             return False
    
    def buscar_estudiante(self,tipo_documento, nro_documento):
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()

            # Buscar estudiante
            cursor.execute('''
                SELECT ip.*, e.*
                FROM informacion_personal ip
                JOIN estudiantes e ON ip.id= e.persona_id
                WHERE ip.tipo='estudiante' AND ip.tipo_documento = ? AND ip.documento_identidad = ?
                LIMIT 1
            ''', (tipo_documento, nro_documento))
            resultado = cursor.fetchone()
            nombres_columnas = [desc[0] for desc in cursor.description]

            if not resultado:
                con.close()
                return None

            estudiante = dict(zip(nombres_columnas, resultado))
            persona_id = estudiante['id']

            # Telefonos solo del estudiante
            cursor.execute('''
                SELECT numero FROM telefonos
                WHERE persona_id = ?
            ''', (persona_id,))
            telefonos = [t[0] for t in cursor.fetchall()]
            estudiante['telefonos'] = telefonos

            # Direccion solo del estudiante
            cursor.execute('''
                SELECT direccion_completa FROM direcciones
                WHERE persona_id = ?
                LIMIT 1
            ''', (persona_id,))
            dir_row = cursor.fetchone()
            estudiante['direccion_completa'] = dir_row[0] if dir_row else ''

            con.close()
            return estudiante

        except Exception as e:
            print(f"Error al realizar la consulta: {e}")
            return False

    def obtener_id_ultimo(self):
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
        
    def obtener_primer_id(self):
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
            
    def obtener_cantidad_estudiantes(self):
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
        

    def update_estudiante(self, id, datos_estudiantes):
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()

            # Actualizar datos en la tabla de informacion_personal
            cursor.execute('''
                           UPDATE informacion_personal
                           SET documento_identidad = ?, tipo_documento = ?, nombres = ?, apellidos = ?, fecha_nacimiento = ?, sexo = ?, estado_civil = ?, nacionalidad = ?, lugar_nacimiento = ?, correo_electronico = ?
                           WHERE id = ?
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
            cursor.execute('''
                            UPDATE telefonos
                            SET tipo_telefono = ?, numero = ?
                            WHERE persona_id = ? AND principal=1
                            ''',(
                                datos_estudiantes['tipo_telefono_p'],
                                datos_estudiantes['telefono_principal'],
                                id
                            ))
            
            cursor.execute('''
                            UPDATE telefonos
                            SET tipo_telefono = ?, numero = ?
                            WHERE persona_id = ? AND principal=0
                            ''',(
                                datos_estudiantes['tipo_telefono_s'],
                                datos_estudiantes['telefono_secundario'],
                                id
                            ))
            
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
        
              
