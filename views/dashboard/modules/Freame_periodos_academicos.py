import customtkinter as ctk
import tkinter.messagebox as messagebox
from views.dashboard.components.widget_utils import *
from views.dashboard.modules.forms.Periodos_academico.formPeriodoAcademico import FormPeriodoAcademico

class PeriodoAcademicoView(ctk.CTkScrollableFrame):

    def __init__(self, master, controlador):
        super().__init__(master, fg_color=COLOR_FONDO_FORMULARIO, label_text="")
        self.master = master
        self.controlador = controlador
        self.datos_periodo = None

        ctk.CTkLabel(self, text="Gestión de Períodos Académicos", font=FUENTE_TITULO_FORMULARIO, text_color=COLOR_TEXTO_PRINCIPAL).pack(pady=(10, 20), padx=20, anchor="w")

        self.datos_periodo = FormPeriodoAcademico(self, self.controlador)
        self.datos_periodo.pack(fill="x", pady=5, padx=5)

        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=(25, 20))

        self.btn_guardar = ctk.CTkButton(self.button_frame, text="Grabar Datos", width=140, #command=self.procesar_formulario,
                                        font=FUENTE_BOTON, fg_color=COLOR_BOTON_PRIMARIO_FG, hover_color=COLOR_BOTON_PRIMARIO_HOVER, text_color=COLOR_BOTON_PRIMARIO_TEXT)
        self.btn_guardar.pack(side="left", padx=10)