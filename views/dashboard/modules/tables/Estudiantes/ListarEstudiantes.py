import customtkinter as ctk
import tkinter as tk
import threading
from views.dashboard.components.widget_utils import *
from views.dashboard.modules.FiltradoBusqueda import FiltradoBusquedaFrame
from views.dashboard.modules.RegistrarEstudiantes import FormularioEstudianteView
from views.dashboard.modules.forms.Estudiantes.asignar_pnf import AsignarPNFFrame


class ListEstudiantesView(ctk.CTkFrame):
    def __init__(self, master, controlador,controller_pnf = None):
        super().__init__(master, fg_color="white")
        self.furmulario_estudiante = FormularioEstudianteView(master, controlador)
        self.master = master
        self.controlador = controlador
        self.controller_pnf = controller_pnf
        
        self.filas_datos = []
        self.cantidad_estudiantes = self.controlador.modelo.obtener_cantidad_estudiantes()
        self.pagina_actual = 1
        self.primer_id_table = self.controlador.modelo.obtener_primer_id()
        self.estudiantes =  self.controlador.obtener_lista_estudiantes(0)
        self.registros_por_pagina = 17
        # Calcula la cantidad total de páginas, asegurando al menos 1 si hay registros
        self.cantidad_total_paginas = (self.cantidad_estudiantes // self.registros_por_pagina) + (1 if self.cantidad_estudiantes % self.registros_por_pagina > 0 else 0)
       
        # Si no hay estudiantes, la cantidad total de páginas es 1 para mostrar la interfaz vacía
        if self.cantidad_estudiantes == 0:
            self.cantidad_total_paginas = 1

        # Validación de campos
        try:
            toplevel = self.winfo_toplevel()

            self.vcmd_num_val = toplevel.register(self.controlador._solo_numeros)
            self.vcmd_fecha_val = toplevel.register(self.controlador._numeros_y_barras)
            self.vcmd_decimal_val = toplevel.register(self.controlador._solo_decimal)
        except Exception: # Fallback si no es un toplevel (ej. si el master es el root)
            self.vcmd_num_val = master.register(self.controlador._solo_numeros)
            self.vcmd_fecha_val = master.register(self.controlador._numeros_y_barras)
            self.vcmd_decimal_val = master.register(self.controlador._solo_decimal)

        # --- FILTRADO DE BÚSQUEDA (FILA 0) ---
        self.busqueda_frame = FiltradoBusquedaFrame(self,self.controlador,self.vcmd_num_val)
        self.busqueda_frame.grid(row=0, column=0, columnspan=6, padx=15, pady=(10, 0), sticky="ew")

        # --- ENCABEZADOS (FILA 1) ---
        headers = ["Tipo Doc.", "Número Doc.", "Nombres", "Apellidos", "Código SNI", "Acción"]
        for col, header in enumerate(headers):
            celda = ctk.CTkFrame(self, fg_color="#e0e0e0", corner_radius=4)
            celda.grid(row=1, column=col, padx=1, pady=1, sticky="nsew")
            label = ctk.CTkLabel(celda, text=header, font=ctk.CTkFont(weight="bold"), text_color=COLOR_TEXTO_PRINCIPAL)
            label.pack(padx=10, pady=5)
        for i in range(len(headers)):
            self.grid_columnconfigure(i, weight=1)

        # --- PAGINACIÓN (se ubicará dinámicamente al final de los datos) ---
        self.frame_paginacion = ctk.CTkFrame(self, fg_color="transparent")
        
        # Configuración de columnas para centrar los elementos de paginación
        # Columna 0 y Columna 4 se expanden para empujar el contenido al centro
        self.frame_paginacion.grid_columnconfigure(0, weight=1) # Columna vacía a la izquierda
        self.frame_paginacion.grid_columnconfigure(1, weight=0) # Columna para botón Anterior (no se expande)
        self.frame_paginacion.grid_columnconfigure(2, weight=0) # Columna para label de página (no se expande)
        self.frame_paginacion.grid_columnconfigure(3, weight=0) # Columna para botón Siguiente (no se expande)
        self.frame_paginacion.grid_columnconfigure(4, weight=1) # Columna vacía a la derecha

        self.boton_anterior = ctk.CTkButton(self.frame_paginacion, text="Anterior", command=self.anterior_pagina)
        self.label_pagina = ctk.CTkLabel(self.frame_paginacion, text=f"{self.pagina_actual} de {self.cantidad_total_paginas}", text_color=COLOR_TEXTO_PRINCIPAL)
        self.boton_siguiente = ctk.CTkButton(self.frame_paginacion, text="Siguiente", command=self.siguiente_pagina)
        
        # Posicionar los botones y el label en las columnas centrales del frame de paginación
        self.boton_anterior.grid(row=0, column=1, padx=(0, 5))
        self.label_pagina.grid(row=0, column=2, padx=5)
        self.boton_siguiente.grid(row=0, column=3, padx=(5, 0))

        # Deshabilita el botón "Anterior" si es la primera página
        self.boton_anterior.configure(state="disabled" if self.pagina_actual == 1 else "normal")
        # Deshabilita el botón "Siguiente" si es la última página
        self.boton_siguiente.configure(state="disabled" if self.pagina_actual == self.cantidad_total_paginas else "normal")

        self.mostrar_pagina()

    def mostrar_pagina(self, indicador = False):
        """
        Muestra los estudiantes de la página actual y actualiza el estado de los botones.
        """
        if indicador:
            # Si se indica, se recarga la página actual
            self.estudiantes = self.controlador.obtener_lista_estudiantes((self.pagina_actual - 1) * self.registros_por_pagina)

        self.cargar_datos(self.estudiantes)
        self.label_pagina.configure(text=f"{self.pagina_actual} de {self.cantidad_total_paginas}")

        # Actualizar estado de los botones de paginación
        self.boton_anterior.configure(state="disabled" if self.pagina_actual == 1 else "normal")
        self.boton_siguiente.configure(state="disabled" if self.pagina_actual == self.cantidad_total_paginas else "normal")

    def mostrar_resultado_busqueda(self, lista_estudiantes):
        """
        Muestra solo los estudiantes pasados en la lista (por ejemplo, el resultado de una búsqueda).
        Deshabilita la paginación y actualiza la tabla.
        """
        self.pagina_actual = 1  # <-- Reinicia la página actual
        self.cargar_datos(lista_estudiantes)
        self.boton_anterior.configure(state="disabled")
        #self.boton_siguiente.configure(state="disabled")
        self.label_pagina.configure(text="1 de 1")
        
    def siguiente_pagina(self):
        """
            Avanza a la siguiente página de estudiantes.
        """
        # Asegura que no se exceda la cantidad total de páginas
        if self.pagina_actual < self.cantidad_total_paginas:
            self.pagina_actual += 1
            # Calcula el offset para la siguiente página
            offset = (self.pagina_actual - 1) * self.registros_por_pagina
            self.cargar_estudiantes_en_segundo_plano(offset)


    def anterior_pagina(self):
        """
        Retrocede a la página anterior de estudiantes.
        """
        # Asegura que no se vaya a una página menor que 1
        if self.pagina_actual > 1:
            self.pagina_actual -= 1
            # Calcula el offset para la página anterior
            offset = (self.pagina_actual - 1) * self.registros_por_pagina
            self.cargar_estudiantes_en_segundo_plano(offset)


    def cargar_estudiantes_en_segundo_plano(self, offset):
        """
        Carga los estudiantes en un hilo separado para no bloquear la interfaz de usuario.
        """
        self.boton_anterior.configure(state="disabled")
        self.boton_siguiente.configure(state="disabled")
        
        def tarea():
            # Obtiene la lista de estudiantes usando el offset calculado
            self.estudiantes = self.controlador.obtener_lista_estudiantes(offset)
            # Actualiza la interfaz de usuario en el hilo principal
            self.after(0, self.mostrar_pagina)
            self.after(0, lambda: self.boton_anterior.configure(state="normal"))
            self.after(0, lambda: self.boton_siguiente.configure(state="normal"))
            
        
        threading.Thread(target=tarea).start()


    def cargar_datos(self, datos):
        """
        Elimina las filas de datos anteriores y carga las nuevas filas.
        """
        # Eliminar filas anteriores
        for fila in self.filas_datos:
            for widget in fila:
                widget.destroy()
        self.filas_datos.clear()

        # Cargar nueva página (desde la fila 2)
        for i, estudiante in enumerate(datos, start=2):
            fila_widgets = [
                self._crear_celda(i, 0, estudiante['tipo_documento']),
                self._crear_celda(i, 1, estudiante['documento_identidad']),
                self._crear_celda(i, 2, estudiante['nombres']),
                self._crear_celda(i, 3, estudiante['apellidos']),
                self._crear_celda(i, 4, estudiante['codigo_unico']),
            ]

            celda_btn = ctk.CTkFrame(self, fg_color="#f5f5f5", corner_radius=4)
            celda_btn.grid(row=i, column=5, padx=(1, 0), pady=1, sticky="nsew")

            # Frame interno para centrar los botones
            frame_botones = ctk.CTkFrame(celda_btn, fg_color="transparent")
            frame_botones.pack(expand=True)

            boton = ctk.CTkButton(
                frame_botones, text="Ver datos", width=100,
                text_color=COLOR_ENTRY_BG,
                command=lambda est=estudiante: self.furmulario_estudiante.ver_datos_completos(est, self)
            )
            # averiguar si el estudiante tiene un PNF asignado
            if not self.controller_pnf.modelo.tiene_pnf_asignado(estudiante['id']):
                text = "Asignar PNF"
                callback = lambda est=estudiante: self.cargar_pnf(est)
            else:
                text = "Ver PNF"
                callback = lambda est=estudiante: self.cargar_pnf(est,para_edicion=True)

            btn_pnf = ctk.CTkButton(
                frame_botones, text=text, width=100,
                text_color="#ffffff",
                fg_color=COLOR_BOTON_FONDO,
                hover_color=COLOR_BOTON_FONDO_HOVER,
                command=callback
            )

            boton.pack(side="left", padx=(0, 4), pady=5)
            btn_pnf.pack(side="left", pady=5)

            fila_widgets.append(celda_btn)
            self.filas_datos.append(fila_widgets)
            

        # SIEMPRE coloca el frame de paginación en la fila siguiente a la última
        # La fila de inicio de los datos es 2, así que si hay 'n' datos, la última fila de datos es 2 + n - 1.

        fila_paginacion = len(datos) + 2
        self.frame_paginacion.grid(row=fila_paginacion, column=0, columnspan=6, pady=15, sticky="ew")

    def _crear_celda(self, row, col, texto):
        """
        Crea una celda de tabla con un fondo y texto específicos.
        """
        celda = ctk.CTkFrame(self, fg_color="#f5f5f5", corner_radius=4)
        celda.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
        label = ctk.CTkLabel(celda, text=texto, text_color=COLOR_TEXTO_PRINCIPAL)
        label.pack(padx=10, pady=5)
        return celda

    def cargar_pnf(self, estudiante,para_edicion=False):
        """
        Abre el formulario para asignar un PNF al estudiante seleccionado.
        """
        # Si ya hay un formulario abierto, lo destruye 
        top = ctk.CTkToplevel(self, fg_color="White")
        top.title("Asignar PNF")
        ancho = 900
        alto = 700

        # Centrar ventana
        top.update_idletasks()
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        x = (screen_width // 2) - (ancho // 2)
        y = (screen_height // 2) - (alto // 2)
        top.geometry(f"{ancho}x{alto}+{x}+{y}")
        top.lift()
        top.focus_force()
        top.grab_set()

        # Scroll principal del modal
        scroll_frame = ctk.CTkScrollableFrame(top, fg_color="White")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        if para_edicion:
            titulo = "Editar PNF de Estudiante"
        else:
            titulo = "Asignar PNF a Estudiante"

        ctk.CTkLabel(scroll_frame, text=titulo, font=FUENTE_TITULO_FORMULARIO, text_color=COLOR_TEXTO_PRINCIPAL).pack(pady=(10, 20), padx=20, anchor="w")

        # Crea el frame para asignar PNF
        
        if para_edicion:
            asignar_pnf_frame = AsignarPNFFrame(scroll_frame, self.controlador,self.controller_pnf, estudiante,True)
            # Si es para edición, carga los datos del PNF asignado
            asignar_pnf_frame.cargar_datos_pnf(estudiante['id'])
        else:
            asignar_pnf_frame = AsignarPNFFrame(scroll_frame, self.controlador,self.controller_pnf, estudiante,False)
        asignar_pnf_frame.pack(fill="both", expand=True)
