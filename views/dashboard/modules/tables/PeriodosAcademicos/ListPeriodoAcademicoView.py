import customtkinter as ctk
import tkinter as tk
import threading
import tkinter.messagebox as messagebox
from tkcalendar import Calendar
from views.dashboard.components.widget_utils import *
from views.dashboard.modules.forms.Periodos_academico.formPeriodoAcademico import FormPeriodoAcademico

class ListPeriodoAcademicoView(ctk.CTkFrame):
    def __init__(self, master, controlador):
        super().__init__(master, fg_color="white")
        self.master = master
        self.controlador = controlador
        self.filas_datos = []

        
        # Datos
        self.periodos = self.controlador.obtener_periodos_academicos()
        self.cantidad_periodos = len(self.periodos)

        # Paginación
        self.pagina_actual = 1
        self.periodos_por_pagina = 13
        self.total_paginas = (len(self.periodos) + self.periodos_por_pagina - 1) // self.periodos_por_pagina

        self.paginas_mostrar = self.periodos[:self.periodos_por_pagina]
        self.posicion_actual = len(self.paginas_mostrar)


        # Botón "Agregar Período Académico"
        self.boton_agregar = ctk.CTkButton(
            self,
            text="Agregar Periodo Académico",
            font=FUENTE_BOTON,
            fg_color=COLOR_BOTON_PRIMARIO_FG,
            hover_color=COLOR_BOTON_PRIMARIO_HOVER,
            text_color=COLOR_BOTON_PRIMARIO_TEXT,
            command=self.abrir_modal_formulario
        )
        self.boton_agregar.grid(row=0, column=0, padx=15, pady=15, sticky="w")


        # --- ENCABEZADOS ---
        headers = ["Código", "Nombre", "Estado", "Acción"]
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
        if len(self.periodos) <= self.periodos_por_pagina:
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
        fila_paginacion = len(self.paginas_mostrar) + 2
        self.frame_paginacion.grid(row=fila_paginacion, column=0, columnspan=5, pady=15, sticky="ew")

        if len(self.periodos) <= self.periodos_por_pagina:
            self.frame_paginacion.grid_remove()
        else:
            self.frame_paginacion.grid()


        # Mostrar registros existentes
        self.mostrar_periodos()

    def mostrar_periodos(self):
        """
        Muestra los períodos académicos de la página actual.
        """
        dic_estado_invertido = {
            "planificacion": "Planificación",
            "inscripcion": "Inscripción",
            "en_curso": "En Curso",
            "evaluaciones": "Evaluaciones",
            "finalizado": "Finalizado",
            "cerrado": "Cerrado"
        }
        # Limpiar registros anteriores
        for fila in self.filas_datos:
            for widget in fila:
                widget.destroy()
        self.filas_datos.clear()

        inicio = (self.pagina_actual - 1) * self.periodos_por_pagina
        fin = inicio + self.periodos_por_pagina
        periodos_mostrar = self.periodos[inicio:fin]

        for idx, periodo in enumerate(periodos_mostrar, start=2):
            fila_widgets = [
                self._crear_celda(idx, 0, periodo["codigo"]),
                self._crear_celda(idx, 1, periodo["nombre"]),
                self._crear_celda(idx, 2, dic_estado_invertido.get(periodo["estado"],"No Seleccionado")),
            ]

            celda_btn = ctk.CTkFrame(self, fg_color="#f5f5f5", corner_radius=4)
            celda_btn.grid(row=idx, column=3, padx=1, pady=1, sticky="nsew")

            btn_ver = ctk.CTkButton(
                celda_btn,
                text="Ver datos",
                width=100,
                height=30,
                text_color=COLOR_ENTRY_BG,
                command=lambda p=periodo: self.ver_datos_completos_periodo(id_periodo=p["id"])
            )
            btn_ver.pack(padx=10, pady=5)

            fila_widgets.append(celda_btn)
            self.filas_datos.append(fila_widgets)

        # Actualizar el frame de paginación al final de la tabla
        fila_paginacion = len(periodos_mostrar) + 2
        self.frame_paginacion.grid(row=fila_paginacion, column=0, columnspan=5, pady=15, sticky="ew")

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
            self.mostrar_periodos()

    def siguiente_pagina(self):
        if self.pagina_actual < self.total_paginas:
            self.pagina_actual += 1
            self.mostrar_periodos()

    
    def calcular_pagina(self, lista_uc=None):
        """
        Habilita/deshabilita los botones de paginación según la página actual y muestra el listado.
        """
        if lista_uc is not None:
            self.lista_UC = lista_uc

        total_registros = len(self.lista_UC)
        self.total_paginas = (total_registros + self.periodos_por_pagina - 1) // self.periodos_por_pagina if total_registros > 0 else 0

        # Ajustar página actual
        if self.total_paginas == 0:
            self.pagina_actual = 0
        elif self.pagina_actual > self.total_paginas:
            self.pagina_actual = self.total_paginas
        elif self.pagina_actual < 1:
            self.pagina_actual = 1

        inicio = (self.pagina_actual - 1) * self.periodos_por_pagina if self.pagina_actual > 0 else 0
        fin = inicio + self.periodos_por_pagina
        self.paginas_mostrar = self.lista_UC[inicio:fin] if self.total_paginas > 0 else []

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

        self.mostrar_periodos()

    def abrir_modal_formulario(self):
        """
        Abre el formulario de registro de periodos académicos en un modal con scroll.
        """
        top = ctk.CTkToplevel(self, fg_color="white")
        top.title("Agregar Período Académico")
        ancho, alto = 700, 700

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
        scrollable_frame = ctk.CTkScrollableFrame(top, width=ancho-40, height=alto-120, fg_color="white")
        scrollable_frame.pack(padx=20, pady=20, fill="both", expand=True)

        form = FormPeriodoAcademico(scrollable_frame, self.controlador)
        form.pack(fill="both", expand=True)

        # Botón guardar
        # btn_guardar = ctk.CTkButton(
        #     top, text="Guardar",
        #     fg_color=COLOR_BOTON_PRIMARIO_FG,
        #     font=FUENTE_BOTON,
        #     hover_color=COLOR_BOTON_PRIMARIO_HOVER,
        #     text_color=COLOR_BOTON_PRIMARIO_TEXT,
        #     command=lambda: self.guardar_periodo(form, top)
        # )
        # btn_guardar.pack(pady=10)

        # btn_cerrar_ventana = ctk.CTkButton(
        #     top, text="Cerrar",
        #     fg_color=COLOR_BOTON_SECUNDARIO_FG,
        #     font=FUENTE_BOTON,
        #     hover_color=COLOR_BOTON_SECUNDARIO_HOVER,
        #     text_color=COLOR_BOTON_SECUNDARIO_TEXT,
        #     command=top.destroy
        # )
        # btn_cerrar_ventana.pack(pady=10)
        # Empacar los frames
        self.button_frame = ctk.CTkFrame(top, fg_color="transparent")
        self.button_frame.pack(pady=(25, 20))

        self.btn_guardar = ctk.CTkButton(self.button_frame, text="Guardar", width=140, command=lambda: self.guardar_periodo(form, top),
                                        font=FUENTE_BOTON, fg_color=COLOR_BOTON_PRIMARIO_FG, hover_color=COLOR_BOTON_PRIMARIO_HOVER, text_color=COLOR_BOTON_PRIMARIO_TEXT
                                        )
        self.btn_guardar.pack(side="left", padx=10)

        self.btn_cancelar = ctk.CTkButton(self.button_frame, text="Cerrar", width=140, command=top.destroy,
                                        font=FUENTE_BOTON, fg_color=COLOR_BOTON_SECUNDARIO_FG, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, text_color=COLOR_BOTON_SECUNDARIO_TEXT
                                        )
        self.btn_cancelar.pack(side="left", padx=10)

    def guardar_periodo(self, form, ventana):
        datos = self.controlador.obtener_datos_vista(form)
        if self.controlador.validar_campos_obligatorios(datos,ventana):
            exito = self.controlador.registrar_periodo_academico(datos, ventana)
            if exito:
                ventana.destroy()
                self.periodos = self.controlador.obtener_periodos_academicos()
                self.mostrar_periodos()

    def ver_datos_completos_periodo(self, id_periodo):
        periodo = self.controlador.obtener_periodo_academico_datos(id_periodo)
        ventana = ctk.CTkToplevel(self)

        if not periodo:
            messagebox.showerror("Error", "No se encontraron datos para este período académico.", parent=ventana)
            return
        
        periodo = periodo[0]

        ventana.title(f"Detalles del Período Académico: {periodo.get('nombre', '')}")
        ventana.geometry("850x750")
        ventana.grab_set()

        contenedor_scroll = ctk.CTkScrollableFrame(ventana, fg_color=COLOR_FONDO_FORMULARIO)
        contenedor_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        form = FormPeriodoAcademico(contenedor_scroll, self.controlador)
        form.pack(fill="both", expand=True, padx=10, pady=10)

        try:
            # Limpiar campos
            form.codigo_entry.delete(0, "end")
            form.nombre_entry.delete(0, "end")
            form.duracion_semanas_entry.delete(0, "end")
            form.observacion_entry.delete(0, "end")

            # Insertar datos
            form.codigo_entry.insert(0, periodo.get("codigo", ""))
            form.nombre_entry.insert(0, periodo.get("nombre", ""))
            form.var_tipo.set(periodo.get("tipo", "Regular"))
            form.duracion_semanas_entry.insert(0, str(periodo.get("duracion_semanas", "")))

            estado_db = periodo.get("estado", "")
            dic_estado_invertido = {
                "planificacion": "Planificación",
                "inscripcion": "Inscripción",
                "en_curso": "En Curso",
                "evaluaciones": "Evaluaciones",
                "finalizado": "Finalizado",
                "cerrado": "Cerrado"
            }
            form.var_estado.set(dic_estado_invertido.get(estado_db, "Planificación"))

            form.observacion_entry.insert(0, periodo.get("observaciones", ""))

            # Fechas
            if periodo.get("fecha_inicio"):
                form.set_fecha_inicio(periodo["fecha_inicio"])
            if periodo.get("fecha_fin"):
                form.set_fecha_fin(periodo["fecha_fin"])
            if periodo.get("fecha_inicio_inscripcion"):
                form.set_fecha_inicio_inscripcion(periodo["fecha_inicio_inscripcion"])
            if periodo.get("fecha_fin_inscripcion"):
                form.set_fecha_fin_inscripcion(periodo["fecha_fin_inscripcion"])
            if periodo.get("fecha_inicio_clases"):
                form.set_fecha_inicio_clases(periodo["fecha_inicio_clases"])
            if periodo.get("fecha_fin_clases"):
                form.set_fecha_fin_clases(periodo["fecha_fin_clases"])
            if periodo.get("fecha_inicio_evaluaciones"):
                form.set_fecha_inicio_evaluaciones(periodo["fecha_inicio_evaluaciones"])
            if periodo.get("fecha_fin_evaluaciones"):
                form.set_fecha_fin_evaluaciones(periodo["fecha_fin_evaluaciones"])

            # AHORA bloquear campos
            form.deshabilitar_campos()

        except Exception as e:
            print(f"Error al cargar datos en el formulario de vista completa: {e}")

        botones_frame = ctk.CTkFrame(contenedor_scroll, fg_color="transparent")
        botones_frame.pack(pady=10)

        btn_actualizar = ctk.CTkButton(
            botones_frame,
            text="Actualizar Datos",
            state="disabled",
            command=lambda: actualizar_periodo()
        )
        btn_actualizar.pack(side="left", padx=10)

        def habilitar_edicion():
            form.habilitar_campos()
            btn_actualizar.configure(state="normal")

        ctk.CTkButton(botones_frame, text="Editar Campos", command=habilitar_edicion).pack(side="left", padx=10)
        ctk.CTkButton(botones_frame, text="Cerrar", command=ventana.destroy).pack(side="left", padx=10)

        def actualizar_periodo():
            datos_actualizados = self.controlador.obtener_datos_vista(form)
            periodo_id = periodo.get("id") 

            if not periodo_id:
                print("Error: No se pudo identificar el ID del período para actualizar.")
                messagebox.showerror("Error", "No se pudo identificar el ID del período para actualizar.", parent=ventana)
                return

            exito = self.controlador.actualizar_periodo_academico(periodo_id, datos_actualizados, ventana)
            if exito:
                self.periodos = self.controlador.obtener_periodos_academicos()
                self.actualizar_listado()
                self.mostrar_periodos()
                
                ventana.destroy()
                

    def actualizar_listado(self):
        #self.lista_sedes = self.periodos
        self.calcular_pagina(self.periodos)
        #self.mostrar_periodos()
        self.frame_paginacion.grid()
        self.frame_paginacion.grid_remove()
        self.frame_paginacion.grid()