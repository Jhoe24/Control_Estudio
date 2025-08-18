import sqlite3 as sql
import os
import hashlib
from pprint import pprint

class UserModel:
    
    def __init__(self):
        self.db_ruta = os.path.join('db', 'sistema_academico.db')
    
    def obtener_tipo_user(self,id):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute(
                """
                SELECT tipo FROM informacion_personal WHERE id = ?
                """,
                (id,)
            )
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except Exception as e:
            print(f"Error al obtener tipo de usuario: {e}")
            return None
        finally:
            if con is not None:
                con.close()

    def obtener_lista_usuarios(self):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            con.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
            cursor = con.cursor()
            cursor.execute(
                """
                SELECT ip.documento_identidad, ip.nombres, ip.apellidos,u.id, u.nombre_usuario
                from informacion_personal ip
                JOIN usuarios u ON ip.id = u.persona_id

                ORDER BY ip.nombres, ip.apellidos
                """)
            #nelson pilla eso
            result = cursor.fetchall()
            return result if result else []
        except Exception as e:
            print(f"Error al obtener lista de usuarios: {e}")
            return []  
        finally:
            if con is not None:
                con.close() 

    def cambiar_user_admin(self):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            password_hash = hashlib.sha256("123".encode()).hexdigest()
            user_name = "admin"
            cursor.execute(
                
                """
                UPDATE usuarios SET nombre_usuario = ?, password_hash = ?  WHERE id = ?
                """,(user_name, password_hash, 1))
            con.commit()
            print("Usuario cambiado a administrador exitosamente.")
        except Exception as e:
            print(f"Error al cambiar usuario a administrador: {e}")
        finally:
            if con is not None:
                con.close()
    
    def obtener_datos_personales(self, id_persona):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            con.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
            cursor = con.cursor()
            cursor.execute(
                """
                SELECT * FROM informacion_personal WHERE id = ?
                """,(id_persona,))
            result = cursor.fetchone()
            return result if result else {}
        except Exception as e:
            print(f"Error al obtener datos personales: {e}")
            return {}
        finally:
            if con is not None:
                con.close()

    def obtener_telefono(self, id_persona):
        con = None
        try:
            con = sql.connect(self.db_ruta)
           
            cursor = con.cursor()
            cursor.execute(
                """
                SELECT tipo_telefono, numero FROM telefonos WHERE persona_id = ?
                """,(id_persona,))
            result = cursor.fetchall()
            return result if result else []
        except Exception as e:
            print(f"Error al obtener telefono: {e}")
            return {}
        finally:
            if con is not None:
                con.close()

    def obtener_direccion(self, id_persona):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            con.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
            cursor = con.cursor()
            cursor.execute(
                """
                SELECT * FROM direcciones WHERE persona_id = ?
                """,(id_persona,))
            result = cursor.fetchone()
            return result if result else {}
        except Exception as e:
            print(f"Error al obtener direccion: {e}")
            return ""
        finally:
            if con is not None:
                con.close()

n = UserModel()
