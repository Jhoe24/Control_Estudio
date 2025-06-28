import customtkinter as ctk
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase
from views.dashboard.modules.forms.DatosPersonales import DatosPersonalesFrame
from controllers.dashboard.PNF.controller_pnf import ControllerPNF
import pprint

from config.app_config import AppConfig


class UnidadCurricular(SectionFrameBase):
    def __init__(self, master, vcmd_num, controlador):
        super().__init__(master, "Unidad Curricular PNF")
        self.vcmd_num = vcmd_num # Validación para números
        self.controlador = controlador # Guardar el controlador para usar en los métodos
        #self.vcmd_fecha = vcmd_fecha # Guardar para usar en fechas
        self.var_tipo = ctk.StringVar(value="Obligatoria") # Variable para el tipo de U.C
        self.var_caracter = ctk.StringVar(value="Teórico") # Variable para el carácter de la U.C
        self.var_modalidad = ctk.StringVar(value="Presencial") # Variable para la modalidad de evaluación
        self.var_complejidad = ctk.StringVar(value="Baja") # Variable para la complejidad de la U.C
        self.var_estado = ctk.StringVar(value="activo") # Variable para el estado de la U.C

        # # Registrar funciones de validación
        # try:
        #     toplevel = self.winfo_toplevel()
        #     self.vcmd_num_val = toplevel.register(self.controlador._solo_numeros)
        #     self.vcmd_fecha_val = toplevel.register(self.controlador._numeros_y_barras)
        #     self.vcmd_decimal_val = toplevel.register(self.controlador._solo_decimal)
        # except Exception: # Fallback si no es un toplevel (ej. si el master es el root)
        #     self.vcmd_num_val = master.register(self.controlador._solo_numeros)
        #     self.vcmd_fecha_val = master.register(self.controlador._numeros_y_barras)
        #     self.vcmd_decimal_val = master.register(self.controlador._solo_decimal)

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=10, pady=10)

        # Empacar los frames
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=(25, 20))

        self.btn_guardar = ctk.CTkButton(self.button_frame, text="Grabar Datos", width=140, command=self.procesar_formulario,
                                        font=FUENTE_BOTON, fg_color=COLOR_BOTON_PRIMARIO_FG, hover_color=COLOR_BOTON_PRIMARIO_HOVER, text_color=COLOR_BOTON_PRIMARIO_TEXT)
        self.btn_guardar.pack(side="left", padx=10)

        self.btn_cancelar = ctk.CTkButton(self.button_frame, text="Limpiar Campos", width=140, command=self.limpiar_formulario_completo,
                                         font=FUENTE_BOTON, fg_color=COLOR_BOTON_SECUNDARIO_FG, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, text_color=COLOR_BOTON_SECUNDARIO_TEXT)
        self.btn_cancelar.pack(side="left", padx=10)

        # Fila para los datos de la Unidad Curricular

        self._crear_fila_widgets([
            ("Código:", crear_entry, {"width":300,"placeholder_text":"Ingrese código"}, 1, self.scroll, 'codigo_entry'),
            ("Nombre:", crear_entry, {"width":300,"placeholder_text":"Ingrese el nombre de la U.C"}, 1, self.scroll, 'nombre_entry'),
            ("Nombre corto:", crear_entry, {"width":300,"placeholder_text":"Ingrese el nombre corto"}, 1, self.scroll, 'nombre_corto_entry'),
            ("Área:", crear_entry, {"width":300,"placeholder_text":"Ingrese área"}, 1, self.scroll, 'area_entry'),
            ("Sub-area:", crear_entry, {"width":300,"placeholder_text":"Ingrese Sub-area"}, 1, self.scroll, 'subarea_entry'),
            ("Eje Formativo:", crear_entry, {"width":300,"placeholder_text":"Ingrese el eje formativo"}, 1, self.scroll, 'eje_formativo_entry'),
        ], es_scroll=True)
        
        # Fila para las horas de la Unidad Curricular
        self._crear_fila_widgets([
            ("Horas Teóricas:", crear_entry, {"width":300,"placeholder_text":"Ingrese horas"}, 1, self.scroll, 'horas_teoricas_entry', 
             {'validate': 'key', 'validatecommand': (self.vcmd_num, '%P')}),
            ("Horas Prácticas:", crear_entry, {"width":300,"placeholder_text":"Ingrese horas"}, 1, self.scroll, 'horas_practicas_entry', 
             {'validate': 'key', 'validatecommand': (self.vcmd_num, '%P')}),
            ("Horas Laboratorio:", crear_entry, {"width":300,"placeholder_text":"Ingrese horas"}, 1, self.scroll, 'horas_laboratorio_entry', 
             {'validate': 'key', 'validatecommand': (self.vcmd_num, '%P')}),
            ("Horas Trabajo Pendiente:", crear_entry, {"width":300,"placeholder_text":"Ingrese horas"}, 1, self.scroll, 'horas_trabajo_independiente_entry', 
             {'validate': 'key', 'validatecommand': (self.vcmd_num, '%P')}),
            ("Horas Totales:", crear_entry, {"width":300,"placeholder_text":"Ingrese horas"}, 1, self.scroll, 'horas_totales_entry', 
             {'validate': 'key', 'validatecommand': (self.vcmd_num, '%P')}),
        ], es_scroll=True)

        # Fila para otros datos de la Unidad Curricular
        self._crear_fila_widgets([
            ("Unidad de Crédito:", crear_entry, {"width":300,"placeholder_text":"Ingrese Unidad de crédito"}, 1, self.scroll, 'unidades_credito_entry', 
             {'validate': 'key', 'validatecommand': (self.vcmd_num, '%P')}),
            ("Tipo de U.C:", crear_option_menu, {"values": ["Obligatoria", "Electiva"], "width":300}, 1, self.scroll, 'tipo_menu'),
            ("Carácter:", crear_option_menu, {"values": ["Teórico", "Práctico", "Teórico-Práctico"], "width":300}, 1, self.scroll, 'caracter_menu'),
            ("Modalidad de Evaluación:", crear_option_menu, {"values": ["Presencial", "Semi-presencial", "A distancia"], "width":300}, 1, self.scroll, 'modalidad_menu'),
            ("Complejidad:", crear_option_menu, {"values": ["Baja", "Media", "Alta"], "width":300}, 1, self.scroll, 'complejidad_menu'),
            ("Prelaciones:", crear_entry, {"width": 300, "placeholder_text": "Ingrese prelaciones"}, 1, self.scroll, 'prelaciones_entry'),
        ], es_scroll=True)

        # Fila para competencias y saberes
        self._crear_fila_widgets([
            ("Competencias Genéricas:", crear_entry, {"width": 300, "placeholder_text": "Ingrese competencias genéricas"}, 1, self.scroll, 'competencias_genericas_entry'),
            ("Competencias Específicas:", crear_entry, {"width": 300, "placeholder_text": "Ingrese competencias específicas"}, 1, self.scroll, 'competencias_especificas_entry'),
        ], es_scroll=True)
        self._crear_fila_widgets([
            ("Saberes Cognitivos:", crear_entry, {"width": 300, "placeholder_text": "Ingrese saberes cognitivos"}, 1, self.scroll, 'saberes_cognitivos_entry'),
            ("Saberes Procedimentales:", crear_entry, {"width": 300, "placeholder_text": "Ingrese saberes procedimentales"}, 1, self.scroll, 'saberes_procedimentales_entry'),
            ("Saberes Actitudinales:", crear_entry, {"width": 300, "placeholder_text": "Ingrese saberes actitudinales"}, 1, self.scroll, 'saberes_actitudinales_entry'),
        ], es_scroll=True)

        # Fila para estrategias, recursos y evaluación
        self._crear_fila_widgets([
            ("Estrategias de Enseñanza:", crear_entry, {"width": 300, "placeholder_text": "Ingrese estrategias de enseñanza"}, 1, self.scroll, 'estrategias_ensenanza_entry'),
            ("Recursos Didácticos:", crear_entry, {"width": 300, "placeholder_text": "Ingrese recursos didácticos"}, 1, self.scroll, 'recursos_didacticos_entry'),
            ("Evaluación:", crear_entry, {"width": 300, "placeholder_text": "Ingrese criterios de evaluación"}, 1, self.scroll, 'evaluacion_entry'),
        ], es_scroll=True)

        # Fila para bibliografía, homologación y clave especial
        self._crear_fila_widgets([
            ("Bibliografía:", crear_entry, {"width": 300, "placeholder_text": "Ingrese bibliografía"}, 1, self.scroll, 'bibliografia_entry'),
            ("Homologación Clave:", crear_entry, {"width": 300, "placeholder_text": "Ingrese clave de homologación"}, 1, self.scroll, 'homologacion_clave_entry'),
            ("Clave Especial:", crear_entry, {"width": 300, "placeholder_text": "Ingrese clave especial"}, 1, self.scroll, 'clave_especial_entry'),
        ], es_scroll=True)

        # Fila para estado y fechas
        self._crear_fila_widgets([
            ("Estado:", crear_option_menu, {"values": ["activo", "inactivo"], "width": 300}, 1, self.scroll, 'estado_menu'),
            ("Fecha de Creación:", crear_entry, {"width": 300, "placeholder_text": "YYYY-MM-DD"}, 1, self.scroll, 'fecha_creacion_entry'),
            ("Fecha de Actualización:", crear_entry, {"width": 300, "placeholder_text": "YYYY-MM-DD"}, 1, self.scroll, 'fecha_actualizacion_entry'),
        ], es_scroll=True)

    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets

    def limpiar_formulario_completo(self):
        """
        Limpia todos los campos del formulario.
        """
        self.controlador.limpiar_formulario_completo(self)

    def set_datos(self, datos_uc):
        """
        Configura los campos del formulario con los datos de la Unidad Curricular.
        """
        self.codigo_entry.delete(0, ctk.END)
        if datos_uc.get("codigo"):
            self.codigo_entry.insert(0, datos_uc.get("codigo"))
        self.codigo_entry.configure(state="disabled")

        self.nombre_entry.delete(0, ctk.END)
        if datos_uc.get("nombre"):
            self.nombre_entry.insert(0, datos_uc.get("nombre"))
        self.nombre_entry.configure(state="disabled")

        self.nombre_corto_entry.delete(0, ctk.END)
        if datos_uc.get("nombre_corto"):
            self.nombre_corto_entry.insert(0, datos_uc.get("nombre_corto"))
        self.nombre_corto_entry.configure(state="disabled")

        self.area_entry.delete(0, ctk.END)
        if datos_uc.get("area"):
            self.area_entry.insert(0, datos_uc.get("area"))
        self.area_entry.configure(state="disabled")

        self.subarea_entry.delete(0, ctk.END)
        if datos_uc.get("subarea"):
            self.subarea_entry.insert(0, datos_uc.get("subarea"))
        self.subarea_entry.configure(state="disabled")

        self.eje_formativo_entry.delete(0, ctk.END)
        if datos_uc.get("eje_formativo"):
            self.eje_formativo_entry.insert(0, datos_uc.get("eje_formativo"))
        self.eje_formativo_entry.configure(state="disabled")
        
        self.horas_teoricas_entry.delete(0, ctk.END)
        if datos_uc.get("horas_teoricas"):
            self.horas_teoricas_entry.insert(0, datos_uc.get("horas_teoricas"))
        self.horas_teoricas_entry.configure(state="disabled")

        self.horas_practicas_entry.delete(0, ctk.END)
        if datos_uc.get("horas_practicas"):
            self.horas_practicas_entry.insert(0, datos_uc.get("horas_practicas"))
        self.horas_practicas_entry.configure(state="disabled")

        self.horas_laboratorio_entry.delete(0, ctk.END)
        if datos_uc.get("horas_laboratorio"):
            self.horas_laboratorio_entry.insert(0, datos_uc.get("horas_laboratorio"))
        self.horas_laboratorio_entry.configure(state="disabled")

        self.horas_trabajo_independiente_entry.delete(0, ctk.END)
        if datos_uc.get("horas_trabajo_independiente"):
            self.horas_trabajo_independiente_entry.insert(0, datos_uc.get("horas_trabajo_independiente"))
        self.horas_trabajo_independiente_entry.configure(state="disabled")

        self.horas_totales_entry.delete(0, ctk.END)
        if datos_uc.get("horas_totales"):
            self.horas_totales_entry.insert(0, datos_uc.get("horas_totales"))
        self.horas_totales_entry.configure(state="disabled")

        self.unidades_credito_entry.delete(0, ctk.END)
        if datos_uc.get("unidades_credito"):
            self.unidades_credito_entry.insert(0, datos_uc.get("unidades_credito"))
        self.unidades_credito_entry.configure(state="disabled")

        if datos_uc.get('tipo') != None:
            self.var_tipo.set(datos_uc.get("tipo"))
        else:
            self.var_tipo.set("Obligatoria")
        self.tipo_menu.configure(state="disabled")

        if datos_uc.get('caracter') != None:
            self.var_caracter.set(datos_uc.get("caracter"))
        else:
            self.var_caracter.set("Teórico")
        self.caracter_menu.configure(state="disabled")

        if datos_uc.get('modalidad') != None:
            self.var_modalidad.set(datos_uc.get("modalidad"))
        else:
            self.var_modalidad.set("Presencial")
        self.modalidad_menu.configure(state="disabled")

        if datos_uc.get('complejidad') != None:
            self.var_complejidad.set(datos_uc.get("complejidad"))
        else:
            self.var_complejidad.set("Baja")
        self.complejidad_menu.configure(state="disabled")

        self.prelaciones_entry.delete(0, ctk.END)
        if datos_uc.get("prelaciones"):
            self.prelaciones_entry.insert(0, datos_uc.get("prelaciones"))
        self.prelaciones_entry.configure(state="disabled")

        self.competencias_genericas_entry.delete(0, ctk.END)
        if datos_uc.get("competencias_genericas"):
            self.competencias_genericas_entry.insert(0, datos_uc.get("competencias_genericas"))
        self.competencias_genericas_entry.configure(state="disabled")

        self.competencias_especificas_entry.delete(0, ctk.END)
        if datos_uc.get("competencias_especificas"):
            self.competencias_especificas_entry.insert(0, datos_uc.get("competencias_especificas"))
        self.competencias_especificas_entry.configure(state="disabled")

        self.saberes_cognitivos_entry.delete(0, ctk.END)
        if datos_uc.get("saberes_cognitivos"):
            self.saberes_cognitivos_entry.insert(0, datos_uc.get("saberes_cognitivos"))
        self.saberes_cognitivos_entry.configure(state="disabled")

        self.saberes_procedimentales_entry.delete(0, ctk.END)
        if datos_uc.get("saberes_procedimentales"):
            self.saberes_procedimentales_entry.insert(0, datos_uc.get("saberes_procedimentales"))
        self.saberes_procedimentales_entry.configure(state="disabled")
        
        self.saberes_actitudinales_entry.delete(0, ctk.END)
        if datos_uc.get("saberes_actitudinales"):
            self.saberes_actitudinales_entry.insert(0, datos_uc.get("saberes_actitudinales"))  
        self.saberes_actitudinales_entry.configure(state="disabled")

        self.estrategias_ensenanza_entry.delete(0, ctk.END)
        if datos_uc.get("estrategias_ensenanza"):
            self.estrategias_ensenanza_entry.insert(0, datos_uc.get("estrategias_ensenanza"))
        self.estrategias_ensenanza_entry.configure(state="disabled")

        self.recursos_didacticos_entry.delete(0, ctk.END)
        if datos_uc.get("recursos_didacticos"):
            self.recursos_didacticos_entry.insert(0, datos_uc.get("recursos_didacticos"))
        self.recursos_didacticos_entry.configure(state="disabled")

        self.evaluacion_entry.delete(0, ctk.END)
        if datos_uc.get("evaluacion"):
            self.evaluacion_entry.insert(0, datos_uc.get("evaluacion"))
        self.evaluacion_entry.configure(state="disabled")

        self.bibliografia_entry.delete(0, ctk.END)
        if datos_uc.get("bibliografia"):
            self.bibliografia_entry.insert(0, datos_uc.get("bibliografia"))
        self.bibliografia_entry.configure(state="disabled")

        self.homologacion_clave_entry.delete(0, ctk.END)
        if datos_uc.get("homologacion_clave"):
            self.homologacion_clave_entry.insert(0, datos_uc.get("homologacion_clave"))
        self.homologacion_clave_entry.configure(state="disabled")

        self.clave_especial_entry.delete(0, ctk.END)
        if datos_uc.get("clave_especial"):
            self.clave_especial_entry.insert(0, datos_uc.get("clave_especial"))
        self.clave_especial_entry.configure(state="disabled")

        if datos_uc.get('estado') != None:
            self.var_estado.set(datos_uc.get("estado"))
        else:
            self.var_estado.set("activo")
        self.estado_menu.configure(state="disabled")

        self.fecha_creacion_entry.delete(0, ctk.END)
        if datos_uc.get("fecha_creacion"):
            self.fecha_creacion_entry.insert(0, datos_uc.get("fecha_creacion"))
        self.fecha_creacion_entry.configure(state="disabled")

        self.fecha_actualizacion_entry.delete(0, ctk.END)
        if datos_uc.get("fecha_actualizacion"):
            self.fecha_actualizacion_entry.insert(0, datos_uc.get("fecha_actualizacion"))
        self.fecha_actualizacion_entry.configure(state="disabled")

    def procesar_formulario(self, datos_uc=None):
        """
        Procesa el formulario y registra los datos de la Unidad Curricular.
        """
        datos_uc = self.obtener_todos_los_datos()
        # resultado = self.controlador.obtener_todos_los_datos(self)
        # exito = self.controlador.registrar_unidad_curricular(resultado, self)
        # if exito:
        #     self.controlador.limpiar_formulario_completo(self)
        print(datos_uc)

    def habilitar_campos(self):
        """
        Habilita todos los campos del formulario para edición.
        """
        for entry in self.scroll.winfo_children():
            if isinstance(entry, ctk.CTkEntry):
                entry.configure(state="normal")
            elif isinstance(entry, ctk.CTkOptionMenu):
                entry.configure(state="normal")
        
        self.btn_guardar.configure(state="normal")
        self.btn_cancelar.configure(state="normal")

