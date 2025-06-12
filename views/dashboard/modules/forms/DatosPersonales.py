import customtkinter as ctk
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase

class DatosPersonalesFrame(SectionFrameBase):

    def __init__(self, master, vcmd_num, vcmd_fecha):
        super().__init__(master, header_text="Datos Personales")

        self.tipo_documento_var = ctk.StringVar(value="cedula") # Valor por defecto: Cédula
        self.vcmd_num = vcmd_num # Guardar para usar en nro_documento_entry y teléfonos
        self.vcmd_fecha = vcmd_fecha # Guardar para usar en fechas
        self.lista_telefonos = [] # Lista para guardar los teléfonos

        # --- Fila para Tipo y Número de Documento (Reemplaza Cédula entry) ---
        self.frame_tipo_numero_doc = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_tipo_numero_doc.pack(fill="x", pady=PADY_FILA, padx=15)

        label_doc_principal = ctk.CTkLabel(self.frame_tipo_numero_doc, text="Documento:", font=FUENTE_LABEL_CAMPO, text_color=COLOR_TEXTO_PRINCIPAL, anchor="w")
        label_doc_principal.grid(row=0, column=0, sticky="w", padx=PADX_LABEL)

        radio_button_container = ctk.CTkFrame(self.frame_tipo_numero_doc, fg_color="transparent")
        radio_button_container.grid(row=0, column=1, sticky="w", padx=(0,15))

        self.radio_cedula = crear_radio_button(radio_button_container, text="Cédula", variable=self.tipo_documento_var, value="cedula", command=self._actualizar_estado_nro_doc)
        self.radio_cedula.pack(side="left", padx=(0, 5), pady=0)

        self.radio_pasaporte = crear_radio_button(radio_button_container, text="Pasaporte", variable=self.tipo_documento_var, value="pasaporte", command=self._actualizar_estado_nro_doc)
        self.radio_pasaporte.pack(side="left", padx=(0, 5), pady=0)

        self.label_nro_doc = ctk.CTkLabel(self.frame_tipo_numero_doc, text="Nro. Cédula:", font=FUENTE_LABEL_CAMPO, text_color=COLOR_TEXTO_PRINCIPAL, anchor="w")
        self.label_nro_doc.grid(row=0, column=2, sticky="w", padx=PADX_LABEL)

        self.nro_documento_entry = crear_entry(self.frame_tipo_numero_doc, width=170, validate="key", validatecommand=(self.vcmd_num, "%S"))
        self.nro_documento_entry.grid(row=0, column=3, sticky="ew", padx=PADX_ENTRY)
        self.frame_tipo_numero_doc.grid_columnconfigure(1, weight=100) # Permitir que el entry se expanda
        self._actualizar_estado_nro_doc() # Llamada inicial para configurar el estado
        # --- Fin Fila Documento ---

        self._crear_fila_widgets([
            ("Nombres:", crear_entry, {"width":300}, 1, self, 'nombre_entry'),
            ("Apellidos:", crear_entry, {"width":300}, 1, self, 'apellido_entry')
        ])
        self.var_sexo = ctk.StringVar(value='M')
        self.var_estadoCivil = ctk.StringVar(value='Soltero')
        self.var_nacionalidad =ctk.StringVar(value='Venezolano')
        self.var_telefono_p = ctk.StringVar(value='movil')
        self.var_telefono_s = ctk.StringVar(value='movil')
        # --- Fila para genero, estado civil ---
        self._crear_fila_widgets([
            ("Género:", crear_option_menu, {"values":["M", "F"],'variable': self.var_sexo,"command": lambda v: setattr(self.genero_menu, '_current_value',v)}, 1, self, 'genero_menu'),
            ("Edo Civil:", crear_option_menu, {"values":["Soltero", "Casado", "Divorciado"],"variable":self.var_estadoCivil ,"command": lambda v: setattr(self.edo_civil_menu, '_current_value',v)}, 1, self, 'edo_civil_menu')
        ])

        # --- Fila para nacionalidad ---
        self._crear_fila_widgets([
            ("Nacionalidad",crear_option_menu, {"values":["Venezolano", "Extranjero"] ,"variable":self.var_nacionalidad,"command": lambda v: setattr(self.nacionalidad_menu, '_current_value',v)}, 1, self, 'nacionalidad_menu'),
        ])

        # --- Fila para fecha de nacimiento, lugar de nacimiento y fecha de ingreso ---
        self._crear_fila_widgets([
            ("F. Nacimiento:", crear_entry, {"width":120, "placeholder_text":"dd-mm-aaaa"}, 1, self, 'fnac_entry'),
            ("Lugar Nacimiento:", crear_entry, {"width":300}, 1, self, 'lugar_nac_entry'),
            ("F. Ingreso:", crear_entry, {"width":120,"placeholder_text":"dd-mm-aaaa"}, 1, self, 'fingreso_entry')
        ])

        # --- Fila para correo electronico ---
        self._crear_fila_widgets([
            ("Correo Electrónico:", crear_entry, {"width":300}, 1, self, 'correo_electronico_entry')
        ])

        # --- Apartado dinámico de Teléfonos ---
        self.frame_telefonos = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_telefonos.pack(fill="x", pady=PADY_FILA, padx=15)

        self.btn_agregar_telefono = ctk.CTkButton(
            self.frame_telefonos,
            text="Agregar Teléfono",
            command=self.agregar_telefono
        )
        self.btn_agregar_telefono.pack(anchor="w", pady=5)

        self.telefono_widgets = []  # Lista para guardar las filas de teléfonos

        

    def agregar_telefono(self):
        """
        Agrega una fila dinámica de teléfono (tipo + número + eliminar).
        """
        fila = ctk.CTkFrame(self.frame_telefonos, fg_color="transparent")
        fila.pack(fill="x", pady=2)

        self.var_tipo = ctk.StringVar(value="movil")
        tipo_menu = crear_option_menu(
            fila,
            values=['movil', 'casa', 'trabajo', 'otro'],
            variable=self.var_tipo
        )
        tipo_menu.pack(side="left", padx=(0, 5))

        self.entry_num = crear_entry(
            fila,
            width=150,
            validate="key",
            validatecommand=(self.vcmd_num, "%S")
        )
        self.entry_num.pack(side="left", padx=(0, 5))

        btn_eliminar = ctk.CTkButton(
            fila,
            text="Eliminar",
            width=70,
            command=lambda: self.eliminar_telefono(fila)
        )
        btn_eliminar.pack(side="left", padx=(0, 5))
        # Agregar teléfono a la lista
        self.lista_telefonos.append((self.var_tipo.get(), self.entry_num.get()))

        self.telefono_widgets.append((fila, self.var_tipo, tipo_menu, self.entry_num))

    def obtener_telefonos(self):
        telefonos = [
            (tipo_var.get(), entry_num.get())
            for _, tipo_var, _, entry_num in self.telefono_widgets
            if entry_num.get().strip()  # Solo si el número no está vacío
        ]
        return telefonos

    def eliminar_telefono(self, fila):
        """
        Elimina una fila de teléfono de la interfaz y de la lista.
        """
        fila.destroy()
        self.telefono_widgets = [
            t for t in self.telefono_widgets if t[0] != fila
        ]

    def limpiar_telefonos(self):
        """
        Elimina todas las filas de teléfonos dinámicos.
        """
        for fila, _, _, _ in self.telefono_widgets:
            fila.destroy()
        self.telefono_widgets.clear()

    def _actualizar_estado_nro_doc(self, _=None): # Acepta un argumento opcional por el command
        tipo_doc = self.tipo_documento_var.get()
        if tipo_doc == "Cédula":
            self.label_nro_doc.configure(text="Nro. Cédula:")
            self.nro_documento_entry.configure(state="normal", placeholder_text="Ingrese cédula")
        elif tipo_doc == "Pasaporte":
            self.label_nro_doc.configure(text="Nro. Pasaporte:")
            self.nro_documento_entry.configure(state="normal", placeholder_text="Ingrese pasaporte")
        

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

    

    def set_datos(self, estudiante):
        """
        Carga los datos del estudiante en los campos y deshabilita la edición.
        Adapta los campos fijos de teléfono a la vista dinámica.
        """
        tipo_doc = estudiante.get("tipo_documento", "Cédula")
        self.radio_cedula.configure(state="disabled")
        self.radio_pasaporte.configure(state="disabled")
        
        self.nro_documento_entry.configure(state="normal")
        self.nro_documento_entry.delete(0, 'end')
        self.nro_documento_entry.insert(0, str(estudiante.get("documento_identidad", "")))
        self.nro_documento_entry.configure(state="disabled")

        self.nombre_entry.configure(state="normal")
        self.nombre_entry.delete(0, 'end')
        self.nombre_entry.insert(0, estudiante.get("nombres", ""))
        self.nombre_entry.configure(state="disabled")

        self.apellido_entry.configure(state="normal")
        self.apellido_entry.delete(0, 'end')
        self.apellido_entry.insert(0, estudiante.get("apellidos", ""))
        self.apellido_entry.configure(state="disabled")

        #Configuracion del sexo
        if estudiante.get('sexo') != None:
            self.var_sexo.set(estudiante.get('sexo'))
        else:
            self.var_sexo.set('M')
        self.genero_menu.configure(state="disabled")

        #Configuracion del estado civil
        if estudiante.get('estado_civil') != None:
            self.var_estadoCivil.set(estudiante.get('estado_civil'))
        else:
            self.var_estadoCivil.set('Soltero')
        self.edo_civil_menu.configure(state="disabled")

        #Configuracion de la nacionalidad
        if estudiante.get('nacionalidad') != None:
            self.var_nacionalidad.set(estudiante.get("nacionalidad"))
        else:
            self.var_nacionalidad.set("Venezolano")
        self.nacionalidad_menu.configure(state="disabled")     

        #Configuracion de la fecha de nacimiento
        self.fnac_entry.configure(state="normal")
        self.fnac_entry.delete(0, ctk.END)
        fecha_nacimiento = estudiante.get('fecha_nacimiento')
        if fecha_nacimiento is not None and fecha_nacimiento != '':
            self.fnac_entry.insert(0, str(fecha_nacimiento))
            print(fecha_nacimiento)
        self.fnac_entry.configure(state="disabled")

        #Configuracion del lugar de nacimiento
        self.lugar_nac_entry.delete(0, ctk.END)
        if estudiante.get('lugar_nacimiento') != None:
            self.lugar_nac_entry.insert(0,estudiante.get("lugar_nacimiento"))
        else:
            self.lugar_nac_entry.insert("")
        self.lugar_nac_entry.configure(state="disabled")

        #Configuracion de la fecha de ingreso
        self.fingreso_entry.configure(state="normal")
        self.fingreso_entry.delete(0, ctk.END)
        fecha_ingreso = estudiante.get('fecha_ingreso')
        if fecha_ingreso is not None and fecha_ingreso != '':
            self.fingreso_entry.insert(0, str(fecha_ingreso))
            print(fecha_ingreso)
        self.fingreso_entry.configure(state="disabled")

        #Configuaracion correoelectronico
        self.correo_electronico_entry.delete(0,ctk.END)
        if estudiante.get('correo_electronico') != None:
            self.correo_electronico_entry.insert(0,estudiante.get('correo_electronico'))
        self.correo_electronico_entry.configure(state="disabled")
        
        self.correo_electronico_entry.insert(0, estudiante.get('correo_electronico'))
        self.correo_electronico_entry.configure(state="disabled")

         # --- Teléfonos dinámicos: mostrar todos los guardados ---
        self.limpiar_telefonos()
        telefonos = estudiante.get('telefonos', [])
        for tipo, numero, principal in telefonos:
            self.agregar_telefono()
            fila, var_tipo, tipo_menu, entry_num = self.telefono_widgets[-1]
            var_tipo.set(tipo)
            entry_num.insert(0, numero)
            entry_num.configure(state="disabled")
            tipo_menu.configure(state="disabled")
            # Deshabilitar botón eliminar
            for widget in fila.winfo_children():
                if isinstance(widget, ctk.CTkButton) and widget.cget("text") == "Eliminar":
                    widget.configure(state="disabled")
        # Deshabilita el botón agregar teléfono en modo solo lectura
        self.btn_agregar_telefono.configure(state="disabled")
            # --- Fin de la carga de teléfonos ---

        

    #metodo para habilitar la edicion de los campos sin eliminar el contenido
    def habilitar_edicion(self):
        # Habilitar campos de entrada
        self.nombre_entry.configure(state="normal")
        self.apellido_entry.configure(state="normal")
        self.genero_menu.configure(state="normal")
        self.edo_civil_menu.configure(state="normal")
        self.nacionalidad_menu.configure(state="normal")
        self.fnac_entry.configure(state="normal")
        self.lugar_nac_entry.configure(state="normal")
        self.fingreso_entry.configure(state="normal")
        self.correo_electronico_entry.configure(state="normal")
        

        self.btn_agregar_telefono.configure(state="normal")    
        # Habilitar edición en los teléfonos dinámicos
        for fila, _, tipo_menu, entry_num in self.telefono_widgets:
            entry_num.configure(state="normal")
            tipo_menu.configure(state="normal")
            for widget in fila.winfo_children():
                if isinstance(widget, ctk.CTkButton) and widget.cget("text") == "Eliminar":
                    widget.configure(state="normal")