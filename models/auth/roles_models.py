import sqlite3 as sql
import os
import hashlib

class RolUserModel:
    
    def __init__(self):
        self.db_ruta = os.path.join('db', 'sistema_academico.db')
    
    def obtener_rol(self,user_id):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            # Obtener el rol_id por el usuario_id
            cursor.execute(
                """
                SELECT rol_id FROM usuarios_roles WHERE usuario_id = ?
                """,
                (user_id,)
            )
            result = cursor.fetchone()

            if result:
                # Obtener el codigo del rol por el rol_id
                cursor.execute( 
                """
                SELECT codigo FROM roles WHERE id = ? 
                """,
                (result[0],))

                rol = cursor.fetchone()

                if rol:
                    return rol[0]
                else:
                    return None
            else:
                return None
            
        except Exception as e:

            print(f"Error al obtener rol: {e}") 
            return False
        
        finally:
            if con is not None:
                con.close()

    
    def asignar_rol(self, user_id, rol_id):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute(
                """
                INSERT INTO usuarios_roles (usuario_id, rol_id) VALUES (?, ?)
                """,
                (user_id, rol_id)
            )
            con.commit()
            return True
        except Exception as e:
            print(f"Error al asignar rol: {e}")
            return False
        finally:
            if con is not None:
                con.close()
    
    def cambiar_rol(self, user_id, nuevo_rol_id):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute(
                """
                UPDATE usuarios_roles SET rol_id = ? WHERE usuario_id = ?
                """,
                (nuevo_rol_id, user_id)
            )
            con.commit()
            return True
        except Exception as e:
            print(f"Error al cambiar rol: {e}")
            return False
        finally:
            if con is not None:
                con.close()
    
    def obtener_roles(self):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute(
                """
                SELECT id, codigo FROM roles
                """)
            result = cursor.fetchall()
            #obtener una lista de los codigo de los roles
            result = [rol[1] for rol in result]
            return result if result else []
        except Exception as e:
            print(f"Error al obtener roles: {e}")
            return []  
        finally:
            if con is not None:
                con.close()

    def obtener_id_por_codigo(self, codigo):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute(
                """
                SELECT id FROM roles WHERE codigo = ?
                """,
                (codigo,)
            )
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except Exception as e:
            print(f"Error al obtener id por codigo: {e}")
            return None
        finally:
            if con is not None:
                con.close()


    def listar_registros(self):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            cursor.execute(
                """
                SELECT * FROM usuarios_roles
                """)
            result = cursor.fetchall()
            return result if result else []
        except Exception as e:
            print(f"Error al listar registros: {e}")
            return []  
        finally:
            if con is not None:
                con.close()

# bd = RolUserModel()
# print(bd.listar_registros())