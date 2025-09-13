# views/admin/estudiante_form_view.py
import customtkinter as ctk
import tkinter as tk
import tkinter.messagebox as messagebox
from views.dashboard.components.widget_utils import *
from views.dashboard.modules.forms.DatosPersonales import DatosPersonalesFrame
from views.dashboard.modules.forms.DatosUbicacion import DatosUbicacionFrame
from views.dashboard.modules.forms.Docentes.FrameDocente import FrameDocente

from config.app_config import AppConfig
class FormularioDocenteView(ctk.CTkScrollableFrame):

    def __init__(self, master, controlador, role_user):
        super().__init__(master, fg_color=COLOR_FONDO_FORMULARIO, label_text="")
        self.master = master
        self.controlador = controlador
        self.btn_actualizar = None
        self.datos_personales_frame = None
        self.datos_ubicacion_frame = None
        self.role_user = role_user
        #self.controlador.master_controlaor.docente.obtener_lista_docentes()
        # Registrar funciones de validación
        try:
            toplevel = self.winfo_toplevel()
            self.vcmd_num_val = toplevel.register(self.controlador._solo_numeros)
            self.vcmd_fecha_val = toplevel.register(self.controlador._numeros_y_barras)
            self.vcmd_decimal_val = toplevel.register(self.controlador._solo_decimal)
        except Exception: # Fallback si no es un toplevel (ej. si el master es el root)
            self.vcmd_num_val = master.register(self.controlador._solo_numeros)
            self.vcmd_fecha_val = master.register(self.controlador._numeros_y_barras)
            self.vcmd_decimal_val = master.register(self.controlador._solo_decimal)

        ctk.CTkLabel(self, text="Gestión de Datos de Docente", font=FUENTE_TITULO_FORMULARIO, text_color=COLOR_TEXTO_PRINCIPAL).pack(pady=(10, 20), padx=20, anchor="w")

        # Instanciar los frames de sección, pasando las validaciones
        self.datos_personales_frame = DatosPersonalesFrame(self, self.vcmd_num_val, self.vcmd_fecha_val)
        self.datos_docente_frame = FrameDocente(self, self.vcmd_num_val, self.vcmd_fecha_val)
        self.datos_ubicacion_frame = DatosUbicacionFrame(self, self.vcmd_num_val)
        
        # Empacar los frames
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=(25, 20))

        self.btn_guardar = ctk.CTkButton(self.button_frame, text="Grabar Datos", width=140, command=self.procesar_formulario,
                                        font=FUENTE_BOTON, fg_color=COLOR_BOTON_PRIMARIO_FG, hover_color=COLOR_BOTON_PRIMARIO_HOVER, text_color=COLOR_BOTON_PRIMARIO_TEXT)
        self.btn_guardar.pack(side="left", padx=10)

        self.btn_cancelar = ctk.CTkButton(self.button_frame, text="Limpiar Campos", width=140, command=self.limpiar_formulario_completo,
                                         font=FUENTE_BOTON, fg_color=COLOR_BOTON_SECUNDARIO_FG, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, text_color=COLOR_BOTON_SECUNDARIO_TEXT)
        self.btn_cancelar.pack(side="left", padx=10)


    def limpiar_formulario_completo(self):
        """
        Limpia todos los campos del formulario.
        """
        self.controlador.limpiar_formulario_completo(self)


    def procesar_formulario(self):
        resultado = self.controlador.obtener_todos_los_datos(self)
        exito = self.controlador.registrar_docente(resultado, self)
        if exito:
            self.controlador.limpiar_formulario_completo(self)
        
    # sFormulario de actualizacion
    def ver_datos_completos(self, docente, role_user):
        """
        Muestra una ventana emergente con los datos completos de un docente, en formato similar al formulario.
        """
        ventana = ctk.CTkToplevel(self)
        ventana.title("Datos Completos del Docente")
        ventana.geometry("850x700") 
        AppConfig().centrar_ventana(ventana, 850, 700)

        ventana.grab_set() # Bloquea la ventana principal

        # Crear un contenedor scrollable para la ventana emergente
        contenedor_scroll = ctk.CTkScrollableFrame(ventana, fg_color=COLOR_FONDO_FORMULARIO)
        contenedor_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        # Instanciando los frames en la ventana emergente
        self.datos_personales_frame = DatosPersonalesFrame(contenedor_scroll, self.vcmd_num_val, self.vcmd_fecha_val)
        self.datos_docente_frame = FrameDocente(contenedor_scroll, self.vcmd_num_val, self.vcmd_fecha_val)
        self.datos_ubicacion_frame = DatosUbicacionFrame(contenedor_scroll, self.vcmd_num_val)

        # Empacar para que se muestren
        self.datos_personales_frame.pack(fill="x", pady=5, padx=5)
        self.datos_ubicacion_frame.pack(fill="x", pady=5, padx=5)

        # Cargar datos y bloquear campos
        #for frame in [self.datos_personales_frame, self.informacion_academica_frame, self.sistema_ingreso_frame, self.datos_ubicacion_frame]:
        #   frame.set_datos(estudiante)
        #     frame.set_estado_campos(modo_lectura=True)
        self.datos_personales_frame.set_datos(docente)
        self.datos_docente_frame.set_datos(docente)
        self.datos_ubicacion_frame.set_datos(docente)

        # Botones
        botones_frame = ctk.CTkFrame(contenedor_scroll, fg_color="transparent")
        botones_frame.pack(pady=10)

        # Botón para actualizar datos
        docente_id = docente['persona_id']
        if role_user.lower() == "coord_pnf":
            ctk.CTkButton(botones_frame, text="Cerrar", command=ventana.destroy).pack(side="left", padx=10)
        else:
            self.btn_actualizar = ctk.CTkButton(
                botones_frame, text="Actualizar Datos", state="disabled", command=lambda: self.actualizar_docente(docente_id,ventana)  # Cambia el comando aquí
            )
            self.btn_actualizar.pack(side="left", padx=10)
            # Botón para editar campos
            ctk.CTkButton(botones_frame, text="Editar Campos", command=self._editar_datos).pack(side="left", padx=10)
            ctk.CTkButton(botones_frame, text="Cerrar", command=ventana.destroy).pack(side="left", padx=10)

    def _editar_datos(self):
        # Cambia el estado de los botones y habilita la edición de los campos
        if self.btn_actualizar is not None:
            self.btn_actualizar.configure(state="normal")
        if self.datos_personales_frame is not None:
            self.datos_personales_frame.habilitar_edicion()
        if self.datos_docente_frame is not None:
            self.datos_docente_frame.habilitar_edicion()
        if self.datos_ubicacion_frame is not None:
            self.datos_ubicacion_frame.habilitar_edicion()
    
    def actualizar_docente(self, id, ventana):
        # Obtener los datos de los frames para actualizarlos
        datos = self.controlador.obtener_todos_los_datos(self)
        if self.controlador.validar_campos_obligatorios(datos, self):
            exito = self.controlador.cargar_docente_edicion(id, datos, self)
            if exito:
                ventana.destroy()
            else:
                pass
    