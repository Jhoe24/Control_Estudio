# views/admin/estudiante_form_view.py
import customtkinter as ctk
import tkinter as tk
import tkinter.messagebox as messagebox
from util.widget_utils import *
from .Frames_Estudiantes.DatosPersonales import DatosPersonalesFrame
from .Frames_Estudiantes.InformacionAcademica import InformacionAcademicaFrame
from .Frames_Estudiantes.SistemaIngreso import SistemaIngresoFrame
from .Frames_Estudiantes.DatosUbicacion import DatosUbicacionFrame

class FormularioEstudianteView(ctk.CTkScrollableFrame):

    def __init__(self, master, controlador):
        super().__init__(master, fg_color=COLOR_FONDO_FORMULARIO, label_text="")
        self.master = master
        self.controlador = controlador
        
        self.evento_mouse()

        # Registrar funciones de validación
        try:
            toplevel = self.winfo_toplevel()
            self.vcmd_num_val = toplevel.register(self.controlador.master_controlador.estudiantes._solo_numeros)
            self.vcmd_fecha_val = toplevel.register(self.controlador.master_controlador.estudiantes._numeros_y_barras)
            self.vcmd_decimal_val = toplevel.register(self.controlador.master_controlador.estudiantes._solo_decimal)
        except Exception: # Fallback si no es un toplevel (ej. si el master es el root)
            self.vcmd_num_val = master.register(self.controlador.master_controlador.estudiantes._solo_numeros)
            self.vcmd_fecha_val = master.register(self.controlador.master_controlador.estudiantes._numeros_y_barras)
            self.vcmd_decimal_val = master.register(self.controlador.master_controlador.estudiantes._solo_decimal)

        ctk.CTkLabel(self, text="Gestión de Datos del Alumno", font=FUENTE_TITULO_FORMULARIO, text_color=COLOR_TEXTO_PRINCIPAL).pack(pady=(10, 20), padx=20, anchor="w")

        # Instanciar los frames de sección, pasando las validaciones
        self.datos_personales_frame = DatosPersonalesFrame(self, self.vcmd_num_val, self.vcmd_fecha_val)
        self.informacion_academica_frame = InformacionAcademicaFrame(self, self.vcmd_fecha_val, self.vcmd_decimal_val)
        self.sistema_ingreso_frame = SistemaIngresoFrame(self, self.vcmd_num_val)
        self.datos_ubicacion_frame = DatosUbicacionFrame(self, self.vcmd_num_val)

        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=(25, 20))

        self.btn_guardar = ctk.CTkButton(self.button_frame, text="Grabar Datos", width=140, command=self.procesar_formulario,
                                        font=FUENTE_BOTON, fg_color=COLOR_BOTON_PRIMARIO_FG, hover_color=COLOR_BOTON_PRIMARIO_HOVER, text_color=COLOR_BOTON_PRIMARIO_TEXT)
        self.btn_guardar.pack(side="left", padx=10)

        self.btn_cancelar = ctk.CTkButton(self.button_frame, text="Limpiar Campos", width=140, command=self.limpiar_formulario_completo,
                                        font=FUENTE_BOTON, fg_color=COLOR_BOTON_SECUNDARIO_FG, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, text_color=COLOR_BOTON_SECUNDARIO_TEXT)
        self.btn_cancelar.pack(side="left", padx=10)

    def procesar_formulario(self):
        datos = self.controlador.master_controlador.estudiantes.obtener_todos_los_datos(self)
        if self.controlador.master_controlador.estudiantes.validar_campos_obligatorios(datos, self):
            exito = self.controlador.master_controlador.estudiantes.procesar_guardado_estudiante(datos, self)
            if exito:
                self.controlador.master_controlador.estudiantes.limpiar_formulario_completo(self)
            else:
                pass

    def limpiar_formulario_completo(self):
        self.controlador.master_controlador.estudiantes.limpiar_formulario_completo(self)

        #hola mundo
    
    def evento_mouse(self):
        # Accede al canvas interno de CTkScrollableFrame
        canvas = self._parent_canvas  # atributo privado, pero funciona
        # Para Windows y Mac
        canvas.bind_all("<MouseWheel>", self.movimiento_mouse)
        # Para Linux
        canvas.bind_all("<Button-4>", self.movimiento_mouse)
        canvas.bind_all("<Button-5>", self.movimiento_mouse)
    
    def movimiento_mouse(self, event):
        
        canvas = self._parent_canvas
        if event.num == 4:  # Linux scroll up
            canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # Linux scroll down
            canvas.yview_scroll(1, "units")
        else:  # Windows/Mac
            canvas.yview_scroll(int(-1*(event.delta/5)), "units")

