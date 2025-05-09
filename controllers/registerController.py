# controladores/register_controlador.py
from models.modelUsuario import ModeloUsuario

class ControladorRegistroUsuario:
    def __init__(self):
        self.modelo = ModeloUsuario()
        pass

    def registrarUsuario(self, nombre_usuario, cedula, contraseña, pregunta_1, pregunta_2, pregunta_3):
        if self.modelo.registrarUsuario(nombre_usuario, cedula, contraseña, pregunta_1, pregunta_2, pregunta_3):
            return True
        else:
            return False
    
    def verificarUsuario(self, usuario):
        if self.modelo.validar_usuario(usuario):
            return True
        else:
            return False
