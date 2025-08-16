import customtkinter as ctk
from views.auth.base_auth_visual import BaseAuthVisualView
from config.app_config import AppConfig

class LoginView(BaseAuthVisualView):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, controller, titulo="Iniciar Sesión", es_login=True, **kwargs)
        self.master = master
        self.controller = controller
        

    def crear_contenido_especifico(self):
        self.crear_titulo("Inicio de Sesión")
        self.entry_username = self.crear_campo(self.frame_contenido, "Usuario:")
        self.entry_password = self.crear_campo(self.frame_contenido, "Contraseña:", es_password=True)

        # Crear enlace para recuperar contraseña
        self.btn_olvide = self.crear_boton_texto(
            self.frame_contenido,
            '¿Has olvidado tu contraseña?',
            "Click Aqui",
            None
        )
        
        # Crea el label y lo empaca antes del botón, pero sin texto
        self.mensaje_label = ctk.CTkLabel(self.frame_contenido, text="", text_color="red")
        
        self.button_login = ctk.CTkButton(
            self.frame_contenido, text="Iniciar Sesión", command=self.login
        )
        self.button_login.pack(fill=ctk.X, padx=20, pady=10)
        
        
        # Crear enlace para registro
        self.registrarU = self.crear_boton_texto(
            self.frame_contenido,
            '¿No tienes cuenta?',
            "Registrate Aqui",
            self.controller["Mostrar_Ventanas"].mostrar_vista_registro_personal
        )
        
        # Crear enlace de ayuda
        self.btn_ayuda = self.crear_boton_texto(
            self.frame_contenido,
            '¿Necesitas Ayuda?',
            "Click Aqui",
            None
        )
        self.entry_username.bind("<Return>", lambda event: self.entry_password.focus())
        self.entry_password.bind("<Return>", lambda event: self.login())

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        if not username or not password:
            if not username:
                self.mensaje_label.configure(text="Usuario no puede estar vacío.", text_color="red")
            if not password:
                self.mensaje_label.configure(text="Contraseña no puede estar vacía.", text_color="red")
            
            self.mensaje_label.pack(before=self.button_login, fill=ctk.X, padx=20, pady=(0, 5))
        
        elif self.controller["LoginAuth"].login(username, password):
            # Si las credenciales son correctas, muestra un mensaje y procede al dashboard
            # self.mensaje_label.configure(text="Inicio de Sesión Exitoso!", text_color="green")
            # self.mensaje_label.pack_forget()
            # self.mensaje_label.pack(before=self.button_login, fill=ctk.X, padx=20, pady=(0, 5))
            #self.mostrar_mensaje("Éxito", "Inicio de Sesión Exitoso!", "info")
            self.controller['Mostrar_Ventanas'].mostrar_vista_dashboardd("Andy", "admin")
            
        else:
            
            # if username != "admin":
            #     self.mensaje_label.configure(text="Usuario Incorrecto.", text_color="red")
            #     self.mensaje_label.pack_forget()
            #     self.mensaje_label.pack(before=self.button_login, fill=ctk.X, padx=20, pady=(0, 5))  
            # elif password != "123":
            #     self.mensaje_label.configure(text="Contraseña Incorrecta.", text_color="red")
            #     self.mensaje_label.pack_forget()
            #     self.mensaje_label.pack(before=self.button_login, fill=ctk.X, padx=20, pady=(0, 5))
            
           # else:
                self.mensaje_label.configure(text="Credenciales Incorrectas.", text_color="red")
                self.mensaje_label.pack_forget()
                self.mensaje_label.pack(before=self.button_login, fill=ctk.X, padx=20, pady=(0, 5))


