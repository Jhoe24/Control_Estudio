import customtkinter as ctk
#import tkinter.messagebox as messagebox
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase
#from controllers.dashboard.PNF.controller_pnf import ControllerPNF

from ..DatosPersonales import DatosPersonalesFrame

class FrameTramos(SectionFrameBase):
    def __init__(self, master,controlador, vcmd_num, vcmd_fecha, titulo = "Datos Tramos"):
        super().__init__(master, titulo)
        self.controlador = controlador
        self.vcmd_num = vcmd_num # Guardar para usar en números
        self.vcmd_fecha = vcmd_fecha # Guardar para usar en fechas
        
        # -- Fila de Datos del Tramo --
        self._crear_fila_widgets([
            ("Número:", crear_entry, {"width":300,"placeholder_text":"Ingrese número"}, 1, self, 'numero_entry'),
            ("Nombre:", crear_entry, {"width":360,"placeholder_text":"Ingrese nombre"}, 1, self, 'nombre_entry'),
        ])

        # -- Fila de Duración --
        self._crear_fila_widgets([
            ("Duración en semanas:", crear_entry, {"width":300,"placeholder_text":"Ingrese duración"}, 1, self, 'duracion_semanas_entry'),
            ("Duración en horas:", crear_entry, {"width":300,"placeholder_text":"Ingrese duración"}, 1, self, 'duracion_horas_entry'),
        ])

        # -- Fila de información adicional --
        self._crear_fila_widgets([
            ("Créditos:", crear_entry, {"width":300,"placeholder_text":"Ingrese créditos"}, 1, self, 'creditos_entry'),
            ("Objetivos:", crear_entry, {"width":300,"placeholder_text":"Ingrese objetivos"}, 1, self, 'objetivos_entry'),
            ("Estado:", crear_option_menu, {"values": ["activo", "inactivo"], "width":300}, 1, self, 'estado_option_menu')
        ])

        self.entries_a_validar = [
            self.numero_entry,
            self.nombre_entry,
            self.duracion_semanas_entry,
            self.duracion_horas_entry,
            self.creditos_entry,
            self.objetivos_entry,
            self.estado_option_menu,
        ]

        # Bind para validar campos al escribir
        for entry in self.entries_a_validar:
            entry.bind("<KeyRelease>", lambda event: self.validar_campos_tramo())


    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets

    def procesar_tramo(self):
        return self.controlador.getTramos(self)
    
    
    def validar_campos_tramo(self):
        todos_llenos = all(str(entry.get()).strip() for entry in self.entries_a_validar)
        # Notifica al padre (FrameTrayecto) para que valide el botón global
        if hasattr(self.master.master, "validar_campos_tramos_global"):
            self.master.master.validar_campos_tramos_global()   


    def set_datos(self, datos):
        # Primero habilitar todos los campos
        self.habilitar_campos()
        
        # Limpiar campos antes de insertar nuevos datos
        self.limpiar_campos()
        
        # Insertar los nuevos datos de forma segura
        self._insertar_dato_seguro(self.numero_entry, datos.get("numero", ""))
        self._insertar_dato_seguro(self.nombre_entry, datos.get("nombre", ""))
        self._insertar_dato_seguro(self.duracion_semanas_entry, datos.get("duracion_semanas", ""))
        self._insertar_dato_seguro(self.duracion_horas_entry, datos.get("duracion_horas", ""))
        self._insertar_dato_seguro(self.creditos_entry, datos.get("creditos", ""))
        self._insertar_dato_seguro(self.objetivos_entry, datos.get("objetivos", ""))
        self.estado_option_menu.set(datos.get("estado", "activo"))
        
        # Si tienes un campo para competencias, agrégalo aquí
        if hasattr(self, "competencias_entry"):
            self._insertar_dato_seguro(self.competencias_entry, datos.get("competencias", ""))
        
        # Después deshabilitar los campos (excepto el número que ya está deshabilitado)
        for campo in self.entries_a_validar:
            if campo != self.numero_entry:  # No deshabilitar el número si ya está deshabilitado
                campo.configure(state="disabled")

    def _insertar_dato_seguro(self, entry, valor):
        """Inserta un valor en un entry de forma segura"""
        try:
            # Asegurarse de que el entry esté habilitado
            if str(entry.cget("state")) == "disabled":
                entry.configure(state="normal")
            
            # Insertar el valor
            entry.insert(0, str(valor))
            
        except Exception as e:
            print(f"Error al insertar dato en entry: {e}")
            # Intentar habilitar y volver a insertar
            try:
                entry.configure(state="normal")
                entry.insert(0, str(valor))
            except Exception as e2:
                print(f"Error crítico al insertar dato: {e2}")

    def limpiar_campos(self):
        """Limpia todos los campos de entrada"""
        for entry in self.entries_a_validar:
            if hasattr(entry, 'delete'):
                entry.delete(0, 'end')
            elif hasattr(entry, 'set'):
                entry.set("")
    
    def habilitar_campos(self):
        for campo in self.entries_a_validar:
            campo.configure(state="normal")
        self.numero_entry.configure(state="disabled")  # Habilita el campo de número