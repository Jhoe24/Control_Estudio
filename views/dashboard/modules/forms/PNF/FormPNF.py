import customtkinter as ctk
import tkinter.messagebox as messagebox
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase

from ..DatosPersonales import DatosPersonalesFrame

class DatosPNFPensumFrame(SectionFrameBase):
    def __init__(self, master, vcmd_num, vcmd_fecha):
        super().__init__(master, header_text="Datos de PNF y Pensum")
        self.tipo_documento_var = ctk.StringVar(value="cedula") # Valor por defecto: Cédula
        self.vcmd_num = self.register(self.solo_numeros) 
        self.vcmd_fecha = vcmd_fecha # Guardar para usar en fechas
        self.lista_telefonos = [] # Lista para guardar los teléfonos
        
        # --- Fila para codigo del PNF ---
        self._crear_fila_widgets([
            ("Código:", crear_entry, {"width":300,"placeholder_text":"Ingrese código"}, 1, self, 'codigo_entry'),
            ("Código Nacional:", crear_entry, {"width":300,"placeholder_text":"Ingrese código nacional"}, 1, self, 'codigo_nacional_entry')
        ])

        # --- Fila para nombre del PNF ---
        self._crear_fila_widgets([
            ("Nombre del PNF:", crear_entry, {"width":300,"placeholder_text":"Ingrese nombre"}, 1, self, 'nombre_entry'),
            ("Siglas:", crear_entry, {"width":300,"placeholder_text":"Ingrese siglas"}, 1, self, 'siglas_entry')
        ])

        # --- Fila para tipo de PNF ---
        self.var_tipo_pnf = ctk.StringVar(value='TSU')
        self._crear_fila_widgets([
            ("Tipo de PNF:", crear_option_menu, {
                "values": ["TSU", "Ingeniería", "Especialización", "Licenciatura", "Medicina"],
                'variable': self.var_tipo_pnf,
                "command": lambda v: setattr(self.tipo_pnf_menu, '_current_value', v)
            }, 1, self, 'tipo_pnf_menu')
        ])

        # --- Fila para area de conocimiento ---
        self._crear_fila_widgets([
            ('Área de Conocimiento:', crear_entry, {"width":300,"placeholder_text":"Ingrese área de conocimiento"}, 1, self, 'area_conocimiento_entry')
        ])

        # 1. Crear el frame contenedor
        self.duracion_contenedor = ctk.CTkFrame(self,fg_color="transparent")
        self.duracion_contenedor.pack(fill="x", pady=10, padx=10)

        # 2. Crear el label dentro del frame
        self.label_duracion_contenedor = ctk.CTkLabel(
            self.duracion_contenedor,
            text="Duración del PNF:",
            text_color=COLOR_TEXTO_PRINCIPAL,
            font=("Arial", 14, "bold")
        )
        self.label_duracion_contenedor.pack(anchor="w", pady=(0, 5))

        # 3. Crear los entries dentro del mismo frame
        self.label_trayectos = ctk.CTkLabel(self.duracion_contenedor, text="Trayectos",text_color=COLOR_TEXTO_PRINCIPAL, font=("Arial", 12, "bold"))
        self.label_trayectos.pack(side="left", padx=(0, 15))
        self.duracion_trayectos_entry = crear_entry(
            self.duracion_contenedor,
            width=180,
            placeholder_text="Duración Trayectos",
            validate="key",
            validatecommand=(self.vcmd_num, '%S')  # Validación para solo números

        )
        self.duracion_trayectos_entry.pack(side="left", padx=(0, 10))

        self.label_semanas = ctk.CTkLabel(self.duracion_contenedor, text="Semanas", text_color=COLOR_TEXTO_PRINCIPAL, font=("Arial", 12, "bold"))
        self.label_semanas.pack(side="left", padx=(0, 15))

        self.duracion_semanas_entry = crear_entry(
            self.duracion_contenedor,
            width=180,
            placeholder_text="Duración Semanas",
            validate="key",
            validatecommand=(self.vcmd_num, '%S')  # Validación para solo números
        )
        self.duracion_semanas_entry.pack(side="left")

        self.label_creditos = ctk.CTkLabel(self.duracion_contenedor, text="Créditos", text_color=COLOR_TEXTO_PRINCIPAL, font=("Arial", 12, "bold"))
        self.label_creditos.pack(side="left", padx=(0, 15))
        self.duracion_creditos_entry = crear_entry(
            self.duracion_contenedor,
            width=180,
            placeholder_text="Duración Créditos",
            validate="key",
            validatecommand=(self.vcmd_num, '%S')  # Validación para solo números

        )
        self.duracion_creditos_entry.pack(side="left", padx=(0, 10))

        self.label_horas = ctk.CTkLabel(self.duracion_contenedor, text="Horas", text_color=COLOR_TEXTO_PRINCIPAL, font=("Arial", 12, "bold"))
        self.label_horas.pack(side="left", padx=(0, 15))

        self.duracion_horas_entry = crear_entry(
            self.duracion_contenedor,
            width=180,
            placeholder_text="Duración Horas",
            validate="key",
            validatecommand=(self.vcmd_num, '%S')  # Validación para solo números
        )
        self.duracion_horas_entry.pack(side="left")

        self.modalidad_var = ctk.StringVar(value="Presencial")  # Valor por defecto: Presencial
        
        # --- Fila para modalidad del PNF ---
        self._crear_fila_widgets([
            ("Modalidad:", crear_option_menu, {
                "values": ["Virtual", "Mixta"],
                'variable': self.modalidad_var,
                "command": lambda v: setattr(self.modalidad_menu, '_current_value', v)
            }, 1, self, 'modalidad_menu')
        ])
        # --- Fila para datos del PNF ---
        self._crear_fila_widgets([
            ('Titulo a Otorgar:', crear_entry, {"width":300,"placeholder_text":"Ingrese titulo"}, 1, self, 'titulo_otorga_entry'),
            ("Perfil Egresado:", crear_entry, {"width":300,"placeholder_text":"Ingrese perfil del egresado"}, 1, self, 'perfil_egreso_entry'),
            ("Campo Ocupacional:", crear_entry, {"width":300,"placeholder_text":"Ingrese campo ocupacional"}, 1, self, 'campo_ocupacional_entry'),
            ("Resolución - Creación:", crear_entry, {"width":300,"placeholder_text":"Ingrese resolución"}, 1, self, 'resolucion_entry'),
            ("Fecha Resolución:", crear_entry, {"width":300, "placeholder_text": "dd-mm-aaaa", "validatecommand": (self.vcmd_fecha, '%S')}, 1, self, 'fecha_resolucion_entry'),
            ('Fecha de Creación:', crear_entry, {"width":300, "placeholder_text": "dd-mm-aaaa", "validatecommand": (self.vcmd_fecha, '%S')}, 1, self, 'fecha_creacion_entry'),
            ("Fecha de Actualización:", crear_entry, {"width":300, "placeholder_text": "dd-mm-aaaa", "validatecommand": (self.vcmd_fecha, '%S')}, 1, self, 'fecha_actualizacion_entry'),
        ])
        # --- Fila para datos del pensum ---
        self._crear_fila_widgets([
            ("Versión del Pensum:", crear_entry, {"width":300,"placeholder_text":"Ingrese versión"}, 1, self, 'version_pensum_entry'),
            ("Coordinador Nacional:", crear_entry, {"width":300,"placeholder_text":"Ingrese nombre del coordinador"}, 1, self, 'coordinador_nacional_entry'),
            ("Estado:", crear_entry, {"width":300,"placeholder_text":"Ingrese estado"}, 1, self, 'estado_entry'),
        ])

    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets

    def solo_numeros(self, char_input):
        """Validación para permitir solo números en los campos de entrada."""
        return char_input.isdigit()