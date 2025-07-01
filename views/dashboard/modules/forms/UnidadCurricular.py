import customtkinter as ctk
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase
from views.dashboard.modules.forms.DatosPersonales import DatosPersonalesFrame
from controllers.dashboard.PNF.controller_pnf import ControllerPNF
import pprint

from config.app_config import AppConfig

class UnidadCurricular(SectionFrameBase):
    def __init__(self, master, vcmd_num, controlador=None):
        super().__init__(master, "Unidad Curricular PNF")
        self.vcmd_num = vcmd_num # Validación para números

        if controlador is not None:
            self.controlador = controlador
        else:
            self.controlador = ControllerPNF()
        #self.vcmd_fecha = vcmd_fecha # Guardar para usar en fechas

        #obtener la lista de pnf
        self.lista_pnf = self.controlador.listado_pnf
        self.lista_trayecto = self.controlador.listado_trayecto
        self.lista_tramo = self.controlador.listado_tramo
        # Crear mapeos id <-> nombre para PNF y Trayecto
        self.pnf_id_por_nombre = {tupla[2]: tupla[0] for tupla in self.lista_pnf}  # nombre: id
        self.trayecto_id_por_nombre = {tupla[1]: tupla[0] for tupla in self.lista_trayecto}  # nombre: id
        self.tramo_id_por_nombre = {tupla[1]: tupla[0] for tupla in self.lista_tramo}  # nombre: id
        self.nombre_pnf = self.obtener_nombre_pnf()
        self.nombre_trayecto = self.obtener_nombre_trayecto()
        self.nombre_tramo = self.obtener_nombre_tramo()
        self.var_tipo = ctk.StringVar(value="Obligatoria") # Variable para el tipo de U.C
        self.var_caracter = ctk.StringVar(value="Teórica") # Variable para el carácter de la U.C
        self.var_modalidad = ctk.StringVar(value="Presencial") # Variable para la modalidad de evaluación
        self.var_complejidad = ctk.StringVar(value="Básica") # Variable para la complejidad de la U.C
        self.var_estado = ctk.StringVar(value="activa") # Variable para el estado de la U.C

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=10, pady=10)
        self.evento_mouse()

        # Fila para los datos de la Unidad Curricular

        self._crear_fila_widgets([
            ("Código:", crear_entry, {"width":300,"placeholder_text":"Ingrese código"}, 1,  self.scroll, 'codigo_entry'),
            ("Nombre:", crear_entry, {"width":300,"placeholder_text":"Ingrese el nombre de la U.C"}, 1,  self.scroll, 'nombre_entry'),
            ("Nombre corto:", crear_entry, {"width":300,"placeholder_text":"Ingrese el nombre corto"}, 1,  self.scroll, 'nombre_corto_entry'),
            ("Área:", crear_entry, {"width":300,"placeholder_text":"Ingrese área"}, 1, self.scroll, 'area_entry'),
            ("Sub-area:", crear_entry, {"width":300,"placeholder_text":"Ingrese Sub-area"}, 1,  self.scroll, 'subarea_entry'),
            ("Eje Formativo:", crear_entry, {"width":300,"placeholder_text":"Ingrese el eje formativo"}, 1,  self.scroll, 'eje_formativo_entry'),
        ], es_scroll=True)
        
        # Fila para las horas de la Unidad Curricular
        self._crear_fila_widgets([
            ("Horas Teóricas:", crear_entry, {"width":300,"placeholder_text":"Ingrese horas"}, 1,  self.scroll, 'horas_teoricas_entry', 
             {'validate': 'key', 'validatecommand': (self.vcmd_num, '%P')}),
            ("Horas Prácticas:", crear_entry, {"width":300,"placeholder_text":"Ingrese horas"}, 1,  self.scroll, 'horas_practicas_entry', 
             {'validate': 'key', 'validatecommand': (self.vcmd_num, '%P')}),
            ("Horas Laboratorio:", crear_entry, {"width":300,"placeholder_text":"Ingrese horas"}, 1,  self.scroll, 'horas_laboratorio_entry', 
             {'validate': 'key', 'validatecommand': (self.vcmd_num, '%P')}),
            ("Horas Trabajo Independiente:", crear_entry, {"width":300,"placeholder_text":"Ingrese horas"}, 1,  self.scroll, 'horas_trabajo_independiente_entry', 
             {'validate': 'key', 'validatecommand': (self.vcmd_num, '%P')}),
            ("Horas Totales:", crear_entry, {"width":300,"placeholder_text":"Ingrese horas"}, 1,  self.scroll, 'horas_totales_entry', 
             {'validate': 'key', 'validatecommand': (self.vcmd_num, '%P')}),
        ], es_scroll=True)

        # Fila para otros datos de la Unidad Curricular
        self._crear_fila_widgets([
            ("Unidad de Crédito:", crear_entry, {"width":300,"placeholder_text":"Ingrese Unidad de crédito"}, 1,  self.scroll, 'unidades_credito_entry', 
             {'validate': 'key', 'validatecommand': (self.vcmd_num, '%P')}),
            ("Tipo de U.C:", crear_option_menu, {"values": ["Obligatoria", "Electiva"], "width":300}, 1,  self.scroll, 'tipo_menu'),
            ("Carácter:", crear_option_menu, {"values": ["Teórica", "Práctica", "Teórico-Práctica", "Laboratorio"], "width":300}, 1,  self.scroll, 'caracter_menu'),
            ("Modalidad de Evaluación:", crear_option_menu, {"values": ["Presencial", "Semi-presencial", "A distancia"], "width":300}, 1,  self.scroll, 'modalidad_menu'),
            ("Complejidad:", crear_option_menu, {"values": ["Básica", "Intermedia", "Avanzada"], "width":300}, 1,  self.scroll, 'complejidad_menu'),
            ("Prelaciones:", crear_entry, {"width": 300, "placeholder_text": "Ingrese prelaciones"}, 1,  self.scroll, 'prelaciones_entry'),
        ], es_scroll=True)

        # Fila para competencias y saberes
        self._crear_fila_widgets([
            ("Competencias Genéricas:", crear_entry, {"width": 300, "placeholder_text": "Ingrese competencias genéricas"}, 1,  self.scroll, 'competencias_genericas_entry'),
            ("Competencias Específicas:", crear_entry, {"width": 300, "placeholder_text": "Ingrese competencias específicas"}, 1,  self.scroll, 'competencias_especificas_entry'),
        ], es_scroll=True)
        self._crear_fila_widgets([
            ("Saberes Cognitivos:", crear_entry, {"width": 300, "placeholder_text": "Ingrese saberes cognitivos"}, 1,  self.scroll, 'saberes_cognitivos_entry'),
            ("Saberes Procedimentales:", crear_entry, {"width": 300, "placeholder_text": "Ingrese saberes procedimentales"}, 1,  self.scroll, 'saberes_procedimentales_entry'),
            ("Saberes Actitudinales:", crear_entry, {"width": 300, "placeholder_text": "Ingrese saberes actitudinales"}, 1,  self.scroll, 'saberes_actitudinales_entry'),
        ], es_scroll=True)

        # Fila para estrategias, recursos y evaluación
        self._crear_fila_widgets([
            ("Estrategias de Enseñanza:", crear_entry, {"width": 300, "placeholder_text": "Ingrese estrategias de enseñanza"}, 1,  self.scroll, 'estrategias_ensenanza_entry'),
            ("Recursos Didácticos:", crear_entry, {"width": 300, "placeholder_text": "Ingrese recursos didácticos"}, 1,  self.scroll, 'recursos_didacticos_entry'),
            ("Evaluación:", crear_entry, {"width": 300, "placeholder_text": "Ingrese criterios de evaluación"}, 1, self.scroll, 'evaluacion_entry'),
        ], es_scroll=True)

        # Fila para bibliografía, homologación y clave especial
        self._crear_fila_widgets([
            ("Bibliografía:", crear_entry, {"width": 300, "placeholder_text": "Ingrese bibliografía"}, 1,  self.scroll, 'bibliografia_entry'),
            ("Homologación Clave:", crear_entry, {"width": 300, "placeholder_text": "Ingrese clave de homologación"}, 1,  self.scroll, 'homologacion_clave_entry'),
            ("Clave Especial:", crear_entry, {"width": 300, "placeholder_text": "Ingrese clave especial"}, 1, self.scroll, 'clave_especial_entry'),
        ], es_scroll=True)

        # Fila para estado y fechas
        self._crear_fila_widgets([
            ("Estado:", crear_option_menu, {"values": ["activa", "inactiva", "revision"], "width": 300}, 1,  self.scroll, 'estado_menu'),
            # ("Fecha de Creación:", crear_entry, {"width": 300, "placeholder_text": "YYYY-MM-DD"}, 1,  self.scroll, 'fecha_creacion_entry'),
            # ("Fecha de Actualización:", crear_entry, {"width": 300, "placeholder_text": "YYYY-MM-DD"}, 1,  self.scroll, 'fecha_actualizacion_entry'),
        ], es_scroll=True)

        # Crear un frame para la fila de PNF, Trayecto y Tramo con etiquetas
        self.fila_pnf_trayecto_tramo = ctk.CTkFrame(self.scroll, fg_color="transparent")
        self.fila_pnf_trayecto_tramo.pack(fill="x", padx=10, pady=5)

        # Valores seguros por defecto si las listas están vacías
        valores_pnf = self.nombre_pnf if self.nombre_pnf else ["Sin opciones disponibles"]
        valores_trayecto = self.nombre_trayecto if self.nombre_trayecto else ["Sin opciones disponibles"]
        valores_tramo = self.nombre_tramo if self.nombre_tramo else ["Sin opciones disponibles"]

        # PNF
        pnf_frame = ctk.CTkFrame(self.fila_pnf_trayecto_tramo, fg_color="transparent")
        pnf_frame.pack(side="left", padx=10)
        pnf_label = ctk.CTkLabel(pnf_frame, text="PNF:", font=FUENTE_BASE, text_color=COLOR_TEXTO_PRINCIPAL)
        pnf_label.pack(side="left", padx=(0, 5))
        self.pnfmenu = ctk.CTkOptionMenu(
            pnf_frame, values=valores_pnf, command=self.actualizar_trayectos_por_pnf,
            font=FUENTE_BASE, fg_color=COLOR_ENTRY_BG, button_color=COLOR_BOTON_PRIMARIO_FG,
            text_color=COLOR_ENTRY_TEXT, dropdown_fg_color=COLOR_ENTRY_PLACEHOLDER
        )
        self.pnfmenu.pack(side="left")

        # Trayecto
        trayecto_frame = ctk.CTkFrame(self.fila_pnf_trayecto_tramo, fg_color="transparent")
        trayecto_frame.pack(side="left", padx=10)
        trayecto_label = ctk.CTkLabel(trayecto_frame, text="Trayecto:", font=FUENTE_BASE, text_color=COLOR_TEXTO_PRINCIPAL)
        trayecto_label.pack(side="left", padx=(0, 5))
        self.trayectomenu = ctk.CTkOptionMenu(
            trayecto_frame, values=valores_trayecto, command=self.actualizar_tramos_por_trayecto,
            font=FUENTE_BASE, fg_color=COLOR_ENTRY_BG, button_color=COLOR_BOTON_PRIMARIO_FG,
            text_color=COLOR_ENTRY_TEXT, dropdown_fg_color=COLOR_ENTRY_PLACEHOLDER
        )
        self.trayectomenu.pack(side="left")

        # Tramo
        tramo_frame = ctk.CTkFrame(self.fila_pnf_trayecto_tramo, fg_color="transparent")
        tramo_frame.pack(side="left", padx=10)
        tramo_label = ctk.CTkLabel(tramo_frame, text="Tramo:", font=FUENTE_BASE, text_color=COLOR_TEXTO_PRINCIPAL)
        tramo_label.pack(side="left", padx=(0, 5))
        self.tramomenu = ctk.CTkOptionMenu(
            tramo_frame, values=valores_tramo,
            font=FUENTE_BASE, fg_color=COLOR_ENTRY_BG, button_color=COLOR_BOTON_PRIMARIO_FG,
            text_color=COLOR_ENTRY_TEXT, dropdown_fg_color=COLOR_ENTRY_PLACEHOLDER
        )
        self.tramomenu.pack(side="left")


        # Empacar los frames
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=(25, 20))

        self.btn_guardar = ctk.CTkButton(self.button_frame, text="Grabar Datos", width=140, command=self.procesar_formulario,
                                        font=FUENTE_BOTON, fg_color=COLOR_BOTON_PRIMARIO_FG, hover_color=COLOR_BOTON_PRIMARIO_HOVER, 
                                        text_color=COLOR_BOTON_PRIMARIO_TEXT, state="disabled")
        self.btn_guardar.pack(side="left", padx=10)

        self.btn_cancelar = ctk.CTkButton(self.button_frame, text="Limpiar Campos", width=140, command=self.limpiar_formulario_completo,
                                        font=FUENTE_BOTON, fg_color=COLOR_BOTON_SECUNDARIO_FG, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, 
                                        text_color=COLOR_BOTON_SECUNDARIO_TEXT)
        self.btn_cancelar.pack(side="left", padx=10)

        # Crear alias en self para que el controlador acceda directo a los widgets dentro del scroll
        self.codigo_entry = self.scroll.codigo_entry
        self.nombre_entry = self.scroll.nombre_entry
        self.nombre_corto_entry = self.scroll.nombre_corto_entry
        self.area_entry = self.scroll.area_entry
        self.subarea_entry = self.scroll.subarea_entry
        self.eje_formativo_entry = self.scroll.eje_formativo_entry

        self.horas_teoricas_entry = self.scroll.horas_teoricas_entry
        self.horas_practicas_entry = self.scroll.horas_practicas_entry
        self.horas_laboratorio_entry = self.scroll.horas_laboratorio_entry
        self.horas_trabajo_independiente_entry = self.scroll.horas_trabajo_independiente_entry
        self.horas_totales_entry = self.scroll.horas_totales_entry

        self.unidades_credito_entry = self.scroll.unidades_credito_entry
        self.prelaciones_entry = self.scroll.prelaciones_entry

        self.competencias_genericas_entry = self.scroll.competencias_genericas_entry
        self.competencias_especificas_entry = self.scroll.competencias_especificas_entry

        self.saberes_cognitivos_entry = self.scroll.saberes_cognitivos_entry
        self.saberes_procedimentales_entry = self.scroll.saberes_procedimentales_entry
        self.saberes_actitudinales_entry = self.scroll.saberes_actitudinales_entry

        self.estrategias_ensenanza_entry = self.scroll.estrategias_ensenanza_entry
        self.recursos_didacticos_entry = self.scroll.recursos_didacticos_entry
        self.evaluacion_entry = self.scroll.evaluacion_entry

        self.bibliografia_entry = self.scroll.bibliografia_entry
        self.homologacion_clave_entry = self.scroll.homologacion_clave_entry
        self.clave_especial_entry = self.scroll.clave_especial_entry

        # self.fecha_creacion_entry = self.scroll.fecha_creacion_entry
        # self.fecha_actualizacion_entry = self.scroll.fecha_actualizacion_entry

        self.tipo_menu = self.scroll.tipo_menu
        self.caracter_menu = self.scroll.caracter_menu
        self.modalidad_menu = self.scroll.modalidad_menu
        self.complejidad_menu = self.scroll.complejidad_menu
        self.estado_menu = self.scroll.estado_menu

        # Bindings para validar al cambiar campos de texto
        for entry_name in [
            'codigo_entry', 'nombre_entry', 'nombre_corto_entry', 'area_entry', 'subarea_entry',
            'eje_formativo_entry', 'horas_teoricas_entry', 'horas_practicas_entry',
            'horas_laboratorio_entry', 'horas_trabajo_independiente_entry', 'horas_totales_entry',
            'unidades_credito_entry', 'prelaciones_entry', 'competencias_genericas_entry',
            'competencias_especificas_entry', 'saberes_cognitivos_entry', 'saberes_procedimentales_entry',
            'saberes_actitudinales_entry', 'estrategias_ensenanza_entry', 'recursos_didacticos_entry',
            'evaluacion_entry', 'bibliografia_entry', 'homologacion_clave_entry', 'clave_especial_entry'
            # 'fecha_creacion_entry', 'fecha_actualizacion_entry'
        ]:
            entry = getattr(self, entry_name, None)
            if entry:
                entry.bind("<KeyRelease>", lambda e: self.validar_estado_boton_guardar())

        # Bindings para OptionMenus
        self.tipo_menu.configure(command=lambda _: self.validar_estado_boton_guardar())
        self.caracter_menu.configure(command=lambda _: self.validar_estado_boton_guardar())
        self.modalidad_menu.configure(command=lambda _: self.validar_estado_boton_guardar())
        self.complejidad_menu.configure(command=lambda _: self.validar_estado_boton_guardar())
        self.estado_menu.configure(command=lambda _: self.validar_estado_boton_guardar())

        # Bindings para PNF, Trayecto y Tramo
        self.pnfmenu.configure(command=lambda _: [self.actualizar_trayectos_por_pnf(self.pnfmenu.get()), self.validar_estado_boton_guardar()])
        self.trayectomenu.configure(command=lambda _: [self.actualizar_tramos_por_trayecto(self.trayectomenu.get()), self.validar_estado_boton_guardar()])
        self.tramomenu.configure(command=lambda _: self.validar_estado_boton_guardar())

    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets

    def procesar_formulario(self):
        """
        Procesa el formulario de Unidad Curricular:
        - Captura datos de campos
        - Añade id_pnf, id_trayecto e id_tramo
        - Valida y envía al controlador
        """
        # Obtiene datos del formulario usando el controlador
        datos_uc = self.controlador.getUnidadCurricular(self)

        # Capturar nombres seleccionados
        nombre_pnf = self.pnfmenu.get()
        nombre_trayecto = self.trayectomenu.get()
        nombre_tramo = self.tramomenu.get()

        # Obtener IDs a partir de los nombres
        id_pnf = self.pnf_id_por_nombre.get(nombre_pnf)
        id_trayecto = self.trayecto_id_por_nombre.get(nombre_trayecto)
        id_tramo = self.tramo_id_por_nombre.get(nombre_tramo)

        # Agregar estos IDs al diccionario de datos_uc
        datos_uc['id_pnf'] = id_pnf
        datos_uc['id_trayecto'] = id_trayecto
        datos_uc['id_tramo'] = id_tramo

        pprint.pprint(datos_uc)  # Para verificar en consola

        # Valida campos obligatorios
        if not self.controlador.validar_campos_obligatorios_uc(datos_uc, self):
            return

        # Registra en el modelo usando el controlador
        exito = self.controlador.registrar_unidad_curricular(datos_uc, self)

        if exito:
            self.limpiar_formulario_completo()
            

    def limpiar_formulario_completo(self):
        """
        Limpia todos los campos del formulario y resetea los OptionMenu a valores por defecto.
        """
        entradas = [
            'codigo_entry', 'nombre_entry', 'nombre_corto_entry', 'area_entry', 'subarea_entry',
            'eje_formativo_entry', 'horas_teoricas_entry', 'horas_practicas_entry',
            'horas_laboratorio_entry', 'horas_trabajo_independiente_entry', 'horas_totales_entry',
            'unidades_credito_entry', 'prelaciones_entry', 'competencias_genericas_entry',
            'competencias_especificas_entry', 'saberes_cognitivos_entry', 'saberes_procedimentales_entry',
            'saberes_actitudinales_entry', 'estrategias_ensenanza_entry', 'recursos_didacticos_entry',
            'evaluacion_entry', 'bibliografia_entry', 'homologacion_clave_entry', 'clave_especial_entry'
            # 'fecha_creacion_entry', 'fecha_actualizacion_entry'
        ]
        for entry_name in entradas:
            entry = getattr(self, entry_name, None)
            if entry:
                entry.delete(0, 'end')

        # Resetear OptionMenus a valores por defecto
        self.tipo_menu.set("Obligatoria")
        self.caracter_menu.set("Teórico")
        self.modalidad_menu.set("Presencial")
        self.complejidad_menu.set("Baja")
        self.estado_menu.set("activo")

    def evento_mouse(self):
        """
        Habilita el scroll con la rueda del mouse en el CTkScrollableFrame para Windows, Mac y Linux.
        """
        canvas = self.scroll._parent_canvas  # Accede al canvas del scroll
        # Windows y Mac
        canvas.bind_all("<MouseWheel>", self.movimiento_mouse)
        # Linux
        canvas.bind_all("<Button-4>", self.movimiento_mouse)
        canvas.bind_all("<Button-5>", self.movimiento_mouse)

    def movimiento_mouse(self, event):
        """
        Controla el movimiento del scroll con el mouse en distintas plataformas.
        """
        canvas = self.scroll._parent_canvas
        if event.num == 4:  # Linux scroll up
            canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # Linux scroll down
            canvas.yview_scroll(1, "units")
        else:  # Windows/Mac
            velocidad = 16
            canvas.yview_scroll(int(-1*(event.delta/60)* velocidad), "units")

    def obtener_nombre_pnf(self):
        nombre_pnf = []
        if self.lista_pnf:
            for tupla in self.lista_pnf:
                nombre_pnf.append(tupla[2])
        return nombre_pnf
    
    def obtener_nombre_trayecto(self):
        nombre_trayecto = []
        if self.lista_trayecto:
            for tupla in self.lista_trayecto:
                nombre_trayecto.append(tupla[1])
        return nombre_trayecto
    
    def obtener_nombre_tramo(self):
        nombre_tramo = []
        if self.lista_tramo:
            for tupla in self.lista_tramo:
                nombre_tramo.append(tupla[1])
        return nombre_tramo
    
    def actualizar_trayectos_por_pnf(self, nombre_pnf):
        pnf_id = self.pnf_id_por_nombre.get(nombre_pnf)
        if pnf_id:
            nuevos_trayectos = self.controlador.obtener_trayectos_por_pnf(pnf_id)
            nombres_trayectos = [t[1] for t in nuevos_trayectos] if nuevos_trayectos else ["Sin opciones disponibles"]
            # Actualizar OptionMenu de trayectos
            self.trayectomenu.configure(values=nombres_trayectos)
            if nombres_trayectos:
                self.trayectomenu.set(nombres_trayectos[0])
            # Actualizar mapeo de trayectos
            self.trayecto_id_por_nombre = {t[1]: t[0] for t in nuevos_trayectos} if nuevos_trayectos else {}

            # También limpiar tramos si cambió el PNF
            self.tramomenu.configure(values=["Seleccione un trayecto primero"])
            self.tramomenu.set("Seleccione un trayecto primero")
        else:
            print(f"No se encontró ID para PNF: {nombre_pnf}")

    def actualizar_tramos_por_trayecto(self, nombre_trayecto):
        """
        Actualiza el OptionMenu de tramos según el trayecto seleccionado.
        """
        trayecto_id = self.trayecto_id_por_nombre.get(nombre_trayecto)
        if trayecto_id:
            nuevos_tramos = self.controlador.obtener_tramos_por_trayecto(trayecto_id)
            nombres_tramos = [t[1] for t in nuevos_tramos] if nuevos_tramos else ["Sin opciones disponibles"]

            # Actualiza los valores en el OptionMenu de tramos
            self.tramomenu.configure(values=nombres_tramos)
            if nombres_tramos:
                self.tramomenu.set(nombres_tramos[0])  # Selecciona automáticamente el primero

            # Actualiza el mapeo de nombre -> id para los tramos
            self.tramo_id_por_nombre = {t[1]: t[0] for t in nuevos_tramos} if nuevos_tramos else {}
        else:
            print(f"[INFO] No se encontró ID para Trayecto seleccionado: {nombre_trayecto}")
            self.tramomenu.configure(values=["Sin opciones disponibles"])
            self.tramomenu.set("Sin opciones disponibles")
            self.tramo_id_por_nombre = {}

    def validar_estado_boton_guardar(self):
        """
        Obtiene los datos actuales del formulario y llama al controlador para validar,
        habilitando o deshabilitando el botón de guardar según corresponda.
        """
        datos_uc = self.controlador.getUnidadCurricular(self)

        # Captura ids actuales de PNF, Trayecto y Tramo
        nombre_pnf = self.pnfmenu.get()
        nombre_trayecto = self.trayectomenu.get()
        nombre_tramo = self.tramomenu.get()

        id_pnf = self.pnf_id_por_nombre.get(nombre_pnf)
        id_trayecto = self.trayecto_id_por_nombre.get(nombre_trayecto)
        id_tramo = self.tramo_id_por_nombre.get(nombre_tramo)

        datos_uc['id_pnf'] = id_pnf
        datos_uc['id_trayecto'] = id_trayecto
        datos_uc['id_tramo'] = id_tramo

        # Validar y gestionar el botón
        self.controlador.validar_campos_obligatorios_uc(datos_uc, self)