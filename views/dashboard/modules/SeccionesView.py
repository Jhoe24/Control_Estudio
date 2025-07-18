import customtkinter as ctk
import tkinter.messagebox as messagebox
from views.dashboard.components.widget_utils import *
from views.dashboard.modules.forms.PNF.FrameSecciones import FremeSecciones


class SeccionView(ctk.CTkScrollableFrame):
    def __init__(self, master, controller_Doc, controller_pnf,controller_secciones):
        super().__init__(master, fg_color="transparent")
        self.controller_Doc = controller_Doc
        self.controller_pnf = controller_pnf
        self.form_seccion = FremeSecciones(self, self.controller_Doc, self.controller_pnf, controller_secciones)

        # Empacar los frames
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=(25, 20))

        self.btn_guardar = ctk.CTkButton(self.button_frame, text="Grabar Datos", width=140, command=self.procesar_formulario,
                                        font=FUENTE_BOTON, fg_color=COLOR_BOTON_PRIMARIO_FG, hover_color=COLOR_BOTON_PRIMARIO_HOVER, text_color=COLOR_BOTON_PRIMARIO_TEXT)
        self.btn_guardar.pack(side="left", padx=10)

        self.btn_cancelar = ctk.CTkButton(self.button_frame, text="Limpiar Campos", width=140, #command=self.limpiar_formulario_completo,
                                        font=FUENTE_BOTON, fg_color=COLOR_BOTON_SECUNDARIO_FG, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, text_color=COLOR_BOTON_SECUNDARIO_TEXT)
        self.btn_cancelar.pack(side="left", padx=10)

    def procesar_formulario(self):
        datos = self.form_seccion.obtener_datos_vista()
        print(datos)