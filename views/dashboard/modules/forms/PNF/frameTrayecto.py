import customtkinter as ctk
import tkinter.messagebox as messagebox
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase
from views.dashboard.modules.forms.PNF.frameTramos import FrameTramos
from ..DatosPersonales import DatosPersonalesFrame
import re
class FrameTrayecto(SectionFrameBase):
    def __init__(self, master,controlador,vcmd_num, vcmd_fecha,titulo = "Trayecto"):
        super().__init__(master, titulo )
        self.master = master
        self.controlador = controlador
        self.vcmd_num = vcmd_num 
        
        # self.var = ctk.StringVar()
        # self.var.set("Activo")  # Valor por defecto para el estado
        # self.var2 = ctk.StringVar()
        # self.var2.set("Trayectos de IV")  # Valor por defecto para el tipo
        # self.var3 = ctk.StringVar()
        # self.var3.set("Técnico Superior Universitario")  # Valor por defecto para el perfil de egreso
        # self.var4 = ctk.StringVar()
        # self.var4.set("Si")  # Valor por defecto para obligatorio
        # self.var5 = ctk.StringVar()
        # self.var5.set("Si")  # Valor por defecto para secuencial
        # self.var6 = ctk.StringVar()
        # self.var6.set("Si")  # Valor por defecto para estado
        self.vcmd_fecha = vcmd_fecha # Guardar para usar en fechas
        self.lista_tramos = []
        self.lista_datos_tramos = []

        self.para_edicion = False
        self.btn_agregar_nuevos_tramos = None
        self.lista_frame_nuevos_tramos = []
        self.lista_nuevos_datos_tramos = []

        self.tipo_trayecto = int(re.search(r'\d+', titulo).group(0))
        
        # --- Fila para los datos de Trayecto ---
        self._crear_fila_widgets([
            ("Número:", crear_entry, {"width":300,"placeholder_text":"Ingrese número"}, 1, self, 'numero_entry'),
            ("Nombre:", crear_entry, {"width":360,"placeholder_text":"Ingrese nombre"}, 1, self, 'nombre_entry'),
        ])

        # --- Fila para información de Trayecto ---
        self._crear_fila_widgets([
            ("Duración en semanas:", crear_entry, {"width":300,"placeholder_text":"Ingrese duración"}, 1, self, 'duracion_semanas_entry'),
            ("Duración en horas:", crear_entry, {"width":300,"placeholder_text":"Ingrese duración"}, 1, self, 'duracion_horas_entry'),
            ("Créditos Mínimos:", crear_entry, {"width":300,"placeholder_text":"Ingrese créditos"}, 1, self, 'creditos_minimos_entry'),
            ("Créditos Máximos:", crear_entry, {"width":300,"placeholder_text":"Ingrese créditos"}, 1, self, 'creditos_maximos_entry'),
            ("Número de Tramos:", crear_option_menu, {"values":["1", "2", "3"], "command": lambda v: setattr(self.numero_tramos_menu, '_current_value',v)}, 1, self, 'numero_tramos_menu'),
        ])

        # --- Fila para información adicional de Trayecto ---
        self._crear_fila_widgets([
            ("Objetivos:", crear_entry, {"width":300,"placeholder_text":"Ingrese objetivos"}, 1, self, 'objetivos_entry'),
            ("Perfil de Egreso:", crear_option_menu, {"values":["Técnico Superior Universitario", "Ingeniería", "Licenciatura", "Doctorado", "Especialista"], "command": lambda v: setattr(self.perfil_egreso_menu, '_current_value',v)}, 1, self, 'perfil_egreso_menu'),
            ("Obligatorio:", crear_option_menu, {"values":["Si", "No"], "command": lambda v: setattr(self.obligatorio_menu, '_current_value',v)}, 1, self, 'obligatorio_menu'),
            ("Secuencial:", crear_option_menu, {"values":["Si", "No"], "command": lambda v: setattr(self.secuencial_menu, '_current_value',v)}, 1, self, 'secuencial_menu'),
            ("Estado:", crear_option_menu, {"values":["activo", "inactivo"], "command": lambda v: setattr(self.estado_option_menu, '_current_value',v)}, 1, self, 'estado_option_menu')
        ])
        # --- Fila para el botón de agregar tramos ---
        self.botones_tramos_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.botones_tramos_frame.pack(pady=(20, 0), anchor="w")  # Puedes ajustar anchor según tu diseño

        self.btn_tramos = ctk.CTkButton(
            self.botones_tramos_frame,
            text    ="Agregar Tramos",
            width=140,
            font=FUENTE_BOTON,
            fg_color=COLOR_BOTON_PRIMARIO_FG,
            hover_color=COLOR_BOTON_PRIMARIO_HOVER,
            text_color=COLOR_BOTON_PRIMARIO_TEXT,
            command=self.agregar_tramos,
            state="disabled"  # Deshabilitar al inicio
        )
        self.btn_tramos.pack(side="left", padx=(0, 10))

        # Botón para agregar nuevos tramos
        # Solo se muestra si el trayecto es editable
        self.btn_agregar_nuevos_tramos = ctk.CTkButton(
            self.botones_tramos_frame,
            text="Agregar Nuevos Tramos",
            width=140,
            font=FUENTE_BOTON,
            fg_color=COLOR_BOTON_PRIMARIO_FG,
            hover_color=COLOR_BOTON_PRIMARIO_HOVER,
            text_color=COLOR_BOTON_PRIMARIO_TEXT,
            command=self.agregar_nuevos_tramos,
            )

        # Label para mostrar el estado de los tramos cargados
        self.tramos_status_label = ctk.CTkLabel(self, text="No hay tramos cargados previamente.", font=FUENTE_LABEL_CAMPO, 
                                                 text_color=COLOR_TEXTO_PRINCIPAL, anchor="w", width=300)
        self.tramos_status_label.pack(pady=(0, 10), anchor="w")


        self.entries_a_validar = [
            self.numero_entry,
            self.nombre_entry,
            self.duracion_semanas_entry,
            self.duracion_horas_entry,
            self.creditos_minimos_entry,
            self.creditos_maximos_entry,
            self.numero_tramos_menu,
            self.objetivos_entry,
            self.perfil_egreso_menu,
            self.obligatorio_menu,
            self.secuencial_menu,
            self.estado_option_menu,
        ]

        for entry in self.entries_a_validar:
            entry.bind("<KeyRelease>", lambda event: self.validar_campos())

    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets

    def agregar_tramos(self):
        for entry in self.entries_a_validar:
            entry.bind("<KeyRelease>", lambda event: self.validar_campos_tramos_global()) 
        self.desactivar_scroll()  # Desactiva el scroll al abrir la ventana de tramos
        
        def cerrar_top():
            # Desvincula el scroll antes de destruir la ventana
            try:
                self.master.unbind_all("<MouseWheel>")
            except Exception:
                pass
            top.destroy()
            self.activar_scroll()

        top = ctk.CTkToplevel(self, fg_color="White")
        top.title("Agregar Tramos")

        ancho = 600
        alto = 500

        # Obtén el tamaño de la pantalla
        top.update_idletasks()  # Asegura que winfo_screenwidth/height sean correctos
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()

        # Calcula la posición centrada
        x = (screen_width // 2) - (ancho // 2)
        y = (screen_height // 2) - (alto // 2)

        top.geometry(f"{ancho}x{alto}+{x}+{y}")
        top.lift()
        top.focus_force()
        top.grab_set()
        #top.resizable(False, False)  # Evita que la ventana se redimensione    

        scrollable_frame = ctk.CTkScrollableFrame(top, fg_color="transparent")
        scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        numero_tramos  = int(self.numero_tramos_menu.get())
        print(numero_tramos)
        if numero_tramos <= 0:
            messagebox.showerror("Error", "Debe seleccionar un número de tramos válido.")
            return
        
        if len(self.lista_tramos) > 0:
            for frame in self.lista_tramos:
                frame.destroy() 
        self.lista_tramos = []

        # Si hay datos guardados, los muestra y deshabilita los campos
       
        if self.lista_datos_tramos:
            for i, datos in enumerate(self.lista_datos_tramos):
                tramo = FrameTramos(scrollable_frame, self.controlador, self.vcmd_num, self.vcmd_fecha, titulo=f"Tramo #{i+1}")

                tramo.pack(fill="x", padx=10, pady=10)
                # Define el orden y las llaves esperadas según tu modelo y formulario
                campos = [
                    "numero",             # Número
                    "nombre",             # Nombre
                    "duracion_semanas",   # Duración en semanas
                    "duracion_horas",     # Duración en horas
                    "creditos",           # Créditos (o "creditos_minimos" si así lo guardas)
                    "objetivos",          # Objetivos
                    "estado"              # Estado
                ]
                print("si")
                for entry, campo in zip(tramo.entries_a_validar, campos):
                    valor = datos.get(campo, "")
                    if isinstance(entry, ctk.CTkOptionMenu):
                        entry.set(valor)
                    else:
                        entry.insert(0, valor)
                    if self.para_edicion == False:
                        entry.configure(state="disabled")
                tramo.numero_entry.configure(state="disabled")
                self.lista_tramos.append(tramo)
            # No permite grabar de nuevo
            self.button_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
            self.button_frame.pack(pady=(25, 20))
            if self.para_edicion:
                self.btn_guardar = ctk.CTkButton(self.button_frame, text="Grabar Datos Nuevos", width=140, command= lambda:self.procesar_tramos(top),
                                            font=FUENTE_BOTON, fg_color=COLOR_BOTON_PRIMARIO_FG, hover_color=COLOR_BOTON_PRIMARIO_HOVER, text_color=COLOR_BOTON_PRIMARIO_TEXT,
                                            state="normal")
                self.btn_guardar.pack(side="left", padx=10)

            self.btn_cancelar = ctk.CTkButton(self.button_frame, text="Cerrar", width=140, command=cerrar_top,
                                            font=FUENTE_BOTON, fg_color=COLOR_BOTON_SECUNDARIO_FG, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, text_color=COLOR_BOTON_SECUNDARIO_TEXT)
            self.btn_cancelar.pack(side="left", padx=10)
            top.protocol("WM_DELETE_WINDOW", cerrar_top)
            top.mainloop()
            return

        # Si no hay datos guardados, crea los tramos según el número seleccionado
        for i in range(numero_tramos):
            tramo = FrameTramos(scrollable_frame, self.controlador, self.vcmd_num, self.vcmd_fecha, titulo=f"Tramo #{i+1}")
            tramo.numero_entry.insert(0, i + 1)  # Asigna el número del tramo
            tramo.numero_entry.configure(state="disabled")  # Deshabilita el campo de número
            tramo.pack(fill="x", padx=10, pady=10)
            self.lista_tramos.append(tramo)
            # Vincula la validación a cada campo de cada tramo
            for entry in tramo.entries_a_validar:
                entry.bind("<KeyRelease>", lambda event: self.validar_campos_tramos_global())

        # Botón para cerrar la ventana de tramos
        # Empacar los frames
        self.button_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        self.button_frame.pack(pady=(25, 20))

        self.btn_guardar = ctk.CTkButton(self.button_frame, text="Grabar Datos", width=140, command= lambda:self.procesar_tramos(top),
                                        font=FUENTE_BOTON, fg_color=COLOR_BOTON_PRIMARIO_FG, hover_color=COLOR_BOTON_PRIMARIO_HOVER, text_color=COLOR_BOTON_PRIMARIO_TEXT,
                                        state="disabled")
        self.btn_guardar.pack(side="left", padx=10)

        #self.validar_campos_tramos_global(self.btn_guardar)

        self.btn_cancelar = ctk.CTkButton(self.button_frame, text="Cerrar", width=140, command=cerrar_top,
                                        font=FUENTE_BOTON, fg_color=COLOR_BOTON_SECUNDARIO_FG, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, text_color=COLOR_BOTON_SECUNDARIO_TEXT)
        self.btn_cancelar.pack(side="left", padx=10)
        
    #    self.btn_guardar.configure(state="desabled")  # Deshabilitar el botón de guardar al inicio
        top.protocol("WM_DELETE_WINDOW", cerrar_top) # Para manejar el cierre de la ventana
        self.validar_campos_tramos_global()
        top.mainloop()
    
    #metodo para agregar nuevos tramos
    def agregar_nuevos_tramos(self):
        self.desactivar_scroll()  # Desactiva el scroll al abrir la ventana de tramos
        self.lista_frame_nuevos_tramos = []  # Limpia la lista para evitar duplicados

        def cerrar_top():
            try:
                self.master.unbind_all("<MouseWheel>")
            except Exception:
                pass
            top.destroy()
            self.activar_scroll()

        top = ctk.CTkToplevel(self, fg_color="White")
        top.title("Agregar Tramos")
        ancho = 600
        alto = 500
        top.update_idletasks()
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        x = (screen_width // 2) - (ancho // 2)
        y = (screen_height // 2) - (alto // 2)
        top.geometry(f"{ancho}x{alto}+{x}+{y}")
        top.lift()
        top.focus_force()
        top.grab_set()

        scrollable_frame = ctk.CTkScrollableFrame(top, fg_color="transparent")
        scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        numero_tramos = int(self.numero_tramos_menu.get())
        cantidad_tramos_actuales = len(self.lista_datos_tramos)
        cantidad_tramos_nuevos = numero_tramos - cantidad_tramos_actuales

        # --- FUNCIÓN DE VALIDACIÓN LOCAL ---
        def validar_campos_nuevos_tramos():
            todos_llenos = True
            for frame in self.lista_frame_nuevos_tramos:
                for entry in getattr(frame, "entries_a_validar", []):
                    try:
                        valor = str(entry.get()).strip()
                    except Exception:
                        todos_llenos = False
                        break
                    if valor == "":
                        todos_llenos = False
                        break
                if not todos_llenos:
                    break
            if hasattr(self, "btn_guardar") and self.btn_guardar.winfo_exists():
                if todos_llenos and self.lista_frame_nuevos_tramos:
                    self.btn_guardar.configure(state="normal")
                else:
                    self.btn_guardar.configure(state="disabled")

        # --- CREACIÓN DE TRAMOS NUEVOS ---
        if cantidad_tramos_nuevos > 0:
            for i in range(cantidad_tramos_nuevos):
                frame = FrameTramos(scrollable_frame, self.controlador, self.vcmd_num, self.vcmd_fecha, titulo=f"Tramo #{cantidad_tramos_actuales + i + 1}")
                frame.numero_entry.insert(0, cantidad_tramos_actuales + i + 1)  # Asigna el número del tramo
                frame.numero_entry.configure(state="disabled")  # Deshabilita el campo de número
                frame.pack(fill="x", padx=10, pady=10)
                self.lista_frame_nuevos_tramos.append(frame)
                # Vincula la validación a cada campo de cada tramo  
                for entry in frame.entries_a_validar:
                    entry.bind("<KeyRelease>", lambda event: validar_campos_nuevos_tramos())

        self.button_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        self.button_frame.pack(pady=(25, 20))
        if self.para_edicion:
            self.btn_guardar = ctk.CTkButton(self.button_frame, text="Grabar Datos Nuevos", width=140, command=lambda: self.procesar_tramos_nuevos(top),
                                        font=FUENTE_BOTON, fg_color=COLOR_BOTON_PRIMARIO_FG, hover_color=COLOR_BOTON_PRIMARIO_HOVER, text_color=COLOR_BOTON_PRIMARIO_TEXT,
                                        state="disabled")  # Deshabilitado al inicio
            self.btn_guardar.pack(side="left", padx=10)

        self.btn_cancelar = ctk.CTkButton(self.button_frame, text="Cerrar", width=140, command=cerrar_top,
                                        font=FUENTE_BOTON, fg_color=COLOR_BOTON_SECUNDARIO_FG, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, text_color=COLOR_BOTON_SECUNDARIO_TEXT)
        self.btn_cancelar.pack(side="left", padx=10)
        top.protocol("WM_DELETE_WINDOW", cerrar_top)

        # Llama a la validación al final para el estado inicial
        validar_campos_nuevos_tramos()
        top.mainloop()

    def _on_mousewheel(self, event):
        # Ajusta el nombre del frame si tu scrollable_frame tiene otro nombre
        try:
            canvas = getattr(self.master, "_parent_canvas", None)
            if canvas and str(canvas):
                canvas.yview_scroll(int(-1*(event.delta/2)), "units")
        except Exception:
            pass
    # Deshabilitar el scroll
    def desactivar_scroll(self):
        self.master.unbind_all("<MouseWheel>")

    # Habilitar el scroll
    def activar_scroll(self):
        self.master.bind_all("<MouseWheel>", self._on_mousewheel)

    def procesar_tramos(self,top = None):
       
        self.lista_datos_tramos = []
        if self.lista_tramos:
            for frame in self.lista_tramos:
                datos = frame.procesar_tramo()
                self.lista_datos_tramos.append(datos)
        if top:
            messagebox.showinfo("Información", "Tramos procesados correctamente.",parent=top)

        # Cierra la ventana de tramos si está abierta
        for widget in self.master.winfo_children():
            if isinstance(widget, ctk.CTkToplevel):
                widget.destroy()
                break
        self.activar_scroll()
        self.deshabilitar_campos_tramos()
        self.actualizar_status_tramos()
        return self.lista_datos_tramos
        
    def procesar_tramos_nuevos(self,top = None):
        self.lista_nuevos_datos_tramos = []
        if self.lista_frame_nuevos_tramos:
            for frame in self.lista_frame_nuevos_tramos:
                datos = frame.procesar_tramo()
                self.lista_nuevos_datos_tramos.append(datos)
        #print(self.lista_nuevos_datos_tramos)
        if top:
            messagebox.showinfo("Información", "Tramos procesados correctamente.",parent=top)

        # Cierra la ventana de tramos si está abierta
        for widget in self.master.winfo_children():
            if isinstance(widget, ctk.CTkToplevel):
                widget.destroy()
                break
        self.activar_scroll()
        self.actualizar_status_tramos()
        #return self.lista_nuevos_datos_tramos
    
    def obtener_datos_trayectos(self, lis_datos=None):
        # 1. Obtén los datos del trayecto principal
        datos_trayecto = {
            "numero": self.numero_entry.get(),
            "nombre": self.nombre_entry.get(),
            "duracion_semanas": self.duracion_semanas_entry.get(),
            "duracion_horas": self.duracion_horas_entry.get(),
            "creditos_minimos": self.creditos_minimos_entry.get(),
            "creditos_maximos": self.creditos_maximos_entry.get(),
            "numero_tramos": self.numero_tramos_menu.get(),
            "objetivos": self.objetivos_entry.get(),
            "perfil_egreso": self.perfil_egreso_menu.get(),
            "obligatorio": self.obligatorio_menu.get(),
            "secuencial": self.secuencial_menu.get(),
            "estado": self.estado_option_menu.get(),
        }

        # 2. Obtén los datos de los tramos asociados a este trayecto
        lista_tramos = []
        for frame_tramo in self.lista_tramos:
            if frame_tramo.winfo_exists() and hasattr(frame_tramo, "procesar_tramo"):
                datos_tramo = frame_tramo.procesar_tramo()
                if datos_tramo:
                    lista_tramos.append(datos_tramo)
        datos_trayecto["lista_tramos"] = self.lista_datos_tramos
        if self.lista_nuevos_datos_tramos:
            datos_trayecto["lista_tramos_nuevos"] = self.lista_nuevos_datos_tramos
        else:
            datos_trayecto["lista_tramos_nuevos"] = []
        return datos_trayecto

    def validar_campos(self):
        todos_llenos = all(str(entry.get()).strip() for entry in self.entries_a_validar)
        if todos_llenos:
            self.btn_tramos.configure(state="normal")
        else:
            self.btn_tramos.configure(state="disabled")

    def validar_campos_tramos_global(self):
        todos_llenos = True
        for frame_tramo in self.lista_tramos:
            for entry in getattr(frame_tramo, "entries_a_validar", []):
                try:
                    valor = str(entry.get()).strip()
                except Exception:
                    todos_llenos = False
                    break
                if valor == "":
                    todos_llenos = False
                    break
            if not todos_llenos:
                break
        # Verifica que el botón existe antes de configurarlo
        if hasattr(self, "btn_guardar") and self.btn_guardar.winfo_exists():
            if todos_llenos and self.lista_tramos:
                self.btn_guardar.configure(state="normal")
            else:
                self.btn_guardar.configure(state="disabled")

    def deshabilitar_campos_tramos(self):
        # Deshabilita todos los campos de los tramos y el botón de guardar
        for frame_tramo in getattr(self, "lista_tramos", []):
            for entry in getattr(frame_tramo, "entries_a_validar", []):
                entry.configure(state="disabled")
        if hasattr(self, "btn_guardar"):
            self.btn_guardar.configure(state="disabled")

    def actualizar_status_tramos(self):
        cantidad = len(self.lista_datos_tramos)
        if cantidad == 0:
            self.tramos_status_label.configure(text="No hay tramos cargados previamente.")
        else:
            self.tramos_status_label.configure(text=f"{cantidad} tramo(s) cargado(s) correctamente.")
        

    def set_datos(self, datos):
        if datos:
            self.numero_entry.insert(0, datos.get("numero", ""))
            self.numero_entry.configure(state="disabled")
            self.nombre_entry.insert(0, datos.get("nombre", ""))
            self.nombre_entry.configure(state="disabled")
            self.duracion_semanas_entry.insert(0, datos.get("duracion_semanas", ""))
            self.duracion_semanas_entry.configure(state="disabled")
            self.duracion_horas_entry.insert(0, datos.get("duracion_horas", ""))
            self.duracion_horas_entry.configure(state="disabled")
            self.creditos_minimos_entry.insert(0, datos.get("creditos_minimos", ""))
            self.creditos_minimos_entry.configure(state="disabled")
            self.creditos_maximos_entry.insert(0, datos.get("creditos_maximos", ""))
            self.creditos_maximos_entry.configure(state="disabled")
            self.numero_tramos_menu.set(str(datos.get("numero_tramos", "")))
            self.numero_tramos_menu.configure(state="disabled")
            self.objetivos_entry.insert(0, datos.get("objetivos", ""))
            self.objetivos_entry.configure(state="disabled")
            self.perfil_egreso_menu.set(datos.get("perfil_egreso", ""))
            self.perfil_egreso_menu.configure(state="disabled")
            self.obligatorio_menu.set("Si" if datos.get("obligatorio", True) else "No")
            self.obligatorio_menu.configure(state="disabled")
            self.secuencial_menu.set("Si" if datos.get("secuencial", True) else "No")
            self.secuencial_menu.configure(state="disabled")
            self.estado_option_menu.set(datos.get("estado", "activo"))
            self.estado_option_menu.configure(state="disabled")
            if datos["lista_tramos"]:
                self.lista_datos_tramos = datos["lista_tramos"]
                self.btn_tramos.configure(text="Ver Tramos",state="normal",command=lambda:self.decirhola(datos["lista_tramos"]))
                self.tramos_status_label.configure(text = "Hay tramos cargados")

        else:
            for campo in self.entries_a_validar:
                campo.configure(state="disabled")
        
    def decirhola(self,lista_datos):
       if not self.lista_datos_tramos:
            self.lista_datos_tramos = lista_datos
       self.agregar_tramos()

    def habilitar_campos(self):
        for campo in self.entries_a_validar:
            campo.configure(state="normal")
        self.numero_entry.configure(state="disabled")  # Deshabilitar el campo de número
        self.para_edicion = True

        self.btn_agregar_nuevos_tramos.pack(side="left")
