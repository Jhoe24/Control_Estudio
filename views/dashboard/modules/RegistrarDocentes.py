# views/admin/estudiante_form_view.py
import customtkinter as ctk
import tkinter as tk
import tkinter.messagebox as messagebox
from views.dashboard.components.widget_utils import *
from views.dashboard.modules.forms.DatosPersonales import DatosPersonalesFrame
from views.dashboard.modules.forms.DatosUbicacion import DatosUbicacionFrame
from views.dashboard.modules.forms.Docentes.FrameDocente import FrameDocente

from config.app_config import AppConfig
class FormularioDocenteView(ctk.CTkFrame):

    def __init__(self, master, controlador, role_user):
        super().__init__(master, fg_color=COLOR_FONDO_FORMULARIO)
        self.master = master
        self.controlador = controlador
        self.btn_actualizar = None
        
        # Frames de secciones
        self.datos_personales_frame = None
        self.datos_docente_frame = None
        self.datos_ubicacion_frame = None
        self.role_user = role_user

        # lista de secciones e índice actual
        self.secciones = []
        self.seccion_actual = 0
        #self.controlador.master_controlaor.docente.obtener_lista_docentes()
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

        ctk.CTkLabel(self, text="Gestión de Datos de Docente", font=FUENTE_TITULO_FORMULARIO, text_color=COLOR_TEXTO_PRINCIPAL).pack(pady=(10, 20), padx=20, anchor="w")

        self.contenedor_seccion = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor_seccion.pack(fill="both", expand=False, padx=5, pady=5)

        # Instanciar los frames de sección, pasando las validaciones
        self.datos_personales_frame = DatosPersonalesFrame(self.contenedor_seccion, self.vcmd_num_val, self.vcmd_fecha_val)
        self.datos_docente_frame = FrameDocente(self.contenedor_seccion, self.vcmd_num_val, self.vcmd_fecha_val)
        self.datos_ubicacion_frame = DatosUbicacionFrame(self.contenedor_seccion, self.vcmd_num_val)

        self.secciones = [
            ("Datos Personales", self.datos_personales_frame),
            ("Datos Docente", self.datos_docente_frame),
            ("Datos de Ubicación", self.datos_ubicacion_frame)
        ]

        # Navegación (botones reutilizables)
        self.nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.nav_frame.pack(pady=(15,20))

        self.btn_anterior = ctk.CTkButton(self.nav_frame, text="Anterior", width=120, command=self.anterior_seccion)
        self.btn_limpiar_seccion = ctk.CTkButton(self.nav_frame, text="Limpiar Campos", width=140, command=self.limpiar_seccion_actual)
        self.btn_siguiente = ctk.CTkButton(self.nav_frame, text="Siguiente", width=140, command=self.siguiente_seccion)
        self.btn_guardar = ctk.CTkButton(self.nav_frame, text="Grabar Datos", width=140, command=self.procesar_formulario,
                                         font=FUENTE_BOTON, fg_color=COLOR_BOTON_PRIMARIO_FG, hover_color=COLOR_BOTON_PRIMARIO_HOVER, text_color=COLOR_BOTON_PRIMARIO_TEXT)

        # Mostrar primera sección
        self.mostrar_seccion(0)
    def mostrar_seccion(self, index):
        # ocultar hijos previos del contenedor para evitar superposición
        for child in self.contenedor_seccion.winfo_children():
            child.pack_forget()

        self.seccion_actual = max(0, min(index, len(self.secciones)-1))
        _, frame = self.secciones[self.seccion_actual]
        frame.pack(fill="x", pady=5, padx=5)

        # actualizar botones
        for w in self.nav_frame.winfo_children():
            w.pack_forget()

        self.btn_limpiar_seccion.pack(side="left", padx=8)
        if self.seccion_actual > 0:
            self.btn_anterior.pack(side="left", padx=8)
        if self.seccion_actual < len(self.secciones)-1:
            self.btn_siguiente.pack(side="left", padx=8)
        else:
            self.btn_guardar.pack(side="left", padx=8)

    def siguiente_seccion(self):
        if not self.validar_seccion_actual():
            return
        self.mostrar_seccion(self.seccion_actual + 1)

    def anterior_seccion(self):
        self.mostrar_seccion(self.seccion_actual - 1)

    def limpiar_seccion_actual(self):
        _, frame = self.secciones[self.seccion_actual]

        if frame is self.datos_personales_frame:
            try:
                self.datos_personales_frame.nro_documento_entry.configure(state="normal")
                self.datos_personales_frame.nro_documento_entry.delete(0,'end')
                self.datos_personales_frame.nombre_entry.delete(0, 'end')
                self.datos_personales_frame.apellido_entry.delete(0, 'end')
                self.datos_personales_frame.lugar_nac_entry.delete(0, 'end')
                if self.datos_personales_frame.correo_electronico_entry:
                    self.datos_personales_frame.correo_electronico_entry.delete(0, 'end')
                self.datos_personales_frame.limpiar_telefonos()
            except Exception:
                pass

        elif frame is self.datos_docente_frame:
            try:
                # limpiar campos del frame docente según su API pública
                self.datos_docente_frame.limpiar_campos()
            except Exception:
                # si no existe método, intentar limpiar campos conocidos
                try:
                    for attr in ("titulo_entry","especialidad_entry", "categoria_entry","registro_entry"):
                        w = getattr(self.datos_docente_frame, attr, None)
                        if w:
                            w.delete(0,'end')
                except Exception:
                    pass

        elif frame is self.datos_ubicacion_frame:
            try:
                self.datos_ubicacion_frame.estado_entry.delete(0,'end')
                self.datos_ubicacion_frame.municipio_entry.delete(0,'end')
                self.datos_ubicacion_frame.parroquia_entry.delete(0,'end')
                self.datos_ubicacion_frame.sector_entry.delete(0,'end')
                self.datos_ubicacion_frame.calle_entry.delete(0,'end')
                self.datos_ubicacion_frame.casa_apart_entry.delete(0,'end')
                self.datos_ubicacion_frame.var_opcion.set('residencia')
            except Exception:
                pass

    def validar_seccion_actual(self):
        _, frame = self.secciones[self.seccion_actual]

        # validar Datos Personales (tipo/nro, nombre, apellido)
        if frame is self.datos_personales_frame:
            tipo = self.datos_personales_frame.tipo_documento_var.get()
            nro = self.datos_personales_frame.nro_documento_entry.get().strip()
            nombre = self.datos_personales_frame.nombre_entry.get().strip()
            apellido = self.datos_personales_frame.apellido_entry.get().strip()
            correo = ""
            if self.datos_personales_frame.correo_electronico_entry:
                correo = self.datos_personales_frame.correo_electronico_entry.get().strip()

            if tipo.lower().startswith("ced") and not nro:
                messagebox.showwarning("Validación", "El Nro. de Cédula es obligatorio.", parent=self)
                return False
            if not nombre:
                messagebox.showwarning("Validación", "El Nombre es obligatorio.", parent=self)
                return False
            if not apellido:
                messagebox.showwarning("Validación", "El Apellido es obligatorio.", parent=self)
                return False
            if not correo:
                messagebox.showwarning("Validación", "El Correo Electrónico es obligatorio.", parent=self)
                return False
            # correo si existe, validar formato básico
            if correo:
                if "@" not in correo or "." not in correo.split("@")[-1]:
                    messagebox.showwarning("Validación", "El Correo Electrónico no tiene un formato válido.", parent=self)
                    return False
            return True

        # validar Datos Docente (ejemplo: al menos campo de profesión obligatorio)
        if frame is self.datos_docente_frame:
            try:
                profesion = getattr(self.datos_docente_frame, "profesion_entry", None)
                if profesion:
                    if not profesion.get().strip():
                        messagebox.showwarning("Validación", "La profesión es obligatoria.", parent=self)
                        return False
            except Exception:
                pass
            return True

        # validar Datos de Ubicación (estado y municipio)
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
        resultado = self.controlador.obtener_todos_los_datos(self)

        # Evitar duplicados (misma lógica que en el formulario de estudiantes)
        existe = False
        try:
            if hasattr(self.controlador, "modelo") and hasattr(self.controlador.modelo, "buscar_docente"):
                existe = self.controlador.modelo.buscar_docente(resultado.get('tipo_documento'), resultado.get('nro_documento'))
            elif hasattr(self.controlador, "modelo") and hasattr(self.controlador.modelo, "buscar_estudiante"):
                existe = self.controlador.modelo.buscar_estudiante(resultado.get('tipo_documento'), resultado.get('nro_documento'))
        except Exception as e:
            print("Warning: error comprobando duplicado:", e)
            existe = False

        if existe:
            messagebox.showerror("Error", f"Documento de identidad '{resultado.get('nro_documento')}' ya registrado.", parent=self)
            return

        # Validación final y registro
        if not self.controlador.validar_campos_obligatorios(resultado, self):
            return

        exito = None
        try:
            exito = self.controlador.registrar_docente(resultado, self)
        except Exception as e:
            print("Error en controlador.registrar_docente:", e)
            messagebox.showerror("Error", "Ocurrió un error al registrar. Revisa la consola.", parent=self)
            return

        # Asegurarse de que el controlador indique éxito (True) para proceder
        if exito:
            # Limpiar formulario y volver a la primera sección (Datos Personales)
            try:
                self.controlador.limpiar_formulario_completo(self)
            except Exception as e:
                print("Warning: limpiar_formulario_completo falló:", e)
            self.mostrar_seccion(0)
        else:
            # Mostrar mensaje para saber por qué falló (el controlador debería detallar)
            print("registrar_docente devolvió:", exito)
            messagebox.showerror("Error", "No se pudo registrar el docente. Revisa mensajes del controlador.", parent=self)

    # sFormulario de actualizacion
    def ver_datos_completos(self, docente, role_user):
        """
        Muestra una ventana emergente con los datos completos de un docente, en formato similar al formulario.
        """
        ventana = ctk.CTkToplevel(self)
        ventana.title("Datos Completos del Docente")
        ventana.geometry("850x700") 
        AppConfig().centrar_ventana(ventana, 850, 700)

        ventana.grab_set() # Bloquea la ventana principal

        # Crear un contenedor scrollable para la ventana emergente
        contenedor_scroll = ctk.CTkScrollableFrame(ventana, fg_color=COLOR_FONDO_FORMULARIO)
        contenedor_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        # Instanciando los frames en la ventana emergente
        self.datos_personales_frame = DatosPersonalesFrame(contenedor_scroll, self.vcmd_num_val, self.vcmd_fecha_val)
        self.datos_docente_frame = FrameDocente(contenedor_scroll, self.vcmd_num_val, self.vcmd_fecha_val)
        self.datos_ubicacion_frame = DatosUbicacionFrame(contenedor_scroll, self.vcmd_num_val)

        # Empacar para que se muestren
        self.datos_personales_frame.pack(fill="x", pady=5, padx=5)
        self.datos_ubicacion_frame.pack(fill="x", pady=5, padx=5)

        # Cargar datos y bloquear campos
        #for frame in [self.datos_personales_frame, self.informacion_academica_frame, self.sistema_ingreso_frame, self.datos_ubicacion_frame]:
        #   frame.set_datos(estudiante)
        #     frame.set_estado_campos(modo_lectura=True)
        self.datos_personales_frame.set_datos(docente)
        self.datos_docente_frame.set_datos(docente)
        self.datos_ubicacion_frame.set_datos(docente)

        # Botones
        botones_frame = ctk.CTkFrame(contenedor_scroll, fg_color="transparent")
        botones_frame.pack(pady=10)

        # Botón para actualizar datos
        docente_id = docente['persona_id']
        if role_user.lower() == "coord_pnf":
            ctk.CTkButton(botones_frame, text="Cerrar", command=ventana.destroy).pack(side="left", padx=10)
        else:
            self.btn_actualizar = ctk.CTkButton(
                botones_frame, text="Actualizar Datos", state="disabled", command=lambda: self.actualizar_docente(docente_id,ventana)  # Cambia el comando aquí
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
        if self.datos_docente_frame is not None:
            self.datos_docente_frame.habilitar_edicion()
        if self.datos_ubicacion_frame is not None:
            self.datos_ubicacion_frame.habilitar_edicion()
    
    def actualizar_docente(self, id, ventana):
        # Obtener los datos de los frames para actualizarlos
        datos = self.controlador.obtener_todos_los_datos(self)
        if self.controlador.validar_campos_obligatorios(datos, self):
            exito = self.controlador.cargar_docente_edicion(id, datos, self)
            if exito:
                ventana.destroy()
            else:
                pass
