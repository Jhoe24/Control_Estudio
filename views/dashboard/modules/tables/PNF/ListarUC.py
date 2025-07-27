import customtkinter as ctk
import tkinter as tk
from views.dashboard.components.widget_utils import *
from views.dashboard.modules.forms.UnidadCurricular import UnidadCurricular
from views.dashboard.modules.FiltradoPNFFrame import FiltradoPNFFrame


class ListarUC(ctk.CTkFrame):

    def __init__(self, master, controller,tupla_datos = None):
        super().__init__(master, fg_color="white")
        self.controller = controller
        tupla_id = ()
        self.tuplas_nombre = ()
        if tupla_datos:
            for i in range(len(tupla_datos)):
                if i == 0 or i == 1 or i == 2:
                    tupla_id = tupla_id + (tupla_datos[i],)
                if i == 0 or i == 3 or i == 4:
                    self.tuplas_nombre = self.tuplas_nombre + (tupla_datos[i],)

            print(f"Tuplas con ids = {tupla_id}, Tupas nombres = {self.tuplas_nombre}")
            
            self.lista_UC = self.controller.obtener_UC(tupla_id)
        else:
            self.lista_UC = self.controller.obtener_UC()

        self.pagina_actual = 1
        self.uc_por_pagina = 13
        self.total_paginas = (len(self.lista_UC) + self.uc_por_pagina - 1) // self.uc_por_pagina

        self.paginas_mostrar = self.lista_UC[:self.uc_por_pagina]
        self.posicion_actual = len(self.paginas_mostrar)
        self.button_uc = None
        self.frame_uc = None

        if not tupla_datos:
            self.busqueda_frame = FiltradoPNFFrame(self, self.controller)
            self.busqueda_frame.grid(row=0, column=0, columnspan=5, padx=15, pady=(10, 0), sticky="ew")

        self.fila_datos = []

        # Encabezados de la tabla
        headers = ["Código", "Nombre", "Credito","Horas", "Acciones"]
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
        if len(self.lista_UC) <= self.uc_por_pagina:
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

        if len(self.lista_UC) <= self.uc_por_pagina:
            self.frame_paginacion.grid_remove()
        else:
            self.frame_paginacion.grid()

        # Lista para almacenar las filas de datos
        self.mostrar_listado()
        
    def mostrar_listado(self):
        """
        Muestra la lista de UC en la tabla, con sus botones de acción.
        """
        if self.busqueda_frame.pnf_var.get() == "Seleccione un PNF":
            self.paginas_mostrar = []
            self.total_paginas = 0
            self.pagina_actual = 0
            self.label_pagina.configure(text="0 de 0")
            self.boton_anterior.configure(state="disabled")
            self.boton_siguiente.configure(state="disabled")
        # Si hay un PNF seleccionado, filtra la lista de UC de acuerdo al PNF
        if self.busqueda_frame.pnf_var.get() != "Seleccione un PNF":    
            # Limpia las filas anteriores
            for fila in self.fila_datos:
                for widget in fila:
                    widget.destroy()
            self.fila_datos.clear()
            # Empieza en la fila 2 porque la fila 1 es el encabezado
            for fila, tupla_uc in enumerate(self.paginas_mostrar, start=2):
                fila_widgets = [
                    self._crear_celda(fila, 0, tupla_uc[1]),  # Código
                    self._crear_celda(fila, 1, tupla_uc[2]),  # Nombre
                    self._crear_celda(fila, 2, tupla_uc[15]),  # Crédito
                    self._crear_celda(fila, 3, tupla_uc[14]),  # Horas
                ]
                celda_btn = ctk.CTkFrame(self, fg_color="#f5f5f5", corner_radius=4)
                celda_btn.grid(row=fila, column=4, padx=1, pady=1, sticky="nsew")
                boton = ctk.CTkButton(
                    celda_btn, text="Ver datos", width=100,
                    text_color="#222",
                    command=lambda uc=tupla_uc: self.ver_datos_completos(uc)
                )
                boton.pack(padx=10, pady=5)
                fila_widgets.append(celda_btn)
                self.fila_datos.append(fila_widgets)
        else:
            # Deja la tabla vacía si no hay PNF seleccionado y los botones de paginación deshabilitados
            for fila in self.fila_datos:
                for widget in fila:
                    widget.destroy()
            self.fila_datos.clear()


    def _crear_celda(self, row, col, texto):
        """
        Crea una celda de la tabla con el texto dado.
        """
        celda = ctk.CTkFrame(self, fg_color="#f5f5f5", corner_radius=4)
        celda.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
        label = ctk.CTkLabel(celda, text=texto, text_color="#222")
        label.pack(padx=10, pady=5)
        return celda
    
    def anterior_pagina(self):
        """
        Retrocede a la página anterior de la tabla.
        """
        if self.pagina_actual > 1:
            self.pagina_actual -= 1
            nuevo_inicio = (self.pagina_actual - 1) * self.uc_por_pagina
            nuevo_fin = nuevo_inicio + self.uc_por_pagina
            self.paginas_mostrar = self.lista_UC[nuevo_inicio:nuevo_fin]
            self.label_pagina.configure(text=f"{self.pagina_actual} de {self.total_paginas}")
            self.calcular_pagina()
        
    def siguiente_pagina(self):
        """
        Avanza a la siguiente página de la tabla.
        """
        nuevo_inicio = self.pagina_actual * self.uc_por_pagina
        nuevo_fin = nuevo_inicio + self.uc_por_pagina
        if self.pagina_actual < self.total_paginas:
            self.pagina_actual += 1
            self.paginas_mostrar = self.lista_UC[nuevo_inicio:nuevo_fin]
            self.label_pagina.configure(text=f"{self.pagina_actual} de {self.total_paginas}")
            self.calcular_pagina()
    
    def calcular_pagina(self, lista_uc=None):
        """
        Habilita/deshabilita los botones de paginación según la página actual y muestra el listado.
        """
        if lista_uc is not None:
            self.lista_UC = lista_uc

        total_registros = len(self.lista_UC)
        self.total_paginas = (total_registros + self.uc_por_pagina - 1) // self.uc_por_pagina if total_registros > 0 else 0

        # Ajustar página actual
        if self.total_paginas == 0:
            self.pagina_actual = 0
        elif self.pagina_actual > self.total_paginas:
            self.pagina_actual = self.total_paginas
        elif self.pagina_actual < 1:
            self.pagina_actual = 1

        inicio = (self.pagina_actual - 1) * self.uc_por_pagina if self.pagina_actual > 0 else 0
        fin = inicio + self.uc_por_pagina
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

        self.mostrar_listado()


    def ver_datos_completos(self, uc):
        """
        Muestra los datos completos de la UC seleccionada.
        """
        dic_datos = self.controller.obtener_datos_completos_uc(uc[0])
        #dic_id = self.controller.obtener_id(dic_datos)
        top = ctk.CTkToplevel(self, fg_color="White")
        top.title("Datos Completos de las Unidades Curriculares")
        ancho = 900
        alto = 700
        # top.resizable(False, False)
        # top.minsize(ancho, alto)
        # top.maxsize(ancho, alto)

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
        content_frame = ctk.CTkFrame(top, fg_color="white")
        content_frame.pack(fill="both", expand=True)

        def on_close():
            #content_frame.unbind_all("<MouseWheel>")
            top.destroy()
        top.protocol("WM_DELETE_WINDOW", on_close)

        #Frame de los datos generales de UC
        self.frame_uc = UnidadCurricular(content_frame, self.controller, mostrar_botones=False)
        self.frame_uc.set_datos(dic_datos)
        self.frame_uc.pack(fill="both", expand=True, padx=0, pady=0)

        # Ocultar botones de grabar y limpiar en el modal
        try:
            self.frame_uc.btn_guardar.pack_forget()
            self.frame_uc.btn_cancelar.pack_forget()
        except AttributeError:
            pass

        # al abrir el modal:
        self.id_uc_modal = uc[0]

        # Frame de botones de acción
        self.botones_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        self.botones_frame.pack(pady=10)

        self.btn_actualizar = ctk.CTkButton(
            self.botones_frame, text="Actualizar Datos", state="disabled", command=lambda: self.actualizar_uc(self.frame_uc, None, self.id_uc_modal, top)
        )
        self.btn_actualizar.pack(side="left", padx=10)

        ctk.CTkButton(self.botones_frame, text="Editar Campos", command=lambda: self.habilitar_todos(self.frame_uc)).pack(side="left", padx=10)
        ctk.CTkButton(self.botones_frame, text="Cerrar", command=top.destroy).pack(side="left", padx=10)
        self.deshabilitar_todos(self.frame_uc)
        
    def deshabilitar_todos(self, frame_uc):
        """
        Deshabilita todos los campos de edición en el modal y desactiva los botones de acción.
        """
        frame_uc.deshabilitar_campos()
        self.btn_actualizar.configure(state="disabled")
    
    def habilitar_todos(self, frame_uc):
        """
        Habilita todos los campos de edición en el modal y activa los botones de acción.
        """
        frame_uc.habilitar_campos()
        self.btn_actualizar.configure(state="normal")

    def actualizar_uc(self, frame_uc, datos_uc, id_uc, top):
        """
        Actualiza los datos de UC en la base de datos.
        """
        datos_uc = self.controller.getUnidadCurricular(frame_uc)
        exito = self.controller.update_unidad_curricular(datos_uc, id_uc, top)
        if exito:
            top.destroy()
            #self.lista_uc = self.controller.obtener_lista_uc()
            #actualiza la paginacion y muestra el listado
            self.total_paginas = (len(self.lista_uc) + self.uc_por_pagina - 1) // self.uc_por_pagina
            self.paginas_mostrar = self.lista_uc[(self.pagina_actual-1)*self.uc_por_pagina:self.pagina_actual*self.uc_por_pagina]
            self.label_pagina.configure(text=f"{self.pagina_actual} de {self.total_paginas}")
            self.mostrar_listado()
    
    def mostrar_resultado_busqueda(self, lista_uc):
        """
        Muestra el resultado filtrado por PNF.
        """
        self.pagina_actual = 1
        self.total_paginas = (len(lista_uc) + self.uc_por_pagina - 1) // self.uc_por_pagina
        self.paginas_mostrar = lista_uc[:self.uc_por_pagina]
        self.label_pagina.configure(text=f"{self.pagina_actual} de {self.total_paginas}")

        # Ocultar paginación si no es necesaria
        if len(self.lista_UC) <= self.uc_por_pagina:
            self.frame_paginacion.grid_remove()
        else:
            self.frame_paginacion.grid()

        self.mostrar_listado()


    def actualizar_pagina(self):
        """
        Actualiza la página actual y muestra el listado.
        """
        self.paginas_mostrar = self.lista_UC[(self.pagina_actual-1)*self.uc_por_pagina:self.pagina_actual*self.uc_por_pagina]
        self.label_pagina.configure(text=f"{self.pagina_actual} de {self.total_paginas}")
        self.calcular_pagina()

    def actualizar_botones_paginacion(self):
        """
        Habilita o deshabilita los botones de paginación según la página actual y el total de páginas.
        """
        # deshabilita los botones si no hay registros en la lista
        if not self.lista_UC or len(self.lista_UC) <= 0:
            self.frame_paginacion.grid_remove()
            self.boton_anterior.configure(state="disabled")
            self.boton_siguiente.configure(state="disabled")
        else:
            self.frame_paginacion.grid()
            self.boton_anterior.configure(state="disabled" if self.pagina_actual <= 1 else "normal")
            self.boton_siguiente.configure(state="disabled" if self.pagina_actual >= self.total_paginas else "normal")
            # Actualiza el estado de los botones de paginación
            self.boton_anterior.configure(state="normal" if self.pagina_actual > 1 else "disabled")
            self.boton_siguiente.configure(state="normal" if self.pagina_actual < self.total_paginas else "disabled")



