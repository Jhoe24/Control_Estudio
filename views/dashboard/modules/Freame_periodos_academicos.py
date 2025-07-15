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
        self.evento_mouse()

        ctk.CTkLabel(self, text="Gestión de Períodos Académicos", font=FUENTE_TITULO_FORMULARIO, text_color=COLOR_TEXTO_PRINCIPAL).pack(pady=(10, 20), padx=20, anchor="w")

        self.datos_periodo = FormPeriodoAcademico(self, self.controlador)
        self.datos_periodo.pack(fill="x", pady=5, padx=5)

        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=(25, 20))

        self.btn_guardar = ctk.CTkButton(self.button_frame, text="Grabar Datos", width=140, command=self.procesar_formulario,
                                        font=FUENTE_BOTON, fg_color=COLOR_BOTON_PRIMARIO_FG, hover_color=COLOR_BOTON_PRIMARIO_HOVER, text_color=COLOR_BOTON_PRIMARIO_TEXT)
        self.btn_guardar.pack(side="left", padx=10)
    
    def procesar_formulario(self):
        datos_periodo = self.controlador.obtener_datos_vista(self.datos_periodo)
        exito = self.controlador.registrar_periodo_academico(datos_periodo, self)
        if exito:
            messagebox.showinfo("Registro Exitoso", "El periodo académico ha sido registrado exitosamente.")

    def evento_mouse(self):
        canvas = self._parent_canvas
        canvas.bind_all("<MouseWheel>", self.movimiento_mouse)
        canvas.bind_all("<Button-4>", self.movimiento_mouse)  
        canvas.bind_all("<Button-5>", self.movimiento_mouse)  

    def movimiento_mouse(self, event):
        canvas = self._parent_canvas
        if event.num == 4:
            canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            canvas.yview_scroll(1, "units")
        else:
            velocidad = 16 
            canvas.yview_scroll(int(-1*(event.delta/60)* velocidad), "units")

        