import customtkinter as ctk
from util.generic import Utilidades 

class VistaBase(ctk.CTkFrame, Utilidades):
    """
    Clase base para todas las vistas de la aplicación.
    Contiene los elementos comunes a todas las interfaces.
    """
    
    def __init__(self, master, controlador, titulo="Aplicación UPT", es_login=False):
        super().__init__(master)
        self.controlador = controlador
        self.master = master
        
        # Configuración general de la ventana
        self.master.title(titulo)
        self.master.iconbitmap("./src/logo.ico")
        self.configure(fg_color='#2e2e2e')
        self.pack(fill="both", expand=True, pady=10, padx=10)
        self.centrar_ventana(self.master, 1200, 800)
        
        # Carga de imágenes comunes
        self.logoLogin = self.leer_imagen("./src/upt.jpg", (500, 600))
        self.icon2 = self.leer_imagen("./src/esconder.png", (16, 16))
        self.icon = self.leer_imagen("./src/ojo.png", (16, 16))
        self.icon3 = self.leer_imagen("./src/flecha_izquierda.png", (16, 16))
        
        # Estructura básica de la interfaz
        self.crear_estructura_base(es_login)
        self.crear_contenido_especifico()
    
    def crear_estructura_base(self, es_login):
        """
        Crea la estructura básica común a todas las vistas:
        - Panel izquierdo con logo
        - Panel derecho para contenido
        - Encabezado con título
        - Sección para el contenido específico
        """
        # Frame izquierdo para el logo (común a todas las vistas)
        self.frame_logo = ctk.CTkFrame(self, width=400)
        self.frame_logo.pack(side='left', expand=ctk.YES, fill=ctk.BOTH, padx=0, pady=0)
        
        self.label_logo = ctk.CTkLabel(self.frame_logo, text=None, image=self.logoLogin)
        self.label_logo.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Frame derecho para el contenido específico
        self.frame_derecho = ctk.CTkFrame(self, width=400, fg_color='#2e2e2e')
        self.frame_derecho.pack(side="right", expand=ctk.YES, fill=ctk.BOTH, padx=0, pady=0)
    
        # Frame para el encabezado
        self.frame_cabecera = ctk.CTkFrame(self.frame_derecho, fg_color="transparent", width=400)
        self.frame_cabecera.pack(side="top", fill=ctk.X, pady=(80 if es_login else 40, 0))
        
        # Frame para el contenido específico de cada vista
        self.frame_contenido = ctk.CTkFrame(self.frame_derecho, fg_color="transparent")
        self.frame_contenido.pack(side="bottom", expand=ctk.YES, fill=ctk.BOTH, pady=(30, 0))
    
    def crear_contenido_especifico(self):
        """
        Método que debe ser sobrescrito por las clases hijas para 
        implementar el contenido específico de cada vista.
        """
        pass
    
    def crear_titulo(self, texto):
        """Crea un título en la cabecera con formato estándar"""
        label_titulo = ctk.CTkLabel(self.frame_cabecera, text=texto, font=('Times', 30), text_color="#fff")
        label_titulo.pack(expand=ctk.YES, fill=ctk.BOTH)
    
    def crear_campo(self, frame, etiqueta, es_password=False):
        """
        Crea un campo de entrada con su etiqueta
        Retorna el objeto de entrada creado
        """
        label = ctk.CTkLabel(frame, text=etiqueta, font=('Times', 18), anchor='w', text_color="#fff")
        label.pack(fill=ctk.X, padx=20, pady=0)
        
        if not es_password:
            campo = ctk.CTkEntry(frame, font=('Times', 18), text_color="black", fg_color="#fff")
            campo.pack(fill=ctk.X, padx=20, pady=2)
            return campo
        else:
            frame_password = ctk.CTkFrame(frame, fg_color="transparent")
            frame_password.pack(fill=ctk.X, padx=20, pady=2)

            campo = ctk.CTkEntry(frame_password, font=('Times', 18), show="*", text_color="black", fg_color="#fff")
            campo.pack(side="left", fill=ctk.X, expand=True)

            ver_ocultar = ctk.CTkButton(frame_password, text=None, image=self.icon2, width=30, height=30, hover=True, fg_color="#fff")
            ver_ocultar.pack(side="right", padx=0, pady=4)
            
            # Configurar el botón para mostrar/ocultar contraseña
            ver_ocultar.configure(command=lambda: self.mostrarclave('clave', campo, ver_ocultar, self.icon, self.icon2))
            
            return campo, ver_ocultar
    
    def crear_boton(self, frame, texto, comando, fg_color="#fff", text_color="black", height=32, padx=20, pady=10):
        """Crea un botón con formato estándar"""
        boton = ctk.CTkButton(frame, text=texto, font=('Times', 18, "bold"), height=height, 
                               text_color=text_color, fg_color=fg_color, command=comando)
        boton.pack(fill=ctk.X, padx=padx, pady=pady)
        return boton
    
    def crear_boton_texto(self, frame, texto_etiqueta, texto_boton, comando):
        """Crea una etiqueta seguida de un botón de texto (como "¿Olvidaste tu contraseña? Click Aquí")"""
        frame_aux = ctk.CTkFrame(frame, fg_color="transparent")
        frame_aux.pack(fill=ctk.X, padx=20, pady=0)
        
        etiqueta = ctk.CTkLabel(frame_aux, text=texto_etiqueta, font=('Times', 14), anchor='w', text_color="#fff")
        etiqueta.pack(side="left", fill=ctk.X, expand=False, padx=0, pady=0)
        
        boton = ctk.CTkButton(frame_aux, text=texto_boton, font=('Times', 14, "bold"), width=30, 
                             hover=False, cursor="hand2", fg_color="transparent", command=comando)
        boton.pack(side="left", padx=0, pady=0)
        
        return boton