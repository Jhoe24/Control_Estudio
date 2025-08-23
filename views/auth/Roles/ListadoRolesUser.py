import customtkinter as ctk
import tkinter.messagebox as messagebox
from views.dashboard.components.widget_utils import *


class FrameRoles(ctk.CTkFrame):
    def __init__(self, master, controller, modo_desbloqueo=None):
        super().__init__(master, fg_color="transparent")
        # Inicializa el controlador de usuario
        self.controller_user = controller["Usuario"]
    
        self.usuarios_dato = self.controller_user.obtener_lista_usuarios()
        self.cantidad_usuarios = len(self.usuarios_dato)
        self.pagina_actual = 1
        self.registros_por_pagina = 7
        # Primeras páginas a mostrar
        self.paginas_mostrar = self.usuarios_dato
        self.posicion_actual = len(self.paginas_mostrar)
        self.fila_datos = []
        self.modo_desbloqueo = modo_desbloqueo

       
         # Calcula la cantidad total de páginas, asegurando al menos 1 si hay registros
        self.cantidad_total_paginas = (self.cantidad_usuarios // self.registros_por_pagina) + (1 if self.cantidad_usuarios % self.registros_por_pagina > 0 else 0)

         # Si no hay estudiantes, la cantidad total de páginas es 1 para mostrar la interfaz vacía
        if self.cantidad_usuarios == 0:
            self.cantidad_total_paginas = 1

        # headers de la tabla
        if self.modo_desbloqueo:
            headers = ["Doc. Identidad", "Nombres", "Apellidos", "Usuario", "Rol", "Bloquera"]
        else:   
            headers = ["Doc. Identidad", "Nombres", "Apellidos", "Usuario", "Rol", "Gestión Rol"]
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
        self.frame_paginacion.grid_columnconfigure(4, weight=0)
        self.frame_paginacion.grid_columnconfigure(5, weight=1)

        # Botones de paginación
        self.boton_anterior = ctk.CTkButton(self.frame_paginacion, text="Anterior", command=self.anterior_pagina)
        self.label_pagina = ctk.CTkLabel(self.frame_paginacion, text=f"{self.pagina_actual} de {self.cantidad_total_paginas}", text_color="#222")
        self.boton_siguiente = ctk.CTkButton(self.frame_paginacion, text="Siguiente", command=self.siguiente_pagina)

        self.boton_anterior.grid(row=0, column=1, padx=(0, 5))
        self.label_pagina.grid(row=0, column=2, padx=5)
        self.boton_siguiente.grid(row=0, column=3, padx=(5, 0))

        # Coloca el frame de paginación al final de la tabla
        fila_paginacion = len(self.paginas_mostrar) + 2
        self.frame_paginacion.grid(row=fila_paginacion, column=0, columnspan=4, pady=15, sticky="ew")
        
        self.mostrar_pagina()

    def mostrar_pagina(self):
        """
        Habilita/deshabilita los botones de paginación según la página actual y muestra el listado.
        """
        estado_btn_siguiente = "normal"
        estado_btn_anterio = "normal"
        if self.pagina_actual == 1:
            estado_btn_anterio = "disabled"
        self.boton_anterior.configure(state=estado_btn_anterio)
        if self.pagina_actual == self.cantidad_total_paginas:
            estado_btn_siguiente = "disabled"
        self.boton_siguiente.configure(state=estado_btn_siguiente)
        # Calcular el rango de usuarios para la página actual
        inicio = (self.pagina_actual - 1) * self.registros_por_pagina
        fin = inicio + self.registros_por_pagina
        
        # Actualizar self.paginas_mostrar con los usuarios de la página
        self.paginas_mostrar = self.usuarios_dato[inicio:fin]
        
        # Actualizar la etiqueta de la página
        self.label_pagina.configure(text=f"{self.pagina_actual} de {self.cantidad_total_paginas}")
        
        # Llamar a cargar_datos para renderizar la tabla con la nueva lista
        self.cargar_datos()

    def siguiente_pagina(self):
        """
        Avanza a la siguiente página de la tabla.
        """
        nuevo_inicio = self.pagina_actual * self.registros_por_pagina
        nuevo_fin = nuevo_inicio + self.registros_por_pagina
        if self.pagina_actual < self.cantidad_total_paginas:
            self.pagina_actual += 1
            self.paginas_mostrar = self.usuarios_dato[nuevo_inicio:nuevo_fin]
            self.label_pagina.configure(text=f"{self.pagina_actual} de {self.cantidad_total_paginas}")
            self.mostrar_pagina()

    def anterior_pagina(self):
        """
        Retrocede a la página anterior de la tabla.
        """
        if self.pagina_actual > 1:
            self.pagina_actual -= 1
            nuevo_inicio = (self.pagina_actual - 1) * self.registros_por_pagina
            nuevo_fin = nuevo_inicio + self.registros_por_pagina
            self.paginas_mostrar = self.usuarios_dato[nuevo_inicio:nuevo_fin]
            self.label_pagina.configure(text=f"{self.pagina_actual} de {self.cantidad_total_paginas}")
            self.mostrar_pagina()

    def cargar_datos(self):
        """
        Muestra el listado de usuarios para asignar los roles a cada uno de ellos.
        """
        print(f"Cargando {len(self.paginas_mostrar)} usuarios en la tabla")
        # Se limpia la tabla
        for fila in self.fila_datos:
            for widget in fila:
                widget.destroy()
        self.fila_datos.clear()

        self.fila_datos = []
        # se obtienen los datos y me devuelve el diccionario
        for fila, dic_user in enumerate(self.paginas_mostrar, start=2):
            roles = self.controller_user.obtener_roles()
            hay_rol = self.controller_user.obtener_rol(dic_user['id'])
            fila_widgets = [
                self._crear_celda(fila, 0, dic_user['documento_identidad']),
                self._crear_celda(fila, 1, dic_user['nombres']),
                self._crear_celda(fila, 2, dic_user['apellidos']),
                self._crear_celda(fila, 3, dic_user['nombre_usuario']),
                #self._crear_celda(fila, 4, dic_user['rol_id']),
            ]

            celda_btn = ctk.CTkFrame(self, fg_color="#f5f5f5", corner_radius=4)
            celda_btn.grid(row=fila, column=5, padx=1, pady=1, sticky="nsew")
            

            # Frame interno para centrar los botones
            if self.modo_desbloqueo:
                fila_widgets.append(self._crear_celda(fila,4,hay_rol))
                if self.controller_user.the_user_is_blocked(dic_user['id']):
                    text_btn = "Desbloquear Usuario"
                    command_ = lambda id = dic_user['id'], c = 0 : self.desbloquear_usuario(id,c)
                else:
                    text_btn = "Bloquear Usuario"
                    command_ = lambda id = dic_user['id'], c = 1 : self.desbloquear_usuario(id,c)

                boton = ctk.CTkButton(
                celda_btn, text=text_btn, 
                width=120,
                fg_color = "#23272f",
                hover_color = "#31343c",
                text_color = "#fff",
                border_width = 2,
                border_color =  "#444857",
                command=command_
                )
                boton.pack(padx=10, pady=5)
                
            else:
                celda_optionmenu = ctk.CTkFrame(self, fg_color="#f5f5f5", corner_radius=6)
                celda_optionmenu.grid(row=fila, column=4, padx=1, pady=6, sticky="nsew")
                frame_botones = ctk.CTkFrame(celda_btn, fg_color="transparent")
                frame_botones.pack(expand=True)
                var_role = ctk.StringVar(value=roles[0] if roles else "")  
                state_asignar = "normal"
                state_actualizar = "disabled"
                if hay_rol:
                    state_asignar = "disabled"
                    state_actualizar = "normal"
                    var_role.set(hay_rol)

                role_menu = ctk.CTkOptionMenu(
                    celda_optionmenu,
                    values=roles,
                    variable=var_role,
                    width=120,
                    state=state_asignar
                )
                role_menu.pack(padx=10, pady=5)
                fila_widgets.append(celda_optionmenu)

                # Botón para asignar rol
                boton = ctk.CTkButton(
                    frame_botones,
                    text="Asignar Rol",
                    width=120,
                    fg_color = "#23272f",
                    hover_color = "#31343c",
                    text_color = "#fff",
                    border_width = 2,
                    border_color =  "#444857",
                    command=lambda rol=var_role, user_id=dic_user['id']: self.asignar_rol(rol,user_id),
                    state=state_asignar 
                    
                )
                boton.pack(side="left", padx=10, pady=5)
                # Boton para habilitar el boton de asignar rol
                btn = ctk.CTkButton(
                    frame_botones, 
                    text="Habilitar Rol",
                    width=120,
                    fg_color = "#23272f",
                    hover_color = "#31343c",
                    text_color = "#fff",
                    border_width = 2,
                    border_color =  "#444857",
                    command=lambda boton=boton, role_menu=role_menu: self.habilitar_botones(boton, role_menu),
                    state=state_actualizar
                )
                btn.pack(side="left", padx=10, pady=5)

            fila_widgets.append(celda_btn)
            self.fila_datos.append(fila_widgets)


        # Se añaden las filas a la tabla
        fila_paginacion = len(self.paginas_mostrar) + 2
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
    
    def asignar_rol(self,var_role, user_id):
        """
        Asigna un rol a un usuario seleccionado.
        """
        
        if self.controller_user.register_rol(var_role.get(), user_id):
            messagebox.showinfo("Éxito", "Rol asignado correctamente.")
            self.mostrar_pagina()
        else:
            messagebox.showerror("Error", "No se pudo asignar el rol.")
        
    def habilitar_botones(self,boton,role_menu):
        boton.configure(state="normal")
        role_menu.configure(state="normal")

    def desbloquear_usuario(self,user_id, is_to_block):
        """
        Desbloquea un usuario seleccionado.
        """
        mess = "Usuario desbloqueado correctamente," if is_to_block == 1 else "Usuario bloqueado correctamente."
        messError = "No se pudo desbloquear el usuario." if is_to_block == 0 else "No se pudo bloquear el usuario."
        
        
        if self.controller_user.block_user(user_id, is_to_block):
            messagebox.showinfo("Éxito", mess)
            self.mostrar_pagina()
        else:
            messagebox.showerror("Error", messError)