import tkinter.messagebox as messagebox
import tkinter as tk
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase
from views.dashboard.modules.forms.Estudiantes.Ingreso_seccion import AsignarSeccionFrame
from ..DatosPersonales import DatosPersonalesFrame
from pprint import pprint

class AsignarPNFFrame(SectionFrameBase):
    def __init__(self, master, controller, controller_pnf,controller_secciones, estudiante,para_edicion,callbak):
        super().__init__(master,"Asignar PNF a Estudiante",COLOR_HEADER_SECCION_BG_2)
        self.controller = controller
        self.controller_pnf = controller_pnf
        self.estudiante = estudiante
        self.fecha_inicio = ""
        self.fecha_fin = ""
        self.btn_fecha = None
        self.controller_secciones = controller_secciones
        self.callbak = callbak
        self.mensajesSecciones = None
        self.asignacion_seccion = None

        self.para_edicion = para_edicion  # Variable para indicar si es para edición

        if not self.controller_pnf:
            print("Error: El controlador de PNF no está definido.")
        else:
            vcmd = self.register(self.controller_pnf.solo_decimal)  # Registrar el método de validación
            self.var_estado = ctk.StringVar(value="Activo")  # Valor por defecto para el estado
            
            self.nombres_pnf = self.controller_pnf.obtener_nombres_pnf()
            self.var1 = ctk.StringVar(value=self.nombres_pnf[0] if self.nombres_pnf else "") # Valor por defecto para el PNF
            self.id_estudiante = self.estudiante.get("id")
            self.tuple_pnf = self.controller_pnf.listado_pnf

            self.pnf_id_por_nombre = {tupla[2]: tupla[0] for tupla in self.tuple_pnf}  # nombre: id
            self.trayecto_id_por_nombre = {trayecto[1]: trayecto[0] for trayecto in self.controller_pnf.obtener_trayectos_por_pnf(self.pnf_id_por_nombre[self.var1.get()])}  # nombre: id

            self.valores_trayecto = [trayecto[1] for trayecto in self.controller_pnf.obtener_trayectos_por_pnf(self.pnf_id_por_nombre[self.var1.get()])]  # Obtener los trayectos para el PNF seleccionado
            
            self.var_turno = ctk.StringVar(value="Diurno")  # Valor por defecto para el turno
            self.var_trayecto = ctk.StringVar(value=self.valores_trayecto[0] if self.valores_trayecto else "Trayecto")  # Valor por defecto para el trayecto
          
            self.tupla_tramos = self.controller_pnf.obtener_tramos_por_trayecto(self.trayecto_id_por_nombre[self.var_trayecto.get()])  # Obtener los tramos para el trayecto seleccionado
            self.valores_tramos = [tramo[1] for tramo in self.tupla_tramos]
            self.var_tramo = ctk.StringVar(value=self.valores_tramos[0] if self.valores_tramos else "No seleccionado")  # Valor por defecto para el tramo
            self.tramo_id_por_nombre = {tramo[1]: tramo[0] for tramo in self.tupla_tramos}
            
            self._crear_fila_widgets([
                ("Seleccione un P.N.F:", crear_option_menu, {"values":self.nombres_pnf, "variable":self.var1, "command": self.set_trayecto  }, 1, self, 'pnf_menu')
            ])
            # Asignar Fecha de Inicio y Fin
            self.registrar_fecha(self.set_fecha_inicio, titulo_btn="Fecha de Inicio",attr_name="btn_fecha_inicio")
            self.fecha_inicio_label = ctk.CTkLabel(self, text="Fecha de Inicio: No seleccionada", font=FUENTE_LABEL_CAMPO, text_color=COLOR_TEXTO_PRINCIPAL)
            self.fecha_inicio_label.pack(pady=(10, 0), padx=10, anchor="w")

            self.registrar_fecha(self.set_fecha_fin, titulo_btn="Fecha de Fin",attr_name="btn_fecha_fin")
            self.fecha_fin_label = ctk.CTkLabel(self, text="Fecha de Fin: No seleccionada", font=FUENTE_LABEL_CAMPO, text_color=COLOR_TEXTO_PRINCIPAL)
            self.fecha_fin_label.pack(pady=(10, 0), padx=10, anchor="w")

            self._crear_fila_widgets([
                ("Cohorte:", crear_entry, {"width":300,"placeholder_text":"Ingrese la cohorte"}, 1, self, 'cohorte_entry'),
                ("Turno:", crear_option_menu, {"values": ["Diurno", "Nocturno", "Fin de semana"], "variable": self.var_turno}, 1, self, 'turno_menu'),
            ])

            self._crear_fila_widgets([
                ("Trayecto Actual:", crear_option_menu, {"values": self.valores_trayecto, "variable": self.var_trayecto,"command": self.set_tramo}, 1, self, 'trayecto_menu'),
                ("Tramo Actual:", crear_option_menu, {"values": self.valores_tramos, "variable": self.var_tramo, "command": self.set_seccion}, 1, self, 'tramo_menu'),
                ("Creditos aprobados:", crear_entry, {"width":300,"placeholder_text":"Ingrese los créditos aprobados"}, 1, self, 'creditos_aprobados_entry'),
                ("Creditos cursados:", crear_entry, {"width":300,"placeholder_text":"Ingrese los créditos cursados"}, 1, self, 'creditos_cursados_entry'),
                ("Promedio General:", crear_entry, {"width":150,"placeholder_text":"Ingrese el promedio general","validate":"key","validatecommand":(vcmd,"%P")}, 1, self, 'promedio_general_entry'),
                ("Estado:", crear_option_menu, {"values": ["Activo", "Inactivo","Graduado","Retirado","Suspendido","Transferido"], "variable": self.var_estado}, 1, self, 'estado_menu'),
                ("Observaciones:", crear_entry, {"width":300,"placeholder_text":"Ingrese observaciones"}, 1, self, 'observaciones_entry'),
            ])
            
            self.instancias_widgets = [
                self.pnf_menu,
                self.trayecto_menu,
                self.tramo_menu,
                self.cohorte_entry,
                self.turno_menu,
                self.creditos_aprobados_entry,
                self.creditos_cursados_entry,
                self.promedio_general_entry,
                self.estado_menu,
                self.observaciones_entry,
            ]

            # Empacar los frames
            self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
            self.button_frame.pack(pady=(25, 20))
            # Crear los botones
            if self.para_edicion:
                text = "Actualizar Datos"
                text2 = "Editar PNF"
                command = self.actualizar_datos_pnf
                command2 = self.habilitar_edicion_pnf
            else:
                text = "Registrar PNF"
                text2 = "Limpiar Campos"
                command = self.guardar_datos
                command2 = self.limpiar_campos
                
            self.btn_guardar = ctk.CTkButton(self.button_frame, text=text, width=140,
                                            font=FUENTE_BOTON, fg_color=COLOR_BOTON_PRIMARIO_FG, hover_color=COLOR_BOTON_PRIMARIO_HOVER, 
                                            command=command,
                                            text_color=COLOR_BOTON_PRIMARIO_TEXT, state="normal")
            self.btn_guardar.pack(side="left", padx=10)

            self.btn_cancelar = ctk.CTkButton(self.button_frame, text=text2, width=140, 
                                            font=FUENTE_BOTON, fg_color=COLOR_BOTON_SECUNDARIO_FG, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, 
                                            command=command2,
                                            text_color=COLOR_BOTON_SECUNDARIO_TEXT)
            self.btn_cancelar.pack(side="left", padx=10)

            self.btn_secciones = ctk.CTkButton(
                self.button_frame,
                text="Inscribir Sección",width=140,
                font=FUENTE_BOTON, fg_color=COLOR_BOTON_PRIMARIO_FG, 
                hover_color=COLOR_BOTON_PRIMARIO_HOVER,
                text_color=COLOR_BOTON_PRIMARIO_TEXT,
                command=self.mostrar_form_seccion
            )
            self.btn_secciones.pack(side="left", padx=10)


    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets

    def mostrar_form_seccion(self,datos = None):
        if self.mensajesSecciones:
            self.mensajesSecciones.pack_forget()
        self.btn_secciones.configure(text="Cancelar Seccion", command=self.cancelar_asignacion_seccion,state="normal")

        self.tupla_tramos = self.controller_pnf.obtener_tramos_por_trayecto(self.trayecto_id_por_nombre[self.var_trayecto.get()])  # Obtener los tramos para el trayecto seleccionado
        self.tramo_id_por_nombre = {tramo[1]: tramo[0] for tramo in self.tupla_tramos}

        state_frame = False
        if datos:
            state_frame = True

        self.asignacion_seccion = AsignarSeccionFrame(self,self.controller_secciones,
                                                      self.pnf_id_por_nombre[self.var1.get()],
                                                      self.trayecto_id_por_nombre[self.var_trayecto.get()],
                                                      self.tramo_id_por_nombre[self.var_tramo.get()],
                                                      carga_datos=True)
        
        self.asignacion_seccion.pack(pady = 10, padx = 10, fill="both", expand=True)
        if datos:
            self.asignacion_seccion.cargar_datos_secciones(datos)
    
        self.button_frame.pack_forget()
        self.button_frame.pack(pady=(25, 20))
    
    def no_secciones_disponibles(self):
         # Elimina el mensaje anterior si existe
        if self.mensajesSecciones and self.mensajesSecciones.winfo_exists():
            self.mensajesSecciones.destroy()
        # Crea el nuevo mensaje y guárdalo correctamente
        self.mensajesSecciones = ctk.CTkLabel(self, text="No hay secciones disponibles", font=FUENTE_LABEL_CAMPO, text_color=COLOR_TEXTO_PRINCIPAL)
        self.mensajesSecciones.pack(pady=(10, 0), padx=10, anchor="w")
 
    def cancelar_asignacion_seccion(self):
        self.asignacion_seccion.destroy()
        self.asignacion_seccion = None
        self.button_frame.pack(pady=(25, 20))
        self.btn_secciones.configure(text="Inscribir Sección", command=self.mostrar_form_seccion)
        if self.mensajesSecciones and self.mensajesSecciones.winfo_exists():
            self.mensajesSecciones.destroy()

    def registrar_fecha(self,callback,titulo_btn="Seleccionar Fecha",attr_name=None):
       
        def calendario():
            top = ctk.CTkToplevel(self, fg_color="White")
            top.title("Seleccionar Fecha")

            # Tamaño deseado de la ventana emergente
            ancho = 350
            alto = 350

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
            label = ctk.CTkLabel(top, text="Seleccione Fecha", font=FUENTE_LABEL_CAMPO, text_color=COLOR_TEXTO_PRINCIPAL)
            label.pack(pady=10)
            self.cal = Calendar(top, locale='es_ES', date_pattern='yyyy-mm-dd')
            self.cal.pack(pady=20)

            def mostrar_fecha(date):
                label.configure(text=f"Fecha seleccionada: {date}")

            def guardar_fecha():
                fecha = self.cal.get_date()
                callback(fecha)  # Llama al callback con la fecha seleccionada
                top.destroy()

            self.cal.bind("<<CalendarSelected>>", lambda e: mostrar_fecha(self.cal.get_date()))
            boton_guardar = ctk.CTkButton(top, text="Guardar Fecha", command=guardar_fecha)
            boton_guardar.pack(pady=10)
             # Crea una ventana emergente
        frame_fecha = ctk.CTkFrame(self, fg_color="transparent")
        frame_fecha.pack(fill="x", pady=(10, 0), padx=10)

        self.btn_fecha = ctk.CTkButton(
            frame_fecha,
            text=titulo_btn,
            command=calendario,
            width=100,
            font=FUENTE_BOTON,
            fg_color=COLOR_BOTON_PRIMARIO_FG,
            hover_color=COLOR_BOTON_PRIMARIO_HOVER,
            text_color=COLOR_BOTON_PRIMARIO_TEXT
        )
        self.btn_fecha.pack(side="left", pady=(10, 0), anchor="w")
        if attr_name:
            setattr(self, attr_name, self.btn_fecha)


    def set_fecha_inicio(self,fecha):
        if fecha:
            self.fecha_inicio = fecha
            print("Fecha de inicio establecida:", self.fecha_inicio)
            self.fecha_inicio_label.configure(text=f"Fecha de Inicio: {self.fecha_inicio}")
    
    def set_fecha_fin(self, fecha):
        if fecha:
            self.fecha_fin = fecha
            print("Fecha de fin establecida:", self.fecha_fin)
            self.fecha_fin_label.configure(text=f"Fecha de Fin: {self.fecha_fin}")

    def set_trayecto(self, value):
        if self.mensajesSecciones:
            self.mensajesSecciones.pack_forget()
        tupla_trayectos = self.controller_pnf.obtener_trayectos_por_pnf(self.pnf_id_por_nombre[value])
        self.valores_trayecto = [trayecto[1] for trayecto in tupla_trayectos]  # Obtener solo los nombres de los trayectos
        self.var_trayecto.set(self.valores_trayecto[0] if self.valores_trayecto else "Trayecto")  # Valor por defecto para el trayecto
        self.trayecto_menu.configure(values=self.valores_trayecto)
        self.set_tramo(self.var_trayecto.get())
        if self.asignacion_seccion:
            self.asignacion_seccion.actualizar_datos_secciones(self.pnf_id_por_nombre[value],self.trayecto_id_por_nombre[self.var_trayecto.get()],self.tramo_id_por_nombre[self.var_tramo.get()])


    def set_tramo(self, value):
        if self.mensajesSecciones:
            self.mensajesSecciones.pack_forget()
        tupla_tramos = self.controller_pnf.obtener_tramos_por_trayecto(self.trayecto_id_por_nombre[value])
        self.valores_tramos = [tramo[1] for tramo in tupla_tramos]
        self.var_tramo.set(self.valores_tramos[0] if self.valores_tramos else "Tramo")
        self.tramo_menu.configure(values=self.valores_tramos)
        self.tramo_id_por_nombre = {tramo[1]: tramo[0] for tramo in tupla_tramos}
        if self.asignacion_seccion:
            self.asignacion_seccion.actualizar_datos_secciones(self.pnf_id_por_nombre[self.var1.get()],self.trayecto_id_por_nombre[value],self.tramo_id_por_nombre[self.var_tramo.get()])

    def set_seccion(self,value):
         if self.asignacion_seccion:
            
            self.asignacion_seccion.actualizar_datos_secciones(self.pnf_id_por_nombre[self.var1.get()],
                                                               self.trayecto_id_por_nombre[self.var_trayecto.get()],
                                                               self.tramo_id_por_nombre[value])

    def guardar_datos(self):
        datos = self.controller_pnf.obtener_asignacion_pnf(self)
       
        if not datos:
            print("Error: No se pudieron obtener los datos de la asignación del PNF.")
            return
        datos["pnf_id"] = self.pnf_id_por_nombre[self.var1.get()]
        if not self.controller_pnf.validar_campos_obligatorios_asignacion(datos,self):
            print("Error: Los datos de la asignación del PNF no son válidos.")
            return
        if self.controller_pnf.modelo.registrar_asignacion_estudiante_pnf(datos):
            messagebox.showinfo("Éxito", "La asignación se realizo exitosamente.", parent=self)
            """
            Registro de asignacion del estudiante a una Seccion
            """   
            if self.asignacion_seccion:
                datos_secciones = self.controller_secciones.obtener_datos_vista_seccionAsignada(self.asignacion_seccion)
                datos_secciones["estudiante_id"] = self.id_estudiante
                print(datos_secciones)
                exito = self.controller_secciones.registrar_estudiante_seccion(datos_secciones)
                if exito:
                    print("La inscripcion se realizo exitosamente")
                else:
                    print("No se pudo realizar la inscripcion")

            self.callbak()
            self.winfo_toplevel().destroy()    # Cierra el formulario después de guardar
        else:
            messagebox.showerror("Error", "No se pudo realizar la asignación, intente nuevamente.", parent=self)

        

    def cargar_datos_pnf(self, estudiante_id):
        datos_pnf = self.controller_pnf.modelo.obtener_pnf_asignado(estudiante_id)
        if datos_pnf:
            #cargar los datos de las variables de control y desactivar los campos
            nombre_pnf = next((nombre for nombre, id_ in self.pnf_id_por_nombre.items() if id_ == datos_pnf["pnf_id"]), None)
            if nombre_pnf:
                self.var1.set(nombre_pnf)
                self.pnf_menu.configure(state="disabled")
            
            self.var_trayecto.set(datos_pnf["trayecto_actual"])
            self.trayecto_menu.configure(state="disabled")

            self.var_tramo.set(datos_pnf["tramo_actual"])
            self.tramo_menu.configure(state="disabled")


            if datos_pnf["turno"]:
                self.var_turno.set(datos_pnf["turno"])
                self.turno_menu.configure(state="disabled")

            self.cohorte_entry.insert(0, datos_pnf["cohorte"])
            self.cohorte_entry.configure(state="disabled")

            self.creditos_aprobados_entry.insert(0, datos_pnf["creditos_aprobados"])
            self.creditos_aprobados_entry.configure(state="disabled")

            self.creditos_cursados_entry.insert(0, datos_pnf["creditos_cursados"])
            self.creditos_cursados_entry.configure(state="disabled")

            promedio_general = str(datos_pnf.get("promedio_general", ""))
            self.promedio_general_entry.insert(0, promedio_general)
            self.promedio_general_entry.configure(state="disabled")

            self.var_estado.set(datos_pnf["estado"])
            self.estado_menu.configure(state="disabled")
            
            if datos_pnf["observaciones"]:
                self.observaciones_entry.insert(0, datos_pnf["observaciones"])
            self.observaciones_entry.configure(state="disabled")

            self.fecha_inicio = datos_pnf.get("fecha_inicio", "")
            if self.fecha_inicio:
                self.fecha_inicio_label.configure(text=f"Fecha de Inicio: {self.fecha_inicio}")
            else:
                self.fecha_inicio_label.configure(text="Fecha de Inicio: No seleccionada")
            
            self.fecha_fin = datos_pnf.get("fecha_fin", "")
            if self.fecha_fin:
                self.fecha_fin_label.configure(text=f"Fecha de Fin: {self.fecha_fin}")
            else:
                self.fecha_fin_label.configure(text="Fecha de Fin: No seleccionada")
            self.btn_fecha_inicio.configure(state="disabled")
            self.btn_fecha_fin.configure(state="disabled")
            self.btn_guardar.configure(state="disabled")

            resultado = self.controller_secciones.obtener_seccion_estudiante(estudiante_id)
            if resultado:
                self.mostrar_form_seccion(resultado)
                self.btn_secciones.configure(state="disabled")
            
        else:
            print("Error: No se pudieron cargar los datos del PNF.")

    def actualizar_datos_pnf(self):
        datos = self.controller_pnf.obtener_asignacion_pnf(self)
        if not datos:
            print("Error: No se pudieron obtener los datos de la asignación del PNF.")
            return
        datos["pnf_id"] = self.pnf_id_por_nombre[self.var1.get()]
        if not self.controller_pnf.validar_campos_obligatorios_asignacion(datos,self):
            print("Error: Los datos de la asignación del PNF no son válidos.")
            return
        if self.controller_pnf.modelo.update_pnf_asignado(self.estudiante["id"],datos):
            messagebox.showinfo("Exito", "La actualización se realizo exitosamente.", parent=self)

            if self.asignacion_seccion:
                datos_secciones = self.controller_secciones.obtener_datos_vista_seccionAsignada(self.asignacion_seccion)
                datos_secciones["estudiante_id"] = self.id_estudiante
                exito = self.controller_secciones.registrar_estudiante_seccion(datos_secciones)
                if exito:
                    print("La inscripcion se realizo exitosamente")
                else:
                    print("No se pudo realizar la inscripcion")

            self.callbak()
            self.winfo_toplevel().destroy()  # Cierra el formulario después de guardar
        else:
            messagebox.showerror("Error", "No se pudo actualizar.", parent=self)

       

    def habilitar_edicion_pnf(self):
        for widget in self.instancias_widgets:
            widget.configure(state="normal")
        self.btn_fecha_inicio.configure(state="normal")
        self.btn_fecha_fin.configure(state="normal")
        self.btn_guardar.configure(state="normal")

        if self.asignacion_seccion:
            self.asignacion_seccion.habilitar_campos()

    def limpiar_campos(self):
        for widget in self.instancias_widgets:
            if isinstance(widget, ctk.CTkEntry):
                widget.delete(0, "end")
            elif isinstance(widget, ctk.CTkButton):
                widget.configure(state="normal")
        
        self.fecha_inicio_label.configure(text="Fecha de Inicio: No seleccionada")
        self.fecha_fin_label.configure(text="Fecha de Fin: No seleccionada")
        self.btn_fecha_inicio.configure(state="normal")
        self.btn_fecha_fin.configure(state="normal")

    
