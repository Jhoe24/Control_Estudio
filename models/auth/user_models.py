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
            #con.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
            cursor = con.cursor()
            cursor.execute(
                """
                SELECT * FROM informacion_personal WHERE id = ?
                """,(id_persona,))
            resultado = cursor.fetchone()
            if not resultado:
                con.close()
                return None  # No encontrado

            nombres_columnas = [desc[0] for desc in cursor.description]
            datos = dict(zip(nombres_columnas, resultado))
        
            cursor.execute('''
                SELECT tipo_telefono, numero, principal FROM telefonos
                WHERE persona_id = ?
            ''', (id_persona,))

            telefonos = cursor.fetchall()
            datos['telefonos'] = [(tipo_telefono, numero, principal) for tipo_telefono, numero, principal in telefonos]

            return datos if datos else {}
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
                SELECT tipo_telefono, numero, principal FROM telefonos WHERE persona_id = ?
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

    def update_datos_personales(self, id_persona, datos):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute(
                """
                UPDATE informacion_personal SET nombres = ?, apellidos = ?, correo_electronico = ?, sexo = ?, estado_civil = ?, nacionalidad = ?, lugar_nacimiento = ? WHERE id = ?
                """,(datos['nombres'], datos['apellidos'], datos['correo_electronico'], datos['sexo'], datos['estado_civil'], datos['nacionalidad'], datos['lugar_nacimiento'], id_persona))
            con.commit()    
            return True
        except Exception as e:
            print(f"Error al actualizar datos personales: {e}")
            return False
        finally:
            if con is not None:
                con.close()
    
    def update_telefonos(self, id_persona, telefonos):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute(
                """
                DELETE FROM telefonos WHERE persona_id = ?
                """,(id_persona,))
            con.commit()
            for tipo, numero in telefonos:
                cursor.execute( 
                """
                INSERT INTO telefonos (persona_id, tipo_telefono, numero) VALUES (?, ?, ?)
                """,(id_persona, tipo, numero))
            con.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar telefonos: {e}")
            return False
        finally:
            if con is not None:
                con.close() 

    def update_direccion(self, id_persona, direccion):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute(
                """
                DELETE FROM direcciones WHERE persona_id = ?
                """,(id_persona,))
            con.commit()
            cursor.execute("""
                INSERT INTO direcciones (persona_id, direccion) VALUES (?, ?)
                """,(id_persona, direccion))
            con.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar direccion: {e}")
            return False
        finally:
            if con is not None:
                con.close()
    
    def change_user_and_pass(self, id_persona, user, password):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            if password :
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                cursor.execute(
                    """
                    UPDATE usuarios SET nombre_usuario = ?, password_hash = ?  WHERE persona_id = ?
                    """,(user, password_hash, id_persona))
            else:
                cursor.execute(
                    """
                    UPDATE usuarios SET nombre_usuario = ?  WHERE persona_id = ?
                    """,(user, id_persona)) 
            con.commit()

            return True
        except Exception as e:
            print(f"Error al cambiar credenciales: {e}")
            return False
        finally:
            if con is not None:
                con.close()

    def the_user_is_blocked(self, id_user):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute(
                """
                    SELECT bloqueado FROM usuarios WHERE id = ?
                """,(id_user,)
                )
            result = cursor.fetchone()
            if result:
                return result[0] == 1
            return False
        except Exception as e:
            print(f"Error al verificar si el usuario esta bloqueado: {e}")
            return False
        finally:
            if con is not None:
                con.close()

    def block_user(self, id_user, block):
        con = None
        try:
            con = sql.connect(self.db_ruta)      
            cursor = con.cursor()
            #Verificar que ta exista un registro
            cursor.execute(
                """
                    SELECT id FROM usuarios WHERE id = ?
                """,(id_user,)
                )
            if cursor.fetchone():
                cursor.execute(
                    """
                        UPDATE usuarios SET bloqueado = ? WHERE id = ?
                    """,(block, id_user))
            else:
                cursor.execute(
                    """
                        INSERT INTO usuarios (id, bloqueado) VALUES (?, ?)
                    """,(id_user, block))
            con.commit()
            return True
        except Exception as e:
            print(f"Error al bloquear usuario: {e}")
        finally:
            if con is not None:
                con.close()

#print(UserModel().the_user_is_blocked(3))