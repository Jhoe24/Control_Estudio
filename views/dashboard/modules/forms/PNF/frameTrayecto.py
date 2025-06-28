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
        
        self.btn_tramos = ctk.CTkButton(
            self,
            text    ="Agregar Tramos",
            width=140,
            font=FUENTE_BOTON,
            fg_color=COLOR_BOTON_PRIMARIO_FG,
            hover_color=COLOR_BOTON_PRIMARIO_HOVER,
            text_color=COLOR_BOTON_PRIMARIO_TEXT,
            command=self.agregar_tramos,
            state="disabled"  # Deshabilitar al inicio
        )
        self.btn_tramos.pack(pady=(20, 0), ancho="w")

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
                # Asigna los valores guardados a los campos
                for entry, valor in zip(tramo.entries_a_validar, datos.values()):
                    if isinstance(entry, ctk.CTkOptionMenu):
                        entry.set(valor)
                    else:
                        entry.insert(0, valor)
                    entry.configure(state="disabled")  # Deshabilita el campo
                self.lista_tramos.append(tramo)
            # No permite grabar de nuevo
            self.button_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
            self.button_frame.pack(pady=(25, 20))
            self.btn_cancelar = ctk.CTkButton(self.button_frame, text="Cerrar", width=140, command=cerrar_top,
                                            font=FUENTE_BOTON, fg_color=COLOR_BOTON_SECUNDARIO_FG, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, text_color=COLOR_BOTON_SECUNDARIO_TEXT)
            self.btn_cancelar.pack(side="left", padx=10)
            top.protocol("WM_DELETE_WINDOW", cerrar_top)
            top.mainloop()
            return

        # Si no hay datos guardados, crea los tramos según el número seleccionado
        for i in range(numero_tramos):
            tramo = FrameTramos(scrollable_frame, self.controlador, self.vcmd_num, self.vcmd_fecha, titulo=f"Tramo #{i+1}")
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

    def _on_mousewheel(self, event):
        # Ajusta el nombre del frame si tu scrollable_frame tiene otro nombre
        try:
            self.master._parent_canvas.yview_scroll(int(-1*(event.delta/2)), "units")
        except AttributeError:
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
        messagebox.showinfo("Información", "Tramos procesados correctamente.")

        # Cierra la ventana de tramos si está abierta
        for widget in self.master.winfo_children():
            if isinstance(widget, ctk.CTkToplevel):
                widget.destroy()
                break
        self.activar_scroll()
        self.deshabilitar_campos_tramos()
        self.actualizar_status_tramos()
        return self.lista_datos_tramos
        
    def obtener_datos_trayectos(self):
        return self.controlador.getTrayectos(self,self.lista_datos_tramos)

    def validar_campos(self):
        todos_llenos = all(entry.get().strip() for entry in self.entries_a_validar)
        if todos_llenos:
            self.btn_tramos.configure(state="normal")
        else:
            self.btn_tramos.configure(state="disabled")

    def validar_campos_tramos_global(self):
         # Verifica que todos los FrameTramos existan y todos sus campos estén llenos
        todos_llenos = True
        for frame_tramo in self.lista_tramos:
            for entry in getattr(frame_tramo, "entries_a_validar", []):
                # Verifica que el entry tenga el método get (no ha sido destruido)
                if not hasattr(entry, "get") or entry.get() is None or entry.get().strip() == "":
                    todos_llenos = False
                    break
            if not todos_llenos:
                break
        if hasattr(self, "btn_guardar"):
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
        else:
            for campo in self.entries_a_validar:
                campo.configure(state="disabled")