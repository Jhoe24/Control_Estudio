import customtkinter as ctk
import tkinter as tk
from views.dashboard.components.widget_utils import *
from views.dashboard.modules.forms.PNF.FormPNF import DatosPNFPensumFrame
from views.dashboard.modules.forms.PNF.frameTrayecto import FrameTrayecto
from pprint import pprint

class ListarPNF(ctk.CTkScrollableFrame):
    """
    Frame principal para listar, visualizar y editar los PNF y sus trayectos.
    Incluye paginación, visualización modal y edición de datos.
    """
    def __init__(self, master, controller):
        """
        Inicializa el frame de listado de PNF con paginación y configuración de eventos.
        """
        super().__init__(master, fg_color="white")
        self.controller = controller
        self.lista_pnf = self.controller.listado_pnf  # Lista de tuplas (id, codigo, nombre)
        self.nuevos_trayectos = []
        self.frame_pnf = None
        self.list_trayecto = []
        self.button_trayecto = None
        self.botones_frame = None

        self.pagina_actual = 1
        self.cantidad_mostrar = 5
        self.cantidad_paginas = (len(self.lista_pnf) // self.cantidad_mostrar) + (1 if len(self.lista_pnf) % self.cantidad_mostrar > 0 else 0)
        self.filas_datos = []

        # Validadores para los campos
        try:
            toplevel = self.winfo_toplevel()
            self.vcmd_num_val = toplevel.register(self.controller._solo_numeros)
            self.vcmd_fecha_val = toplevel.register(self.controller._numeros_y_barras)
            self.vcmd_decimal_val = toplevel.register(self.controller._solo_decimal)
        except Exception:
            self.vcmd_num_val = master.register(self.controller._solo_numeros)
            self.vcmd_fecha_val = master.register(self.controller._numeros_y_barras)
            self.vcmd_decimal_val = master.register(self.controller._solo_decimal)

        # Primeras páginas a mostrar
        self.paginas_mostrar = self.lista_pnf[:self.cantidad_mostrar]
        self.posicion_actual = len(self.paginas_mostrar)

        # Encabezados de la tabla
        headers = ["ID", "Código", "Nombre", "Acción"]
        for col, header in enumerate(headers):
            celda = ctk.CTkFrame(self, fg_color="#e0e0e0", corner_radius=4)
            celda.grid(row=1, column=col, padx=1, pady=1, sticky="nsew")
            label = ctk.CTkLabel(celda, text=header, font=ctk.CTkFont(weight="bold"), text_color="#222")
            label.pack(padx=10, pady=5)
        for i in range(len(headers)):
            self.grid_columnconfigure(i, weight=1)

        # Frame de paginación
        self.frame_paginacion = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_paginacion.grid_columnconfigure(0, weight=1)
        self.frame_paginacion.grid_columnconfigure(1, weight=0)
        self.frame_paginacion.grid_columnconfigure(2, weight=0)
        self.frame_paginacion.grid_columnconfigure(3, weight=0)
        self.frame_paginacion.grid_columnconfigure(4, weight=1)

        self.boton_anterior = ctk.CTkButton(self.frame_paginacion, text="Anterior", command=self.anterior_pagina)
        self.label_pagina = ctk.CTkLabel(self.frame_paginacion, text=f"{self.pagina_actual} de {self.cantidad_paginas}", text_color="#222")
        self.boton_siguiente = ctk.CTkButton(self.frame_paginacion, text="Siguiente", command=self.siguiente_pagina)

        self.boton_anterior.grid(row=0, column=1, padx=(0, 5))
        self.label_pagina.grid(row=0, column=2, padx=5)
        self.boton_siguiente.grid(row=0, column=3, padx=(5, 0))

        # Coloca el frame de paginación al final de la tabla
        fila_paginacion = len(self.paginas_mostrar) + 2
        self.frame_paginacion.grid(row=fila_paginacion, column=0, columnspan=4, pady=15, sticky="ew")

        self.calcular_pagina()

    def mostrar_listado(self):
        """
        Muestra la lista de PNF en la tabla, con sus botones de acción.
        """
        # Limpia las filas anteriores
        for fila in self.filas_datos:
            for widget in fila:
                widget.destroy()
        self.filas_datos.clear()
        # Empieza en la fila 2 porque la fila 1 es el encabezado
        for fila, tupla_pnf in enumerate(self.paginas_mostrar, start=2):
            fila_widgets = [
                self._crear_celda(fila, 0, tupla_pnf[0]),  # ID
                self._crear_celda(fila, 1, tupla_pnf[1]),  # Código
                self._crear_celda(fila, 2, tupla_pnf[2]),  # Nombre
            ]
            celda_btn = ctk.CTkFrame(self, fg_color="#f5f5f5", corner_radius=4)
            celda_btn.grid(row=fila, column=3, padx=1, pady=1, sticky="nsew")
            boton = ctk.CTkButton(
                celda_btn, text="Ver datos", width=100,
                text_color="#222",
                command=lambda pnf=tupla_pnf: self.ver_datos_completos(pnf)
            )
            boton.pack(padx=10, pady=5)
            fila_widgets.append(celda_btn)
            self.filas_datos.append(fila_widgets)

    def _crear_celda(self, row, col, texto):
        """
        Crea una celda de la tabla con el texto dado.
        """
        celda = ctk.CTkFrame(self, fg_color="#f5f5f5", corner_radius=4)
        celda.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
        label = ctk.CTkLabel(celda, text=texto, text_color="#222")
        label.pack(padx=10, pady=5)
        return celda

    def ver_datos_completos(self, pnf):
        """
        Abre una ventana modal para ver y editar todos los datos del PNF seleccionado.
        """
        dic_datos = self.controller.obtener_datos_completos(pnf[0])
        dic_id = self.controller.obtener_id(dic_datos)
        top = ctk.CTkToplevel(self, fg_color="White")
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

        def on_close():
            scroll_frame.unbind_all("<MouseWheel>")
            top.destroy()
        top.protocol("WM_DELETE_WINDOW", on_close)

        # Frame de datos generales del PNF
        self.frame_pnf = DatosPNFPensumFrame(scroll_frame, self.vcmd_num_val, self.vcmd_fecha_val)
        self.frame_pnf.set_datos(dic_datos)
        self.frame_pnf.pack(fill="x", padx=20, pady=10)

        # Botón para agregar trayectos (deshabilitado hasta editar)
        self.button_trayecto = ctk.CTkButton(
            scroll_frame,
            text="Agregar Mas Trayectos",
            width=140,
            font=FUENTE_BOTON,
            fg_color=COLOR_BOTON_PRIMARIO_FG,
            hover_color=COLOR_BOTON_PRIMARIO_HOVER,
            text_color=COLOR_BOTON_PRIMARIO_TEXT,
            command=lambda: self.agregar_trayecto(scroll_frame),
            state="disabled"
        )
        self.button_trayecto.pack(pady=(20, 0))

        self.list_trayecto = []

        # Carga los trayectos existentes
        if dic_datos["lista_trayectos"]:
            i = 1
            for datos_trayecto in dic_datos["lista_trayectos"]:
                frame = FrameTrayecto(scroll_frame, self.controller, self.vcmd_num_val, self.vcmd_fecha_val, f"Trayecto #{i}")
                frame.set_datos(datos_trayecto)
                self.list_trayecto.append(frame)
                i += 1
            for frame in self.list_trayecto:
                frame.pack(fill="x", padx=20, pady=10)

        # Frame de botones de acción
        self.botones_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        self.botones_frame.pack(pady=10)

        self.btn_actualizar = ctk.CTkButton(
            self.botones_frame, text="Actualizar Datos", state="disabled", command=lambda: self.actualizar_pnf(self.frame_pnf, dic_id, top)
        )
        self.btn_actualizar.pack(side="left", padx=10)

        ctk.CTkButton(self.botones_frame, text="Editar Campos", command=lambda: self.habilitar_todos(self.frame_pnf, self.list_trayecto)).pack(side="left", padx=10)
        ctk.CTkButton(self.botones_frame, text="Cerrar", command=top.destroy).pack(side="left", padx=10)

    def siguiente_pagina(self):
        """
        Avanza a la siguiente página de la tabla.
        """
        nuevo_inicio = self.pagina_actual * self.cantidad_mostrar
        nuevo_fin = nuevo_inicio + self.cantidad_mostrar
        if self.pagina_actual < self.cantidad_paginas:
            self.pagina_actual += 1
            self.paginas_mostrar = self.lista_pnf[nuevo_inicio:nuevo_fin]
            self.label_pagina.configure(text=f"{self.pagina_actual} de {self.cantidad_paginas}")
            self.calcular_pagina()

    def anterior_pagina(self):
        """
        Retrocede a la página anterior de la tabla.
        """
        if self.pagina_actual > 1:
            self.pagina_actual -= 1
            nuevo_inicio = (self.pagina_actual - 1) * self.cantidad_mostrar
            nuevo_fin = nuevo_inicio + self.cantidad_mostrar
            self.paginas_mostrar = self.lista_pnf[nuevo_inicio:nuevo_fin]
            self.label_pagina.configure(text=f"{self.pagina_actual} de {self.cantidad_paginas}")
            self.calcular_pagina()

    def calcular_pagina(self):
        """
        Habilita/deshabilita los botones de paginación según la página actual y muestra el listado.
        """
        estado_btn_siguiente = "normal"
        estado_btn_anterio = "normal"
        if self.pagina_actual == 1:
            estado_btn_anterio = "disabled"
        self.boton_anterior.configure(state=estado_btn_anterio)
        if self.pagina_actual == self.cantidad_paginas:
            estado_btn_siguiente = "disabled"
        self.boton_siguiente.configure(state=estado_btn_siguiente)
        self.mostrar_listado()

    def habilitar_todos(self, frame_pnf, lista_trayecto):
        """
        Habilita todos los campos de edición en el modal y activa los botones de acción.
        """
        frame_pnf.habilitar_campos()
        self.button_trayecto.configure(state="normal")
        for frame_trayecto in lista_trayecto:
            frame_trayecto.habilitar_campos()
        self.btn_actualizar.configure(state="normal")

    def obtener_todos_los_datos_trayectos(self):
        """
        Obtiene los datos de todos los trayectos (existentes y nuevos) para actualizar o guardar.
        """
        lista_datos_trayecto = []
        for frame_trayecto in self.list_trayecto:
            datos_trayecto = frame_trayecto.obtener_datos_trayectos()
            if datos_trayecto:
                lista_datos_trayecto.append(datos_trayecto)
        if self.nuevos_trayectos:
            n_lista_datos_trayecto = []
            for frame_trayecto in self.nuevos_trayectos:
                datos_trayecto = frame_trayecto.obtener_datos_trayectos()
                if datos_trayecto:
                    n_lista_datos_trayecto.append(datos_trayecto)
            return (lista_datos_trayecto, n_lista_datos_trayecto)
        else:
            return (lista_datos_trayecto, [])

    def actualizar_pnf(self, frame_pnf, dic_id, top):
        """
        Actualiza los datos del PNF y sus trayectos/tramos en la base de datos.
        """
        lista_datos_trayecto, n_lista_datos_trayecto = self.obtener_todos_los_datos_trayectos()
        dic_pnf = self.controller.getPNF(frame_pnf, lista_datos_trayecto)
        print("Datos PNF a actualizar:")
        pprint(dic_pnf)
        print("\n\n\n\nDatos Trayectos a actualizar:")
        pprint(lista_datos_trayecto)
        exito = self.controller.update_pnf(dic_pnf, dic_id, top, n_lista_datos_trayecto)
        if exito:
            top.destroy()
            self.lista_pnf = self.controller.listado_pnf

    def agregar_trayecto(self, frame_scroll):
        """
        Agrega un nuevo trayecto al modal de edición.
        """
        cantidad_existente = len(self.list_trayecto)
        nueva_cantidad = self.frame_pnf.get_trayecto()
        for i in range(cantidad_existente, nueva_cantidad):
            if i < 6:
                frame_trayecto = FrameTrayecto(frame_scroll, self.controller, self.vcmd_num_val, None, f"Trayecto #{i + (cantidad_existente)}")
                frame_trayecto.pack(fill="x", padx=20, pady=10)
                self.nuevos_trayectos.append(frame_trayecto)
        # Reposiciona los botones al final
        self.botones_frame.pack_forget()
        self.botones_frame.pack(pady=10)