import customtkinter as ctk
import tkinter as tk
import threading
from views.dashboard.components.widget_utils import *
from views.dashboard.modules.forms.PNF.FormPNF import DatosPNFPensumFrame
from views.dashboard.modules.forms.PNF.frameTrayecto import FrameTrayecto

class ListarPNF(ctk.CTkScrollableFrame):
    def __init__(self, master, controller):
        super().__init__(master, fg_color="white")
        self.controller = controller
        self.lista_pnf = self.controller.listado_pnf  # Debe ser una lista de tuplas (id, codigo, nombre)
        
        self.pagina_actual = 1
        self.cantidad_mostrar = 5

        self.cantidad_paginas = (len(self.lista_pnf) // self.cantidad_mostrar) + (1 if len(self.lista_pnf) % self.cantidad_mostrar > 0 else 0)
       
        self.filas_datos = []
        """
        Implementar logica para la paginacion 
        """
        try:
            toplevel = self.winfo_toplevel()
            self.vcmd_num_val = toplevel.register(self.controller._solo_numeros)
            self.vcmd_fecha_val = toplevel.register(self.controller._numeros_y_barras)
            self.vcmd_decimal_val = toplevel.register(self.controller._solo_decimal)
        except Exception: # Fallback si no es un toplevel (ej. si el master es el root)
            self.vcmd_num_val = master.register(self.controller._solo_numeros)
            self.vcmd_fecha_val = master.register(self.controller._numeros_y_barras)
            self.vcmd_decimal_val = master.register(self.controller._solo_decimal)

        #Primeras paginas a mostrar
        self.paginas_mostrar = self.lista_pnf[:self.cantidad_mostrar]
        self.posicion_actual = len(self.paginas_mostrar)
        # --- ENCABEZADOS (FILA 1) ---
        headers = ["ID", "Código", "Nombre", "Acción"]
        for col, header in enumerate(headers):
            celda = ctk.CTkFrame(self, fg_color="#e0e0e0", corner_radius=4)
            celda.grid(row=1, column=col, padx=1, pady=1, sticky="nsew")
            label = ctk.CTkLabel(celda, text=header, font=ctk.CTkFont(weight="bold"), text_color="#222")
            label.pack(padx=10, pady=5)
        for i in range(len(headers)):
            self.grid_columnconfigure(i, weight=1)


      
# --- PAGINACIÓN (se ubicará dinámicamente al final de los datos) ---
        self.frame_paginacion = ctk.CTkFrame(self, fg_color="transparent")

        # Configuración de columnas para centrar los elementos de paginación
        self.frame_paginacion.grid_columnconfigure(0, weight=1)
        self.frame_paginacion.grid_columnconfigure(1, weight=0)
        self.frame_paginacion.grid_columnconfigure(2, weight=0)
        self.frame_paginacion.grid_columnconfigure(3, weight=0)
        self.frame_paginacion.grid_columnconfigure(4, weight=1)

        self.boton_anterior = ctk.CTkButton(self.frame_paginacion, text="Anterior", command=self.anterior_pagina)
        self.label_pagina = ctk.CTkLabel(self.frame_paginacion, text=f"{self.pagina_actual} de {self.cantidad_paginas}", text_color="#222")
        self.boton_siguiente = ctk.CTkButton(self.frame_paginacion, text="Siguiente",command=self.siguiente_pagina)

        self.boton_anterior.grid(row=0, column=1, padx=(0, 5))
        self.label_pagina.grid(row=0, column=2, padx=5)
        self.boton_siguiente.grid(row=0, column=3, padx=(5, 0))

        # Coloca el frame de paginación al final de la tabla (ajusta la fila según tus datos)
        fila_paginacion = len(self.paginas_mostrar) + 2
        self.frame_paginacion.grid(row=fila_paginacion, column=0, columnspan=4, pady=15, sticky="ew")
                
        self.calcular_pagina()

    def mostrar_listado(self):
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
        celda = ctk.CTkFrame(self, fg_color="#f5f5f5", corner_radius=4)
        celda.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
        label = ctk.CTkLabel(celda, text=texto, text_color="#222")
        label.pack(padx=10, pady=5)
        return celda

    def ver_datos_completos(self, pnf):
        # Por ahora no hace nada, puedes implementar la lógica aquí más adelante
        dic_datos = self.controller.obtener_datos_completos(pnf[0])
        dic_id = self.controller.obtener_id(dic_datos)
        top = ctk.CTkToplevel(self,fg_color="White")
        ancho = 900
        alto = 700

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

        #agregar scroll
        scroll_frame = ctk.CTkScrollableFrame(top,fg_color="White")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        frame_pnf = DatosPNFPensumFrame(scroll_frame,self.vcmd_num_val,self.vcmd_fecha_val)
        frame_pnf.set_datos(dic_datos)
        frame_pnf.pack(fill="x", padx=20, pady=10)

        list_trayecto = []  # <-- inicializa aquí


        if dic_datos["lista_trayectos"]:
            
            i = 1
            for datos_trayecto in dic_datos["lista_trayectos"]:
                frame = FrameTrayecto(scroll_frame,self.controller,self.vcmd_num_val,self.vcmd_fecha_val,f"Trayecto #{i}")
                frame.set_datos(datos_trayecto)
                list_trayecto.append(frame)
            for frame in list_trayecto:
                frame.pack(fill="x", padx=20, pady=10)

        botones_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        botones_frame.pack(pady=10)

        self.btn_actualizar = ctk.CTkButton(
            botones_frame, text="Actualizar Datos", state="disabled", command=lambda:self.actualizar_pnf(frame_pnf,list_trayecto,dic_datos["lista_trayectos"],dic_id,top)
        )
        self.btn_actualizar.pack(side="left", padx=10)

        # Botón para editar campos
        ctk.CTkButton(botones_frame, text="Editar Campos",command=lambda:self.habilitar_todos(frame_pnf,list_trayecto)).pack(side="left", padx=10)
        ctk.CTkButton(botones_frame, text="Cerrar").pack(side="left", padx=10)
    
    #Logica para la paginacion
    def siguiente_pagina(self):
         # Calcula el nuevo inicio
        nuevo_inicio = self.pagina_actual * self.cantidad_mostrar
        nuevo_fin = nuevo_inicio + self.cantidad_mostrar

        # Solo avanza si no es la última página
        if self.pagina_actual < self.cantidad_paginas:
            self.pagina_actual += 1
            self.paginas_mostrar = self.lista_pnf[nuevo_inicio:nuevo_fin]
            self.label_pagina.configure(text=f"{self.pagina_actual} de {self.cantidad_paginas}")

            # Muestra la nueva página
            self.calcular_pagina()

    def anterior_pagina(self):
        # Solo retrocede si no es la primera página
        if self.pagina_actual > 1:
            self.pagina_actual -= 1
            nuevo_inicio = (self.pagina_actual - 1) * self.cantidad_mostrar
            nuevo_fin = nuevo_inicio + self.cantidad_mostrar
            self.paginas_mostrar = self.lista_pnf[nuevo_inicio:nuevo_fin]
            self.label_pagina.configure(text=f"{self.pagina_actual} de {self.cantidad_paginas}")
            self.calcular_pagina()


    def calcular_pagina(self):

        estado_btn_siguiente = "normal"
        estado_btn_anterio = "normal"

        if self.pagina_actual == 1: estado_btn_anterio = "disabled"
        self.boton_anterior.configure(state=estado_btn_anterio)

        if self.pagina_actual == self.cantidad_paginas: estado_btn_siguiente = "disabled"
        self.boton_siguiente.configure(state=estado_btn_siguiente)

        self.mostrar_listado()

    def habilitar_todos(self,frame_pnf, lista_trayecto):
        frame_pnf.habilitar_campos()

        for frame_trayecto in lista_trayecto:
            frame_trayecto.habilitar_campos()
        self.btn_actualizar.configure(state="normal")

    def actualizar_pnf(self,frame_pnf, lista_trayecto,listaDatosTrayecto,dic_id,top):
        lista_datos_trayecto=[]
        for trayecto,datos_trayecto in zip(lista_trayecto,listaDatosTrayecto):
            lista_datos_trayecto.append(trayecto.obtener_datos_trayectos(datos_trayecto["lista_tramos"]))
        dic_pnf = self.controller.getPNF(frame_pnf,lista_datos_trayecto)
        exito = self.controller.update_pnf(dic_pnf,dic_id,top)
        if exito:
            top.destroy()
            self.lista_pnf = self.controller.listado_pnf
