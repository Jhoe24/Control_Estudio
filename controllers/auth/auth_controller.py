from models.auth.login_models import LoginUserModel
from models.auth.roles_models import RolUserModel
from models.auth.user_models import UserModel
from datetime import datetime
class AuthController:
    def __init__(self):
        self.modelo = LoginUserModel()
        self.rol_model = RolUserModel()
        self.user_model = UserModel()

    def search_document(self,tip_doc,document):
        return self.modelo.search_document(tip_doc,document)
    
    def exists_personal(self, tip_doc, document):
        result = self.search_document(tip_doc, document)
        return result is not None
    
    def exists_user(self,tip_doc, document):
        result = self.search_document(tip_doc, document)
        if result:
            return self.modelo.exists_username(result[0])
        return False
    
    def exists_name_user(self, user_name):
        return self.modelo.exists_user(user_name)

    def login(self, user, password):
        return self.modelo.login_user(user, password)
    
    def obtener_rol(self, user_id):
        return self.rol_model.obtener_rol(user_id)

    def register_user(self,persona_id, username, password):
        user_id = self.modelo.register_user(username, password, persona_id)
        if user_id:
            if self.user_model.obtener_tipo_user(persona_id) == 'estudiante':
                self.rol_model.asignar_rol(user_id, 5)# Si es estudiante, asignar el rol de estudiante automaticamente 
            return user_id
        return False
    
    def register_person(self, person_data):
        return self.modelo.register_person(person_data, self.obtener_fecha_actual())

    def obtener_fecha_actual(self):
        return datetime.now().strftime("%Y-%m-%d")