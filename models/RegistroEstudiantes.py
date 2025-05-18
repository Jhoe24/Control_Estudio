import sqlite3 as sql
import os

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
    