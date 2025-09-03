import tkinter.messagebox as messagebox
import customtkinter as ctk
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase
from views.dashboard.modules.forms.Docentes.listaAsignacionUC import ListaAsignacionUC
from ..DatosPersonales import DatosPersonalesFrame

class AsignarDocentePNFFrame(SectionFrameBase):
    def __init__(self, master, controller, controller_pnf, docente, para_edicion):
        super().__init__(master, "Asignar PNF a Docente",COLOR_HEADER_SECCION_BG_2)

        self.master = master
        self.controller = controller
        self.controller_pnf = controller_pnf
        self.docente = docente
        self.fecha_asignacion = ""
        self.fecha_desasignacion = ""
        self.btn_fecha_asignacion = None
        self.btn_fecha_desasignacion = None

        self.para_edicion = para_edicion
        self.id_asignacion = None
        self.pnf_id_original = None
        self.es_coordinador_original = False

        self.uc_frame = None

        if not self.controller_pnf:
            print("Error: El controlador de PNF no está definido.")
        else:
             
            vcmd = self.register(self.controller_pnf.solo_decimal)
            self.var_estado = ctk.StringVar(value="Activo")
            self.nombres_pnf = self.controller_pnf.obtener_nombres_pnf()

            self.tuple_pnf = self.controller_pnf.listado_pnf
            self.pnf_id_por_nombre = {tupla[2]: tupla[0] for tupla in self.tuple_pnf}

            if not self.para_edicion:
                self.sacar_pnf_existentes()
            
            if self.nombres_pnf:
                self.var_pnf = ctk.StringVar(value=self.nombres_pnf[0] if self.nombres_pnf else "")
                self.id_docente = self.docente.get("id")
            
                self.var_coordinador = ctk.BooleanVar(value=False)
                self.var_activo = ctk.BooleanVar(value=True)
                self.var_observaciones = ctk.StringVar(value="")

                # Widgets
                self._crear_fila_widgets([
                    ("Seleccione un P.N.F:", crear_option_menu, {"values": self.nombres_pnf, "variable": self.var_pnf, "command": self.validar_coordinador}, 1, self, 'pnf_menu'),
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

                if not self.para_edicion:
                    self.validar_coordinador()
            else:
                self.master.no_pnf_disponibles()
                self.destroy()
                

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

    def validar_coordinador(self, *args):
        id_pnf = self.pnf_id_por_nombre.get(self.var_pnf.get())
        if not id_pnf:
            self.check_coordinador.configure(state="disabled")
            return

        existe_coordinador = self.controller_pnf.modelo.existe_coordinador(id_pnf)

        if not existe_coordinador:
            self.check_coordinador.configure(state="normal")
            return

        # Si existe un coordinador, solo se habilita el checkbox si estamos
        # editando al docente que es precisamente ese coordinador.
        if self.para_edicion and id_pnf == self.pnf_id_original and self.es_coordinador_original:
            self.check_coordinador.configure(state="normal")
            return

        self.check_coordinador.configure(state="disabled")
        self.var_coordinador.set(False)

    def guardar_datos(self):
        datos = {
            "docente_id": self.id_docente,
            "pnf_id": self.pnf_id_por_nombre[self.var_pnf.get()],
            "fecha_asignacion": self.fecha_asignacion,
            "fecha_desasignacion": self.fecha_desasignacion,
            "coordinador": self.var_coordinador.get(),
            "activo": self.var_activo.get(),
            "observaciones": self.var_observaciones.get(),
            "uc_seleccionadas": [uc['id'] for uc in self.obtener_uc_seleccionadas()],
        }
       
        if self.controller_pnf.modelo.registrar_asignacion_docente_pnf(datos):
            messagebox.showinfo("Éxito", "La asignación se realizó exitosamente.")
        else:
            messagebox.showerror("Error", "No se pudo realizar la asignación, intente nuevamente.")

    def actualizar_datos_pnf(self):
        datos = {
            "docente_id": self.id_docente,
            "pnf_id": self.pnf_id_por_nombre[self.var_pnf.get()],
            "fecha_asignacion": self.fecha_asignacion,
            "fecha_desasignacion": self.fecha_desasignacion,
            "coordinador": self.var_coordinador.get(),
            "activo": self.var_activo.get(),
            "observaciones": self.var_observaciones.get(),
            "uc_seleccionadas": [uc['id'] for uc in self.obtener_uc_seleccionadas()],
        }

       
        if self.controller_pnf.modelo.update_pnf_asignado_docente(self.id_docente,datos,self.id_asignacion):
            messagebox.showinfo("Éxito", "La actualización se realizó exitosamente.")
        else:
            messagebox.showerror("Error", "No se pudo actualizar.")

    def habilitar_edicion_pnf(self):
        for widget in self.instancias_widgets:
            widget.configure(state="normal")
        self.btn_fecha_asignacion.configure(state="normal")
        self.btn_fecha_desasignacion.configure(state="normal")
        self.validar_coordinador()

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

    def sacar_pnf_existentes(self):
        lista_valores = self.master.existentes_pnf_asignados()
        llaves_encontradas = [] # Usaremos una lista para almacenar las llaves únicas
        for llave, valor_diccionario in self.pnf_id_por_nombre.items():
            # Verificamos si el valor del diccionario está en la lista de valores deseados
            # Y si la llave aún no ha sido agregada a nuestra lista de resultados
            if valor_diccionario in lista_valores and llave not in llaves_encontradas:
                llaves_encontradas.append(llave)           
        
        for llave in llaves_encontradas:
            self.nombres_pnf.remove(llave)

    def cargar_datos_pnf(self, datos_pnf):
        """
        Carga los datos de la asignación PNF del docente y desactiva los campos.
        """
        

        if datos_pnf:
            # PNF
            self.pnf_id_original = datos_pnf["pnf_id"]
            self.id_asignacion= datos_pnf["id"]
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
            self.es_coordinador_original = bool(datos_pnf.get("coordinador", 0))
            self.var_coordinador.set(self.es_coordinador_original)
            self.check_coordinador.configure(state="disabled")
            self.var_activo.set(bool(datos_pnf.get("activo", 1)))
            self.check_activo.configure(state="disabled")

            # Observaciones
            self.var_observaciones.set(datos_pnf.get("observaciones", ""))
            self.observaciones_entry.configure(state="disabled")

            # Botón guardar desactivado
            #self.btn_guardar.configure(state="disabled")
        else:
            messagebox.showerror("Error", "No se pudieron cargar los datos del PNF.", parent=self)

#===================================================================================

    def mostrar_uc_frame(self):
        # Si ya existe, destrúyelo antes de crear uno nuevo
        if self.uc_frame:
            self.uc_frame.destroy()
        self.uc_frame = ListaAsignacionUC(self, self.controller_pnf, self.docente)
        self.uc_frame.pack(fill="both", expand=True, pady=(10, 0))

    def obtener_uc_seleccionadas(self):
        if hasattr(self, 'uc_frame') and self.uc_frame:
            return [uc for uc, var in self.uc_frame.uc_vars if var.get()]
        return []
    
    def existe_coordinador(self):
        return self.controller_pnf.modelo.existe_coordinador(self.pnf_id_por_nombre[self.var_pnf.get()])
        
    
    
    