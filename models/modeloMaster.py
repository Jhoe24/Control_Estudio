import sqlite3 as sql
from .modelo import Modelo
import bcrypt

class ModeloMaster(Modelo):
    
    def __init__(self):
        super().__init__()
    
    def insertarHistorial(self, funcion, posicion, palabra, fecha, hora, id_usuario):
        con = sql.connect("base_de_datos.db")
        cursor = con.cursor()
        instruccion = f"INSERT INTO historial (funcion, posicion, palabra, fecha, hora, id_usuario) VALUES (?, ?, ?, ?, ?, ?)"
        cursor.execute(instruccion, (funcion, posicion, palabra, fecha, hora, id_usuario,))
        con.commit()
        
    
    def obtenerHistorial(self, id_usuario):
        con = sql.connect("base_de_datos.db")
        cursor = con.cursor()
        instruccion = 'SELECT funcion, posicion, palabra, fecha, hora FROM historial WHERE id_usuario = ?'
        cursor.execute(instruccion, (id_usuario,))
        datos = cursor.fetchall()
        return datos

    def obtener_nombre_usuario(self, id_usuario):
        con = sql.connect("base_de_datos.db")
        cursor = con.cursor()
        
        instruccion = 'SELECT Usuario FROM usuario WHERE id_usuario = ?'
        cursor.execute(instruccion, (id_usuario,))
        
        resultado = cursor.fetchone()
        
        con.close()
        
        if resultado:
            return resultado[0]  
        else:
            return None 
    
    def agregar_imagen(self, id_usuario, destino):
        con = sql.connect("base_de_datos.db")
        cursor = con.cursor()
        
        # Insertar la nueva imagen en la base de datos
        instruccion = 'INSERT INTO imagen (destino, id_usuario) VALUES (?, ?)'
        cursor.execute(instruccion, (destino, id_usuario))
        con.commit()
        con.close()
    
    def obtener_destino_imagen(self, user_id):
        con = sql.connect("base_de_datos.db")
        cursor = con.cursor()
        
        # Obtener el destino de la imagen para el usuario
        instruccion = 'SELECT destino FROM imagen WHERE id_usuario = ?'
        cursor.execute(instruccion, (user_id,))
        resultado = cursor.fetchone()
        con.close()
        
        if resultado:
            return resultado[0]
        else:
            return None
    
    def actualizar_ruta_imagen(self, id_usuario, destino):
        con = sql.connect("base_de_datos.db")
        cursor = con.cursor()
        
        # Actualizar la ruta de la imagen en la base de datos
        instruccion = 'UPDATE imagen SET destino = ? WHERE id_usuario = ?'
        cursor.execute(instruccion, (destino, id_usuario))
        con.commit()
        con.close()
    
    def existe_imagen(self, user_id):
        con = sql.connect("base_de_datos.db")
        cursor = con.cursor()
        
        # Verificar si ya existe una imagen para el usuario
        instruccion = 'SELECT COUNT(*) FROM imagen WHERE id_usuario = ?'
        cursor.execute(instruccion, (user_id,))
        resultado = cursor.fetchone()[0]
        con.close()
        return resultado > 0
    
    
    def actualizar_Usuario(self, id_usuario, nuevo_usuario):
        con = sql.connect("base_de_datos.db")
        cursor = con.cursor()
        
        instruccion = '''UPDATE usuario SET Usuario = ? WHERE id_usuario = ?'''
        cursor.execute(instruccion, (nuevo_usuario, id_usuario))
        
        con.commit()
        
    def cambiar_clave(self, id_usuario, clave):
        con = sql.connect("base_de_datos.db")
        cursor = con.cursor()
        
        # Encriptar la nueva contraseña
        Contraseña_encriptada = bcrypt.hashpw(clave.encode(), bcrypt.gensalt())
        instruccion = '''UPDATE usuario SET Contraseña = ? WHERE id_usuario = ?'''
        
        cursor.execute(instruccion, (Contraseña_encriptada, id_usuario))
        
        con.commit()
        

    
    
    
    
    