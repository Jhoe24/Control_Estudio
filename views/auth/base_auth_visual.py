import customtkinter as ctk
from views.base_view import BaseView
from config.settings import Settings


class BaseAuthVisualView(BaseView):
    
    def __init__(self, master, controller, titulo="Sistema UPT", es_login=False, **kwargs):
        super().__init__(master, controller, **kwargs)
        self.master = master

        self.controller = controller
        
        # La vista base (BaseView) ya maneja el empaquetado.
        # El padding (padx, pady) se aplicará cuando esta vista sea empaquetada en la MainWindow.
        
        self.update_idletasks()  # Asegúrate de que el frame esté renderizado
        
        # Usamos solo la altura (48) para que la imagen mantenga su proporción.
        # La función leer_imagen calculará el ancho automáticamente.
        imagen_cintillo = self.leer_imagen("resources/images/cintillo.png", 48)
        cintillo = ctk.CTkLabel(self, image=imagen_cintillo, text='', fg_color="transparent")
        cintillo.pack(side="top", fill="x", expand=False)

        # Estructura visual
        self.crear_estructura_base(es_login)
        self.crear_contenido_especifico()

    def cargar_imagen_logo(self, event=None):
        # Obtenemos el tamaño actual del frame del logo
        ancho = self.frame_logo.winfo_width()
        alto = self.frame_logo.winfo_height()
        
        # Evitamos recargar si el tamaño es inválido (inicialización)
        if ancho <= 1 or alto <= 1:
            return
            
        logo = self.leer_imagen(Settings().rutas_imagenes.get("logo", "resources/images/logo.jpg"), (ancho, alto))
        self.label_logo = ctk.CTkLabel(self.frame_logo, text='', image=logo)
        self.label_logo.place(x=0, y=0, relwidth=1, relheight=1)
        # Desvinculamos el evento para que no se ejecute repetidamente si la ventana se redimensiona
        self.frame_logo.unbind("<Configure>")

    def crear_estructura_base(self, es_login):
        # Panel izquierdo (logo)
        self.frame_logo = ctk.CTkFrame(self, width=400)
        self.frame_logo.pack(side='left', expand=ctk.YES, fill=ctk.BOTH)
        # Vinculamos el evento <Configure> para cargar la imagen cuando el frame tenga tamaño
        self.frame_logo.bind("<Configure>", self.cargar_imagen_logo)
        
        # Panel derecho (contenido)
        self.frame_derecho = ctk.CTkFrame(self, width=400, fg_color='#2e2e2e')
        self.frame_derecho.pack(side="right", expand=ctk.YES, fill=ctk.BOTH)

        # Cabecera
        self.frame_cabecera = ctk.CTkFrame(self.frame_derecho, fg_color="transparent", width=400)
        self.frame_cabecera.pack(side="top", fill=ctk.X, pady=(80 if es_login else 40, 0))

        # Contenido específico
        self.frame_contenido = ctk.CTkFrame(self.frame_derecho, fg_color="transparent")
        self.frame_contenido.pack(side="bottom", expand=ctk.YES, fill=ctk.BOTH, pady=(30, 0))

    def crear_contenido_especifico(self):
        # Debe ser implementado por las vistas hijas
        pass

    def crear_titulo(self, texto):
        label_titulo = ctk.CTkLabel(self.frame_cabecera, text=texto, font=('Arial', 30), text_color="#fff")
        label_titulo.pack(expand=ctk.YES, fill=ctk.BOTH)

    def crear_campo(self, frame, etiqueta, es_password=False):
        label = ctk.CTkLabel(frame, text=etiqueta, font=('Arial', 14), anchor='w', text_color="#fff")
        label.pack(fill=ctk.X, padx=20, pady=0)
        if not es_password:
            campo = ctk.CTkEntry(frame, font=('Arial', 14), text_color="black", fg_color="#fff")
            campo.pack(fill=ctk.X, padx=20, pady=2)
            return campo
        else:
            campo = ctk.CTkEntry(frame, font=('Arial', 14), show="*", text_color="black", fg_color="#fff")
            campo.pack(fill=ctk.X, padx=20, pady=2)
            return campo

    def crear_boton_texto(self, frame, texto_etiqueta, texto_boton, comando):
        """Crea una etiqueta seguida de un botón de texto (como "¿Olvidaste tu contraseña? Click Aquí")"""
        frame_aux = ctk.CTkFrame(frame, fg_color="transparent")
        frame_aux.pack(fill=ctk.X, padx=20, pady=0)
        
        etiqueta = ctk.CTkLabel(frame_aux, text=texto_etiqueta, font=('Arial', 14), anchor='w', text_color="#fff")
        etiqueta.pack(side="left", fill=ctk.X, expand=False, padx=0, pady=0)
        
        boton = ctk.CTkButton(frame_aux, text=texto_boton, font=('Arial', 14, "bold"), width=30, 
                             hover=False, cursor="hand2", fg_color="transparent", command=comando)
        boton.pack(side="left", padx=0, pady=0)
        
        return boton