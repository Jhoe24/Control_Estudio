import tkinter.messagebox as messagebox
import customtkinter as ctk
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase
from views.dashboard.modules.forms.Docentes.asignar_pnf_docente import AsignarDocentePNFFrame

class ListaAsignacionPNF(SectionFrameBase):
    def __init__(self, master,controller_pnf, docente):
        super().__init__(master,"")
        self.controller_pnf = controller_pnf
        self.docente = docente
        self.id_docente = self.docente.get("id")
        self.listado_asignaciones = self.controller_pnf.modelo.obtener_pnf_asignado_docente(self.id_docente)
        self.listaFrameCargados = []
        self.listaFrameAgregados = []

        self.frame_contenedor = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_contenedor.pack(fill="x", padx=10, pady=10)

        self.frame_contenedor.grid_columnconfigure(0, weight=0) # Columna del label
        self.frame_contenedor.grid_columnconfigure(1, weight=1) # Columna de expansión
        self.frame_contenedor.grid_columnconfigure(2, weight=0) # Columna del botón

        ctk.CTkLabel(self.frame_contenedor, text="Gestion de P.N.F Asignados", font=FUENTE_TITULO_FORMULARIO, text_color=COLOR_TEXTO_PRINCIPAL).grid(row=0, column=0, padx=(10, 0), pady=10, sticky="w")
        self.btn_agregar = ctk.CTkButton(
            self.frame_contenedor,
            text="Agregar P.N.F",
            width=140,
            font=FUENTE_BOTON,
            fg_color=COLOR_BOTON_FONDO2,
            hover_color=COLOR_BOTON_FONDO_HOVER,
            text_color=COLOR_TEXTO_PRINCIPAL,
            command=self.agregar_pnf
        )
        self.btn_agregar.grid(row=0, column=2, padx=(0, 10), pady=10, sticky="e")
        self.carga_datos()
        # Botones
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=(25, 20))

        self.btn_guardar = ctk.CTkButton(self.button_frame, text="Actualizar Datos", width=140,
                                        font=FUENTE_BOTON, fg_color=COLOR_BOTON_PRIMARIO_FG, hover_color=COLOR_BOTON_PRIMARIO_HOVER,
                                        command=self.actualizar_datos_completos,
                                        text_color=COLOR_BOTON_PRIMARIO_TEXT, state="normal")
        self.btn_guardar.pack(side="left", padx=10)

        self.btn_cancelar = ctk.CTkButton(self.button_frame, text="Editar Asignaciónes", width=140,
                                        font=FUENTE_BOTON, fg_color=COLOR_BOTON_SECUNDARIO_FG, hover_color=COLOR_BOTON_SECUNDARIO_HOVER,
                                        command=self.habilitar_edicion_pnf,
                                        text_color=COLOR_BOTON_SECUNDARIO_TEXT)
        self.btn_cancelar.pack(side="left", padx=10)


    def carga_datos(self):
        if self.listado_asignaciones:
            for asignacion in self.listado_asignaciones:
                framePnfAsignado = AsignarDocentePNFFrame(self,None,self.controller_pnf,self.docente,True)
                framePnfAsignado.cargar_datos_pnf(asignacion)
                self.listaFrameCargados.append(framePnfAsignado)
    
    def agregar_pnf(self):
        framePnfAsignado = AsignarDocentePNFFrame(self,None,self.controller_pnf,self.docente,False)   
        self.listaFrameAgregados.append(framePnfAsignado)
        self.button_frame.pack_forget()
        self.button_frame.pack(pady=(25, 20))

    def habilitar_edicion_pnf(self):
        for frames_update in self.listaFrameCargados:
            frames_update.habilitar_edicion_pnf()

    def actualizar_datos_completos(self):
        #registrar los pnf nuevos
        for frames_new in self.listaFrameAgregados:
            if frames_new.winfo_exists():
                frames_new.guardar_datos()

        #actualizar los pnf existentes
        for frames_update in self.listaFrameCargados:
            frames_update.actualizar_datos_pnf()
        
        self.winfo_toplevel().destroy()
        
        
    def existentes_pnf_asignados(self):
        framePnfAsignado = []
        for datos_asignacion in self.listado_asignaciones:
            framePnfAsignado.append(datos_asignacion["pnf_id"])
        return framePnfAsignado

    def no_pnf_disponibles(self):
        ctk.CTkLabel(self, text="No hay mas P.N.F disponibles", font=FUENTE_LABEL_CAMPO, text_color=COLOR_TEXTO_PRINCIPAL).pack(pady=(10, 0), padx=10, anchor="w")
        self.btn_agregar.configure(state="disabled")
 