from models.modelUsuario import ModeloUsuario


class ControladorOlvideClave:
    
    def __init__(self):
        self.modelo =  ModeloUsuario()
    
    def recuperarClave(self, usuario, preg1, preg2, preg3):
        if self.modelo.verificarDatos(usuario, preg1, preg2, preg3):
            return True
        else:
            return False
    
    def verificarUsuario(self, usuario):
        if self.modelo.validar_usuario(usuario):
            return True
        else:
            return False
        
    def verificarCedula(self, cedula):
        if self.modelo.validar_cedula(cedula):
            return True
        else:
            return False
    
    def cambioClave(self, usuario, clave):
        self.modelo.ActualizarClave(usuario, clave)
            