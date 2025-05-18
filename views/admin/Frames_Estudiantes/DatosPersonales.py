import customtkinter as ctk
from util.widget_utils import *
from views.layouts.SectionFrameBase import SectionFrameBase

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
            ("Género:", crear_option_menu, {"values":["M", "F"], "command": lambda v: setattr(self.genero_menu, '_current_value',v)}, 1, self, 'genero_menu', lambda w: w.set("M")),
            ("Edo Civil:", crear_option_menu, {"values":["Soltero", "Casado", "Divorciado"], "command": lambda v: setattr(self.edo_civil_menu, '_current_value',v)}, 1, self, 'edo_civil_menu', lambda w: w.set("Soltero"))
        ])
        self._crear_fila_widgets([
            ("Nacionalidad",crear_option_menu, {"values":["Venezolano", "Extranjero"], "command": lambda v: setattr(self.nacionalidad_menu, '_current_value',v)}, 1, self, 'nacionalidad_menu', lambda w: w.set("Venezolano")),
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
            ("Tipo de Telefono", crear_option_menu, {"values":['movil', 'casa', 'trabajo', 'otro'], "command": lambda v: setattr(self.tipo_telefono_p, '_current_value',v)}, 1, self, 'tipo_telefono_p', lambda w: w.set("movil")),
            ("Tel. Principal:", crear_entry, {"width":150, "validate":"key", "validatecommand":(self.vcmd_num, "%S")}, 1, self, 'telefono_principal_entry'),
            ('Tipo de Telefono', crear_option_menu, {"values":['movil', 'casa', 'trabajo', 'otro'], "command": lambda v: setattr(self.tipo_telefono_s, '_current_value',v)}, 1, self, 'tipo_telefono_s', lambda w: w.set("movil")),
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
