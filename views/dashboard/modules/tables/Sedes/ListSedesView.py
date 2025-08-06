# archivo : views/dashboard/modules/tables/Sedes/ListSedesView.py
import customtkinter as ctk
import tkinter as tk
import threading
import tkinter.messagebox as messagebox
from tkcalendar import Calendar
from views.dashboard.components.widget_utils import *
from views.dashboard.components.caendario import CTKFecha
from views.dashboard.modules.forms.Sedes.formSedes import FormSedes

class ListSedesView(ctk.CTkFrame):
    def __init__(self, master, controlador):
        super().__init__(master, fg_color="white")
        self.master = master
        self.controlador = controlador
        self.filas_datos = []
        # self.sedes = [{
        #     "codigo": "S001",
        #     "nombre": "Sede Central",
        #     "tipo": "Universidad",
        #     "direccion": "Calle Principal, Ciudad",
        #     "estado": "Planificación",
        # }, {
        #     "codigo": "S002",
        #     "nombre": "Sede Norte",
        #     "tipo": "Instituto",
        #     "direccion": "Avenida Norte, Ciudad",
        #     "estado": "Planificación",
        # }, {
        #     "codigo": "S003",
        #     "nombre": "Sede Sur",
        #     "tipo": "Escuela",
        #     "direccion": "Calle Sur, Ciudad",
        #     "estado": "Planificación",
        # }]

        self.sedes = self.controlador.listar_sedes()
        self.cantidad_sedes = len(self.sedes)
        self.sedes_por_pagina = 13  # Número de sedes por página
        self.pagina_actual = 1      # Página actual
        self.total_paginas = 1      # Total de páginas
        self.lista_sedes = self.sedes  # Lista de sedes para paginación

        # Botón "Agregar Sede"
        self.boton_agregar = ctk.CTkButton(
            self,
            text="Agregar Sede",
            font=FUENTE_BOTON,
            fg_color=COLOR_BOTON_PRIMARIO_FG,
            hover_color=COLOR_BOTON_PRIMARIO_HOVER,
            text_color=COLOR_BOTON_PRIMARIO_TEXT,
            command=self.abrir_modal_formulario
        )
        self.boton_agregar.grid(row=0, column=0, padx=15, pady=15, sticky="w")

        # --- ENCABEZADOS ---
        headers = ["Código", "Nombre", "Tipo", "Dirección", "Estado", "Acción"]
        for col, header in enumerate(headers):
            celda = ctk.CTkFrame(self, fg_color="#e0e0e0", corner_radius=4)
            celda.grid(row=1, column=col, padx=1, pady=1, sticky="nsew")
            label = ctk.CTkLabel(celda, text=header, font=ctk.CTkFont(weight="bold"), text_color=COLOR_TEXTO_PRINCIPAL)
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

        if len(self.sedes) <= self.sedes_por_pagina:
            self.frame_paginacion.grid_remove()
        else:
            self.frame_paginacion.grid()

        # Botones de paginación
        self.boton_anterior = ctk.CTkButton(self.frame_paginacion, text="Anterior", command=self.anterior_pagina)
        self.label_pagina = ctk.CTkLabel(self.frame_paginacion, text=f"{self.pagina_actual} de {self.total_paginas}", text_color="#222")
        self.boton_siguiente = ctk.CTkButton(self.frame_paginacion, text="Siguiente", command=self.siguiente_pagina)
        self.boton_anterior.grid(row=0, column=1, padx=(0, 5))
        self.label_pagina.grid(row=0, column=2, padx=5)
        self.boton_siguiente.grid(row=0, column=3, padx=(5, 0))

        # Coloca el frame de paginación al final de la tabla
        fila_paginacion = len(self.sedes) + 2 if len(self.sedes) <= self.sedes_por_pagina else self.sedes_por_pagina + 2
        self.frame_paginacion.grid(row=fila_paginacion, column=0, columnspan=6, pady=15, sticky="ew")

        if len(self.sedes) <= self.sedes_por_pagina:
            self.frame_paginacion.grid_remove()
        else:
            self.frame_paginacion.grid()

        # Mostrar registros existentes
        self.mostrar_sedes()

    def mostrar_sedes(self):
        """
        Muestra las sedes de la página actual.
        """
        # Limpiar registros anteriores
        for fila in self.filas_datos:
            for widget in fila:
                widget.destroy()
        self.filas_datos.clear()

        # Calcular paginación
        self.total_paginas = (len(self.sedes) + self.sedes_por_pagina - 1) // self.sedes_por_pagina if len(self.sedes) > 0 else 0
        if self.pagina_actual > self.total_paginas:
            self.pagina_actual = self.total_paginas if self.total_paginas > 0 else 1

        inicio = (self.pagina_actual - 1) * self.sedes_por_pagina
        fin = inicio + self.sedes_por_pagina
        sedes_mostrar = self.sedes[inicio:fin]

        for idx, sede in enumerate(sedes_mostrar, start=2):
            fila_widgets = [
                self._crear_celda(idx, 0, sede["codigo"]),
                self._crear_celda(idx, 1, sede["nombre"]),
                self._crear_celda(idx, 2, sede["tipo"]),
                self._crear_celda(idx, 3, sede["direccion"]),
                self._crear_celda(idx, 4, sede["estado"]),
            ]
            celda_btn = ctk.CTkFrame(self, fg_color="#f5f5f5", corner_radius=4)
            celda_btn.grid(row=idx, column=5, padx=1, pady=1, sticky="nsew")
            btn_ver = ctk.CTkButton(
                celda_btn,
                text="Ver datos",
                width=100,
                height=30,
                text_color=COLOR_ENTRY_BG,
                command=lambda p=sede: self.ver_datos_completos_sede(p)
            )
            btn_ver.pack(padx=10, pady=5)
            fila_widgets.append(celda_btn)
            self.filas_datos.append(fila_widgets)

        # Actualizar el frame de paginación al final de la tabla
        fila_paginacion = len(sedes_mostrar) + 2
        self.frame_paginacion.grid(row=fila_paginacion, column=0, columnspan=6, pady=15, sticky="ew")

        # Actualizar label de página
        self.label_pagina.configure(text=f"{self.pagina_actual} de {self.total_paginas}")

        # Habilitar/deshabilitar botones
        self.boton_anterior.configure(state="disabled" if self.pagina_actual <= 1 else "normal")
        self.boton_siguiente.configure(state="disabled" if self.pagina_actual >= self.total_paginas else "normal")

    def _crear_celda(self, row, col, texto):
        celda = ctk.CTkFrame(self, fg_color="#f5f5f5", corner_radius=4)
        celda.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
        label = ctk.CTkLabel(celda, text=texto, text_color=COLOR_TEXTO_PRINCIPAL)
        label.pack(padx=10, pady=5)
        return celda

    def anterior_pagina(self):
        if self.pagina_actual > 1:
            self.pagina_actual -= 1
            self.mostrar_sedes()

    def siguiente_pagina(self):
        if self.pagina_actual < self.total_paginas:
            self.pagina_actual += 1
            self.mostrar_sedes()

    def calcular_pagina(self, lista_sedes=None):
        """
        Calcula la paginación para las sedes.
        """
        if lista_sedes is not None:
            self.lista_sedes = lista_sedes
        total_registros = len(self.lista_sedes)
        self.total_paginas = (total_registros + self.sedes_por_pagina - 1) // self.sedes_por_pagina if total_registros > 0 else 0

        # Ajustar página actual
        if self.total_paginas == 0:
            self.pagina_actual = 0
        elif self.pagina_actual > self.total_paginas:
            self.pagina_actual = self.total_paginas
        elif self.pagina_actual < 1:
            self.pagina_actual = 1

        inicio = (self.pagina_actual - 1) * self.sedes_por_pagina if self.pagina_actual > 0 else 0
        fin = inicio + self.sedes_por_pagina
        self.sedes_mostrar = self.lista_sedes[inicio:fin] if self.total_paginas > 0 else []

        # Actualizar label de paginación
        self.label_pagina.configure(text=f"{self.pagina_actual} de {self.total_paginas}")

        # Mostrar/ocultar frame de paginación
        if self.total_paginas <= 1:
            self.frame_paginacion.grid_remove()
        else:
            self.frame_paginacion.grid()

        # Actualizar estados de botones
        self.boton_anterior.configure(state="disabled" if self.pagina_actual <= 1 else "normal")
        self.boton_siguiente.configure(state="disabled" if self.pagina_actual >= self.total_paginas else "normal")

        self.mostrar_sedes()

    def abrir_modal_formulario(self):
        """
        Abre el formulario de registro de sedes en un modal con scroll.
        """
        top = ctk.CTkToplevel(self, fg_color="white")
        top.title("Agregar Sede")
        ancho, alto = 700, 600

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

        # Crear frame con scroll dentro del modal
        scrollable_frame = ctk.CTkFrame(top, width=ancho-40, height=alto-120, fg_color="white")
        scrollable_frame.pack(padx=20, pady=20, fill="both", expand=True)

        form = FormSedes(scrollable_frame, self.controlador)
        form.pack(fill="both", expand=True)
        
        frame_btn = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        frame_btn.pack(pady=10)
        # # Botón guardar
        # btn_guardar = ctk.CTkButton(
        #     frame_btn, text="Guardar",
        #     fg_color=COLOR_BOTON_PRIMARIO_FG,
        #     font=FUENTE_BOTON,
        #     hover_color=COLOR_BOTON_PRIMARIO_HOVER,
        #     text_color=COLOR_BOTON_PRIMARIO_TEXT,
        #     command=lambda: self.guardar_sede(form, top)
        # )
        # btn_guardar.pack(side="left", pady=10)

        # btn_cerrar = ctk.CTkButton(
        #     frame_btn, text="Cerrar",
        #     fg_color=COLOR_BOTON_SECUNDARIO_FG,
        #     font=FUENTE_BOTON,
        #     hover_color=COLOR_BOTON_SECUNDARIO_HOVER,
        #     text_color=COLOR_BOTON_SECUNDARIO_TEXT,
        #     command=top.destroy
        # )
        # btn_cerrar.pack(side="left",pady=10)
         # Empacar los frames
        self.button_frame = ctk.CTkFrame(frame_btn, fg_color="transparent")
        self.button_frame.pack(pady=(25, 20))

        self.btn_guardar = ctk.CTkButton(self.button_frame, text="Guardar", width=140, command=lambda: self.guardar_sede(form, top),
                                        font=FUENTE_BOTON, fg_color=COLOR_BOTON_PRIMARIO_FG, hover_color=COLOR_BOTON_PRIMARIO_HOVER, text_color=COLOR_BOTON_PRIMARIO_TEXT
                                        )
        self.btn_guardar.pack(side="left", padx=10)

        self.btn_cancelar = ctk.CTkButton(self.button_frame, text="Cerrar", width=140, command=top.destroy,
                                        font=FUENTE_BOTON, fg_color=COLOR_BOTON_SECUNDARIO_FG, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, text_color=COLOR_BOTON_SECUNDARIO_TEXT
                                        )
        self.btn_cancelar.pack(side="left", padx=10)

    def guardar_sede(self, form, ventana):
        """
        Guarda una nueva sede.
        """
        datos = self.controlador.obtener_datos_vista(form)
        exito = self.controlador.registrar_sede(datos, ventana)
        if exito:
            ventana.destroy()
            self.sedes = self.controlador.obtener_sedes()
            self.mostrar_sedes()

    def ver_datos_completos_sede(self, sede):
        """
        Muestra los datos completos de una sede en un modal.
        """
        ventana = ctk.CTkToplevel(self)
        ventana.title(f"Detalles de la Sede: {sede.get('nombre', '')}")
        ventana.geometry("850x750")
        ventana.grab_set()

        contenedor_scroll = ctk.CTkScrollableFrame(ventana, fg_color=COLOR_FONDO_FORMULARIO)
        contenedor_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        form = FormSedes(contenedor_scroll, self.controlador)
        form.cargar_datos(sede)
        form.pack(fill="both", expand=True, padx=10, pady=10)

        botones_frame = ctk.CTkFrame(contenedor_scroll, fg_color="transparent")
        botones_frame.pack(pady=10)

        btn_actualizar = ctk.CTkButton(
            botones_frame,
            text="Actualizar Datos",
            state="disabled",
            command=lambda: actualizar_sede()
        )
        btn_actualizar.pack(side="left", padx=10)

        def habilitar_edicion():
            form.habilitar_campos()
            btn_actualizar.configure(state="normal")

        ctk.CTkButton(botones_frame, text="Editar Campos", command=habilitar_edicion).pack(side="left", padx=10)
        ctk.CTkButton(botones_frame, text="Cerrar", command=ventana.destroy).pack(side="left", padx=10)

        def actualizar_sede():
            datos_actualizados = self.controlador.obtener_datos_vista(form)
            sede_id = sede.get("id") or sede.get("sede_id")
            if not sede_id:
                print("Error: No se pudo identificar el ID de la sede para actualizar.")
                messagebox.showerror("Error", "No se pudo identificar el ID de la sede para actualizar.", parent=ventana)
                return
            exito = self.controlador.actualizar_sede(sede_id, datos_actualizados, ventana)
            if exito:
                self.actualizar_listado()
                ventana.destroy()
                
    
    def actualizar_listado(self):
        self.sedes = self.controlador.listar_sedes()
        self.lista_sedes = self.sedes
        self.calcular_pagina(self.sedes)
        self.mostrar_sedes()
        self.frame_paginacion.grid()
        self.frame_paginacion.grid_remove()
        self.frame_paginacion.grid()
        