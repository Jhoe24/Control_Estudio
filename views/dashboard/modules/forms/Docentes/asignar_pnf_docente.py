import tkinter.messagebox as messagebox
import customtkinter as ctk
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase
from ..DatosPersonales import DatosPersonalesFrame

class AsignarDocentePNFFrame(SectionFrameBase):
    def __init__(self, master, controller, controller_pnf, docente, para_edicion):
        super().__init__(master, "Asignar PNF a Docente")

        self.controller = controller
        self.controller_pnf = controller_pnf
        self.docente = docente
        self.fecha_asignacion = ""
        self.fecha_desasignacion = ""
        self.btn_fecha_asignacion = None
        self.btn_fecha_desasignacion = None

        self.para_edicion = para_edicion

        if not self.controller_pnf:
            print("Error: El controlador de PNF no está definido.")
        else:
            vcmd = self.register(self.controller_pnf.solo_decimal)
            self.var_estado = ctk.StringVar(value="Activo")
            self.nombres_pnf = self.controller_pnf.obtener_nombres_pnf()
            self.var_pnf = ctk.StringVar(value=self.nombres_pnf[0] if self.nombres_pnf else "")
            self.id_docente = self.docente.get("id")
            self.tuple_pnf = self.controller_pnf.listado_pnf

            self.pnf_id_por_nombre = {tupla[2]: tupla[0] for tupla in self.tuple_pnf}
            self.var_coordinador = ctk.BooleanVar(value=False)
            self.var_activo = ctk.BooleanVar(value=True)
            self.var_observaciones = ctk.StringVar(value="")

            # Widgets
            self._crear_fila_widgets([
                ("Seleccione un P.N.F:", crear_option_menu, {"values": self.nombres_pnf, "variable": self.var_pnf}, 1, self, 'pnf_menu'),
            ])

            # Fechas
            self.registrar_fecha(self.set_fecha_asignacion, titulo_btn="Fecha de Asignación", attr_name="btn_fecha_asignacion")
            self.fecha_asignacion_label = ctk.CTkLabel(self, text="Fecha de Asignación: No seleccionada", font=FUENTE_LABEL_CAMPO, text_color=COLOR_TEXTO_PRINCIPAL)
            self.fecha_asignacion_label.pack(pady=(10, 0), padx=10, anchor="w")

            self.registrar_fecha(self.set_fecha_desasignacion, titulo_btn="Fecha de Desasignación", attr_name="btn_fecha_desasignacion")
            self.fecha_desasignacion_label = ctk.CTkLabel(self, text="Fecha de Desasignación: No seleccionada", font=FUENTE_LABEL_CAMPO, text_color=COLOR_TEXTO_PRINCIPAL)
            self.fecha_desasignacion_label.pack(pady=(10, 0), padx=10, anchor="w")

            # Coordinador y Activo
            frame_checks = ctk.CTkFrame(self, fg_color="transparent")
            frame_checks.pack(fill="x", pady=(10, 0), padx=10)
            self.check_coordinador = ctk.CTkCheckBox(frame_checks,text_color=COLOR_TEXTO_PRINCIPAL, text="Coordinador", variable=self.var_coordinador)
            self.check_coordinador.pack(side="left", padx=10)
            self.check_activo = ctk.CTkCheckBox(frame_checks,text_color=COLOR_TEXTO_PRINCIPAL, text="Activo", variable=self.var_activo)
            self.check_activo.pack(side="left", padx=10)

            # Observaciones
            self._crear_fila_widgets([
                ("Observaciones:", crear_entry, {"width":300, "placeholder_text":"Ingrese observaciones", "textvariable": self.var_observaciones}, 1, self, 'observaciones_entry'),
            ])

            self.instancias_widgets = [
                self.pnf_menu,
                self.btn_fecha_asignacion,
                self.btn_fecha_desasignacion,
                self.check_coordinador,
                self.check_activo,
                self.observaciones_entry,
            ]

            # Botones
            self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
            self.button_frame.pack(pady=(25, 20))
            if self.para_edicion:
                text = "Actualizar Datos"
                text2 = "Editar Asignación"
                command = self.actualizar_datos_pnf
                command2 = self.habilitar_edicion_pnf
            else:
                text = "Registrar Asignación"
                text2 = "Limpiar Campos"
                command = self.guardar_datos
                command2 = self.limpiar_campos

            self.btn_guardar = ctk.CTkButton(self.button_frame, text=text, width=140,
                                            font=FUENTE_BOTON, fg_color=COLOR_BOTON_PRIMARIO_FG, hover_color=COLOR_BOTON_PRIMARIO_HOVER,
                                            command=command,
                                            text_color=COLOR_BOTON_PRIMARIO_TEXT, state="normal")
            self.btn_guardar.pack(side="left", padx=10)

            self.btn_cancelar = ctk.CTkButton(self.button_frame, text=text2, width=140,
                                            font=FUENTE_BOTON, fg_color=COLOR_BOTON_SECUNDARIO_FG, hover_color=COLOR_BOTON_SECUNDARIO_HOVER,
                                            command=command2,
                                            text_color=COLOR_BOTON_SECUNDARIO_TEXT)
            self.btn_cancelar.pack(side="left", padx=10)

    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets

    def registrar_fecha(self, callback, titulo_btn="Seleccionar Fecha", attr_name=None):
        def calendario():
            top = ctk.CTkToplevel(self, fg_color="White")
            top.title(titulo_btn)
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
            self.cal = Calendar(top, locale='es_ES', date_pattern='yyyy-mm-dd')
            self.cal.pack(pady=20)

            def mostrar_fecha(date):
                label.configure(text=f"Fecha seleccionada: {date}")

            def guardar_fecha():
                fecha = self.cal.get_date()
                callback(fecha)
                top.destroy()

            self.cal.bind("<<CalendarSelected>>", lambda e: mostrar_fecha(self.cal.get_date()))
            boton_guardar = ctk.CTkButton(top, text="Guardar Fecha", command=guardar_fecha)
            boton_guardar.pack(pady=10)

        frame_fecha = ctk.CTkFrame(self, fg_color="transparent")
        frame_fecha.pack(fill="x", pady=(10, 0), padx=10)
        btn_fecha = ctk.CTkButton(
            frame_fecha,
            text=titulo_btn,
            command=calendario,
            width=100,
            font=FUENTE_BOTON,
            fg_color=COLOR_BOTON_PRIMARIO_FG,
            hover_color=COLOR_BOTON_PRIMARIO_HOVER,
            text_color=COLOR_BOTON_PRIMARIO_TEXT
        )
        btn_fecha.pack(side="left", pady=(10, 0), anchor="w")
        if attr_name:
            setattr(self, attr_name, btn_fecha)

    def set_fecha_asignacion(self, fecha):
        if fecha:
            self.fecha_asignacion = fecha
            self.fecha_asignacion_label.configure(text=f"Fecha de Asignación: {self.fecha_asignacion}")

    def set_fecha_desasignacion(self, fecha):
        if fecha:
            self.fecha_desasignacion = fecha
            self.fecha_desasignacion_label.configure(text=f"Fecha de Desasignación: {self.fecha_desasignacion}")

    def guardar_datos(self):
        datos = {
            "docente_id": self.id_docente,
            "pnf_id": self.pnf_id_por_nombre[self.var_pnf.get()],
            "fecha_asignacion": self.fecha_asignacion,
            "fecha_desasignacion": self.fecha_desasignacion,
            "coordinador": self.var_coordinador.get(),
            "activo": self.var_activo.get(),
            "observaciones": self.var_observaciones.get(),
        }
        if self.controller_pnf.modelo.registrar_asignacion_docente_pnf(datos):
            messagebox.showinfo("Éxito", "La asignación se realizó exitosamente.", parent=self)
            self.winfo_toplevel().destroy()
        else:
            messagebox.showerror("Error", "No se pudo realizar la asignación, intente nuevamente.", parent=self)

    def actualizar_datos_pnf(self):
        datos = {
            "docente_id": self.id_docente,
            "pnf_id": self.pnf_id_por_nombre[self.var_pnf.get()],
            "fecha_asignacion": self.fecha_asignacion,
            "fecha_desasignacion": self.fecha_desasignacion,
            "coordinador": self.var_coordinador.get(),
            "activo": self.var_activo.get(),
            "observaciones": self.var_observaciones.get(),
        }
        if self.controller_pnf.modelo.update_pnf_asignado_docente(self.id_docente, datos):
            messagebox.showinfo("Éxito", "La actualización se realizó exitosamente.", parent=self)
            self.winfo_toplevel().destroy()
        else:
            messagebox.showerror("Error", "No se pudo actualizar.", parent=self)

    def habilitar_edicion_pnf(self):
        for widget in self.instancias_widgets:
            widget.configure(state="normal")
        self.btn_fecha_asignacion.configure(state="normal")
        self.btn_fecha_desasignacion.configure(state="normal")
        self.btn_guardar.configure(state="normal")

    def limpiar_campos(self):
        for widget in self.instancias_widgets:
            if isinstance(widget, ctk.CTkEntry):
                widget.delete(0, "end")
            elif isinstance(widget, ctk.CTkButton):
                widget.configure(state="normal")
            elif isinstance(widget, ctk.CTkCheckBox):
                widget.deselect()
        self.fecha_asignacion_label.configure(text="Fecha de Asignación: No seleccionada")
        self.fecha_desasignacion_label.configure(text="Fecha de Desasignación: No seleccionada")
        self.btn_fecha_asignacion.configure(state="normal")
        self.btn_fecha_desasignacion.configure(state="normal")

    def cargar_datos_pnf(self, docente_id):
        """
        Carga los datos de la asignación PNF del docente y desactiva los campos.
        """
        datos_pnf = self.controller_pnf.modelo.obtener_pnf_asignado_docente(docente_id)
        if datos_pnf:
            # PNF
            nombre_pnf = next((nombre for nombre, id_ in self.pnf_id_por_nombre.items() if id_ == datos_pnf["pnf_id"]), None)
            if nombre_pnf:
                self.var_pnf.set(nombre_pnf)
                self.pnf_menu.configure(state="disabled")

            # Fechas
            self.fecha_asignacion = datos_pnf.get("fecha_asignacion", "")
            self.fecha_desasignacion = datos_pnf.get("fecha_desasignacion", "")
            self.fecha_asignacion_label.configure(
                text=f"Fecha de Asignación: {self.fecha_asignacion or 'No seleccionada'}"
            )
            self.fecha_desasignacion_label.configure(
                text=f"Fecha de Desasignación: {self.fecha_desasignacion or 'No seleccionada'}"
            )
            self.btn_fecha_asignacion.configure(state="disabled")
            self.btn_fecha_desasignacion.configure(state="disabled")

            # Coordinador y Activo
            self.var_coordinador.set(bool(datos_pnf.get("coordinador", 0)))
            self.check_coordinador.configure(state="disabled")
            self.var_activo.set(bool(datos_pnf.get("activo", 1)))
            self.check_activo.configure(state="disabled")

            # Observaciones
            self.var_observaciones.set(datos_pnf.get("observaciones", ""))
            self.observaciones_entry.configure(state="disabled")

            # Botón guardar desactivado
            self.btn_guardar.configure(state="disabled")
        else:
            messagebox.showerror("Error", "No se pudieron cargar los datos del PNF.", parent=self)
            