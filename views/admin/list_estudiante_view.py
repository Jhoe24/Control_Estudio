import customtkinter as ctk
import tkinter as tk
import threading
from util.widget_utils import *
from .Frames_Estudiantes.Filtrado_Busqueda import FiltradoBusquedaFrame
from .estudiante_form_view import FormularioEstudianteView

class ListEstudiantesView(ctk.CTkScrollableFrame):
    def __init__(self, master, controlador):
        super().__init__(master, fg_color="white")
        self.furmulario_estudiante = FormularioEstudianteView(master, controlador)
        self.master = master
        self.controlador = controlador
        self.color_texto = "#222222"
        self.filas_datos = []
        self.cantidad_estudiantes = self.controlador.master_controlador.estudiantes.modelo.obtener_cantidad_estudiantes()
        self.pagina_actual = 1
        self.primer_id_table = self.controlador.master_controlador.estudiantes.modelo.obtener_primer_id()
        self.estudiantes = self.controlador.master_controlador.estudiantes.obtener_lista_estudiantes(0)
        self.registros_por_pagina = 10
        # Calcula la cantidad total de páginas, asegurando al menos 1 si hay registros
        self.cantidad_total_paginas = (self.cantidad_estudiantes // self.registros_por_pagina) + (1 if self.cantidad_estudiantes % self.registros_por_pagina > 0 else 0)
       
        # Si no hay estudiantes, la cantidad total de páginas es 1 para mostrar la interfaz vacía
        if self.cantidad_estudiantes == 0:
            self.cantidad_total_paginas = 1

        # Validación de campos
        try:
            toplevel = self.winfo_toplevel()
            self.vcmd_num_val = toplevel.register(self.controlador.master_controlador.estudiantes._solo_numeros)
            self.vcmd_fecha_val = toplevel.register(self.controlador.master_controlador.estudiantes._numeros_y_barras)
            self.vcmd_decimal_val = toplevel.register(self.controlador.master_controlador.estudiantes._solo_decimal)
        except Exception: # Fallback si no es un toplevel (ej. si el master es el root)
            self.vcmd_num_val = master.register(self.controlador.master_controlador.estudiantes._solo_numeros)
            self.vcmd_fecha_val = master.register(self.controlador.master_controlador.estudiantes._numeros_y_barras)
            self.vcmd_decimal_val = master.register(self.controlador.master_controlador.estudiantes._solo_decimal)

        # --- FILTRADO DE BÚSQUEDA (FILA 0) ---
        self.busqueda_frame = FiltradoBusquedaFrame(self,self.controlador,self.vcmd_num_val)
        self.busqueda_frame.grid(row=0, column=0, columnspan=6, padx=15, pady=(10, 0), sticky="ew")

        # --- ENCABEZADOS (FILA 1) ---
        headers = ["Tipo Doc.", "Número Doc.", "Nombres", "Apellidos", "Código SNI", "Acción"]
        for col, header in enumerate(headers):
            celda = ctk.CTkFrame(self, fg_color="#e0e0e0", corner_radius=4)
            celda.grid(row=1, column=col, padx=1, pady=1, sticky="nsew")
            label = ctk.CTkLabel(celda, text=header, font=ctk.CTkFont(weight="bold"), text_color=self.color_texto)
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
        self.label_pagina = ctk.CTkLabel(self.frame_paginacion, text=f"{self.pagina_actual} de {self.cantidad_total_paginas}", text_color=self.color_texto)
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

    def mostrar_pagina(self):
        """
        Muestra los estudiantes de la página actual y actualiza el estado de los botones.
        """
        self.cargar_datos(self.estudiantes)
        self.label_pagina.configure(text=f"{self.pagina_actual} de {self.cantidad_total_paginas}")

        # Actualizar estado de los botones de paginación
        self.boton_anterior.configure(state="disabled" if self.pagina_actual == 1 else "normal")
        self.boton_siguiente.configure(state="disabled" if self.pagina_actual == self.cantidad_total_paginas else "normal")


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
            self.estudiantes = self.controlador.master_controlador.estudiantes.obtener_lista_estudiantes(offset)
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
            celda_btn.grid(row=i, column=5, padx=1, pady=1, sticky="nsew")
            boton = ctk.CTkButton(
                celda_btn, text="Ver datos", width=100,
                text_color=self.color_texto,
                command=lambda est=estudiante: self.furmulario_estudiante.ver_datos_completos(est)
            )
            boton.pack(padx=10, pady=5)
            fila_widgets.append(celda_btn)
            self.filas_datos.append(fila_widgets)

        # SIEMPRE coloca el frame de paginación en la fila siguiente a la última
        # La fila de inicio de los datos es 2, asÃ­ que si hay 'n' datos, la Ãºltima fila de datos es 2 + n - 1.
        # La fila de paginaciÃ³n serÃ¡ 2 + n.
        fila_paginacion = len(datos) + 2
        self.frame_paginacion.grid(row=fila_paginacion, column=0, columnspan=6, pady=15, sticky="ew")

    def _crear_celda(self, row, col, texto):
        """
        Crea una celda de tabla con un fondo y texto específicos.
        """
        celda = ctk.CTkFrame(self, fg_color="#f5f5f5", corner_radius=4)
        celda.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
        label = ctk.CTkLabel(celda, text=texto, text_color=self.color_texto)
        label.pack(padx=10, pady=5)
        return celda

    