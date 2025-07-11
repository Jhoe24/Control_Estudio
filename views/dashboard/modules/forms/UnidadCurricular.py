import customtkinter as ctk
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase
from views.dashboard.modules.forms.DatosPersonales import DatosPersonalesFrame
from controllers.dashboard.PNF.controller_pnf import ControllerPNF
import pprint

from config.app_config import AppConfig

class UnidadCurricular(SectionFrameBase):
    def __init__(self, master, vcmd_num, controlador=None, mostrar_botones=True):
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
            ("Modalidad de Evaluación:", crear_option_menu, {"values": ["Presencial", "Semipresencial", "Virtual"], "width":300}, 1,  self.scroll, 'modalidad_menu'),
            ("Complejidad:", crear_option_menu, {"values": ["Básica", "Intermedia", "Avanzada"], "width":300}, 1,  self.scroll, 'complejidad_menu'),
        ], es_scroll=True)

        # Fila para bibliografía, homologación y clave especial
        self._crear_fila_widgets([
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
        if mostrar_botones:
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
        else:
            self.button_frame = None
            self.btn_guardar = None
            self.btn_cancelar = None

        # Crear alias en self para que el controlador acceda directo a los widgets dentro del scroll
        self.codigo_entry = self.scroll.codigo_entry
        self.nombre_entry = self.scroll.nombre_entry
        self.nombre_corto_entry = self.scroll.nombre_corto_entry
        self.area_entry = self.scroll.area_entry
        self.subarea_entry = self.scroll.subarea_entry

        self.horas_teoricas_entry = self.scroll.horas_teoricas_entry
        self.horas_practicas_entry = self.scroll.horas_practicas_entry
        self.horas_laboratorio_entry = self.scroll.horas_laboratorio_entry
        self.horas_trabajo_independiente_entry = self.scroll.horas_trabajo_independiente_entry
        self.horas_totales_entry = self.scroll.horas_totales_entry

        self.unidades_credito_entry = self.scroll.unidades_credito_entry
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
            'horas_teoricas_entry', 'horas_practicas_entry',
            'horas_laboratorio_entry', 'horas_trabajo_independiente_entry', 'horas_totales_entry',
            'unidades_credito_entry', 'clave_especial_entry'
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

        # pprint.pprint(datos_uc)  # Para verificar en consola

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
            'horas_teoricas_entry', 'horas_practicas_entry',
            'horas_laboratorio_entry', 'horas_trabajo_independiente_entry', 'horas_totales_entry',
            'unidades_credito_entry', 'clave_especial_entry'
            # 'fecha_creacion_entry', 'fecha_actualizacion_entry'
        ]
        for entry_name in entradas:
            entry = getattr(self, entry_name, None)
            if entry:
                entry.delete(0, 'end')

        # Resetear OptionMenus a valores por defecto
        self.tipo_menu.set("Obligatoria")
        self.caracter_menu.set("Teórica")
        self.modalidad_menu.set("Presencial")
        self.complejidad_menu.set("Básica")
        self.estado_menu.set("activa")

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
    
    def set_datos(self, datos):
        """
        Establece los datos del formulario con un diccionario de datos.
        Maneja valores None y opciones no válidas en OptionMenus.
        """
        def valor_seguro(valor, default=''):
            """Convierte None a string vacío o valor por defecto"""
            return str(valor) if valor is not None else default
        
        def obtener_valor_option_menu(valor, opciones_validas, default):
            """Obtiene un valor válido para OptionMenu o retorna el valor actual si no está en las opciones"""
            if valor is None:
                return default
            if valor in opciones_validas:
                return valor
            # Si el valor no está en las opciones válidas, lo retorna tal como está
            return str(valor)
        
        # Crear mapeos inversos para PNF, Trayecto y Tramo
        pnf_nombre_por_id = {v: k for k, v in self.pnf_id_por_nombre.items()}
        trayecto_nombre_por_id = {v: k for k, v in self.trayecto_id_por_nombre.items()}
        tramo_nombre_por_id = {v: k for k, v in self.tramo_id_por_nombre.items()}
        
        # Rellenar campos de texto básicos
        self.codigo_entry.delete(0, 'end')
        self.codigo_entry.insert(0, valor_seguro(datos.get('codigo')))
        
        self.nombre_entry.delete(0, 'end')
        self.nombre_entry.insert(0, valor_seguro(datos.get('nombre')))
        
        self.nombre_corto_entry.delete(0, 'end')
        self.nombre_corto_entry.insert(0, valor_seguro(datos.get('nombre_corto')))
        
        self.area_entry.delete(0, 'end')
        self.area_entry.insert(0, valor_seguro(datos.get('area')))
        
        self.subarea_entry.delete(0, 'end')
        self.subarea_entry.insert(0, valor_seguro(datos.get('subarea')))

        # Rellenar campos numéricos (horas)
        self.horas_teoricas_entry.delete(0, 'end')
        self.horas_teoricas_entry.insert(0, valor_seguro(datos.get('horas_teoricas'), '0'))
        
        self.horas_practicas_entry.delete(0, 'end')
        self.horas_practicas_entry.insert(0, valor_seguro(datos.get('horas_practicas'), '0'))
        
        self.horas_laboratorio_entry.delete(0, 'end')
        self.horas_laboratorio_entry.insert(0, valor_seguro(datos.get('horas_laboratorio'), '0'))
        
        self.horas_trabajo_independiente_entry.delete(0, 'end')
        self.horas_trabajo_independiente_entry.insert(0, valor_seguro(datos.get('horas_trabajo_independiente'), '0'))
        
        self.horas_totales_entry.delete(0, 'end')
        self.horas_totales_entry.insert(0, valor_seguro(datos.get('horas_totales'), '0'))

        # Rellenar unidades de crédito
        self.unidades_credito_entry.delete(0, 'end')
        self.unidades_credito_entry.insert(0, valor_seguro(datos.get('unidades_credito'), '1'))

        # Rellenar clave especial
        self.clave_especial_entry.delete(0, 'end')
        self.clave_especial_entry.insert(0, valor_seguro(datos.get('clave_especial')))

        # Rellenar OptionMenus con validación
        opciones_tipo = ["Obligatoria", "Electiva"]
        valor_tipo = obtener_valor_option_menu(datos.get('tipo'), opciones_tipo, 'Obligatoria')
        if valor_tipo not in opciones_tipo:
            # Si el valor no está en las opciones, agregarlo temporalmente
            self.tipo_menu.configure(values=opciones_tipo + [valor_tipo])
        self.tipo_menu.set(valor_tipo)

        opciones_caracter = ["Teórica", "Práctica", "Teórico-Práctica", "Laboratorio"]
        valor_caracter = obtener_valor_option_menu(datos.get('caracter'), opciones_caracter, 'Teórica')
        if valor_caracter not in opciones_caracter:
            self.caracter_menu.configure(values=opciones_caracter + [valor_caracter])
        self.caracter_menu.set(valor_caracter)

        opciones_modalidad = ["Presencial", "Semipresencial", "Virtual"]
        valor_modalidad = obtener_valor_option_menu(datos.get('modalidad'), opciones_modalidad, 'Presencial')
        if valor_modalidad not in opciones_modalidad:
            self.modalidad_menu.configure(values=opciones_modalidad + [valor_modalidad])
        self.modalidad_menu.set(valor_modalidad)

        opciones_complejidad = ["Básica", "Intermedia", "Avanzada"]
        valor_complejidad = obtener_valor_option_menu(datos.get('complejidad'), opciones_complejidad, 'Básica')
        if valor_complejidad not in opciones_complejidad:
            self.complejidad_menu.configure(values=opciones_complejidad + [valor_complejidad])
        self.complejidad_menu.set(valor_complejidad)

        opciones_estado = ["activa", "inactiva", "revision"]
        valor_estado = obtener_valor_option_menu(datos.get('estado'), opciones_estado, 'activa')
        if valor_estado not in opciones_estado:
            self.estado_menu.configure(values=opciones_estado + [valor_estado])
        self.estado_menu.set(valor_estado)

        # Rellenar PNF, Trayecto y Tramo
        pnf_id = datos.get("pnf_id")
        if pnf_id is not None:
            pnf_nombre = pnf_nombre_por_id.get(pnf_id)
            if pnf_nombre:
                self.pnfmenu.set(pnf_nombre)
                # Actualizar trayectos basado en el PNF seleccionado
                self.actualizar_trayectos_por_pnf(pnf_nombre)
            else:
                # Si no encuentra el PNF, mostrar el ID
                valores_pnf_actuales = list(self.pnfmenu.cget("values"))
                valor_pnf_display = f"ID: {pnf_id}"
                if valor_pnf_display not in valores_pnf_actuales:
                    self.pnfmenu.configure(values=valores_pnf_actuales + [valor_pnf_display])
                self.pnfmenu.set(valor_pnf_display)
        else:
            # Si no hay PNF seleccionado, usar el primero disponible
            valores_pnf = list(self.pnfmenu.cget("values"))
            if valores_pnf:
                self.pnfmenu.set(valores_pnf[0])

        trayecto_id = datos.get("trayecto_id")
        if trayecto_id is not None:
            trayecto_nombre = trayecto_nombre_por_id.get(trayecto_id)
            if trayecto_nombre:
                self.trayectomenu.set(trayecto_nombre)
                # Actualizar tramos basado en el trayecto seleccionado
                self.actualizar_tramos_por_trayecto(trayecto_nombre)
            else:
                # Si no encuentra el trayecto, mostrar el ID
                valores_trayecto_actuales = list(self.trayectomenu.cget("values"))
                valor_trayecto_display = f"ID: {trayecto_id}"
                if valor_trayecto_display not in valores_trayecto_actuales:
                    self.trayectomenu.configure(values=valores_trayecto_actuales + [valor_trayecto_display])
                self.trayectomenu.set(valor_trayecto_display)
        else:
            # Si no hay trayecto seleccionado, usar el primero disponible
            valores_trayecto = list(self.trayectomenu.cget("values"))
            if valores_trayecto:
                self.trayectomenu.set(valores_trayecto[0])

        tramo_id = datos.get("tramo_id")
        if tramo_id is not None:
            # Actualizar el mapeo de tramos después de actualizar por trayecto
            tramo_nombre_por_id = {v: k for k, v in self.tramo_id_por_nombre.items()}
            tramo_nombre = tramo_nombre_por_id.get(tramo_id)
            if tramo_nombre:
                self.tramomenu.set(tramo_nombre)
            else:
                # Si no encuentra el tramo, mostrar el ID
                valores_tramo_actuales = list(self.tramomenu.cget("values"))
                valor_tramo_display = f"ID: {tramo_id}"
                if valor_tramo_display not in valores_tramo_actuales:
                    self.tramomenu.configure(values=valores_tramo_actuales + [valor_tramo_display])
                self.tramomenu.set(valor_tramo_display)
        else:
            # Si no hay tramo seleccionado, usar el primero disponible
            valores_tramo = list(self.tramomenu.cget("values"))
            if valores_tramo:
                self.tramomenu.set(valores_tramo[0])

        # Validar estado del botón guardar al final
        self.validar_estado_boton_guardar()

    def deshabilitar_campos(self):
        """
        Deshabilita todos los campos del formulario.
        """
        entradas = [
            'codigo_entry', 'nombre_entry', 'nombre_corto_entry', 'area_entry', 'subarea_entry',
            'horas_teoricas_entry', 'horas_practicas_entry',
            'horas_laboratorio_entry', 'horas_trabajo_independiente_entry', 'horas_totales_entry',
            'unidades_credito_entry', 'clave_especial_entry'
            # 'fecha_creacion_entry', 'fecha_actualizacion_entry'
        ]
        for entry_name in entradas:
            entry = getattr(self, entry_name, None)
            if entry:
                entry.configure(state="disabled")

        # Deshabilitar OptionMenus
        self.tipo_menu.configure(state="disabled")
        self.caracter_menu.configure(state="disabled")
        self.modalidad_menu.configure(state="disabled")
        self.complejidad_menu.configure(state="disabled")
        self.estado_menu.configure(state="disabled")

        self.pnfmenu.configure(state="disabled")
        self.trayectomenu.configure(state="disabled")
        self.tramomenu.configure(state="disabled")
        
        # Deshabilitar botones solo si existen
        if self.btn_guardar:
            self.btn_guardar.configure(state="disabled")
        if self.btn_cancelar:
            self.btn_cancelar.configure(state="disabled")
        
    def habilitar_campos(self):
        """
        Habilita todos los campos del formulario.
        """
        entradas = [
            'codigo_entry', 'nombre_entry', 'nombre_corto_entry', 'area_entry', 'subarea_entry',
            'horas_teoricas_entry', 'horas_practicas_entry',
            'horas_laboratorio_entry', 'horas_trabajo_independiente_entry', 'horas_totales_entry',
            'unidades_credito_entry', 'clave_especial_entry'
            # 'fecha_creacion_entry', 'fecha_actualizacion_entry'
        ]
        for entry_name in entradas:
            entry = getattr(self, entry_name, None)
            if entry:
                entry.configure(state="normal")

        # Habilitar OptionMenus
        self.tipo_menu.configure(state="normal")
        self.caracter_menu.configure(state="normal")
        self.modalidad_menu.configure(state="normal")
        self.complejidad_menu.configure(state="normal")
        self.estado_menu.configure(state="normal")
        self.pnfmenu.configure(state="normal")
        self.trayectomenu.configure(state="normal")
        self.tramomenu.configure(state="normal")

        # Habilitar botón guardar si lo necesitas
        if self.btn_guardar:
            self.btn_guardar.configure(state="normal")
        if self.btn_cancelar:
            self.btn_cancelar.configure(state="normal")