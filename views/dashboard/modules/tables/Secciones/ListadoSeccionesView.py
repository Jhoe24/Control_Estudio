# archivo : views/dashboard/modules/tables/Sedes/ListSedesView.py
import customtkinter as ctk
import tkinter as tk
import threading
import tkinter.messagebox as messagebox
from tkcalendar import Calendar
from views.dashboard.components.widget_utils import *
from views.dashboard.modules.forms.Sedes.formSedes import FormSedes
from views.dashboard.modules.forms.PNF.FrameSecciones import FremeSecciones
from views.dashboard.modules.forms.PNF.FrameFiltradoSecciones import FiltradoSecciones

class ListSeccionesView(ctk.CTkFrame):
    def __init__(self, master, controlador_pnf, controlador_secciones, controlador_docentes, controller_sede, controller_PA):
        super().__init__(master, fg_color="white")
        self.master = master
        self.controlador_pnf = controlador_pnf
        self.controlador_secciones = controlador_secciones
        self.controlador_docentes = controlador_docentes
        self.controlador_sede = controller_sede
        self.controlador_PA = controller_PA
        self.filas_datos = []
       
        self.secciones = []
        self.cantidad_secciones = len(self.secciones)
        self.secciones_por_pagina = 13  # Número de sedes por página
        self.pagina_actual = 1          # Página actual
        self.total_paginas = 1          # Total de páginas

        self.filtrado = FiltradoSecciones(self, self.controlador_pnf, self.controlador_secciones)
        self.filtrado.grid(row=0, column=0, columnspan=6, padx=15, pady=(10, 0), sticky="ew")
    
        # --- ENCABEZADOS ---
        headers = ["Código", "PNF", "Trayecto", "Docente Titular", "Estado", "Acción"]
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

        if len(self.secciones) <= self.secciones_por_pagina:
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
        fila_paginacion = len(self.secciones) + 2 if len(self.secciones) <= self.secciones_por_pagina else self.secciones_por_pagina + 2
        self.frame_paginacion.grid(row=fila_paginacion, column=0, columnspan=6, pady=15, sticky="ew")

        if len(self.secciones) <= self.secciones_por_pagina:
            self.frame_paginacion.grid_remove()
        else:
            self.frame_paginacion.grid()

        # Mostrar registros existentes
        self.mostrar_secciones()

    def mostrar_secciones(self):
        """
        Muestra las sedes de la página actual.
        """
        # Limpiar registros anteriores
        for fila in self.filas_datos:
            for widget in fila:
                widget.destroy()
        self.filas_datos.clear()

        # Calcular paginación
        self.total_paginas = (len(self.secciones) + self.secciones_por_pagina - 1) // self.secciones_por_pagina if len(self.secciones) > 0 else 0
        if self.pagina_actual > self.total_paginas:
            self.pagina_actual = self.total_paginas if self.total_paginas > 0 else 1

        inicio = (self.pagina_actual - 1) * self.secciones_por_pagina
        fin = inicio + self.secciones_por_pagina
        secciones_mostrar = self.secciones[inicio:fin]

        for idx, seccion in enumerate(secciones_mostrar, start=2):
            sede = self.cambiar_id_por_nombre(seccion)
            fila_widgets = [
                self._crear_celda(idx, 0, sede["codigo_seccion"]),
                self._crear_celda(idx, 1, sede["pnf_id"]),
                self._crear_celda(idx, 2, sede["trayecto_id"]),
                self._crear_celda(idx, 3, sede["docente_titular_id"]),
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
        fila_paginacion = len(secciones_mostrar) + 2
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
            self.mostrar_secciones()

    def siguiente_pagina(self):
        if self.pagina_actual < self.total_paginas:
            self.pagina_actual += 1
            self.mostrar_secciones()

    def calcular_pagina(self):
        """
        Calcula la paginación para las sedes.
        """
        total_registros = len(self.secciones)
        self.total_paginas = (total_registros + self.secciones_por_pagina - 1) // self.secciones_por_pagina if total_registros > 0 else 0

        # Ajustar página actual
        if self.total_paginas == 0:
            self.pagina_actual = 0
        elif self.pagina_actual > self.total_paginas:
            self.pagina_actual = self.total_paginas
        elif self.pagina_actual < 1:
            self.pagina_actual = 1

        inicio = (self.pagina_actual - 1) * self.secciones_por_pagina if self.pagina_actual > 0 else 0
        fin = inicio + self.secciones_por_pagina
        self.secciones_mostrar = self.secciones[inicio:fin] if self.total_paginas > 0 else []

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

        self.mostrar_secciones()

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

    
    def ver_datos_completos_sede(self, sede):
        """
        Muestra los datos completos de una sede en un modal.
        """
        ventana = ctk.CTkToplevel(self)
        ventana.title(f"Detalles de la Sección: {sede.get('nombre', '')}")
        ancho = 700
        alto = 650

        # Centramos la ventana
        ventana.update_idletasks()
        screen_width = ventana.winfo_screenwidth()
        screen_height = ventana.winfo_screenheight()
        x = (screen_width // 2) - (ancho // 2)
        y = (screen_height // 2) - (alto // 2)
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

        ventana.lift()
        ventana.focus_force()
        ventana.grab_set()

        contenedor_scroll = ctk.CTkFrame(ventana, fg_color=COLOR_FONDO_FORMULARIO)
        contenedor_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        form = FremeSecciones(contenedor_scroll,
            self.controlador_docentes,
            self.controlador_pnf,
            self.controlador_secciones,
            self.controlador_sede,
            self.controlador_PA,
            fgcolor=COLOR_HEADER_SECCION_BG_2
        )

        form.cargar_datos(sede)
        form.pack(fill="both", expand=True, padx=10, pady=10)

        botones_frame = ctk.CTkFrame(contenedor_scroll, fg_color="transparent")
        botones_frame.pack(pady=10)

        btn_actualizar = ctk.CTkButton(
            botones_frame,
            text="Actualizar Datos",
            state="disabled",
            command=lambda: actualizar_seccion()
        )
        btn_actualizar.pack(side="left", padx=10)

        def habilitar_edicion():
            form.habilitar_campos()
            btn_actualizar.configure(state="normal")

        ctk.CTkButton(botones_frame, text="Editar Campos", command=habilitar_edicion).pack(side="left", padx=10)
        ctk.CTkButton(botones_frame, text="Cerrar", command=ventana.destroy).pack(side="left", padx=10)

        def actualizar_seccion():
            datos_actualizados = self.controlador_secciones.obtener_datos_vista(form)
            seccion_id = sede.get("id") or sede.get("seccion_id")
            if not seccion_id:
                print("Error: No se pudo identificar el ID de la sede para actualizar.")
                messagebox.showerror("Error", "No se pudo identificar el ID de la sede para actualizar.", parent=ventana)
                return
            exito = self.controlador_secciones.actualizar_seccion(seccion_id, datos_actualizados, ventana)
            if exito:
                self.actualizar_listado()
                ventana.destroy()
                
    def actualizar_listado(self):
        #self.secciones = self.controlador_secciones.listar_secciones()
        # sin un atributo o método que proporcione el pnf
        id_pnf = None
        try:
            nombre_pnf = self.filtrado.var1.get()
            id_pnf = self.controlador_secciones.obtener_id_por_nombre(nombre_pnf) 
        except Exception as e:
            print(f"No se pudo obtener id_pnf para listar secciones: {e}")

        if id_pnf:
            self.secciones = self.controlador_secciones.listar_secciones(id_pnf)
        else:
            self.secciones = []  

        self.calcular_pagina()
        self.mostrar_secciones()
        self.frame_paginacion.grid()
        self.frame_paginacion.grid_remove()
        self.frame_paginacion.grid()

    # def cambiar_id_por_nombre(self,secciones):
    #     listado = self.controlador_docentes.obtener_solo_nombres_docentes_por_pnf(secciones["pnf_id"])
        
    #     for id, nombre_apellido in listado:
    #         if id == secciones["docente_titular_id"]:
    #             secciones["docente_titular_id"] = nombre_apellido
    #             break
    #     return secciones

    def obtener_nombre_docente_titular(self, docente_id, pnf_id):
        """
        Retorna el nombre completo del docente titular dado su id y pnf_id.
        """
        if docente_id is None:
            return "No hay docente asignado"

        try:
            listado = self.controlador_docentes.obtener_solo_nombres_docentes_por_pnf(pnf_id)
            for id_docente, nombre_apellido in listado:
                if id_docente == docente_id:
                    return nombre_apellido
            return "Docente no encontrado"
        except Exception as e:
            print(f"Error al obtener el nombre del docente titular: {e}")
            return "Error obteniendo docente"

    def cambiar_id_por_nombre(self, seccion):
        # Docente Titular
        listado_docentes = self.controlador_docentes.obtener_solo_nombres_docentes_por_pnf(seccion["pnf_id"])
        for id_docente, nombre_apellido in listado_docentes:
            if id_docente == seccion["docente_titular_id"]:
                seccion["docente_titular_id"] = nombre_apellido
                break
        else:
            seccion["docente_titular_id"] = "Docente no asignado" # O un valor por defecto adecuado

        # Convertir PNF_ID a nombre
        pnf_nombre_tuple = self.controlador_pnf.obtener_nombres_por_id("pnf", seccion["pnf_id"])
        if pnf_nombre_tuple:
            seccion["pnf_id"] = pnf_nombre_tuple[0]
        else:
            seccion["pnf_id"] = "PNF Desconocido"

        # Convertir TRAYECTO_ID a nombre
        trayecto_nombre_tuple = self.controlador_pnf.obtener_nombres_por_id("trayectos", seccion["trayecto_id"])
        if trayecto_nombre_tuple:
            seccion["trayecto_id"] = trayecto_nombre_tuple[0]
        else:
            seccion["trayecto_id"] = "Trayecto Desconocido"

        # Convertir TRAMO_ID a nombre 
        if "tramo_id" in seccion and seccion["tramo_id"] is not None:
            tramo_nombre_tuple = self.controlador_pnf.obtener_nombres_por_id("tramos", seccion["tramo_id"])
            if tramo_nombre_tuple:
                seccion["tramo_id"] = tramo_nombre_tuple[0]
            else:
                seccion["tramo_id"] = "Tramo Desconocido"
        else:
            seccion["tramo_id"] = "No asignado" # O un valor por defecto adecuado

        # Convertir SEDE_ID a nombre
        if "sede" in seccion and seccion["sede"] is not None:
            sede_nombre_tuple = self.controlador_sede.obtener_nombres_por_id("sedes", seccion["sede"])
            if sede_nombre_tuple:
                seccion["sede"] = sede_nombre_tuple[0]
            else:
                seccion["sede"] = "Sede Desconocida"
        else:
            seccion["sede"] = "No asignada" # O un valor por defecto adecuado

        # Convertir PERIODO_ACADEMICO_ID a nombre
        if "periodo_academico" in seccion and seccion["periodo_academico"] is not None:
            periodo_academico_nombre_tuple = self.controlador_PA.obtener_nombres_por_id("periodos_academicos", seccion["periodo_academico"])
            if periodo_academico_nombre_tuple:
                seccion["periodo_academico"] = periodo_academico_nombre_tuple[0]
            else:
                seccion["periodo_academico"] = "Periodo Desconocido"
        else:
            seccion["periodo_academico"] = "No asignado" # O un valor por defecto adecuado

        return seccion