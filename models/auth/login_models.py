import sqlite3 as sql
import os
import hashlib

class ModeloDocente:
    
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
    
                    
                           
    