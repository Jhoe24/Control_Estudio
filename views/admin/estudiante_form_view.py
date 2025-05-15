# views/admin/estudiante_form_view.py
import customtkinter as ctk
import tkinter as tk
import tkinter.messagebox as messagebox

# --- CONSTANTES DE COLOR Y FUENTE ---
COLOR_FONDO_FORMULARIO = "white"
COLOR_TEXTO_PRINCIPAL = "#212529"
COLOR_TEXTO_SECUNDARIO = "#495057"
COLOR_HEADER_SECCION_BG = "#e9ecef"
COLOR_HEADER_SECCION_TEXT = "#343a40"
COLOR_ENTRY_BG = "#FFFFFF"
COLOR_ENTRY_BORDER = "#ced4da"
COLOR_ENTRY_TEXT = "#212529"
COLOR_ENTRY_PLACEHOLDER = "#6c757d"
COLOR_BOTON_PRIMARIO_FG = "#007bff"
COLOR_BOTON_PRIMARIO_HOVER = "#0056b3"
COLOR_BOTON_PRIMARIO_TEXT = "white"
COLOR_BOTON_SECUNDARIO_FG = "#6c757d"
COLOR_BOTON_SECUNDARIO_HOVER = "#545b62"
COLOR_BOTON_SECUNDARIO_TEXT = "white"

FUENTE_BASE = ("Roboto", 13)
FUENTE_TITULO_FORMULARIO = ("Roboto", 18, "bold")
FUENTE_HEADER_SECCION = ("Roboto", 14, "bold")
FUENTE_LABEL_CAMPO = ("Roboto", 13)
FUENTE_BOTON = ("Roboto", 13, "bold")

PADX_LABEL = (0, 5)
PADX_ENTRY = (0, 0)
PADY_FILA = (5, 5)


class SectionFrameBase(ctk.CTkFrame):
    def __init__(self, master, header_text):
        super().__init__(master, fg_color="transparent")
        self.pack(fill="x", pady=(0, 15), padx=10, expand="True")

        if header_text:
            header_label = ctk.CTkLabel(self, text=f" {header_text} ", text_color=COLOR_HEADER_SECCION_TEXT,
                                        fg_color=COLOR_HEADER_SECCION_BG, font=FUENTE_HEADER_SECCION,
                                        height=30, corner_radius=6)
            header_label.pack(fill="x", pady=(0, 10), padx=0)

    # Definición base de _crear_fila_widgets, aunque las clases hijas lo sobreescriben o reasignan.
    def _crear_fila_widgets(self, widgets_info):
        frame_fila = ctk.CTkFrame(self, fg_color="transparent")
        frame_fila.pack(fill="x", pady=PADY_FILA, padx=15)

        col_index = 0
        for label_text, widget_creator_func, widget_creator_args, widget_span in widgets_info:
            widget_obj = widget_creator_func(frame_fila, **widget_creator_args)

            if label_text:
                label = ctk.CTkLabel(frame_fila, text=label_text, font=FUENTE_LABEL_CAMPO, text_color=COLOR_TEXTO_PRINCIPAL, anchor="w")
                label.grid(row=0, column=col_index, sticky="w", padx=PADX_LABEL)
                col_index += 1

            widget_obj.grid(row=0, column=col_index, sticky="ew", columnspan=widget_span, padx=PADX_ENTRY)
            col_index += widget_span

            if widget_span > 0 :
                for i in range(widget_span):
                    frame_fila.grid_columnconfigure(col_index - widget_span + i, weight=1 if widget_span > 1 else 0)


# --- Funciones creadoras de widgets ---
def crear_entry(master, **kwargs):
    return ctk.CTkEntry(master, font=FUENTE_BASE, text_color=COLOR_ENTRY_TEXT, fg_color=COLOR_ENTRY_BG, border_color=COLOR_ENTRY_BORDER, placeholder_text_color=COLOR_ENTRY_PLACEHOLDER, **kwargs)

def crear_option_menu(master, **kwargs):
    return ctk.CTkOptionMenu(master, font=FUENTE_BASE, fg_color=COLOR_ENTRY_BG, button_color=COLOR_BOTON_PRIMARIO_FG, text_color=COLOR_ENTRY_TEXT, dropdown_fg_color=COLOR_ENTRY_PLACEHOLDER, **kwargs)

def crear_check_box(master, **kwargs):
    return ctk.CTkCheckBox(master, font=FUENTE_BASE, text_color=COLOR_TEXTO_PRINCIPAL, border_color=COLOR_ENTRY_BORDER, **kwargs)

def crear_radio_button(master, **kwargs):
    return ctk.CTkRadioButton(master, font=FUENTE_BASE, text_color=COLOR_TEXTO_PRINCIPAL, border_color=COLOR_ENTRY_BORDER, fg_color=COLOR_BOTON_PRIMARIO_FG, hover_color=COLOR_BOTON_PRIMARIO_HOVER, **kwargs)


class DatosPersonalesFrame(SectionFrameBase):
    def __init__(self, master, vcmd_num, vcmd_fecha):
        super().__init__(master, header_text="Datos Personales")

        self.tipo_documento_var = ctk.StringVar(value="Cédula") # Valor por defecto: Cédula
        self.vcmd_num = vcmd_num # Guardar para usar en nro_documento_entry y teléfonos
        self.vcmd_fecha = vcmd_fecha # Guardar para usar en fechas

        # --- Fila para Tipo y Número de Documento (Reemplaza Cédula entry) ---
        self.frame_tipo_numero_doc = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_tipo_numero_doc.pack(fill="x", pady=PADY_FILA, padx=15)

        label_doc_principal = ctk.CTkLabel(self.frame_tipo_numero_doc, text="Documento:", font=FUENTE_LABEL_CAMPO, text_color=COLOR_TEXTO_PRINCIPAL, anchor="w")
        label_doc_principal.grid(row=0, column=0, sticky="w", padx=PADX_LABEL)

        radio_button_container = ctk.CTkFrame(self.frame_tipo_numero_doc, fg_color="transparent")
        radio_button_container.grid(row=0, column=1, sticky="w", padx=(0,15))

        self.radio_cedula = crear_radio_button(radio_button_container, text="Cédula", variable=self.tipo_documento_var, value="Cédula", command=self._actualizar_estado_nro_doc)
        self.radio_cedula.pack(side="left", padx=(0, 5), pady=0)

        self.radio_pasaporte = crear_radio_button(radio_button_container, text="Pasaporte", variable=self.tipo_documento_var, value="Pasaporte", command=self._actualizar_estado_nro_doc)
        self.radio_pasaporte.pack(side="left", padx=(0, 5), pady=0)

        self.radio_sindoc = crear_radio_button(radio_button_container, text="Sin Doc.", variable=self.tipo_documento_var, value="Sin Documento", command=self._actualizar_estado_nro_doc)
        self.radio_sindoc.pack(side="left", padx=(0, 0), pady=0)

        self.label_nro_doc = ctk.CTkLabel(self.frame_tipo_numero_doc, text="Nro. Cédula:", font=FUENTE_LABEL_CAMPO, text_color=COLOR_TEXTO_PRINCIPAL, anchor="w")
        self.label_nro_doc.grid(row=0, column=2, sticky="w", padx=PADX_LABEL)

        self.nro_documento_entry = crear_entry(self.frame_tipo_numero_doc, width=170, validate="key", validatecommand=(self.vcmd_num, "%S"))
        self.nro_documento_entry.grid(row=0, column=3, sticky="ew", padx=PADX_ENTRY)
        self.frame_tipo_numero_doc.grid_columnconfigure(3, weight=1) # Permitir que el entry se expanda
        self._actualizar_estado_nro_doc() # Llamada inicial para configurar el estado
        # --- Fin Fila Documento ---

        self._crear_fila_widgets([
            ("Nombres:", crear_entry, {"width":200}, 2, self, 'nombre_entry'),
            ("Apellidos:", crear_entry, {"width":200}, 2, self, 'apellido_entry')
        ])
        self._crear_fila_widgets([
            ("Género:", crear_option_menu, {"values":["Masculino", "Femenino"], "command": lambda v: setattr(self.genero_menu, '_current_value',v)}, 1, self, 'genero_menu', lambda w: w.set("Masculino")),
            ("Edo Civil:", crear_option_menu, {"values":["Soltero", "Casado", "Divorciado"], "command": lambda v: setattr(self.edo_civil_menu, '_current_value',v)}, 1, self, 'edo_civil_menu', lambda w: w.set("Soltero"))
        ])
        self._crear_fila_widgets([
            ("Nacionalidad:", crear_entry, {"width":150}, 1, self, 'nacionalidad_entry'),
        ])
        self._crear_fila_widgets([
            ("F. Nacimiento:", crear_entry, {"width":120, "validate":"key", "validatecommand":(self.vcmd_fecha, "%S"), "placeholder_text":"dd/mm/aaaa"}, 1, self, 'fnac_entry'),
            ("Lugar Nacimiento:", crear_entry, {"width":200}, 2, self, 'lugar_nac_entry'),
            ("F. Ingreso:", crear_entry, {"width":120, "validate":"key", "validatecommand":(self.vcmd_fecha, "%S"), "placeholder_text":"dd/mm/aaaa"}, 1, self, 'fingreso_entry')
        ])
        self._crear_fila_widgets([
            ("Correo Electrónico:", crear_entry, {"width":200}, 2, self, 'correo_electronico_entry')
        ])
        self._crear_fila_widgets([
            ("Tel. Principal:", crear_entry, {"width":150, "validate":"key", "validatecommand":(self.vcmd_num, "%S")}, 1, self, 'telefono_principal_entry'),
            ("Tel. Secundario:", crear_entry, {"width":150, "validate":"key", "validatecommand":(self.vcmd_num, "%S")}, 1, self, 'telefono_secundario_entry')
        ])
        self._crear_fila_widgets([
            ("Condición:", crear_option_menu, {"values":["Regular", "Repitiente", "Reingreso", "Transferencia"], "command": lambda v: setattr(self.condicion_menu, '_current_value',v)}, 1, self, 'condicion_menu', lambda w: w.set("Regular"))
        ])

    def _actualizar_estado_nro_doc(self, _=None): # Acepta un argumento opcional por el command
        tipo_doc = self.tipo_documento_var.get()
        if tipo_doc == "Cédula":
            self.label_nro_doc.configure(text="Nro. Cédula:")
            self.nro_documento_entry.configure(state="normal", placeholder_text="Ingrese cédula")
        elif tipo_doc == "Pasaporte":
            self.label_nro_doc.configure(text="Nro. Pasaporte:")
            self.nro_documento_entry.configure(state="normal", placeholder_text="Ingrese pasaporte")
        elif tipo_doc == "Sin Documento":
            self.label_nro_doc.configure(text="") # Ocultar o vaciar label
            self.nro_documento_entry.delete(0, 'end')
            self.nro_documento_entry.configure(state="disabled", placeholder_text="")
        else: # Estado por defecto o inesperado
            self.label_nro_doc.configure(text="Número:")
            self.nro_documento_entry.configure(state="disabled", placeholder_text="")

    # Sobreescribir _crear_fila_widgets para asignar a self
    def _crear_fila_widgets(self, widgets_info_list_of_tuples):
        for widgets_info_tuple in widgets_info_list_of_tuples:
            label_text, widget_creator_func, widget_creator_args, widget_span, target_object, attr_name, *optional_setter = widgets_info_tuple

            frame_fila = ctk.CTkFrame(self, fg_color="transparent")
            frame_fila.pack(fill="x", pady=PADY_FILA, padx=15)

            col_index = 0
            widget_obj = widget_creator_func(frame_fila, **widget_creator_args)
            setattr(target_object, attr_name, widget_obj)

            if optional_setter and callable(optional_setter[0]):
                optional_setter[0](widget_obj)

            if label_text:
                label = ctk.CTkLabel(frame_fila, text=label_text, font=FUENTE_LABEL_CAMPO, text_color=COLOR_TEXTO_PRINCIPAL, anchor="w")
                label.grid(row=0, column=col_index, sticky="w", padx=PADX_LABEL)
                col_index += 1

            widget_obj.grid(row=0, column=col_index, sticky="ew", columnspan=widget_span, padx=PADX_ENTRY)
            col_index += widget_span

            if widget_span > 0:
                for i in range(widget_span):
                    frame_fila.grid_columnconfigure(col_index - widget_span + i, weight=1 if widget_span > 1 else 0)


class InformacionAcademicaFrame(SectionFrameBase):
    def __init__(self, master, vcmd_fecha, vcmd_decimal):
        super().__init__(master, header_text="Información Académica")
        self._crear_fila_widgets([
            ("Mención:", crear_option_menu, {"values":["Profesional", "Técnico Superior Universitario", "Bachiller"], "command": lambda v: setattr(self.tipo_inst_menu, '_current_value',v)}, 1, self, 'tipo_inst_menu', lambda w: w.set("Bachiller")),
            ("Tipo Institución:", crear_option_menu, {"values":["Pública", "Privada"], "command": lambda v: setattr(self.tipo_inst_menu, '_current_value',v)}, 1, self, 'tipo_inst_menu', lambda w: w.set("Pública"))
        ])
        self._crear_fila_widgets([
            ("Institución:", crear_entry, {"width":250}, 2, self, 'institucion_entry'),
            ("Fecha Grado:", crear_entry, {"width":120, "validate":"key", "validatecommand":(vcmd_fecha, "%S"), "placeholder_text":"dd/mm/aaaa"}, 1, self, 'fgrado_entry'),
            ("Promedio Bachillerato:", crear_entry, {
                "width":120,
                "validate":"key",
                "validatecommand":(vcmd_decimal, "%P", "%S")
            }, 1, self, 'promedio_entry')
        ])
        self._crear_fila_widgets([
            ("Título Obtenido:", crear_entry, {"width":220}, 2, self, 'titulo_entry')
        ])

    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets


class SistemaIngresoFrame(SectionFrameBase):
    def __init__(self, master, vcmd_num):
        super().__init__(master, header_text="Sistema Nacional de Ingreso")
        self._crear_fila_widgets([
            ("Código:", crear_entry, {"width":150}, 1, self, 'codigo_entry'),
            ("Año:", crear_entry, {"width":100, "validate":"key", "validatecommand":(vcmd_num, "%S"), "placeholder_text":"aaaa"}, 1, self, 'anio_entry')
        ])
    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets


class DatosUbicacionFrame(SectionFrameBase):
    def __init__(self, master, vcmd_num): # vcmd_num se mantiene por si se añaden otros campos en el futuro
        super().__init__(master, header_text="Datos de Ubicación")
        self._crear_fila_widgets([
            ("Estado:", crear_entry, {"width":220}, 1, self, 'estado_entry'),
            ("Municipio:", crear_entry, {"width":220}, 1, self, 'municipio_entry')
        ])
        self._crear_fila_widgets([
            ("Parroquia:", crear_entry, {"width":220}, 2, self, 'parroquia_entry'),
            ("Sector:", crear_entry, {"width":220}, 2, self, 'sector_entry'),
            ("Calle:", crear_entry, {"width":220}, 2, self, 'calle_entry'),
            ("Nro Casa o Apartamento:", crear_entry, {"width":220}, 1, self, 'casa_apart_entry')
        ])
        # CAMPOS DE TELÉFONO ELIMINADOS DE ESTA SECCIÓN

    
    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets


class FormularioEstudianteView(ctk.CTkScrollableFrame):
    def __init__(self, master, controlador_estudiante):
        super().__init__(master, fg_color=COLOR_FONDO_FORMULARIO, label_text="")
        self.controlador_estudiante = controlador_estudiante

        # Registrar funciones de validación
        try:
            toplevel = self.winfo_toplevel()
            self.vcmd_num_val = toplevel.register(self._solo_numeros)
            self.vcmd_fecha_val = toplevel.register(self._numeros_y_barras)
            self.vcmd_decimal_val = toplevel.register(self._solo_decimal)
        except Exception: # Fallback si no es un toplevel (ej. si el master es el root)
            self.vcmd_num_val = master.register(self._solo_numeros)
            self.vcmd_fecha_val = master.register(self._numeros_y_barras)
            self.vcmd_decimal_val = master.register(self._solo_decimal)

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

    def _solo_numeros(self, char_input):
        return char_input.isdigit()

    def _numeros_y_barras(self, char_input):
        return char_input.isdigit() or char_input == '/'

    def _solo_decimal (self, valor_actual, char_input):
        # Permite solo números y un punto decimal, y no permite más de un punto
        if char_input in "0123456789":
            return True
        if char_input == "." and "." not in valor_actual:
            return True
        if char_input == "":
            return True  # Permitir borrar
        return False

    def procesar_formulario(self):
        if not self._validar_campos_obligatorios():
            return
        datos = self._obtener_todos_los_datos()
        # Aquí llamarías a tu controlador para guardar/procesar los datos
        # Ejemplo: self.controlador_estudiante.guardar_estudiante(datos)
        # Por ahora, solo mostramos un mensaje y limpiamos.
        print("Datos del formulario:", datos) # Para depuración
        messagebox.showinfo("Formulario", "Datos procesados.", parent=self)
        # exito = self.controlador_estudiante.procesar_guardado_estudiante(datos, self)
        # if exito: self.limpiar_formulario_completo()
        self.limpiar_formulario_completo() # Limpiar después de procesar

    def _validar_campos_obligatorios(self):
        # Validar el número de documento según el tipo seleccionado
        tipo_doc_seleccionado = self.datos_personales_frame.tipo_documento_var.get()
        nro_doc_widget = self.datos_personales_frame.nro_documento_entry
        nro_doc_valor = nro_doc_widget.get().strip()

        if tipo_doc_seleccionado == "Cédula":
            if not nro_doc_valor:
                messagebox.showwarning("Campo Vacío", "El campo 'Nro. Cédula' es obligatorio.", parent=self)
                nro_doc_widget.focus_set()
                return False
        elif tipo_doc_seleccionado == "Pasaporte":
            if not nro_doc_valor:
                messagebox.showwarning("Campo Vacío", "El campo 'Nro. Pasaporte' es obligatorio.", parent=self)
                nro_doc_widget.focus_set()
                return False
        # No se requiere número si es "Sin Documento"

        campos_a_validar = [
            (self.datos_personales_frame.nombre_entry, "Nombre"),
            (self.datos_personales_frame.apellido_entry, "Apellido"),
            (self.datos_personales_frame.nacionalidad_entry, "Nacionalidad"),
            (self.datos_personales_frame.fnac_entry, "Fecha de Nacimiento"),
            (self.datos_personales_frame.lugar_nac_entry, "Lugar de Nacimiento"),
            (self.datos_personales_frame.fingreso_entry, "Fecha de Ingreso"),
            (self.datos_personales_frame.correo_electronico_entry, "Correo Electrónico"),
            (self.datos_personales_frame.telefono_principal_entry, "Teléfono Principal"),
            (self.datos_personales_frame.condicion_entry, "Condición"),

            (self.informacion_academica_frame.institucion_entry, "Institución"),
            (self.informacion_academica_frame.titulo_entry, "Título Obtenido"),
            (self.informacion_academica_frame.fgrado_entry, "Fecha Grado"),
            (self.informacion_academica_frame.promedio_entry, "Promedio Bachillerato"),
            (self.sistema_ingreso_frame.codigo_entry, "Código SNI"),
            (self.sistema_ingreso_frame.anio_entry, "Año SNI"),
            (self.datos_ubicacion_frame.estado_entry, "Estado"),
            (self.datos_ubicacion_frame.municipio_entry, "Municipio"),
            (self.datos_ubicacion_frame.parroquia_entry, "Parroquia"),
            (self.datos_ubicacion_frame.sector_entry, "Sector"),
            (self.datos_ubicacion_frame.calle_entry, "Calle"),
            (self.datos_ubicacion_frame.casa_apart_entry, "Casa o Apartamento"),
        ]

        for campo_widget, nombre_campo in campos_a_validar:
            valor_campo = ""
            if hasattr(campo_widget, 'get'): # CTkEntry, CTkOptionMenu
                 valor_campo = campo_widget.get().strip()

            # Validación específica para correo electrónico (si es el campo y tiene valor)
            if nombre_campo == "Correo Electrónico" and valor_campo:
                if "@" not in valor_campo or "." not in valor_campo.split("@")[-1] or len(valor_campo.split("@")[-1].split(".")[-1]) < 2 :
                    messagebox.showwarning("Campo Inválido", f"El formato del '{nombre_campo}' no es válido.", parent=self)
                    campo_widget.focus_set()
                    return False
            
            # Validación general de campo vacío para campos obligatorios
            # (El correo ya se validó si tenía contenido, aquí se chequea si es obligatorio y está vacío)
            if not valor_campo:
                messagebox.showwarning("Campo Vacío", f"El campo '{nombre_campo}' es obligatorio.", parent=self)
                if hasattr(campo_widget, 'focus_set'):
                    campo_widget.focus_set()
                return False
        return True

    def _obtener_todos_los_datos(self):
        nro_doc_val = ""
        if self.datos_personales_frame.nro_documento_entry.cget('state') == 'normal':
            nro_doc_val = self.datos_personales_frame.nro_documento_entry.get()

        datos = {
            "tipo_documento": self.datos_personales_frame.tipo_documento_var.get(),
            "nro_documento": nro_doc_val,
            "nombre": self.datos_personales_frame.nombre_entry.get(),
            "apellido": self.datos_personales_frame.apellido_entry.get(),
            "genero": self.datos_personales_frame.genero_menu.get(),
            "edo_civil": self.datos_personales_frame.edo_civil_menu.get(),
            "nacionalidad": self.datos_personales_frame.nacionalidad_entry.get(),
            "f_nacimiento": self.datos_personales_frame.fnac_entry.get(),
            "lugar_nacimiento": self.datos_personales_frame.lugar_nac_entry.get(),
            "f_ingreso": self.datos_personales_frame.fingreso_entry.get(),
            "correo_electronico": self.datos_personales_frame.correo_electronico_entry.get(),
            "telefono_principal": self.datos_personales_frame.telefono_principal_entry.get(),
            "telefono_secundario": self.datos_personales_frame.telefono_secundario_entry.get(),
            "condicion": self.datos_personales_frame.condicion_menu.get(),

            "tipo_institucion": self.informacion_academica_frame.tipo_inst_menu.get(),
            "institucion": self.informacion_academica_frame.institucion_entry.get(),
            "titulo_obtenido": self.informacion_academica_frame.titulo_entry.get(),
            "promedio_bachiller": self.informacion_academica_frame.promedio_entry.get(),
            "f_grado": self.informacion_academica_frame.fgrado_entry.get(),
            "codigo_sni": self.sistema_ingreso_frame.codigo_entry.get(),
            "anio_sni": self.sistema_ingreso_frame.anio_entry.get(),
            "estado": self.datos_ubicacion_frame.estado_entry.get(),
            "municipio": self.datos_ubicacion_frame.municipio_entry.get(),
            "parroquia": self.datos_ubicacion_frame.parroquia_entry.get(),
            "sector": self.datos_ubicacion_frame.sector_entry.get(),
            "calle": self.datos_ubicacion_frame.calle_entry.get(),
            "casa_apart": self.datos_ubicacion_frame.casa_apart_entry.get()
        }
        return datos

    def limpiar_formulario_completo(self):
        entries_a_limpiar = [
            self.datos_personales_frame.nro_documento_entry,
            self.datos_personales_frame.nombre_entry,
            self.datos_personales_frame.apellido_entry,
            self.datos_personales_frame.nacionalidad_entry,
            self.datos_personales_frame.fnac_entry,
            self.datos_personales_frame.lugar_nac_entry,
            self.datos_personales_frame.fingreso_entry,
            self.datos_personales_frame.correo_electronico_entry,
            self.datos_personales_frame.telefono_principal_entry,
            self.datos_personales_frame.telefono_secundario_entry,

            self.informacion_academica_frame.institucion_entry,
            self.informacion_academica_frame.titulo_entry,
            self.informacion_academica_frame.fgrado_entry,
            self.informacion_academica_frame.promedio_entry,
            self.sistema_ingreso_frame.codigo_entry,
            self.sistema_ingreso_frame.anio_entry,
            self.datos_ubicacion_frame.estado_entry,
            self.datos_ubicacion_frame.municipio_entry,
            self.datos_ubicacion_frame.parroquia_entry,
            self.datos_ubicacion_frame.sector_entry,
            self.datos_ubicacion_frame.calle_entry,
            self.datos_ubicacion_frame.casa_apart_entry,
        ]
        option_menus_a_resetear = {
            self.datos_personales_frame.genero_menu: "Masculino",
            self.datos_personales_frame.edo_civil_menu: "Soltero",
            self.informacion_academica_frame.tipo_inst_menu: "Pública"
        }

        for entry in entries_a_limpiar:
            if hasattr(entry, 'delete'):
                entry.delete(0, 'end')
        for menu, valor in option_menus_a_resetear.items():
            if hasattr(menu, 'set'):
                menu.set(valor)

        self.datos_personales_frame.tipo_documento_var.set("Cédula") # Resetear radio
        self.datos_personales_frame._actualizar_estado_nro_doc() # Actualizar estado del entry asociado

        # Establecer foco en el primer campo editable
        if self.datos_personales_frame.tipo_documento_var.get() != "Sin Documento":
            self.datos_personales_frame.nro_documento_entry.focus_set()
        else:
            if self.datos_personales_frame.nombre_entry:
                 self.datos_personales_frame.nombre_entry.focus_set()