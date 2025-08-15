import sqlite3 as sql
import os
import hashlib

class LoginUserModel:
    
    def __init__(self):
        self.db_ruta = os.path.join('db', 'sistema_academico.db')
    
    def login_user(self, user, password):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute(
                """
                SELECT password_hash FROM usuarios WHERE nombre_usuario = ?
                """,
                (user,)
            )
            result = cursor.fetchone()

            if result:
                password_db = result[0]

                password_hash = hashlib.sha256(password.encode()).hexdigest()
                
                if password_db == password_hash:
                    return True
                else:
                    return False
            else:
                    return False
        except Exception as e:

            print(f"Error al iniciar seccion: {e}") 
            return False
        
        finally:
            if con is not None:
                con.close()

    
    def register_user(self, user_name, password):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute(
                """
                INSERT INTO usuarios (nombre_usuario, password_hash) VALUES (?, ?)
                """,
                (user_name, password_hash)
            )
            con.commit()
            return True
        except Exception as e:
            print(f"Error al registrar usuario: {e}")
            return False
        finally:
            if con is not None:
                con.close()

    def person_exists(self, docement):
        con =  None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute(
                """
                SELECT * FROM informacion_personal WHERE documento_identidad = ?
                """,
                (docement,)
            )
            result = cursor.fetchone()
            if result:
                return True
            else:
                return False
        except Exception as e:
            print(f"Error al verificar si la persona existe: {e}")
            return False
        finally:
            if con is not None:
                con.close()
        
    def register_person(self, dic_dates):
        con = None 
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute(
                """
                INSERT INTO informacion_personal (documento_identidad, tipo_documento, nombre, apellido, 
                fecha_nacimiento, sexo, estado_civil, nacionalidad, lugar_nacimiento, correo_electronico, 
                fecha_registro, tipo, estado)
                VALUES  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    dic_dates['documento_identidad'],
                    dic_dates['tipo_documento'],
                    dic_dates['nombre'],
                    dic_dates['apellido'],
                    dic_dates['fecha_nacimiento'],
                    dic_dates['sexo'],
                    dic_dates['estado_civil'],
                    dic_dates['nacionalidad'],
                    dic_dates['lugar_nacimiento'],
                    dic_dates['correo_electronico'],
                    dic_dates['fecha_registro'],
                    dic_dates['genero'],
                    dic_dates['tipo'],
                    dic_dates['estado']
                )
            )

            persona_id = cursor.lastrowid

            telefonos = dic_dates.get('lista_telefonos', [])

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


            cursor.execute('''
                            INSERT INTO direcciones
                            (persona_id, estado, municipio, parroquia, sector, calle, casa_edificio, direccion_completa, tipo_direccion, principal)
                            VALUES (?,?,?,?,?,?,?,?,?,?)
                           ''',(
                               persona_id,
                               dic_dates['estado'],
                               dic_dates['municipio'],
                               dic_dates['parroquia'],
                               dic_dates['sector'],
                               dic_dates['calle'],
                               dic_dates['casa_apart'],
                               f"{dic_dates['estado']}, {dic_dates['municipio']}, {dic_dates['parroquia']},{dic_dates['sector']},{dic_dates['calle']},{dic_dates['casa_apart']}",
                               dic_dates['tipo_direccion'],
                               1 #True
                           ))
            con.commit()
            return True
        

        except Exception as e:                      
            print(f"Error al registrar persona: {e}")
            return False
        finally:
            if con is not None:
                con.close()
