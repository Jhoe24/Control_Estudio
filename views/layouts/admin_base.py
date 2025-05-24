import customtkinter as ctk
from views.layouts.base import VistaBase
from tkinter import filedialog
import shutil, os



class AdminBase(VistaBase):
    """
    Base para vistas de administrador: barra superior, sidebar y cuerpo principal.
    Hereda VistaBase y monta automáticamente la barra y el menú lateral.
    """
    def __init__(self, master, controlador, id_usuario, titulo="Panel de Administración"):
        # conservar id_usuario antes de inicializar VistaBase
        self.id_usuario = id_usuario
        super().__init__(master, controlador, titulo=titulo, es_login=False)
        # Usuario cargado por VistaBase
        self.usuario = self.controlador.master_controlador.obtener_Usuario(self.id_usuario)
    def crear_estructura_base(self, es_login):
        # montar layout admin
        self.barra_superior = ctk.CTkFrame(self, fg_color="#000000", height=40)
        self.barra_superior.pack(side="top", fill="x")

        self.menu_lateral = ctk.CTkFrame(self, fg_color="#18244c", width=200)
        self.menu_lateral.pack(side="left", fill="y")

        self.cuerpo_principal = ctk.CTkFrame(self, fg_color="white")
        self.cuerpo_principal.pack(side="right", fill="both", expand=True)

        # inicializar barra y menú lateral con elementos fijos
        self._inicializar_barra_superior()
        self._inicializar_sidebar()

    def _inicializar_barra_superior(self):
        # imágenes
        icono_cnc = self.leer_imagen("./src/logo2.png", (32,32))
        icono_menu = self.leer_imagen("./src/menu.png", (32,32))

        # título
        ctk.CTkLabel(
            self.barra_superior,
            text="Control de Estudio",
            image=icono_cnc,
            compound="left",
            font=("Roboto",18),
            text_color="white"
        ).pack(side=ctk.LEFT, padx=10)
        # botón toggle
        ctk.CTkButton(
            self.barra_superior,
            text=None,
            image=icono_menu,
            width=32,
            fg_color="transparent",
            hover_color="white",
            command=self.toggle_panel
        ).pack(side=ctk.LEFT)
        # bienvenida
        self.labelUsuario = ctk.CTkLabel(
            self.barra_superior,
            text=f"Bienvenido, {self.id_usuario}",
            font=("Roboto",18),
            text_color="white"
        )
        self.labelUsuario.pack(side=ctk.RIGHT, padx=15)

    def _inicializar_sidebar(self):
        # avatar
        if self.controlador.master_controlador.existe_imagen(self.id_usuario):
            ruta = self.controlador.master_controlador.obtener_destino_imagen(self.id_usuario)
        else:
            ruta = "./src/Perfil.png"
        img_perfil = self.leer_imagen(ruta, (100,100))
        ctk.CTkLabel(self.menu_lateral, image=img_perfil, text=None).pack(pady=10)
        self.img_perfil = img_perfil

        # botones
        menu_items = [
            ("Inicio",       "home.png",          self.inicio),
            ("Estudiantes",  "historial.png",     self.estudiantes),
            ("Ayuda",        "info.png",          self._mostrar_ayuda),
            ("Configuración","config.png",       self.Configuracion),
            ("Cerrar Sesión","cerrar-sesion.png", self.controlador.mostrar_vista_login)
        ]


        for texto, archivo, comando in menu_items:
            if texto == "Estudiantes":
                menu_opciones = ['Registrar Estudiante', 'Listar Estudiantes']
                # Crear el menú desplegable
                menu = ctk.CTkOptionMenu(
                    self.menu_lateral,
                    values=menu_opciones,
                    anchor="w",
                    font=("Roboto",18),
                    #fg_color="white",
                    command=self.opcion_seleccionada,
                    dropdown_fg_color="#3556a3",
                    dropdown_text_color="white" 
                )
                menu.pack(fill="x")
                self.bind_hover_events(menu)
            else:
                icono = self.leer_imagen(f"./src/{archivo}", (32,32))
                btn = ctk.CTkButton(
                    self.menu_lateral,
                    text=texto,
                    image=icono,
                    anchor="w",
                    font=("Roboto",18),
                    fg_color="transparent",
                    command=comando
                )
                pady = 80 if texto == "Cerrar Sesión" else 0
                btn.pack(fill="x", pady=pady)
                self.bind_hover_events(btn)

    # MÉTODOS COMUNES
    def toggle_panel(self):
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
        else:
            self.menu_lateral.pack(side="left", fill="y")

    def bind_hover_events(self, button):
        button.bind("<Enter>", lambda e: button.configure(text_color='white', fg_color="#1f3979"))
        button.bind("<Leave>", lambda e: button.configure(text_color='white', fg_color="#18244c"))

    # Funciones a implementar por subclases para contenido
    def opcion_seleccionada(self, opcion):
        if opcion == "Registrar Estudiante":
            self.estudiantes()
        elif opcion == "Listar Estudiantes":
            self.list_estudiante()
        else:
            print(f"Opción seleccionada: {opcion}")


    def crear_contenido_especifico(self, opcion):
        pass
    def inicio(self):
        pass

    def estudiantes(self):
        pass

    def list_estudiante(self):
        pass

    def _mostrar_ayuda(self):
        pass

    def Configuracion(self):
        pass

