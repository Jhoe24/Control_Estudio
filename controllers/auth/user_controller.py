from models.auth.user_models import UserModel
from models.auth.roles_models import RolUserModel
import tkinter.messagebox as messagebox
class UserController:
    def __init__(self):
        self.user_model = UserModel()
        self.rol_model = RolUserModel()
    
    def obtener_datos_completos_usuario(self, username):
        return self.user_model.obtener_datos_completos_usuario(username)
        
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
    
    def obtener_persona_id(self, user_name):
        return self.rol_model.obtener_valor_especifico('persona_id', 'nombre_usuario', user_name, table='usuarios')

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

    def obtener_datos_personales(self, id_persona):
        dict_persona = self.user_model.obtener_datos_personales(id_persona)
        dict_direccion = self.user_model.obtener_direccion(id_persona)
        dic_completo =  dict_persona | dict_direccion
        #print(dic_completo)
        return dic_completo
    
    def update_datos_personales(self, id_persona, datos, tabla):
        print(datos)
        if tabla == "datos_perosonales":
            if self.user_model.update_datos_personales(id_persona, datos):
                if self.user_model.update_telefonos(id_persona, datos['telefonos']):
                    return True
                else:
                    messagebox.showerror("Error", "Hubo un error al actualizar los teléfonos.")
            else:
                messagebox.showerror("Error", "Hubo un error al actualizar los datos personales.")
                return False
        else:
            if self.user_model.update_direccion(id_persona, datos['direccion']):
                return True
            else:
                messagebox.showerror("Error", "Hubo un error al actualizar la dirección.")
                return False

    def the_user_is_blocked(self, id_persona):
        return self.user_model.the_user_is_blocked(id_persona)
    
    def block_user(self, id_persona, block):
        return self.user_model.block_user(id_persona, block)


            


    