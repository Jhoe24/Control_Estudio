# views/admin/list_estudiante_view.py
import customtkinter as ctk
import tkinter as tk

# Listado de estudiantes con paginación

class ListEstudiantesView(ctk.CTkScrollableFrame):
    def __init__(self, master, controlador):
        super().__init__(master, fg_color="white")
        self.master = master
        self.controlador = controlador
        self.color_texto = "#222222"
        self.filas_datos = []

        # Configuración de paginación
        self.estudiantes = self.controlador.master_controlador.estudiantes.obtener_lista_estudiantes(0)
        self.pagina_actual = 0
        self.registros_por_pagina = 10

        # Encabezados
        headers = ["Tipo Doc.", "Número Doc.", "Nombres", "Apellidos", "Código SNI", "Acción"]
        for col, header in enumerate(headers):
            celda = ctk.CTkFrame(self, fg_color="#e0e0e0", corner_radius=4)
            celda.grid(row=0, column=col, padx=1, pady=1, sticky="nsew")
            label = ctk.CTkLabel(celda, text=header, font=ctk.CTkFont(weight="bold"),
                                 text_color=self.color_texto)
            label.pack(padx=10, pady=5)
        for i in range(len(headers)):
            self.grid_columnconfigure(i, weight=1)

        # Controles de paginación
        self.boton_anterior = ctk.CTkButton(self, text="Anterior", command=self.anterior_pagina)
        self.boton_siguiente = ctk.CTkButton(self, text="Siguiente", command=self.siguiente_pagina)

        self.boton_anterior.grid(row=1000, column=0, columnspan=3, pady=15)
        self.boton_siguiente.grid(row=1000, column=3, columnspan=3, pady=15)

        # Cargar estudiantes de ejemplo
        
        self.mostrar_pagina()

    def mostrar_pagina(self):
        
        self.cargar_datos(self.estudiantes)
        # inicio = self.pagina_actual * self.registros_por_pagina
        # fin = inicio + self.registros_por_pagina
        # datos_pagina = self.estudiantes[inicio:fin]
        # self.cargar_datos(datos_pagina)
        
        # # Estado de los botones
        # primer_id = self.estudiantes[0]['id']
        #self.boton_anterior.configure(state="normal" if primer_id > 0 else "disabled")
        # total_paginas = (len(self.estudiantes) - 1) // self.registros_por_pagina
        # self.boton_siguiente.configure(state="normal" if self.pagina_actual < total_paginas else "disabled")

    def siguiente_pagina(self):
        for estudiante in self.estudiantes:
            pass
        ultimo_id = estudiante['id']
        print(ultimo_id)
        self.estudiantes = self.controlador.master_controlador.estudiantes.obtener_lista_estudiantes(ultimo_id)
        self.mostrar_pagina()

    def anterior_pagina(self):
        primer_id = self.estudiantes[0]['id']
        print(primer_id)
        self.estudiantes = self.controlador.master_controlador.estudiantes.obtener_lista_estudiantes(primer_id-4)
        self.mostrar_pagina()

    def cargar_datos(self, datos):
        # Eliminar filas anteriores
        for fila in self.filas_datos:
            for widget in fila:
                widget.destroy()
        self.filas_datos.clear()

        # Cargar nueva página
        for i, estudiante in enumerate(datos, start=1):
        #    tipo_doc, num_doc, nombres, apellidos, codigo_sni = estudiante
            fila_widgets = [
                self._crear_celda(i, 0, estudiante['tipo_documento']),
                self._crear_celda(i, 1, estudiante['documento_identidad']),
                self._crear_celda(i, 2, estudiante['nombres']),
                self._crear_celda(i, 3, estudiante['apellidos']),
                self._crear_celda(i, 4, estudiante['codigo_unico']),
            ]

            # Botón "Ver datos"
            celda_btn = ctk.CTkFrame(self, fg_color="#f5f5f5", corner_radius=4)
            celda_btn.grid(row=i, column=5, padx=1, pady=1, sticky="nsew")
            boton = ctk.CTkButton(
                celda_btn, text="Ver datos", width=100,
                text_color=self.color_texto,
                command=lambda est=estudiante: self.ver_datos_completos(est)
            )
            boton.pack(padx=10, pady=5)
            # fila_widgets.append(celda_btn)

            # self.filas_datos.append(fila_widgets)

    def _crear_celda(self, row, col, texto):
        celda = ctk.CTkFrame(self, fg_color="#f5f5f5", corner_radius=4)
        celda.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
        label = ctk.CTkLabel(celda, text=texto, text_color=self.color_texto)
        label.pack(padx=10, pady=5)
        return celda

    def ver_datos_completos(self, estudiante):
        # tipo_doc, num_doc, nombres, apellidos, codigo_sni = estudiante
        ventana = ctk.CTkToplevel(self)
        ventana.title("Datos del Estudiante")
        ventana.geometry("400x300")
        ventana.grab_set()

        ctk.CTkLabel(ventana, text="Tipo de Documento:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(20, 0))
        ctk.CTkLabel(ventana, text=estudiante['tipo_documento']).pack(anchor="w", padx=20)

        ctk.CTkLabel(ventana, text="Número de Documento:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(10, 0))
        ctk.CTkLabel(ventana, text=estudiante['documento_identidad']).pack(anchor="w", padx=20)

        ctk.CTkLabel(ventana, text="Nombres:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(10, 0))
        ctk.CTkLabel(ventana, text=estudiante['nombres']).pack(anchor="w", padx=20)

        ctk.CTkLabel(ventana, text="Apellidos:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(10, 0))
        ctk.CTkLabel(ventana, text=estudiante['apellidos']).pack(anchor="w", padx=20)

        ctk.CTkLabel(ventana, text="Código SNI:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(10, 0))
        ctk.CTkLabel(ventana, text=estudiante['codigo_unico']).pack(anchor="w", padx=20)

        ctk.CTkButton(ventana, text="Cerrar", command=ventana.destroy).pack(pady=20)
    