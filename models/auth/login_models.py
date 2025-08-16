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

    
    def register_user(self, user_name, password, persona_id):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute(
                """
                INSERT INTO usuarios (persona_id, nombre_usuario, password_hash) VALUES (?, ?, ?)
                """,
                (persona_id,user_name, password_hash)
            )
            con.commit()
            user_id = cursor.lastrowid
            return user_id
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

    def search_document(self, tip_document,document):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute(
                """
                SELECT * FROM informacion_personal WHERE tipo_documento = ? AND documento_identidad = ? 
                """,
                (tip_document,document,)
            )
            result = cursor.fetchone()
            return result
        except Exception as e:
            print(f"Error al buscar documento: {e}")
            return None
        finally:
            if con is not None:
                con.close()

    def exists_username(self, perosna_id):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute(
                """
                SELECT * FROM usuarios WHERE persona_id = ?
                """,
                (perosna_id,)
            )
            result = cursor.fetchone()
            if result:
                return True
            else:
                return False
        except Exception as e:
            print(f"Error al verificar si el usuario existe: {e}")
            return False
        finally:
            if con is not None:
                con.close()

    def register_person(self, dic_dates,fecha_registro):
        con = None 
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute(
                """
                INSERT INTO informacion_personal (documento_identidad, tipo_documento, nombres, apellidos, 
                fecha_nacimiento, sexo, estado_civil, nacionalidad, lugar_nacimiento, correo_electronico, 
                fecha_registro, tipo, estado)
                VALUES  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                    fecha_registro,
                    dic_dates['tipo'],
                    dic_dates['estado']
                )
            )

            persona_id = cursor.lastrowid
            con.commit()
            return persona_id
        except Exception as e:                      
            print(f"Error al registrar persona: {e}")
            return False
        finally:
            if con is not None:
                con.close()


    