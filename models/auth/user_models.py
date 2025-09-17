import sqlite3 as sql
import os
import hashlib
from pprint import pprint

class UserModel:
    
    def __init__(self):
        self.db_ruta = os.path.join('db', 'sistema_academico.db')

    def obtener_datos_completos_usuario(self,username):
        """
        Obtiene un diccionario con los datos completos de un usuario (personal, rol, etc.)
        a partir de su nombre de usuario.
        """
        con = None
        try:
            con = sql.connect(self.db_ruta)
            # Configurar para que devuelva diccionarios en lugar de tuplas
            con.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
            cursor = con.cursor()
            cursor.execute("""
                SELECT
                    u.id as user_id,
                    u.persona_id,
                    ip.nombres,
                    ip.apellidos,
                    ip.tipo,
                    d.id as docente_id,
                    e.id as estudiante_id
                FROM
                    usuarios u
                JOIN
                    informacion_personal ip ON u.persona_id = ip.id
                LEFT JOIN
                    docentes d ON ip.id = d.persona_id
                LEFT JOIN
                    estudiantes e ON ip.id = e.persona_id
                WHERE
                    u.nombre_usuario = ?
            """, (username,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener los datos completos del usuario: {e}")
            return None
        finally:
            if con:
                con.close()

    
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
                SELECT ip.documento_identidad, ip.nombres, ip.apellidos, u.id, u.persona_id, u.nombre_usuario
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
    
    def _update_telefonos_transaccional(self, cursor, id_persona, telefonos):
        """Método auxiliar para actualizar teléfonos dentro de una transacción existente."""
        try:
            cursor.execute("DELETE FROM telefonos WHERE persona_id = ?", (id_persona,))
            for tipo, numero in telefonos:
                cursor.execute( 
                    "INSERT INTO telefonos (persona_id, tipo_telefono, numero) VALUES (?, ?, ?)",
                    (id_persona, tipo, numero)
                )
            return True
        except Exception as e:
            print(f"Error en _update_telefonos_transaccional: {e}")
            raise # Propaga el error para que la transacción principal haga rollback

    def update_informacion_persona(self, id_persona, datos, tipo_actualizacion):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()

            if tipo_actualizacion == "datos_perosonales":
                # Corregido: faltaba fecha_nacimiento en la consulta original
                cursor.execute(
                    """
                    UPDATE informacion_personal 
                    SET nombres = ?, apellidos = ?, sexo = ?, estado_civil = ?, nacionalidad = ?, lugar_nacimiento = ?, fecha_nacimiento = ? 
                    WHERE id = ?
                    """,
                    (datos['nombres'], datos['apellidos'], datos['sexo'], datos['estado_civil'], 
                     datos['nacionalidad'], datos['lugar_nacimiento'], datos['fecha_nacimiento'], id_persona)
                )
            
            elif tipo_actualizacion == "contactos":
                if 'correo_electronico' in datos:
                    cursor.execute(
                        "UPDATE informacion_personal SET correo_electronico = ? WHERE id = ?",
                        (datos['correo_electronico'], id_persona)
                    )
                if 'telefonos' in datos:
                    self._update_telefonos_transaccional(cursor, id_persona, datos['telefonos'])

            elif tipo_actualizacion == "direccion":
                # Asumiendo que la tabla 'direcciones' tiene una FK a 'informacion_personal'
                # y que se quiere reemplazar la dirección principal.
                cursor.execute("DELETE FROM direcciones WHERE persona_id = ? AND principal = 1", (id_persona,))
                cursor.execute(
                    """
                    INSERT INTO direcciones (persona_id, estado, municipio, parroquia, sector, calle, casa_edificio, tipo_direccion, principal)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
                    """,
                    (id_persona, datos['estado'], datos['municipio'], datos['parroquia'], 
                     datos['sector'], datos['calle'], datos['nro_casa'])
                )

            con.commit()
            return True
        except Exception as e:
            if con:
                con.rollback()
            print(f"Error al actualizar '{tipo_actualizacion}' para la persona {id_persona}: {e}")
            return False
        finally:
            if con:
                con.close()

    # Los métodos antiguos pueden ser eliminados o marcados como obsoletos.
    # def update_datos_personales(self, id_persona, datos): ...
    # def update_contactos(self, id_persona, contactos): ...
    # def update_direccion(self, id_persona, direccion): ...
    
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

    def user_is_coord(self, docente_id):
        con = None
        try:
            con = sql.connect(self.db_ruta)
            cursor = con.cursor()
            # Verifica si el docente es coordinador en cualquier PNF
            cursor.execute(
                """
                    SELECT 1 FROM docente_sede_pnf 
                    WHERE docente_id = ? AND coordinador = 1 AND activo = 1
                """, (docente_id,)
            )
            result = cursor.fetchone()
            return result is not None
        except Exception as e:
            print(f"Error al verificar coordinador: {e}")
            return False
        finally:
            if con is not None:
                con.close()
