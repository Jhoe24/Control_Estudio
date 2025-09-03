import customtkinter as ctk
from views.base_view import BaseView
from config.settings import Settings


class BaseDashboardView(BaseView):
    
    def __init__(self, master, controller, username, user_role, **kwargs):
        super().__init__(master, controller, fg_color="#ffffff", **kwargs)
        self.master = master
        self.controller = controller
        
        self.username = username
        self.user_role = user_role
        
        self.update_idletasks()  # Asegúrate de que el frame esté renderizado
        
        self.topbar()
        self.sidebar()
        
        self.cuerpo_principal = ctk.CTkFrame(self, fg_color="white")
        self.cuerpo_principal.pack(side="right", fill="both", expand=True)


    def topbar(self):
        
        # Le pasamos solo la altura (40) para que la imagen se redimensione sin deformarse.
        cintillo = self.leer_imagen(Settings().rutas_imagenes.get("cintillo", "resources/images/cintillo.png"), 40)
        logo = self.leer_imagen(Settings().rutas_imagenes.get("logo2", "resources/images/logo2.png"), (32,32))
        icon_menu = self.leer_imagen(Settings().rutas_iconos.get("icono_menu", "resources/icons/menu.png"), (32,32))
        
        frameTopbar = ctk.CTkFrame(self)
        
        cintillo = ctk.CTkLabel(frameTopbar, text='', image=cintillo, fg_color="white")
        cintillo.pack(side="top", fill="x", expand=False)
        
        barra = ctk.CTkFrame(frameTopbar, fg_color="#000000", height=40)
        barra.pack(side="bottom", fill="x")
        
        # título
        if self.user_role.lower() in ["admin", "administrador"]:
            titulo = "Administrador"
        elif self.user_role.lower() == "coord_general":
            titulo = "Coordinador General"
        elif self.user_role.lower() == "coord_pnf":
            titulo = "Coordinador P.N.F"
        elif self.user_role.lower() == "docente":
            titulo = "Docente"
        elif self.user_role.lower() == "estudiante":
            titulo = "Estudiante"
        else:
            titulo = "Usuario"

        titulo = ctk.CTkLabel( barra, text=f" Panel de Control - {titulo}", image=logo, compound="left", font=("Roboto",18), text_color="white")
        titulo.pack(side=ctk.LEFT, padx=10)
        
        # botón toggle
        boton = ctk.CTkButton( barra, text="", image=icon_menu, width=32, fg_color="transparent", hover_color="white", command=self.toggle_sidebar)
        boton.pack(side=ctk.LEFT)
        
        # bienvenida
        labelUsuario = ctk.CTkLabel( barra, text="", font=("Roboto",18), text_color="white")
        labelUsuario.pack(side=ctk.RIGHT, padx=15)
        
        frameTopbar.pack(side="top", fill="x", expand=False)
        
    def sidebar(self):
        """
        Crea el sidebar completo con submenús expandibles y ajuste automático de ancho
        """
        # Crear frame principal del sidebar
        self.menu_lateral = ctk.CTkFrame(self, fg_color="#18244c", corner_radius=0, width=180)
        self.menu_lateral.pack(side="left", fill="y")
        self.menu_lateral.pack_propagate(False)
        
        # Variables para controlar submenús
        self.submenu_frames = {}
        self.submenu_buttons = {}
        
        # === AVATAR DE PERFIL ===
        try:
            if (hasattr(self.controller, 'master_controlador') and 
                hasattr(self.controller.master_controlador, 'existe_imagen') and
                self.controller.master_controlador.existe_imagen(self.username)):
                ruta_perfil = self.controller.master_controlador.obtener_destino_imagen(self.username)
            else:
                ruta_perfil = Settings().rutas_imagenes.get("foto_perfil", "resources/images/Perfil.png")
            
            foto_perfil = self.leer_imagen(ruta_perfil, (70, 70))
            if foto_perfil:
                profile_label = ctk.CTkLabel(self.menu_lateral, image=foto_perfil, text="")
                profile_label.pack(pady=(10, 8))
                self.img_perfil = foto_perfil
        except Exception as e:
            print(f"Error cargando perfil: {e}")
        
        # === CONFIGURACIÓN DEL MENÚ SEGÚN ROL ===
        menu_items = []
        
        if self.user_role.lower() in ["admin", "administrador"]:
            menu_items = [
                ("Inicio", "home_icon", self.inicio, False),
                ("Periodos", "pnf_icon", self.periodo, False),
                ("Estudiantes", "estudiantes_icon", None, True),  # Submenú
                ("Docentes", "docentes_icon", self.docentes, True),
                ("Carga de Notas", "carga_notas_icon", self.carga_notas, False),
                ("P.N.F", "pnf_icon", self.pnf, True),
                ("Sedes", "sedes_icon", self.sedes, False),
                ("Ayuda", "ayuda_icon", self._mostrar_ayuda, False),
                ("Configuración", "configuracion_icon", self.configuracion, True),
                ("Cerrar Sesión", "cerrar_sesion_icon", self._confirmar_logout, False),
            ]
        
        elif self.user_role.lower() == "coord_general":
            menu_items = [
                ("Inicio", "home_icon", self.inicio, False),
                ("Periodos", "pnf_icon", self.periodo, False),
                ("Estudiantes", "estudiantes_icon", None, True),  # Submenú
                ("Docentes", "docentes_icon", self.docentes, True),
                ("Carga de Notas", "carga_notas_icon", self.carga_notas, False),
                ("Ayuda", "ayuda_icon", self._mostrar_ayuda, False),
                ("Configuración", "configuracion_icon", self.configuracion, True),
                ("Cerrar Sesión", "cerrar_sesion_icon", self._confirmar_logout, False),
            ]
        
        elif self.user_role.lower() == "coord_pnf":
            menu_items =[
                ("Inicio", "home_icon", self.inicio, False),
                ("Consulta P.N.F", "pnf_icon", self.pnf, False),
                ("Unidades Curriculares", "uc_icon", None, True),
                ("Ayuda", "ayuda_icon", self._mostrar_ayuda, False),
                ("Configuración", "configuracion_icon", self.configuracion, True),
                ("Cerrar Sesión", "cerrar_sesion_icon", self._confirmar_logout, False),
            ]
        
        elif self.user_role.lower() == "docente":
            menu_items = [
                ("Inicio", "home_icon", self.inicio, False),
                ("Gestión de Notas", "carga_notas_icon", self.carga_notas, False),
                ("Configuración", "configuracion_icon", self.configuracion, True),
                ("Cerrar Sesión", "cerrar_sesion_icon", self._confirmar_logout, False),
            ]

        elif self.user_role.lower() == "estudiante":
            menu_items = [
                ("Inicio", "home_icon", self.inicio, False),
                ("Mis Notas", "carga_notas_icon", self.carga_notas, False),
                ("Ayuda", "ayuda_icon", self._mostrar_ayuda, False),
                ("Configuración", "configuracion_icon", self.configuracion, True),
                ("Cerrar Sesión", "cerrar_sesion_icon", self._confirmar_logout, False),
            ]
        else:  # teacher o otros roles
            menu_items = [
                ("Inicio", "home_icon", self.inicio, False),
                ("Estudiantes", "estudiantes_icon", None, True),  # Submenú
                ("Mis Clases", "clases_icon", self.mis_clases, False),
                ("Ayuda", "ayuda_icon", self._mostrar_ayuda, False),
                ("Configuración", "configuracion_icon", self.configuracion, True),
                ("Cerrar Sesión", "cerrar_sesion_icon", self._confirmar_logout, False),
            ]
        
        # === CREAR BOTONES DEL MENÚ ===
        for texto, icono_key, callback, es_submenu in menu_items:
            # Obtener ruta del icono
            icono_path = Settings().rutas_iconos.get(icono_key, f"resources/icons/{icono_key}.png")
            
            if es_submenu:
                # === CREAR BOTÓN CON SUBMENÚ ===
                try:
                    icono = self.leer_imagen(icono_path, (14, 14)) if icono_path else None
                except:
                    icono = None
                
                # Botón principal del submenú
                btn_principal = ctk.CTkButton(
                    self.menu_lateral,
                    text=f"{texto} ▼",
                    image=icono,
                    anchor="w",
                    font=("Roboto", 15),
                    fg_color="#18244c",
                    hover_color="#3556a3",
                    text_color="white",
                    corner_radius=8,
                    height=32,
                    command=lambda t=texto: self._toggle_submenu_sidebar(t)
                )
                btn_principal.pack(fill="x", pady=(2, 2), padx=8)
                
                # Frame para el submenú
                submenu_frame = ctk.CTkFrame(self.menu_lateral, fg_color="#18244c")
                submenu_frame.pack_forget()
                
                # === CREAR ELEMENTOS DEL SUBMENÚ ===
                submenu_items = []
                if texto == "Estudiantes":
                    if self.user_role.lower() in ["admin", "administrador", "coord_general"]:
                        submenu_items = [
                            ("Registrar Estudiante", "registro_icon", self.estudiantes),
                            ("Listar Estudiantes", "list_estudiante_icon", self.list_estudiante),
                        ]
                    # else:  # teacher
                    #     submenu_items = [
                    #         ("Ver Estudiantes", "list_estudiante_icon", self.ver_estudiantes),
                    #         ("Asignar Notas", "notas_icon", self.asignar_notas),
                    #     ]
                elif texto == "Docentes":
                    if self.user_role.lower() in ["admin", "administrador", "coord_general"]:
                        submenu_items = [
                            ("Registrar Docentes", "registro_icon", self.docentes),
                            ("Listar Docentes", "list_estudiante_icon", self.list_docente),
                        ]
                elif texto == "P.N.F":
                    if self.user_role.lower() in ["admin", "administrador"]:
                        submenu_items= [
                            ("Registrar P.N.F", "uc_icon", self.pnf),
                            ("Listas de P.N.F", "uc_icon", self.list_pnf),
                            ("Secciones", "uc_icon", self.secciones),
                            ("Listar Secciones", "uc_icon", self.list_secciones),
                            ("Unidades Curriculares", "uc_icon", self.unid_Curr),
                            ("Listar U.C","uc_icon",self.listar_uc)  
                        ] 
                elif texto == "Unidades Curriculares":
                    if self.user_role == "COORD_PNF":  
                        submenu_items = [    
                            ("Unidades Curriculares", "uc_icon", self.unid_Curr),
                            ("Listar U.C","uc_icon",self.listar_uc),
                            ("Asignar U.C Docente", "list_estudiante_icon", self.list_docente)  
                        ] 
                elif texto == "Configuración":
                    if self.user_role.lower() in ["admin", "administrador"]:
                        submenu_items = [
                            ("Usuarios", "configuracion_icon", self.configuracion_usuarios),
                            ("Sistema", "configuracion_icon", self.configuracion_sistema),
                            ("Respaldos", "configuracion_icon", self.configuracion_respaldos)
                        ]
                    if self.user_role.lower() in ["coord_general","coord_pnf","estudiante","docente"]:
                        submenu_items =[
                            ("Usuario", "configuracion_icon", self.configuracion_usuarios),
                            ("Sistema", "configuracion_icon", self.configuracion_sistema)
                        ]
            
                # Crear botones del submenú
                for sub_texto, sub_icono_key, sub_callback in submenu_items:
                    try:
                        sub_icono_path = Settings().rutas_iconos.get(sub_icono_key, f"resources/icons/{sub_icono_key}.png")
                        sub_icono = self.leer_imagen(sub_icono_path, (12, 12)) if sub_icono_path else None
                    except:
                        sub_icono = None
                    
                    sub_btn = ctk.CTkButton(
                        submenu_frame,
                        text=f"  {sub_texto}",
                        anchor="w",
                        font=("Roboto", 13),
                        fg_color="#18244c",
                        image=sub_icono,
                        hover_color="#3556a3",
                        text_color="white",
                        corner_radius=6,
                        height=28,
                        command=sub_callback if sub_callback else lambda: print(f"Ejecutando: {sub_texto}")
                    )
                    sub_btn.pack(fill="x", pady=1, padx=15)
                
                # Guardar referencias para el toggle
                self.submenu_frames[texto] = submenu_frame
                self.submenu_buttons[texto] = btn_principal
                
            else:
                # === CREAR BOTÓN NORMAL ===
                try:
                    icono = self.leer_imagen(icono_path, (14, 14)) if icono_path else None
                except:
                    icono = None
                
                # Espaciado especial para cerrar sesión
                pady = (25, 10) if texto == "Cerrar Sesión" else (2, 2)
                
                btn = ctk.CTkButton(
                    self.menu_lateral,
                    text=texto,
                    image=icono,
                    anchor="w",
                    font=("Roboto", 15),
                    fg_color="#18244c",
                    hover_color="#3556a3",
                    text_color="white",
                    corner_radius=8,
                    height=32,
                    command=callback if callback else lambda t=texto: print(f"Ejecutando: {t}")
                )
                btn.pack(fill="x", pady=pady, padx=8)
        
        # Ajustar ancho del sidebar
        self._ajustar_ancho_sidebar()

    def _toggle_submenu_sidebar(self, menu_name):
        """Alterna la visibilidad del submenú"""
        if not hasattr(self, 'submenu_frames') or not hasattr(self, 'submenu_buttons'):
            return
        
        submenu_frame = self.submenu_frames.get(menu_name)
        main_button = self.submenu_buttons.get(menu_name)
        
        if submenu_frame and main_button:
            if submenu_frame.winfo_ismapped():
                # Ocultar submenú
                submenu_frame.pack_forget()
                current_text = main_button.cget("text")
                new_text = current_text.replace("▲", "▼")
                main_button.configure(text=new_text)
            else:
                # Mostrar submenú
                submenu_frame.pack(after=main_button, fill="x", padx=8)
                current_text = main_button.cget("text")
                new_text = current_text.replace("▼", "▲")
                main_button.configure(text=new_text)
            
            # Reajustar ancho después del cambio
            self._ajustar_ancho_sidebar()

    def _ajustar_ancho_sidebar(self):
        """Ajusta el ancho del sidebar basado en el contenido"""
        if not hasattr(self, 'menu_lateral'):
            return
        
        self.menu_lateral.update_idletasks()
        
        # Calcular el ancho necesario
        ancho_minimo = 200
        ancho_maximo = 250
        
        try:
            ancho_requerido = self.menu_lateral.winfo_reqwidth()
            ancho_ajustado = ancho_requerido + 30  # Padding extra
        except:
            ancho_ajustado = ancho_minimo
        
        # Mantener dentro de los límites
        ancho_final = max(ancho_minimo, min(ancho_ajustado, ancho_maximo))
        self.menu_lateral.configure(width=ancho_final)
    
    def toggle_sidebar(self):
        """Alterna la visibilidad del sidebar"""
        if hasattr(self, 'menu_lateral'):
            if self.menu_lateral.winfo_ismapped():
                self.menu_lateral.pack_forget()
                self.cuerpo_principal.pack_forget()
                self.cuerpo_principal.pack(side="right", fill="both", expand=True)
            else:
                self.menu_lateral.pack(side="left", fill="y")
                self.menu_lateral.pack_propagate(False)
                self.menu_lateral.lift()
                # Reempaquetar el cuerpo principal para que se ajuste al nuevo espacio
                self.cuerpo_principal.pack_forget()
                self.cuerpo_principal.pack(side="right", fill="both", expand=True)
                self._ajustar_ancho_sidebar()
            self.cuerpo_principal.update_idletasks()
            self.menu_lateral.update_idletasks()

    def _confirmar_logout(self):
        """Confirma antes de cerrar sesión"""
        import tkinter.messagebox as msgbox
        if msgbox.askyesno("Confirmar", "¿Está seguro que desea cerrar sesión?"):
            # if hasattr(self.controller, 'mostrar_vista_login'):
            #     self.controller.mostrar_vista_login()
            try:
                cerrar = self.controller["mostrar_vista_login"]
                cerrar()
                self.controller["Mostrar_Ventanas"].reducir_ventana("800x600")
            except Exception as e:
                print(f"Error al cerrar sesión: {e}")


    
    def inicio(self): pass
    def periodo(self): pass
    def docentes(self): pass
    def list_docente(self): pass
    def estudiantes(self): pass
    def list_estudiante(self): pass
    def ver_estudiantes(self): pass
    def asignar_notas(self): pass
    def carga_notas(self): pass
    def pnf(self): pass
    def list_pnf(self):pass
    def secciones(self): pass
    def list_secciones(self): pass
    def unid_Curr(self): pass
    def listar_uc(self): pass
    def sedes(self): pass
    def perfil(self): pass
    def notas(self): pass
    def mis_clases(self): pass
    def configuracion(self): pass
    def configuracion_usuarios(self): pass
    def configuracion_sistema(self): pass
    def configuracion_respaldos(self): pass
    def _mostrar_ayuda(self): pass