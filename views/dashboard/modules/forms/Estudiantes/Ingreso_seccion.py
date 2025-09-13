import tkinter.messagebox as messagebox
import tkinter as tk
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase
from ..DatosPersonales import DatosPersonalesFrame

class AsignarSeccionFrame(SectionFrameBase):
    def __init__(self, master, controller_secciones,pnf_id, trayecto_id, tramo_id, carga_datos=False):
        super().__init__(master,"Asignar Secciones a Estudiante",COLOR_HEADER_SECCION_BG_2)
        self.controller_secciones = controller_secciones
        self.pnf_id = pnf_id
        self.trayecto_id = trayecto_id
        self.tramo_id = tramo_id
        self.var_seccion = None
        #Secciones_disponibles es donde se extraen los datos de las secciones asignadas a ese pnf
        self.secciones_disponibles = self.controller_secciones.obtener_nombres_secciones_por_pnf(self.pnf_id,trayecto_id,tramo_id)
        self.var_seccion = ctk.StringVar(value=self.secciones_disponibles[0] if self.secciones_disponibles else "Sin secciones")
        self.var_condicion = ctk.StringVar(value="Regular")
        self.var_estado = ctk.StringVar(value="Inscrito")

        # Crear frame para los campos
        self.frame_contenido_seccion = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_contenido_seccion.pack(fill="x", expand=True, pady=5)

        # Secciones Disponibles
        label_seccion = ctk.CTkLabel(self.frame_contenido_seccion, text="Secciones Disponibles:", font=FUENTE_LABEL_CAMPO, text_color=COLOR_TEXTO_PRINCIPAL)
        label_seccion.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.secciones_menu = crear_option_menu(self.frame_contenido_seccion, width=200,values=self.secciones_disponibles, variable=self.var_seccion)
        self.secciones_menu.grid(row=0, column=1, sticky="ew", padx=10, pady=5)

        # Condición
        label_condicion = ctk.CTkLabel(self.frame_contenido_seccion, text="Condición:", font=FUENTE_LABEL_CAMPO, text_color=COLOR_TEXTO_PRINCIPAL)
        label_condicion.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.condicion_menu = crear_option_menu(self.frame_contenido_seccion, width=200,values=["Regular","Equivalencia","Repitente","Especial","Oyente"], variable=self.var_condicion)
        self.condicion_menu.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        # Estado
        label_estado = ctk.CTkLabel(self.frame_contenido_seccion, text="Estado:", font=FUENTE_LABEL_CAMPO, text_color=COLOR_TEXTO_PRINCIPAL)
        label_estado.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.estado_menu = crear_option_menu(self.frame_contenido_seccion, width=200,values=["Inscrito","Retirado","Aprobado","Reprobado","Sin Calificar"], variable=self.var_estado)
        self.estado_menu.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

        self.frame_contenido_seccion.columnconfigure(1, weight=1)

        if self.secciones_disponibles or carga_datos == True:
            
            self.frame_contenido_seccion.pack(fill="x", expand=True, pady=5)
            self.actualizar_datos_secciones(self.pnf_id,self.trayecto_id,self.tramo_id)

        if not self.secciones_disponibles:
            
            self.frame_contenido_seccion.pack_forget()
            self.master.no_secciones_disponibles()  
       

    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets

    def actualizar_datos_secciones(self,pnf_id,trayecto_id,tramo_id):
        self.pnf_id = pnf_id
        self.secciones_disponibles = self.controller_secciones.obtener_nombres_secciones_por_pnf(self.pnf_id,trayecto_id,tramo_id)
        if not self.secciones_disponibles:
            self.master.no_secciones_disponibles()
            self.frame_contenido_seccion.pack_forget()
            self.master.button_frame.pack_forget()

            
            self.master.button_frame.pack(pady=(25, 20))
        else:
            if self.master.mensajesSecciones:
                self.master.mensajesSecciones.pack_forget()
            self.master.button_frame.pack_forget()
            self.frame_contenido_seccion.pack(fill="x", expand=True, pady=5)
            self.secciones_menu.configure(state = "normal")
            self.var_seccion.set(self.secciones_disponibles[0])
            self.secciones_menu.configure(values=self.secciones_disponibles)
            self.master.button_frame.pack(pady=(25, 20))

        # if not self.secciones_disponibles:
        #     # Si no hay secciones disponibles, hacemos como en el master.no_secciones_disponibles()
        #     self.master.no_secciones_disponibles()


    def cargar_datos_secciones(self, datos):
        if self.master.mensajesSecciones:
                self.master.mensajesSecciones.pack_forget()
        if datos["seccion_id"]:
            nombre = self.controller_secciones.obtener_nombre_por_id(datos["seccion_id"])
            if self.var_seccion:
                self.var_seccion.set(nombre["codigo_seccion"])
        self.secciones_menu.configure(state="disabled")

        self.var_condicion.set(datos["condicion"])
        self.condicion_menu.configure(state="disabled")

        self.var_estado.set(datos["estado"])
        self.estado_menu.configure(state="disabled")
    
    def habilitar_campos(self):
        self.secciones_menu.configure(state="normal")
        self.condicion_menu.configure(state="normal")
        self.estado_menu.configure(state="normal")

        
