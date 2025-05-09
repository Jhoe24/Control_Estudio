# controladores/login_controlador.py
from models.modelUsuario import ModeloUsuario

class ControladorInicioSesion:
    def __init__(self):
        self.modelo = ModeloUsuario()

    def login(self, usuario, contraseña):
        if self.modelo.verificarUsuario(usuario, contraseña):
            return True
        else:
            return False
    
    def obtener_idUsuario(self, usuario):
        return self.modelo.obtener_idUsuario(usuario)
