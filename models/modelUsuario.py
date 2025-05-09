import sqlite3 as sql
from .modelo import Modelo
import bcrypt

# declaramos mi modelo de registrar usuario y hacemos que herede del modelo principal
class ModeloUsuario(Modelo):
    
    def __init__(self):
        super().__init__()
    
    def registrarUsuario(self, Usuario, Cedula, Contraseña, pregunta_1, pregunta_2, pregunta_3):
        # Establece una conexión con la base de datos
        con = sql.connect("base_de_datos.db")
        cursor = con.cursor()
        # Encriptar la contraseña 
        Contraseña_encriptada = bcrypt.hashpw(Contraseña.encode(), bcrypt.gensalt())
        # Inserta los datos en la tabla preguntas
        instruccion_1 =f"INSERT INTO preguntas (pregunta_1, pregunta_2, pregunta_3) VALUES(?, ?, ?)"
        cursor.execute(instruccion_1, (pregunta_1, pregunta_2, pregunta_3))
        #obtiene el ultimo id generado de la tabla preguntas
        id_pregunta = cursor.lastrowid
        
        instruccion_2 = f"INSERT INTO usuario (usuario, cedula, Contraseña, id_pregunta) VALUES(?, ?, ?, ?)"
        cursor.execute(instruccion_2, (Usuario, Cedula, Contraseña_encriptada, id_pregunta))
        con.commit()
        con.close()
    
    def validar_usuario(self, usuario):
        con = sql.connect("base_de_datos.db")
        cursor = con.cursor()
        # la función COUNT(*) cuenta el número de filas en la tabla usuario donde el valor de la 
        # columna usuario es igual al valor del primer parámetro de la consulta.
        instruccion = 'SELECT COUNT (*) FROM usuario WHERE usuario = ?'
        cursor.execute(instruccion, (usuario,))
        resultado = cursor.fetchone() [0] > 0
        return resultado

    def validar_cedula(self, cedula):
        con = sql.connect("base_de_datos.db")
        cursor = con.cursor()
        # la función COUNT(*) cuenta el número de filas en la tabla usuario donde el valor de la 
        # columna usuario es igual al valor del primer parámetro de la consulta.
        instruccion = 'SELECT COUNT (*) FROM usuario WHERE cedula = ?'
        cursor.execute(instruccion, (cedula,))
        resultado = cursor.fetchone() [0] > 0
        return resultado

    def verificarUsuario(self, usuario, contraseña):
        # Establece una conexión con la base de datos
        con = sql.connect("base_de_datos.db")
        cursor = con.cursor()
        # Selecciona la fila con el nombre de usuario dado
        instruccion = 'SELECT Usuario, Contraseña FROM usuario WHERE Usuario = ?'
        cursor.execute(instruccion, (usuario,))
        resultado = cursor.fetchone()
        # Si la fila existe, verifica si la contraseña coincide
        if resultado:
            hashed_password = resultado[1]
            
            if bcrypt.checkpw(contraseña.encode('utf-8'), hashed_password):
                return True
        # Si la fila no existe o la contraseña no coincide, devuelve False
        return False

    def verificarDatos(self, usuario, pregunta_1, pregunta_2, pregunta_3):
        con = sql.connect('base_de_datos.db')
        cursor = con.cursor()
        #selecciona todas las columnas de las tablas: usuario y preguntas, utiliza la cláusula 
        # INNER JOIN para combinar las filas de ambas tablas en función de una condición de unión. 
        # también incluye una cláusula WHERE que filtra las filas resultantes según una serie de condiciones
        instruccion ="""
            SELECT * FROM usuario 
            INNER JOIN preguntas ON usuario.id_pregunta = preguntas.id_pregunta 
            WHERE usuario.usuario  = ? AND preguntas.pregunta_1 = ? AND preguntas.pregunta_2 = ? AND preguntas.pregunta_3 = ?
        """
        cursor.execute(instruccion, (usuario, pregunta_1, pregunta_2, pregunta_3))
        # Obtener todas las filas devueltas por la consulta
        rows = cursor.fetchall()
        con.close()
        # Si la consulta devuelve al menos una fila, entonces los datos concuerdan
        return len(rows) > 0

    def ActualizarClave(self, usuario, clave):
        con = sql.connect("base_de_datos.db")
        cursor = con.cursor()
        
        # Encriptar la nueva contraseña
        clave_encriptada = bcrypt.hashpw(clave.encode(), bcrypt.gensalt())
        
        # Actualizar la contraseña del usuario en la base de datos
        instruccion = "UPDATE usuario SET Contraseña = ? WHERE usuario = ?"
        cursor.execute(instruccion, (clave_encriptada, usuario))
        
        con.commit()
        con.close()

    def obtener_idUsuario(self, nombre_usuario):
        con = sql.connect("base_de_datos.db")
        cursor = con.cursor()
        
        instruccion = 'SELECT id_usuario FROM usuario WHERE Usuario = ?'
        cursor.execute(instruccion, (nombre_usuario,))
        
        resultado = cursor.fetchone()
        con.close()
        if resultado:
            return resultado[0]  
        else:
            return None 

