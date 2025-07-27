import tkinter.messagebox as messagebox
import tkinter as tk
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase
from ..DatosPersonales import DatosPersonalesFrame


class FormPeriodoAcademico(SectionFrameBase):
    def __init__(self, master, controller):
        super().__init__(master, header_text="Gestión de Períodos Académicos")

        self.controller = controller
        # Inicialización de las variables de fecha
        self.fecha_inicio = None
        self.fecha_fin = None
        self.fecha_inicio_inscripcion = None
        self.fecha_fin_inscripcion = None
        self.fecha_inicio_clases = None
        self.fecha_fin_clases = None
        self.fecha_inicio_evaluaciones = None
        self.fecha_fin_evaluaciones = None
        # Evento de mouse para el formulario
        #self.evento_mouse()

        # Variables de control
        self.var_tipo = ctk.StringVar(value="Regular")
        self.var_estado = ctk.StringVar(value="Planificación")
        

        self._crear_fila_widgets([
            ("Codigo", crear_entry, {"width": 300, "placeholder_text": "Ingrese el codigo"}, 1, self, "codigo_entry"),
            ("Nombre", crear_entry, {"width": 300, "placeholder_text": "Ingrese el nombre"}, 1, self, "nombre_entry"),
            ("Tipo", crear_option_menu, {"values": ["Regular", "Intensivo", "Intersemestral", "Especial"], "variable": self.var_tipo}, 1, self, "tipo_menu"),
        ])

        # --- Integración de los calendarios para cada fecha ---

        # Labels para mostrar las fechas seleccionadas
        # Período Académico General
        self.registrar_fecha(self.set_fecha_inicio, titulo_btn="Inicio Período")
        self.fecha_inicio_label = ctk.CTkLabel(self, text="Fecha de Inicio del Período: No seleccionada",text_color=COLOR_TEXTO_PRINCIPAL)  
        self.fecha_inicio_label.pack(pady=(10, 0), padx=20, anchor="w")
        
        self.registrar_fecha(self.set_fecha_fin, titulo_btn="Fin Período")
        self.fecha_fin_label = ctk.CTkLabel(self, text="Fecha de Fin del Período: No seleccionada",text_color=COLOR_TEXTO_PRINCIPAL)
        self.fecha_fin_label.pack(pady=(5, 0), padx=20, anchor="w")

        # Inscripciones
        self.registrar_fecha(self.set_fecha_inicio_inscripcion, titulo_btn="Inicio Inscripción")
        self.fecha_inicio_inscripcion_label = ctk.CTkLabel(self, text="Inicio de Inscripción: No seleccionada",text_color=COLOR_TEXTO_PRINCIPAL)
        self.fecha_inicio_inscripcion_label.pack(pady=(10, 0), padx=20, anchor="w")

        self.registrar_fecha(self.set_fecha_fin_inscripcion, titulo_btn="Fin Inscripción")
        self.fecha_fin_inscripcion_label = ctk.CTkLabel(self, text="Fin de Inscripción: No seleccionada",text_color=COLOR_TEXTO_PRINCIPAL)
        self.fecha_fin_inscripcion_label.pack(pady=(5, 0), padx=20, anchor="w")
        
        # Clases
        self.registrar_fecha(self.set_fecha_inicio_clases, titulo_btn="Inicio Clases")
        self.fecha_inicio_clases_label = ctk.CTkLabel(self, text="Inicio de Clases: No seleccionada",text_color=COLOR_TEXTO_PRINCIPAL)
        self.fecha_inicio_clases_label.pack(pady=(10, 0), padx=20, anchor="w")
        
        self.registrar_fecha(self.set_fecha_fin_clases, titulo_btn="Fin Clases")
        self.fecha_fin_clases_label = ctk.CTkLabel(self, text="Fin de Clases: No seleccionada",text_color=COLOR_TEXTO_PRINCIPAL)
        self.fecha_fin_clases_label.pack(pady=(5, 0), padx=20, anchor="w")
        
        # Evaluaciones
        self.registrar_fecha(self.set_fecha_inicio_evaluaciones, titulo_btn="Inicio Evaluaciones")
        self.fecha_inicio_evaluaciones_label = ctk.CTkLabel(self, text="Inicio de Evaluaciones: No seleccionada",text_color=COLOR_TEXTO_PRINCIPAL)
        self.fecha_inicio_evaluaciones_label.pack(pady=(10, 0), padx=20, anchor="w")
        
        self.registrar_fecha(self.set_fecha_fin_evaluaciones, titulo_btn="Fin Evaluaciones")
        self.fecha_fin_evaluaciones_label = ctk.CTkLabel(self, text="Fin de Evaluaciones: No seleccionada",text_color=COLOR_TEXTO_PRINCIPAL)
        self.fecha_fin_evaluaciones_label.pack(pady=(5, 0), padx=20, anchor="w")
        
        self._crear_fila_widgets([
            ("Duración en semanas", crear_entry, {"width": 200, "placeholder_text": "Ingrese la duración en semanas"},1,self,"duracion_semanas_entry"),
            ("Estado", crear_option_menu, {"values": ["Planificación","Inscripción","En Curso","Evaluaciones","Finalizado","Cerrado"],"variable": self.var_estado, "width": 200},1,self,"estado_menu"),
            ("Observación",crear_entry,{"width": 300, "placeholder_text": "Ingrese observaciones"},1,self,"observacion_entry")
        ])

    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets
    
    # --- Métodos Setter para cada fecha ---
    def set_fecha_inicio(self, fecha):
        self.fecha_inicio = fecha
        self.fecha_inicio_label.configure(text=f"Fecha de Inicio del Período: {fecha}")

    def set_fecha_fin(self, fecha):
        self.fecha_fin = fecha
        self.fecha_fin_label.configure(text=f"Fecha de Fin del Período: {fecha}")

    def set_fecha_inicio_inscripcion(self, fecha):
        self.fecha_inicio_inscripcion = fecha
        self.fecha_inicio_inscripcion_label.configure(text=f"Inicio de Inscripción: {fecha}")

    def set_fecha_fin_inscripcion(self, fecha):
        self.fecha_fin_inscripcion = fecha
        self.fecha_fin_inscripcion_label.configure(text=f"Fin de Inscripción: {fecha}")

    def set_fecha_inicio_clases(self, fecha):
        self.fecha_inicio_clases = fecha
        self.fecha_inicio_clases_label.configure(text=f"Inicio de Clases: {fecha}")

    def set_fecha_fin_clases(self, fecha):
        self.fecha_fin_clases = fecha
        self.fecha_fin_clases_label.configure(text=f"Fin de Clases: {fecha}")

    def set_fecha_inicio_evaluaciones(self, fecha):
        self.fecha_inicio_evaluaciones = fecha
        self.fecha_inicio_evaluaciones_label.configure(text=f"Inicio de Evaluaciones: {fecha}")

    def set_fecha_fin_evaluaciones(self, fecha):
        self.fecha_fin_evaluaciones = fecha
        self.fecha_fin_evaluaciones_label.configure(text=f"Fin de Evaluaciones: {fecha}")


    def registrar_fecha(self, callback, titulo_btn="Seleccionar Fecha", attr_name=None, frame=None):
        
        master_frame = frame if frame is not None else self

        def calendario():
            top = ctk.CTkToplevel(self, fg_color="White")
            top.title("Seleccionar Fecha")

            ancho = 350
            alto = 350

            top.update_idletasks() 
            screen_width = top.winfo_screenwidth()
            screen_height = top.winfo_screenheight()

            x = (screen_width // 2) - (ancho // 2)
            y = (screen_height // 2) - (alto // 2)

            top.geometry(f"{ancho}x{alto}+{x}+{y}")
            top.lift()
            top.focus_force()
            top.grab_set()
            label = ctk.CTkLabel(top, text="Seleccione Fecha", font=FUENTE_LABEL_CAMPO, text_color=COLOR_TEXTO_PRINCIPAL)
            label.pack(pady=10)
            # Asegúrate de tener tkcalendar instalado: pip install tkcalendar
            self.cal = Calendar(top, locale='es_ES', date_pattern='yyyy-mm-dd')
            self.cal.pack(pady=20)

            def mostrar_fecha(date):
                label.configure(text=f"Fecha seleccionada: {date}")

            def guardar_fecha():
                fecha = self.cal.get_date()
                callback(fecha)
                top.grab_release() # Libera el control
                top.destroy()

            self.cal.bind("<<CalendarSelected>>", lambda e: mostrar_fecha(self.cal.get_date()))
            boton_guardar = ctk.CTkButton(top, text="Guardar Fecha", command=guardar_fecha)
            boton_guardar.pack(pady=10)

        # Se modificó para que el botón se empaquete en el 'master_frame'
        frame_fecha = ctk.CTkFrame(self, fg_color="transparent")
        frame_fecha.pack(fill="x", pady=(10, 0), padx=10)
        btn_fecha = ctk.CTkButton(
            frame_fecha,
            text=titulo_btn,
            command=calendario,
            width=140, # Ancho ajustado para que quepan más botones
            font=FUENTE_BOTON,
            fg_color=COLOR_BOTON_PRIMARIO_FG,
            hover_color=COLOR_BOTON_PRIMARIO_HOVER,
            text_color=COLOR_BOTON_PRIMARIO_TEXT
        )
        # Se empaqueta con side="left" para que se coloquen uno al lado del otro
        btn_fecha.pack(side="left", pady=(10, 0), anchor="w")
        if attr_name:
            setattr(self, attr_name, btn_fecha)

    def habilitar_campos(self):
        self.codigo_entry.configure(state="normal")
        self.nombre_entry.configure(state="normal")
        self.tipo_menu.configure(state="normal")
        self.duracion_semanas_entry.configure(state="normal")
        self.estado_menu.configure(state="normal")
        self.observacion_entry.configure(state="normal")
        
    def deshabilitar_campos(self):
        self.codigo_entry.configure(state="disabled")
        self.nombre_entry.configure(state="disabled")
        self.tipo_menu.configure(state="disabled")
        self.duracion_semanas_entry.configure(state="disabled")
        self.estado_menu.configure(state="disabled")
        self.observacion_entry.configure(state="disabled")