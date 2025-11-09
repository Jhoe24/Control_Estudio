# views/admin/estudiante_form_view.py
import customtkinter as ctk
import tkinter as tk
import tkinter.messagebox as messagebox
from views.dashboard.modules.forms.DatosPersonales import DatosPersonalesFrame
from views.dashboard.modules.forms.Estudiantes.InformacionAcademica import InformacionAcademicaFrame
from views.dashboard.modules.forms.Estudiantes.SistemaIngreso import SistemaIngresoFrame
from views.dashboard.modules.forms.DatosUbicacion import DatosUbicacionFrame

from views.dashboard.components.widget_utils import *

from config.app_config import AppConfig


class FormularioEstudianteView(ctk.CTkScrollableFrame):

    def __init__(self, master, controlador):
        super().__init__(master, fg_color=COLOR_FONDO_FORMULARIO, label_text="")
        self.master = master
        self.controlador = controlador
        self.btn_actualizar = None

        # Frames de cada sección (se instancian con el contenedor como master)
        self.datos_personales_frame = None
        self.informacion_academica_frame = None
        self.sistema_ingreso_frame = None
        self.datos_ubicacion_frame = None

        # Indice y lista de secciones
        self.secciones = []
        self.seccion_actual = 0

        # Registrar funciones de validación
        try:
            toplevel = self.winfo_toplevel()
            self.vcmd_num_val = toplevel.register(self.controlador._solo_numeros)
            self.vcmd_fecha_val = toplevel.register(self.controlador._numeros_y_barras)
            self.vcmd_decimal_val = toplevel.register(self.controlador._solo_decimal)
        except Exception: # Fallback si no es un toplevel (ej. si el master es el root)
            self.vcmd_num_val = master.register(self.controlador._solo_numeros)
            self.vcmd_fecha_val = master.register(self.controlador._numeros_y_barras)
            self.vcmd_decimal_val = master.register(self.controlador._solo_decimal)

        ctk.CTkLabel(self, text="Gestión de Datos del Alumno", font=FUENTE_TITULO_FORMULARIO, text_color=COLOR_TEXTO_PRINCIPAL).pack(pady=(10, 20), padx=20, anchor="w")

        # Contenedor donde se mostrará la sección actual (se crea antes de instanciar los frames)
        self.contenedor_seccion = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor_seccion.pack(fill="both", expand=False, padx=5, pady=5)

        # Instanciar los frames de sección con el contenedor como master (no empacar aquí)
        self.datos_personales_frame = DatosPersonalesFrame(self.contenedor_seccion, self.vcmd_num_val, self.vcmd_fecha_val)
        self.informacion_academica_frame = InformacionAcademicaFrame(self.contenedor_seccion, self.vcmd_fecha_val, self.vcmd_decimal_val)
        self.sistema_ingreso_frame = SistemaIngresoFrame(self.contenedor_seccion, self.vcmd_num_val)
        self.datos_ubicacion_frame = DatosUbicacionFrame(self.contenedor_seccion, self.vcmd_num_val)

        # Definición de la lista de secciones
        self.secciones = [
            ("Datos Personales", self.datos_personales_frame),
            ("Información Académica", self.informacion_academica_frame),
            ("Sistema de Ingreso", self.sistema_ingreso_frame),
            ("Datos de Ubicación", self.datos_ubicacion_frame)
        ]
        
        # Frame de botones de navegación (se actualiza según sección)
        self.nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.nav_frame.pack(pady=(15, 20))

        # Botones de navegación
        self.btn_anterior = ctk.CTkButton(self.nav_frame, text="Anterior", width=120, command=self.anterior_seccion)
        self.btn_limpiar_seccion = ctk.CTkButton(self.nav_frame, text="Limpiar Campos", width=140, command=self.limpiar_seccion_actual)
        self.btn_siguiente = ctk.CTkButton(self.nav_frame, text="Siguiente", width=140, command=self.siguiente_seccion)
        self.btn_guardar = ctk.CTkButton(self.nav_frame, text="Grabar Datos", width=140, command=self.procesar_formulario,
                                        font=FUENTE_BOTON, fg_color=COLOR_BOTON_PRIMARIO_FG, hover_color=COLOR_BOTON_PRIMARIO_HOVER, text_color=COLOR_BOTON_PRIMARIO_TEXT)

        # Mostrar la primera sección
        self.mostrar_seccion(0)

    def mostrar_seccion(self, index):
        # Ocultar cualquier frame previo dentro del contenedor
        for child in self.contenedor_seccion.winfo_children():
            child.pack_forget()

        self.seccion_actual = max(0, min(index, len(self.secciones) - 1))
        nombre, frame = self.secciones[self.seccion_actual]
        # Empacar el frame correspondiente dentro del contenedor (ya tiene como master al contenedor)
        frame.pack(fill="x", pady=5, padx=5)

        # Actualizar botones según la sección actual
        for widget in self.nav_frame.winfo_children():
            widget.pack_forget()

        # Siempre mostrar limpiar de sección
        self.btn_limpiar_seccion.pack(side="left", padx=8)

        if self.seccion_actual > 0:
            self.btn_anterior.pack(side="left", padx=8)

        if self.seccion_actual < len(self.secciones) - 1:
            self.btn_siguiente.pack(side="left", padx=8)
        else:
            # última sección: mostrar botón de grabar
            self.btn_guardar.pack(side="left", padx=8)

    def siguiente_seccion(self):
        # Validar los campos obligatorios de la sección actual antes de avanzar
        if not self.validar_seccion_actual():
            return
        self.mostrar_seccion(self.seccion_actual + 1)

    def anterior_seccion(self):
        self.mostrar_seccion(self.seccion_actual - 1)

    def limpiar_seccion_actual(self):
        # Limpiar solo los campos de la sección visible
        _, frame = self.secciones[self.seccion_actual]

        # Sección 0: Datos Personales
        if frame is self.datos_personales_frame:
            try:
                self.datos_personales_frame.nro_documento_entry.configure(state="normal")
                self.datos_personales_frame.nro_documento_entry.delete(0, 'end')
                self.datos_personales_frame.nombre_entry.delete(0, 'end')
                self.datos_personales_frame.apellido_entry.delete(0, 'end')
                self.datos_personales_frame.lugar_nac_entry.delete(0, 'end')
                if self.datos_personales_frame.correo_electronico_entry:
                    self.datos_personales_frame.correo_electronico_entry.delete(0, 'end')
                self.datos_personales_frame.limpiar_telefonos()
            except Exception:
                pass

        # Sección 1: Información Académica
        elif frame is self.informacion_academica_frame:
            try:
                self.informacion_academica_frame.tipo_mencion_menu.set("Bachiller")
                self.informacion_academica_frame.tipo_inst_menu.set("Pública")
                self.informacion_academica_frame.institucion_entry.delete(0, 'end')
                self.informacion_academica_frame.titulo_entry.delete(0, 'end')
                try:
                    self.informacion_academica_frame.fecha_grado.set_date("")  # si la clase soporta vaciar
                except Exception:
                    pass
                self.informacion_academica_frame.condicion_menu.set("Regular")
            except Exception:
                pass

        # Sección 2: Sistema de Ingreso
        elif frame is self.sistema_ingreso_frame:
            try:
                self.sistema_ingreso_frame.codigo_entry.configure(state="normal")
                self.sistema_ingreso_frame.codigo_entry.delete(0, 'end')
                self.sistema_ingreso_frame.anio_entry.delete(0, 'end')
            except Exception:
                pass

        # Sección 3: Datos de Ubicación
        elif frame is self.datos_ubicacion_frame:
            try:
                self.datos_ubicacion_frame.estado_entry.delete(0, 'end')
                self.datos_ubicacion_frame.municipio_entry.delete(0, 'end')
                self.datos_ubicacion_frame.parroquia_entry.delete(0, 'end')
                self.datos_ubicacion_frame.sector_entry.delete(0, 'end')
                self.datos_ubicacion_frame.calle_entry.delete(0, 'end')
                self.datos_ubicacion_frame.casa_apart_entry.delete(0, 'end')
                self.datos_ubicacion_frame.var_opcion.set('residencia')
            except Exception:
                pass

    def validar_seccion_actual(self):
        """
        Validaciones mínimas por sección antes de permitir avanzar.
        Si falla retorna False y muestra un mensaje.
        """
        nombre, frame = self.secciones[self.seccion_actual]

        # Sección Datos Personales
        if frame is self.datos_personales_frame:
            tipo = self.datos_personales_frame.tipo_documento_var.get()
            nro = self.datos_personales_frame.nro_documento_entry.get().strip()
            nombre_val = self.datos_personales_frame.nombre_entry.get().strip()
            apellido_val = self.datos_personales_frame.apellido_entry.get().strip()
            correo = ""
            if self.datos_personales_frame.correo_electronico_entry:
                correo = self.datos_personales_frame.correo_electronico_entry.get().strip()

            if tipo.lower().startswith("ced") and not nro:
                messagebox.showwarning("Validación", "El Nro. de Cédula es obligatorio.", parent=self)
                return False
            if tipo.lower().startswith("pas") and not nro:
                messagebox.showwarning("Validación", "El Nro. de Pasaporte es obligatorio.", parent=self)
                return False
            if not nombre_val:
                messagebox.showwarning("Validación", "El Nombre es obligatorio.", parent=self)
                return False
            if not apellido_val:
                messagebox.showwarning("Validación", "El Apellido es obligatorio.", parent=self)
                return False
            if not correo:
                messagebox.showwarning("Validación", "El Correo Electrónico es obligatorio.", parent=self)
                return False
            # correo si existe, validar formato básico
            if correo:
                if "@" not in correo or "." not in correo.split("@")[-1]:
                    messagebox.showwarning("Validación", "El correo electrónico tiene formato inválido.", parent=self)
                    return False
            return True

        # Sección Información Académica
        if frame is self.informacion_academica_frame:
            instit = self.informacion_academica_frame.institucion_entry.get().strip()
            titulo = self.informacion_academica_frame.titulo_entry.get().strip()
            # condición y tipo institución vienen con valores por defecto
            if not instit:
                messagebox.showwarning("Validación", "La Institución es obligatoria.", parent=self)
                return False
            if not titulo:
                messagebox.showwarning("Validación", "El Título obtenido es obligatorio.", parent=self)
                return False
            return True

        # Sección Sistema de Ingreso
        if frame is self.sistema_ingreso_frame:
            codigo = self.sistema_ingreso_frame.codigo_entry.get().strip()
            anio = self.sistema_ingreso_frame.anio_entry.get().strip()
            if not codigo:
                messagebox.showwarning("Validación", "El Código de Ingreso es obligatorio.", parent=self)
                return False
            if not anio:
                messagebox.showwarning("Validación", "El Año de Ingreso es obligatorio.", parent=self)
                return False
            return True

        # Sección Datos Ubicación
        if frame is self.datos_ubicacion_frame:
            estado = self.datos_ubicacion_frame.estado_entry.get().strip()
            municipio = self.datos_ubicacion_frame.municipio_entry.get().strip()
            if not estado:
                messagebox.showwarning("Validación", "El Estado es obligatorio.", parent=self)
                return False
            if not municipio:
                messagebox.showwarning("Validación", "El Municipio es obligatorio.", parent=self)
                return False
            return True

        return True


    def procesar_formulario(self):
        datos = self.controlador.obtener_todos_los_datos(self)
        if self.controlador.modelo.buscar_estudiante(datos['tipo_documento'], datos['nro_documento']):
            messagebox.showerror("Error", f"Documento de identidad '{datos['nro_documento']}' ya registrado.")
        else:
            if self.controlador.validar_campos_obligatorios(datos, self):
                exito = self.controlador.procesar_guardado_estudiante(datos, self)
                if exito:
                    # Limpiar formulario
                    self.controlador.limpiar_formulario_completo(self)
                    # Volver a la primera sección
                    self.mostrar_seccion(0)
                else:
                    pass

    def limpiar_formulario_completo(self):
        self.controlador.limpiar_formulario_completo(self)

    # Formulario de actualizacion
    def ver_datos_completos(self, estudiante, listado_estudiantes=None):
        """
        Muestra una ventana emergente con los datos completos de un estudiante, en formato similar al formulario.
        """
        ventana = ctk.CTkToplevel(self)
        ventana.title("Datos Completos del Estudiante")
        ventana.geometry("850x700") 
        AppConfig().centrar_ventana(ventana, 850, 700)

        ventana.grab_set() # Bloquea la ventana principal

        # Crear un contenedor scrollable para la ventana emergente
        contenedor_scroll = ctk.CTkScrollableFrame(ventana, fg_color=COLOR_FONDO_FORMULARIO)
        contenedor_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        # Instanciando los frames en la ventana emergente
        self.datos_personales_frame = DatosPersonalesFrame(contenedor_scroll, self.vcmd_num_val, self.vcmd_fecha_val)
        self.informacion_academica_frame = InformacionAcademicaFrame(contenedor_scroll, self.vcmd_fecha_val, self.vcmd_decimal_val)
        self.sistema_ingreso_frame = SistemaIngresoFrame(contenedor_scroll, self.vcmd_num_val)
        self.datos_ubicacion_frame = DatosUbicacionFrame(contenedor_scroll, self.vcmd_num_val)

        # Empacar para que se muestren
        self.datos_personales_frame.pack(fill="x", pady=5, padx=5)
        self.informacion_academica_frame.pack(fill="x", pady=5, padx=5)
        self.sistema_ingreso_frame.pack(fill="x", pady=5, padx=5)
        self.datos_ubicacion_frame.pack(fill="x", pady=5, padx=5)

        # Cargar datos y bloquear campos
        #for frame in [self.datos_personales_frame, self.informacion_academica_frame, self.sistema_ingreso_frame, self.datos_ubicacion_frame]:
        #   frame.set_datos(estudiante)
        #     frame.set_estado_campos(modo_lectura=True)
        self.datos_personales_frame.set_datos(estudiante)
        self.datos_ubicacion_frame.set_datos(estudiante)
        self.informacion_academica_frame.set_datos(estudiante)
        self.sistema_ingreso_frame.set_datos(estudiante)

        # Botones
        botones_frame = ctk.CTkFrame(contenedor_scroll, fg_color="transparent")
        botones_frame.pack(pady=10)

        # Botón para actualizar datos
        if estudiante['persona_id']:
            estudiante_id = estudiante['persona_id']
        else:
            estudiante_id = self.controlador.modelo.obtener_id_por_nro_doc(estudiante["documento_identidad"])
            
        self.btn_actualizar = ctk.CTkButton(
            botones_frame, text="Actualizar Datos", state="disabled", command=lambda: self.actualizar_estudiante(estudiante_id,ventana,listado_estudiantes)  # Cambia el comando aquí
        )
        self.btn_actualizar.pack(side="left", padx=10)

        # Botón para editar campos
        ctk.CTkButton(botones_frame, text="Editar Campos", command=self._editar_datos).pack(side="left", padx=10)
        ctk.CTkButton(botones_frame, text="Cerrar", command=ventana.destroy).pack(side="left", padx=10)

    def _editar_datos(self):
        # Cambia el estado de los botones y habilita la edición de los campos
        if self.btn_actualizar is not None:
            self.btn_actualizar.configure(state="normal")
        if self.datos_personales_frame is not None:
            self.datos_personales_frame.habilitar_edicion()
        if self.informacion_academica_frame is not None:
            self.informacion_academica_frame.habilitar_edicion()
        if self.sistema_ingreso_frame is not None:
            self.sistema_ingreso_frame.habilitar_edicion()
        if self.datos_ubicacion_frame is not None:
            self.datos_ubicacion_frame.habilitar_edicion()
            

    def actualizar_estudiante(self, id, ventana, listado_estudiantes):
    
        #Obtener los datos de los frames para actualizarlos
        datos = self.controlador.obtener_todos_los_datos(self)
        
        if self.controlador.validar_campos_obligatorios(datos, self):
            
            exito = self.controlador.cargar_estudiante_para_edicion(id, datos, self)
            if exito:
                #self.controlador.master_controlador.estudiantes.limpiar_formulario_completo(self)
                if listado_estudiantes:
                    listado_estudiantes.mostrar_pagina(True)
                ventana.destroy()
            else:
                pass


