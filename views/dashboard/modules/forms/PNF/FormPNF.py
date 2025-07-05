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
       
        self.dict_trayectos = {
            "I": 1,
            "II": 2,
            "III": 3,
            "IV": 4,
            "V": 5
        }
        self.dict_trayectos_invertido = {
            1: "I",
            2: "II",
            3: "III",
            4: "IV",
            5: "V"
        }

        self.fecha_resolucion = None  # Inicializar la variable fecha_resolucion
        self.cal = None
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
        self.var_cantidad_trayectos = ctk.StringVar(value="I")  # Valor por defecto para trayectos
        self.var_cantidad_tramos = ctk.StringVar(value="I")

        self.label_trayectos = ctk.CTkLabel(self.duracion_contenedor, text="Trayectos",text_color=COLOR_TEXTO_PRINCIPAL, font=("Arial", 12, "bold"))
        self.label_trayectos.pack(side="left", padx=(0, 15))

        self.duracion_trayectos_entry = crear_option_menu(
            self.duracion_contenedor,
            width=40,
            values=["I", "II", "III", "IV", "V"],
            variable=self.var_cantidad_trayectos,
            command=self.on_trayecto_selected
            
        )
        self.duracion_trayectos_entry.pack(side="left", padx=(0, 10))

        self.label_tramos = ctk.CTkLabel(self.duracion_contenedor, text="Tramos",text_color=COLOR_TEXTO_PRINCIPAL, font=("Arial", 12, "bold"))
        self.label_tramos.pack(side="left", padx=(0, 15))
        self.duracion_tramos_entry = crear_option_menu(
            self.duracion_contenedor,
            width=40,
            values=["I", "II", "III"],
            variable=self.var_cantidad_tramos,
            #command=self.on_trayecto_selected
            
        )
        self.duracion_tramos_entry.pack(side="left", padx=(0, 10))

        self.label_semanas = ctk.CTkLabel(self.duracion_contenedor, text="Semanas", text_color=COLOR_TEXTO_PRINCIPAL, font=("Arial", 12, "bold"))
        self.label_semanas.pack(side="left", padx=(0, 15))

        self.duracion_semanas_entry = crear_option_menu(
            self.duracion_contenedor,
            width=40,
            values=['12', '16', '20', '24', '28', '32', '36', '40', '44', '48'],
            command=lambda v: setattr(self.duracion_semanas_entry, '_current_value', v)
        )
        self.duracion_semanas_entry.pack(side="left")

        self.label_creditos = ctk.CTkLabel(self.duracion_contenedor, text=" Créditos", text_color=COLOR_TEXTO_PRINCIPAL, font=("Arial", 12, "bold"))
        self.label_creditos.pack(side="left", padx=(0, 15))

        self.duracion_creditos_entry = crear_entry(
            self.duracion_contenedor,
            width=100,
            placeholder_text="Duración Créditos",
            validate="key",
            validatecommand=(self.vcmd_num, '%S')  # Validación para solo números

        )
        self.duracion_creditos_entry.pack(side="left", padx=(0, 10))

        self.label_horas = ctk.CTkLabel(self.duracion_contenedor, text="Horas", text_color=COLOR_TEXTO_PRINCIPAL, font=("Arial", 12, "bold"))
        self.label_horas.pack(side="left", padx=(0, 15))

        self.duracion_horas_entry = crear_entry(
            self.duracion_contenedor,
            width=100,
            placeholder_text="Duración Horas",
            validate="key",
            validatecommand=(self.vcmd_num, '%S')  # Validación para solo números
        )
        self.duracion_horas_entry.pack(side="left")

       
        # --- Fila para datos del PNF ---
        self._crear_fila_widgets([
            ('Titulo a Otorgar:', crear_entry, {"width":300,"placeholder_text":"Ingrese titulo"}, 1, self, 'titulo_otorga_entry'),
            ("Perfil Egresado:", crear_entry, {"width":300,"placeholder_text":"Ingrese perfil del egresado"}, 1, self, 'perfil_egreso_entry'),
            #("Campo Ocupacional:", crear_entry, {"width":300,"placeholder_text":"Ingrese campo ocupacional"}, 1, self, 'campo_ocupacional_entry'),
        ])

        self.registrar_fecha(self.set_fecha_resolucion,"Fecha Resolución")  # Registrar la fecha de resolución
        #label para mostrar la fecha de resolución
        self.fecha_resolucion_label = ctk.CTkLabel(self, text="Fecha de Resolución: No seleccionada", text_color=COLOR_TEXTO_PRINCIPAL, font=("Arial", 14, "bold"))
        self.fecha_resolucion_label.pack(pady=(10, 0), padx=10, anchor="w")
        # Actualizar el label de fecha de resolución cuando se seleccione una fecha

        # --- Fila para datos del pensum ---

        self._crear_fila_widgets([
            ("Versión del Pensum:", crear_entry, {"width":300,"placeholder_text":"Ingrese versión"}, 1, self, 'version_pensum_entry'),
            ("Estado:", crear_option_menu, {"values":["activo", "anactivo", "revision"], "command": lambda v: setattr(self.estado_menu, '_current_value',v)}, 1, self, 'estado_menu')
        ])
        
        self.entries_a_validar = [
            self.codigo_entry,
            self.codigo_nacional_entry,
            self.nombre_entry,
            self.siglas_entry,
            self.area_conocimiento_entry,
            self.duracion_creditos_entry,
            self.duracion_horas_entry,
            self.titulo_otorga_entry,
            self.perfil_egreso_entry,
            self.version_pensum_entry,
        ]

    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets

    def registrar_fecha(self,callback,titulo_btn="Seleccionar Fecha"):
       
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

    def solo_numeros(self, char_input):
        """Validación para permitir solo números en los campos de entrada."""
        return char_input.isdigit()

    def on_trayecto_selected(self, value):
      
        print("Seleccion: ", value)
        #print("Fecha Resolución: ", self.fecha_resolucion)
    
    def get_trayecto(self):
        """Obtener el valor del trayecto seleccionado."""
        self.dict_trayectos = {
            "I": 1,
            "II": 2,
            "III": 3,
            "IV": 4,
            "V": 5
        }
        return self.dict_trayectos.get(self.var_cantidad_trayectos.get(), 1)
    
    #Crear un método para establecer la fecha de resolución
    def set_fecha_resolucion(self,fecha):
        if fecha:
            self.fecha_resolucion = fecha
            print("Fecha de resolución establecida:", self.fecha_resolucion)
            self.fecha_resolucion_label.configure(text=f"Fecha de Resolución: {self.fecha_resolucion}")
            # Llama a la validación en el formulario principal
            if hasattr(self.master, "validar_campos_trayecto"):
                self.master.validar_campos_trayecto()

    def deshabilitar_campos(self):
        # Deshabilita todos los entries a validar
        for entry in self.entries_a_validar:
            entry.configure(state="disabled")
        # Deshabilita los OptionMenu si los tienes (ejemplo)
        self.tipo_pnf_menu.configure(state="disabled")
        self.duracion_trayectos_entry.configure(state="disabled")
        self.duracion_semanas_entry.configure(state="disabled")
        self.estado_menu.configure(state="disabled")
        # Deshabilita el botón de fecha
        self.btn_fecha.configure(state="disabled")
        # Deshabilita el botón de grabar Trayecto
        if hasattr(self.master, 'button_siguiente'):
            self.master.button_siguiente.configure(state="disabled")
    
    def set_datos(self, datos):
        self.codigo_entry.insert(0, datos.get("codigo", ""))
        self.codigo_entry.configure(state="disabled")

        self.codigo_nacional_entry.insert(0, datos.get("codigo_nacional", ""))
        self.codigo_nacional_entry.configure(state="disabled")

        self.nombre_entry.insert(0, datos.get("nombre", ""))
        self.nombre_entry.configure(state="disabled")

        self.siglas_entry.insert(0, datos.get("nombre_corto", ""))
        self.siglas_entry.configure(state="disabled")
        
        self.var_tipo_pnf.set(datos.get("nivel", "TSU"))
        self.tipo_pnf_menu.configure(state="disabled")

        self.area_conocimiento_entry.insert(0, datos.get("area_conocimiento", ""))
        self.area_conocimiento_entry.configure(state="disabled")

        self.duracion_semanas_entry.set(str(datos.get("duracion_semanas", "")))
        self.duracion_semanas_entry.configure(state="disabled")

        horas_credito_str = str(datos.get("total_creditos", "")) if datos.get("total_creditos") is not None else "0"
        self.duracion_creditos_entry.insert(0, horas_credito_str)
        self.duracion_creditos_entry.configure(state="disabled")

        self.duracion_horas_entry.insert(0, str(datos.get("total_horas", "")))
        self.duracion_horas_entry.configure(state="disabled")

        # Si tienes modalidad, puedes agregarlo aquí si tienes un campo correspondiente
        self.titulo_otorga_entry.insert(0, datos.get("titulo_otorga", ""))
        self.titulo_otorga_entry.configure(state="disabled")

        self.perfil_egreso_entry.insert(0, datos.get("perfil_egreso", ""))
        self.perfil_egreso_entry.configure(state="disabled")

        self.version_pensum_entry.insert(0, datos.get("version_pensum", ""))
        self.version_pensum_entry.configure(state="disabled")

        self.estado_menu.set(datos.get("estado", "activo"))
        self.estado_menu.configure(state="disabled")

        # Fecha de resolución
        if "fecha_resolucion" in datos and datos["fecha_resolucion"]:
            self.set_fecha_resolucion(datos["fecha_resolucion"])
        self.btn_fecha.configure(state="disabled")

        cantidad = self.dict_trayectos_invertido[len(datos["lista_trayectos"])]
        if cantidad:
            self.var_cantidad_trayectos.set(cantidad)
            self.duracion_trayectos_entry.configure(state="disabled")
        
        for trayecto in datos["lista_trayectos"]:
            if trayecto["lista_tramos"]:
                cantidad_tramos = len(trayecto["lista_tramos"])
                break

        self.var_cantidad_tramos.set(self.dict_trayectos_invertido[cantidad_tramos])
        self.duracion_tramos_entry.configure(state="disabled")



    def habilitar_campos(self):
        for campo in self.entries_a_validar:
            campo.configure(state="normal")
            self.duracion_trayectos_entry.configure(state="normal")
            self.duracion_semanas_entry.configure(state="normal")
            self.btn_fecha.configure(state="normal")
            self.estado_menu.configure(state="normal")
            self.tipo_pnf_menu.configure(state="normal")
            self.duracion_tramos_entry.configure("normal")
           
        # Habilitar el botón de grabar Trayecto si existe
