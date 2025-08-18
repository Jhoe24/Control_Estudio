from models.auth.user_models import UserModel
from models.auth.roles_models import RolUserModel

class UserController:
    def __init__(self):
        self.user_model = UserModel()
        self.rol_model = RolUserModel()

    def obtener_rol(self, user_id):
        return self.rol_model.obtener_rol(user_id)

    def obtener_tipo_user(self, id):
        return self.user_model.obtener_tipo_user(id)

    def obtener_lista_usuarios(self):
        return self.user_model.obtener_lista_usuarios()
    
    def obtener_usuario_por_id(self, id):
        usuarios = self.user_model.obtener_lista_usuarios()
        for usuario in usuarios:
            if usuario['id'] == id:
                return usuario
        return None

    def obtener_roles(self):
        return self.rol_model.obtener_roles()
    
    def register_rol(self, codigo, id_user):
        """Registra un rol para un usuario dado."""
        rol_id = self.rol_model.obtener_valor_especifico('id', 'codigo', codigo)
        if rol_id is not None:
            if self.rol_model.obtener_rol(id_user) is None:
                result = self.rol_model.asignar_rol(id_user, rol_id)
                if result:
                   # print(f"Error al asignar rol {codigo} a usuario con ID {id_user}.")
                    return False
                #print(f"Rol {codigo} asignado a usuario con ID {id_user}.")
                return True 
            else:
                result = self.rol_model.cambiar_rol(id_user, rol_id)
                if not result:
                    #print(f"Error al cambiar rol a {codigo} para usuario con ID {id_user}.")
                    return False
                print(f"Rol {codigo} cambiado a usuario con ID {id_user}.")
                return True

        return False

    