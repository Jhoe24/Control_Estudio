import customtkinter as ctk
from util.generic import Utilidades
from util.mensaje import CustomMessageBox

class VistaRegisterPreguntas(ctk.CTkFrame, Utilidades):
    def __init__(self, master, controlador, nuevo_usuario, nueva_cedula, nueva_contraseña):
        super().__init__(master)
        self.controlador = controlador
        self.master = master
        self.master.title("Registrar Preguntas de seguridad")
        self.master.iconbitmap("./src/logo.ico")
        self.configure(fg_color='#2e2e2e')
        self.pack(fill="both", expand=True, pady=30, padx= 10)
        self.centrar_ventana(self.master, 900, 600)
        
        self.usuario = nuevo_usuario
        self.cedula = nueva_cedula 
        self.clave = nueva_contraseña
        
        self.logoLogin = self.leer_imagen("./src/upt.jpg", (500, 600))
        self.icon3 = self.leer_imagen("./src/flecha_izquierda.png", (16, 16))
        self.icon2 = self.leer_imagen("./src/esconder.png", (16, 16))
        self.icon = self.leer_imagen("./src/ojo.png", (16, 16))
        
        
        frame_logo = ctk.CTkFrame(self, width=400)
        frame_logo.pack(side='left', expand=ctk.YES, fill=ctk.BOTH, padx=0, pady=0)
        
        label_logo = ctk.CTkLabel(frame_logo, text=None, image=self.logoLogin)
        label_logo.place(x=0, y=0, relwidth=1, relheight=1)
        
        FrameDerechaLogin = ctk.CTkFrame(self, width=400, fg_color='#2e2e2e')
        FrameDerechaLogin.pack(side="right", expand=ctk.YES, fill=ctk.BOTH, padx=0, pady=0)
    
        frame_form_cabecera = ctk.CTkFrame(FrameDerechaLogin, fg_color="transparent", width=400)
        frame_form_cabecera.pack(side="top", fill=ctk.X, pady=(40, 0))
        
        label_titulo = ctk.CTkLabel(frame_form_cabecera, text="Registrar preguntas de seguridad", font=('Times', 30), text_color="#fff")
        label_titulo.pack(expand=ctk.YES, fill=ctk.BOTH)
        
        frame_form_pie = ctk.CTkFrame(FrameDerechaLogin, fg_color="transparent")
        frame_form_pie.pack(side="bottom", expand=ctk.YES, fill=ctk.BOTH, pady=(20, 0))
        
        
        LoginEtiquetapregun1 = ctk.CTkLabel(frame_form_pie, text='¿Cuál es tu comida favorita?', font=('Times', 18), anchor='w', text_color="#fff")
        LoginEtiquetapregun1.pack(fill=ctk.X, padx=20, pady=0)
        
        frame_visible1 = ctk.CTkFrame(frame_form_pie, fg_color="transparent")
        frame_visible1.pack(fill=ctk.X, padx=20, pady=0)

        self.Loginpregun1 = ctk.CTkEntry(frame_visible1, font=('Times', 18), show="*", text_color="black", fg_color="#fff")
        self.Loginpregun1.pack(side="left", fill=ctk.X, expand=True)
        
        self.verOcultar = ctk.CTkButton(frame_visible1, text=None, image=self.icon2, width=30, height=30, hover=True, fg_color="#fff")
        self.verOcultar.pack(side="right", padx=0, pady=0)
        
        LoginEtiquetapregun2 = ctk.CTkLabel(frame_form_pie, text='¿En qué ciudad naciste?', font=('Times', 18), anchor='w', text_color="#fff")
        LoginEtiquetapregun2.pack(fill=ctk.X, padx=20, pady=0)
        
        frame_visible2 = ctk.CTkFrame(frame_form_pie, fg_color="transparent")
        frame_visible2.pack(fill=ctk.X, padx=20, pady=0)
        
        self.Loginpregun2 = ctk.CTkEntry(frame_visible2, font=('Times', 18), show="*", text_color="black", fg_color="#fff")
        self.Loginpregun2.pack(side="left", fill=ctk.X, expand=True)
        
        self.verOcultar2 = ctk.CTkButton(frame_visible2, text=None, image=self.icon2, width=30, height=30, hover=True, fg_color="#fff")
        self.verOcultar2.pack(side="right", padx=0, pady=0)
        
        
        LoginEtiquetapregun3 = ctk.CTkLabel(frame_form_pie, text='¿Cuál es tu película favorita?', font=('Times', 18), anchor='w', text_color="#fff")
        LoginEtiquetapregun3.pack(fill=ctk.X, padx=20, pady=0)
        
        frame_visible3 = ctk.CTkFrame(frame_form_pie, fg_color="transparent")
        frame_visible3.pack(fill=ctk.X, padx=20, pady=0)
        
        self.Loginpregun3 = ctk.CTkEntry(frame_visible3, font=('Times', 18), show="*", text_color="black", fg_color="#fff")
        self.Loginpregun3.pack(side="left", fill=ctk.X, expand=True)
        
        self.verOcultar3 = ctk.CTkButton(frame_visible3, text=None, image=self.icon2, width=30, height=30, hover=True, fg_color="#fff")
        self.verOcultar3.pack(side="right", padx=0, pady=0)
        
            
        self.siguiente = ctk.CTkButton(frame_form_pie, text="   Registrar   ", font=('Times', 18, "bold"), text_color="black", height=32, fg_color="#fff", command=self.registrarUsuario)
        self.siguiente.pack(padx=20, pady=(15, 10))
        
        self.volver = ctk.CTkButton(frame_form_pie, text="Volver   ", font=('Times', 18, "bold"), text_color="black", height=32,  image=self.icon3, compound="left", command=self.controlador.mostrar_vista_registro, fg_color="#fff")
        self.volver.pack(padx=20, pady=0)
        
        self.verOcultar.configure(command=lambda: self.mostrarclave('clave', self.Loginpregun1, self.verOcultar, self.icon, self.icon2))
        self.verOcultar2.configure(command=lambda: self.mostrarclave('confirmar', self.Loginpregun2, self.verOcultar2, self.icon, self.icon2))
        self.verOcultar3.configure(command=lambda: self.mostrarclave('confirmar', self.Loginpregun3, self.verOcultar3, self.icon, self.icon2))

    def registrarUsuario(self):
        pregunta1= self.Loginpregun1.get()
        pregunta2= self.Loginpregun2.get()
        pregunta3= self.Loginpregun3.get()
        
        if len(pregunta1) == 0 or len(pregunta2)== 0 or len(pregunta3)== 0:
            CustomMessageBox(self.master, "Mensaje", "   Error campos vacios  ", 'error')
        else:
            if self.controlador.registro_controlador.registrarUsuario(self.usuario, self.cedula, self.clave, pregunta1, pregunta2, pregunta3):
                CustomMessageBox(self.master, "Mensaje", "   Error al registrar el usuario  ", 'error')
            else:
                CustomMessageBox(self.master, "Mensaje", " Usuario registrado con exito  ", 'info')
                self.controlador.mostrar_vista_login()
            
        