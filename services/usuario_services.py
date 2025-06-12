class UsuarioService:
    def __init__(self, usuario_repository):
        self.usuario_repository = usuario_repository
    
    def authenticate(self, username, password):
        """Autentica un usuario con las credenciales proporcionadas."""
        return self.usuario_repository.authenticate(username, password)

    def get_usuario(self, id):
        return self.usuario_repository.get_usuario(id)

    def create_usuario(self, usuario):
        return self.usuario_repository.create_usuario(usuario)

    def update_usuario(self, id, usuario):
        return self.usuario_repository.update_usuario(id, usuario)

    def delete_usuario(self, id):
        return self.usuario_repository.delete_usuario(id)

    def Usuario(self, username, password, role):
        """Crea un nuevo usuario con las credenciales y rol especificados."""
        return self.usuario_repository.create_usuario({
            'username': username,
            'password': password,
            'role': role
        })