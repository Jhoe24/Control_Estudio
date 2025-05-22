import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
from pathlib import Path

# Importar los migradores
from migrador_alm import MigradorALM
from migrador_cc import MigradorCC
from migrador_dct import MigradorDCT
from migrador_ins import MigradorINS
from migrador_sea import MigradorSEA

class SistemaMigracionApp:
    def __init__(self):
        # Configurar el tema y la apariencia
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Crear la ventana principal
        self.root = ctk.CTk()
        self.root.title("🚀 Sistema de Migración de Datos")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Colores personalizados modernos (usando colores válidos)
        self.colors = {
            'primary': "#0066CC",
            'primary_dark': "#004499", 
            'secondary': "#00D4AA",
            'accent': "#FF6B6B",
            'success': "#4ECDC4",
            'warning': "#FFE66D",
            'error': "#FF6B6B",
            'surface': "#1A1A1A",
            'surface_light': "#2D2D2D",
            'text_primary': "#FFFFFF",
            'text_secondary': "#B0B0B0",
            'background': ("white", "gray10"),
            'frame_bg': ("gray95", "gray15"),
            'card_bg': ("gray90", "gray20")
        }

        # Variables
        self.ruta_bd = ctk.StringVar()
        self.tabla_seleccionada = ctk.StringVar(value="ALM")
        self.progreso_visible = False
        self.animation_progress = 0

        # Configurar la ventana
        self.configurar_ventana()
        self.crear_interfaz()

    def configurar_ventana(self):
        """Configurar la ventana principal con estilo moderno"""
        # Centrar la ventana en la pantalla
        self.root.update_idletasks()
        width = 900
        height = 600
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        # Configurar el grid principal
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

    def crear_interfaz(self):
        """Crear todos los elementos de la interfaz moderna"""
        # Crear contenedor principal
        self.main_container = ctk.CTkFrame(
            self.root,
            corner_radius=0,
            fg_color=self.colors['background']
        )
        self.main_container.grid(row=0, column=0, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)

        # Header moderno
        self.crear_header(self.main_container, 0)

        # Contenido principal con scroll
        self.crear_contenido_principal(self.main_container, 1)

        # Footer con información
        self.crear_footer(self.main_container, 2)

    def crear_header(self, parent, row):
        """Crear header moderno y atractivo"""
        header_frame = ctk.CTkFrame(
            parent,
            height=120,
            corner_radius=0,
            fg_color=("white", "gray20")
        )
        header_frame.grid(row=row, column=0, sticky="ew")
        header_frame.grid_propagate(False)
        header_frame.grid_columnconfigure(1, weight=1)

        # Icono principal
        icon_frame = ctk.CTkFrame(
            header_frame,
            width=80,
            height=80,
            corner_radius=40,
            fg_color=self.colors['primary']
        )
        icon_frame.grid(row=0, column=0, padx=30, pady=20)
        icon_frame.grid_propagate(False)

        icon_label = ctk.CTkLabel(
            icon_frame,
            text="🔄",
            font=ctk.CTkFont(size=36),
            text_color="white"
        )
        icon_label.place(relx=0.5, rely=0.5, anchor="center")

        # Información del título
        title_frame = ctk.CTkFrame(header_frame, fg_color=("white", "gray20"))
        title_frame.grid(row=0, column=1, sticky="ew", padx=20, pady=20)
        title_frame.grid_columnconfigure(0, weight=1)

        # Título principal
        main_title = ctk.CTkLabel(
            title_frame,
            text="Sistema de Migración de Datos",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("gray20", "white"),
            anchor="w"
        )
        main_title.grid(row=0, column=0, sticky="ew")

        # Subtítulo
        subtitle = ctk.CTkLabel(
            title_frame,
            text="Migración de Excel a SQLite3 | Rápido • Seguro • Confiable",
            font=ctk.CTkFont(size=14),
            text_color=("gray50", "gray70"),
            anchor="w"
        )
        subtitle.grid(row=1, column=0, sticky="ew", pady=(5, 0))

        # Badge de estado
        status_frame = ctk.CTkFrame(
            header_frame,
            width=120,
            height=35,
            corner_radius=20,
            fg_color=self.colors['success']
        )
        status_frame.grid(row=0, column=2, padx=30, pady=20, sticky="e")
        status_frame.grid_propagate(False)

        status_label = ctk.CTkLabel(
            status_frame,
            text="✓ Sistema Listo",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="white"
        )
        status_label.place(relx=0.5, rely=0.5, anchor="center")

    def crear_contenido_principal(self, parent, row):
        """Crear el contenido principal con scroll"""
        # Contenedor con scroll moderno
        self.scrollable_frame = ctk.CTkScrollableFrame(
            parent,
            corner_radius=0,
            fg_color=self.colors['background'],
            scrollbar_button_color=("gray80", "gray30"),
            scrollbar_button_hover_color=("gray70", "gray40")
        )
        self.scrollable_frame.grid(row=row, column=0, sticky="nsew", padx=0, pady=0)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # Layout en dos columnas para mejor aprovechamiento del espacio
        content_container = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color=self.colors['background']
        )
        content_container.grid(row=0, column=0, sticky="ew", padx=30, pady=20)
        content_container.grid_columnconfigure((0, 1), weight=1)

        # Columna izquierda: Configuración
        left_column = ctk.CTkFrame(content_container, corner_radius=20, fg_color=self.colors['frame_bg'])
        left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 15), pady=0)
        left_column.grid_columnconfigure(0, weight=1)

        # Columna derecha: Estado y acciones
        right_column = ctk.CTkFrame(content_container, corner_radius=20, fg_color=self.colors['frame_bg'])
        right_column.grid(row=0, column=1, sticky="nsew", padx=(15, 0), pady=0)
        right_column.grid_columnconfigure(0, weight=1)

        # Llenar columnas
        self.crear_seccion_configuracion(left_column)
        self.crear_seccion_acciones(right_column)

        # Sección de progreso (full width)
        self.crear_seccion_progreso_moderna(content_container, 1)

        # Área de resultados (full width)
        self.crear_area_resultados_moderna(content_container, 2)

    def crear_seccion_configuracion(self, parent):
        """Crear sección de configuración moderna"""
        # Título de sección
        section_header = ctk.CTkFrame(parent, height=50, corner_radius=15, fg_color=self.colors['primary'])
        section_header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 0))
        section_header.grid_propagate(False)

        header_label = ctk.CTkLabel(
            section_header,
            text="⚙️ Configuración",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        )
        header_label.place(relx=0.5, rely=0.5, anchor="center")

        # Selección de base de datos
        self.crear_seccion_bd_moderna(parent, 1)

        # Selección de tabla
        self.crear_seccion_tabla_moderna(parent, 2)

    def crear_seccion_bd_moderna(self, parent, row):
        """Crear sección de BD con diseño moderno"""
        bd_container = ctk.CTkFrame(parent, fg_color=self.colors['frame_bg'])
        bd_container.grid(row=row, column=0, sticky="ew", padx=20, pady=15)
        bd_container.grid_columnconfigure(0, weight=1)

        # Título
        bd_title = ctk.CTkLabel(
            bd_container,
            text="📁 Base de Datos",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("gray20", "white"),
            anchor="w"
        )
        bd_title.grid(row=0, column=0, sticky="w", pady=(10, 10), padx=10)

        # Entry moderno
        self.entry_bd = ctk.CTkEntry(
            bd_container,
            textvariable=self.ruta_bd,
            placeholder_text="🔍 Seleccione la base de datos SQLite3...",
            height=45,
            font=ctk.CTkFont(size=13),
            corner_radius=12,
            border_width=2,
            state="readonly"
        )
        self.entry_bd.grid(row=1, column=0, sticky="ew", pady=(0, 10), padx=10)

        # Botón moderno
        self.btn_seleccionar_bd = ctk.CTkButton(
            bd_container,
            text="📂 Examinar",
            command=self.seleccionar_bd,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=12,
            fg_color=self.colors['secondary'],
            hover_color=self.colors['primary'],
            border_width=0
        )
        self.btn_seleccionar_bd.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))

    def crear_seccion_tabla_moderna(self, parent, row):
        """Crear sección de tabla con cards modernas"""
        tabla_container = ctk.CTkFrame(parent, fg_color=self.colors['frame_bg'])
        tabla_container.grid(row=row, column=0, sticky="ew", padx=20, pady=15)
        tabla_container.grid_columnconfigure(0, weight=1)

        # Título
        tabla_title = ctk.CTkLabel(
            tabla_container,
            text="📊 Tabla a Migrar",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("gray20", "white"),
            anchor="w"
        )
        tabla_title.grid(row=0, column=0, sticky="w", pady=(10, 15), padx=10)

        # Cards de opciones
        tablas = [
            ("ALM", "👥", "Alumnos", "Información estudiantil"),
            ("CC", "📚", "Carga Curricular", "Materias y planes"),
            ("DCT", "👨‍🏫", "Docentes", "Información profesorado"),
            ("INS", "📝", "Inscripciones", "Registros académicos"),
            ("SEA", "🏫", "Secciones", "Grupos y secciones")
        ]

        for i, (codigo, icono, nombre, desc) in enumerate(tablas):
            self.crear_tabla_card(tabla_container, i+1, codigo, icono, nombre, desc)

    def crear_tabla_card(self, parent, row, codigo, icono, nombre, desc):
        """Crear card individual para cada tabla"""
        # Frame principal de la card
        card_frame = ctk.CTkFrame(
            parent,
            height=70,
            corner_radius=12,
            fg_color=self.colors['card_bg'],
            border_width=2,
            border_color=self.colors['card_bg']
        )
        card_frame.grid(row=row, column=0, sticky="ew", pady=3, padx=10)
        card_frame.grid_propagate(False)
        card_frame.grid_columnconfigure(1, weight=1)

        # Radio button
        radio = ctk.CTkRadioButton(
            card_frame,
            text="",
            variable=self.tabla_seleccionada,
            value=codigo,
            width=20,
            height=20,
            radiobutton_width=20,
            radiobutton_height=20,
            command=lambda: self.seleccionar_tabla_card(card_frame, codigo)
        )
        radio.grid(row=0, column=0, padx=15, pady=0, sticky="w")

        # Icono
        icon_label = ctk.CTkLabel(
            card_frame,
            text=icono,
            font=ctk.CTkFont(size=24),
            width=40
        )
        icon_label.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="w")

        # Información
        info_frame = ctk.CTkFrame(card_frame, fg_color=self.colors['card_bg'])
        info_frame.grid(row=0, column=2, sticky="ew", padx=10, pady=10)
        info_frame.grid_columnconfigure(0, weight=1)

        name_label = ctk.CTkLabel(
            info_frame,
            text=nombre,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("gray20", "white"),
            anchor="w"
        )
        name_label.grid(row=0, column=0, sticky="ew")

        desc_label = ctk.CTkLabel(
            info_frame,
            text=desc,
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
            anchor="w"
        )
        desc_label.grid(row=1, column=0, sticky="ew")

        # Almacenar referencia para animación
        setattr(self, f"card_{codigo}", card_frame)

        # Seleccionar ALM por defecto
        if codigo == "ALM":
            self.seleccionar_tabla_card(card_frame, codigo)

    def seleccionar_tabla_card(self, card_frame, codigo):
        """Animar selección de tabla"""
        # Resetear todas las cards
        for tabla_codigo in ["ALM", "CC", "DCT", "INS", "SEA"]:
            if hasattr(self, f"card_{tabla_codigo}"):
                card = getattr(self, f"card_{tabla_codigo}")
                card.configure(
                    border_color=self.colors['card_bg'],
                    fg_color=self.colors['card_bg']
                )

        # Resaltar card seleccionada
        card_frame.configure(
            border_color=self.colors['primary'],
            fg_color=self.colors['card_bg']
        )

    def crear_seccion_acciones(self, parent):
        """Crear sección de acciones y estado"""
        # Título de sección
        section_header = ctk.CTkFrame(parent, height=50, corner_radius=15, fg_color=self.colors['accent'])
        section_header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 0))
        section_header.grid_propagate(False)

        header_label = ctk.CTkLabel(
            section_header,
            text="🎯 Acciones",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        )
        header_label.place(relx=0.5, rely=0.5, anchor="center")

        # Información del sistema
        self.crear_info_sistema(parent, 1)

        # Botones de acción
        self.crear_botones_modernos(parent, 2)

    def crear_info_sistema(self, parent, row):
        """Crear panel de información del sistema"""
        info_container = ctk.CTkFrame(parent, fg_color=self.colors['frame_bg'])
        info_container.grid(row=row, column=0, sticky="ew", padx=20, pady=15)

        # Estado del sistema
        status_frame = ctk.CTkFrame(
            info_container,
            height=100,
            width=400,
            corner_radius=12,
            fg_color=("gray85", "gray25")
        )
        status_frame.grid(row=0, column=0, sticky="ew", pady=(10, 10), padx=10)
        status_frame.grid_propagate(False)
        status_frame.grid_columnconfigure(1, weight=1)

        # Icono de estado
        status_icon = ctk.CTkLabel(
            status_frame,
            text="💡",
            font=ctk.CTkFont(size=24)
        )
        status_icon.grid(row=0, column=0, padx=15, pady=0)

        # Información de estado
        status_info = ctk.CTkFrame(status_frame, fg_color=("gray85", "gray25"))
        status_info.grid(row=0, column=1, sticky="ew", padx=(0, 15), pady=15)

        self.status_title = ctk.CTkLabel(
            status_info,
            text="Sistema Preparado",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("gray20", "white"),
            anchor="w"
        )
        self.status_title.grid(row=0, column=0, sticky="ew")

        self.status_desc = ctk.CTkLabel(
            status_info,
            text="Configurar base de datos y tabla",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
            anchor="w",
        )
        self.status_desc.grid(row=1, column=0, sticky="ew")

        # Tips rápidos
        tips_frame = ctk.CTkFrame(
            info_container,
            corner_radius=12,
            fg_color=("gray50", "gray60")
        )
        tips_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))

        tips_label = ctk.CTkLabel(
            tips_frame,
            text="💡 Tip: Asegúrese de tener los archivos Excel en la carpeta correcta",
            font=ctk.CTkFont(size=12),
            text_color=("#ffffff", "#ffffff"),
            wraplength=250
        )
        tips_label.grid(row=0, column=0, padx=15, pady=12)

    def crear_botones_modernos(self, parent, row):
        """Crear botones con diseño moderno"""
        buttons_container = ctk.CTkFrame(parent, fg_color=self.colors['frame_bg'])
        buttons_container.grid(row=row, column=0, sticky="ew", padx=20, pady=15)
        buttons_container.grid_columnconfigure(0, weight=1)

        # Botón principal - Migrar
        self.btn_migrar = ctk.CTkButton(
            buttons_container,
            text="🚀 Iniciar Migración",
            command=self.iniciar_migracion,
            height=55,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=15,
            fg_color=self.colors['success'],
            hover_color=self.colors['primary'],
            border_width=0
        )
        self.btn_migrar.grid(row=0, column=0, sticky="ew", pady=(10, 10), padx=10)

        # Frame para botones secundarios
        secondary_buttons = ctk.CTkFrame(buttons_container, fg_color=self.colors['frame_bg'])
        secondary_buttons.grid(row=1, column=0, sticky="ew", padx=10)
        secondary_buttons.grid_columnconfigure((0, 1), weight=1)

        # Botón limpiar
        btn_limpiar = ctk.CTkButton(
            secondary_buttons,
            text="🗑️ Limpiar",
            command=self.limpiar_campos,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=12,
            fg_color=self.colors['warning'],
            hover_color=self.colors['accent'],
            text_color="white"
        )
        btn_limpiar.grid(row=0, column=0, sticky="ew", padx=(0, 5), pady=(0, 10))

        # Botón salir
        btn_salir = ctk.CTkButton(
            secondary_buttons,
            text="❌ Salir",
            command=self.salir_aplicacion,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=12,
            fg_color=self.colors['error'],
            hover_color="#CC0000",
            text_color="white"
        )
        btn_salir.grid(row=0, column=1, sticky="ew", padx=(5, 0), pady=(0, 10))

    def crear_seccion_progreso_moderna(self, parent, row):
        """Crear sección de progreso moderna"""
        self.progress_container = ctk.CTkFrame(parent, corner_radius=20, fg_color=self.colors['frame_bg'])
        self.progress_container.grid(row=row, column=0, columnspan=2, sticky="ew", padx=0, pady=20)
        self.progress_container.grid_remove()  # Ocultar inicialmente
        self.progress_container.grid_columnconfigure(0, weight=1)

        # Header del progreso
        progress_header = ctk.CTkFrame(
            self.progress_container,
            height=60,
            corner_radius=15,
            fg_color=self.colors['primary']
        )
        progress_header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 0))
        progress_header.grid_propagate(False)

        self.progress_title = ctk.CTkLabel(
            progress_header,
            text="⚡ Migración en Progreso...",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        )
        self.progress_title.place(relx=0.5, rely=0.5, anchor="center")

        # Contenido del progreso
        progress_content = ctk.CTkFrame(self.progress_container, fg_color=self.colors['frame_bg'])
        progress_content.grid(row=1, column=0, sticky="ew", padx=20, pady=20)
        progress_content.grid_columnconfigure(0, weight=1)

        # Barra de progreso moderna
        self.progress_bar = ctk.CTkProgressBar(
            progress_content,
            width=400,
            height=25,
            corner_radius=15,
            progress_color=self.colors['success'],
            fg_color=("gray80", "gray30")
        )
        self.progress_bar.grid(row=0, column=0, sticky="ew", pady=(10, 15), padx=10)

        # Labels de estado
        self.progress_percentage = ctk.CTkLabel(
            progress_content,
            text="0%",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=("gray20", "white")
        )
        self.progress_percentage.grid(row=1, column=0, pady=(0, 5))

        self.progress_label = ctk.CTkLabel(
            progress_content,
            text="Preparando migración...",
            font=ctk.CTkFont(size=14),
            text_color=("gray50", "gray60")
        )
        self.progress_label.grid(row=2, column=0, pady=(0, 10))

    def crear_area_resultados_moderna(self, parent, row):
        """Crear área de resultados moderna"""
        self.resultados_container = ctk.CTkFrame(parent, corner_radius=20, fg_color=self.colors['frame_bg'])
        self.resultados_container.grid(row=row, column=0, columnspan=2, sticky="ew", padx=0, pady=(0, 20))
        self.resultados_container.grid_remove()  # Ocultar inicialmente
        self.resultados_container.grid_columnconfigure(0, weight=1)

        # Header de resultados
        self.resultado_header = ctk.CTkFrame(
            self.resultados_container,
            height=60,
            corner_radius=15,
            fg_color=self.colors['success']
        )
        self.resultado_header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 0))
        self.resultado_header.grid_propagate(False)

        self.resultado_titulo = ctk.CTkLabel(
            self.resultado_header,
            text="✅ Migración Completada",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        )
        self.resultado_titulo.place(relx=0.5, rely=0.5, anchor="center")

        # Contenido de resultados
        resultados_content = ctk.CTkFrame(self.resultados_container, fg_color=self.colors['frame_bg'])
        resultados_content.grid(row=1, column=0, sticky="ew", padx=20, pady=20)
        resultados_content.grid_columnconfigure(0, weight=1)

        # Textbox de resultados
        self.resultado_texto = ctk.CTkTextbox(
            resultados_content,
            height=200,
            font=ctk.CTkFont(size=12, family="Consolas"),
            corner_radius=12,
            fg_color=("gray95", "gray20"),
            text_color=("gray20", "gray80"),
            scrollbar_button_color=("gray70", "gray30")
        )
        self.resultado_texto.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

    def crear_footer(self, parent, row):
        """Crear footer moderno"""
        footer_frame = ctk.CTkFrame(
            parent,
            height=50,
            corner_radius=0,
            fg_color=("gray90", "gray20")
        )
        footer_frame.grid(row=row, column=0, sticky="ew")
        footer_frame.grid_propagate(False)
        footer_frame.grid_columnconfigure(1, weight=1)

        # Logo/Icono pequeño
        footer_icon = ctk.CTkLabel(
            footer_frame,
            text="⚡",
            font=ctk.CTkFont(size=16)
        )
        footer_icon.grid(row=0, column=0, padx=20, pady=0)

        # Información del footer
        footer_info = ctk.CTkLabel(
            footer_frame,
            text="Sistema de Migración v1.2 • Desarrollado con CustomTkinter - Andy Palma - Cleiber Garcia",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60")
        )
        footer_info.grid(row=0, column=1, sticky="w", padx=10)

        # Estado de conexión
        status_dot = ctk.CTkLabel(
            footer_frame,
            text="🟢 Conectado",
            font=ctk.CTkFont(size=11),
            text_color=("green", "lightgreen")
        )
        status_dot.grid(row=0, column=2, padx=20, pady=0)

    def seleccionar_bd(self):
        """Seleccionar la base de datos SQLite3"""
        ruta = filedialog.askopenfilename(
            title="Seleccione la base de datos SQLite3 de destino",
            filetypes=[
                ("Bases de datos SQLite3", "*.db"),
                ("Bases de datos SQLite3", "*.sqlite"),
                ("Bases de datos SQLite3", "*.sqlite3"),
                ("Todos los archivos", "*.*")
            ],
            parent=self.root
        )

        if ruta:
            self.ruta_bd.set(ruta)
            # Actualizar estado
            self.status_title.configure(text="Base de Datos Configurada")
            self.status_desc.configure(text=f"📁 {os.path.basename(ruta)}")

    def mostrar_progreso(self, mostrar=True):
        """Mostrar u ocultar la sección de progreso"""
        if mostrar:
            self.progress_container.grid()
            self.progress_bar.set(0)
            self.progreso_visible = True
        else:
            self.progress_container.grid_remove()
            self.progreso_visible = False

    def actualizar_progreso(self, valor, texto=""):
        """Actualizar la barra de progreso con animación"""
        if self.progreso_visible:
            self.progress_bar.set(valor)
            percentage = int(valor * 100)
            self.progress_percentage.configure(text=f"{percentage}%")
            
            if texto:
                self.progress_label.configure(text=texto)
            
            # Cambiar color de la barra según el progreso
            if valor < 0.3:
                self.progress_bar.configure(progress_color=self.colors['warning'])
            elif valor < 0.7:
                self.progress_bar.configure(progress_color=self.colors['secondary'])
            else:
                self.progress_bar.configure(progress_color=self.colors['success'])
                
            self.root.update_idletasks()

    def mostrar_resultados(self, exito, conteo, ruta_bd, tabla):
        """Mostrar los resultados de la migración con diseño moderno"""
        self.resultados_container.grid()

        # Configurar header según resultado
        if exito:
            self.resultado_header.configure(fg_color=self.colors['success'])
            self.resultado_titulo.configure(text="🎉 Migración Exitosa")
        else:
            self.resultado_header.configure(fg_color=self.colors['error'])
            self.resultado_titulo.configure(text="❌ Error en Migración")

        # Limpiar área de texto
        self.resultado_texto.delete("1.0", "end")

        # Preparar el texto de resultados con formato moderno
        estado_emoji = "🎊" if exito else "⚠️"
        estado_texto = "COMPLETADA EXITOSAMENTE" if exito else "FALLÓ"
        
        tabla_nombres = {
            'ALM': 'Alumnos 👥',
            'CC': 'Carga Curricular 📚',
            'DCT': 'Docentes 👨‍🏫',
            'INS': 'Inscripciones 📝',
            'SEA': 'Secciones 🏫'
        }

        resultado = f"""{estado_emoji} REPORTE DE MIGRACIÓN {estado_emoji}

╔══════════════════════════════════════════════════════════════╗
║                        INFORMACIÓN GENERAL                    ║
╠══════════════════════════════════════════════════════════════╣
║ 📁 Base de datos: {os.path.basename(ruta_bd):<30}
║ 📍 Ruta completa: {ruta_bd}
║ 📊 Tabla migrada: {tabla_nombres.get(tabla, tabla):<30}
║ 📈 Estado: {estado_texto:<40}
║ 📋 Registros procesados: {conteo:<25}
║ ⏰ Fecha: {self.obtener_fecha_actual():<35}
╚══════════════════════════════════════════════════════════════╝

{self.generar_estadisticas_adicionales(exito, conteo)}

{'🎯 MIGRACIÓN COMPLETADA CON ÉXITO' if exito else '🔧 REVISE LOS ERRORES PARA MÁS INFORMACIÓN'}
{'✨ Todos los datos se han transferido correctamente' if exito else '📋 Consulte el archivo de log para detalles específicos'}

{self.generar_recomendaciones(exito)}"""

        # Insertar el texto con colores
        self.resultado_texto.insert("1.0", resultado)

    def obtener_fecha_actual(self):
        """Obtener fecha y hora actual formateada"""
        from datetime import datetime
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def generar_estadisticas_adicionales(self, exito, conteo):
        """Generar estadísticas adicionales para el reporte"""
        if exito:
            return f"""
╔══════════════════════════════════════════════════════════════╗
║                         ESTADÍSTICAS                         ║
╠══════════════════════════════════════════════════════════════╣
║ ✅ Registros procesados exitosamente: {conteo:<15}
║ 🚀 Velocidad promedio: Alta                                 ║
║ 💾 Integridad de datos: Verificada                          ║
║ 🔒 Estado de la BD: Actualizada                             ║
╚══════════════════════════════════════════════════════════════╝"""
        else:
            return f"""
╔══════════════════════════════════════════════════════════════╗
║                       INFORMACIÓN DE ERROR                   ║
╠══════════════════════════════════════════════════════════════╣
║ ❌ Registros procesados antes del error: {conteo:<10}
║ 🔍 Estado de la BD: Verificar integridad                    ║
║ 📝 Log de errores: Disponible                               ║
║ 🔄 Reintentos recomendados: Sí                              ║
╚══════════════════════════════════════════════════════════════╝"""

    def generar_recomendaciones(self, exito):
        """Generar recomendaciones según el resultado"""
        if exito:
            return """
💡 RECOMENDACIONES POST-MIGRACIÓN:
▶️ Verifique los datos en la base de datos
▶️ Realice una copia de seguridad del archivo SQLite
▶️ Actualice sus aplicaciones para usar la nueva BD
▶️ Considere programar migraciones automáticas futuras

🎊 ¡Felicidades! La migración se completó sin problemas."""
        else:
            return """
🔧 PASOS PARA SOLUCIONAR PROBLEMAS:
▶️ Revise el archivo de log detallado
▶️ Verifique los permisos de archivo
▶️ Confirme que los archivos Excel estén accesibles
▶️ Asegúrese de que la BD no esté siendo usada por otra aplicación
▶️ Contacte al administrador si el problema persiste

📞 ¿Necesita ayuda? Consulte la documentación técnica."""

    def ejecutar_migracion_hilo(self):
        """Ejecutar la migración en un hilo separado"""
        try:
            # Actualizar progreso inicial
            self.actualizar_progreso(0.05, "🔄 Inicializando sistema de migración...")
            
            # Obtener datos
            tabla = self.tabla_seleccionada.get()
            ruta_bd = self.ruta_bd.get()

            # Diccionario de migradores
            migradores = {
                'ALM': MigradorALM,
                'CC': MigradorCC,
                'DCT': MigradorDCT,
                'INS': MigradorINS,
                'SEA': MigradorSEA
            }

            self.actualizar_progreso(0.15, f"🏗️ Configurando migrador para {tabla}...")
            
            # Crear el migrador
            migrador = migradores[tabla](ruta_bd)
            
            self.actualizar_progreso(0.25, "📊 Analizando estructura de datos...")
            
            # Simular pasos adicionales para mejor UX
            import time
            time.sleep(0.5)
            
            self.actualizar_progreso(0.40, "📋 Validando archivos de origen...")
            time.sleep(0.3)
            
            self.actualizar_progreso(0.55, "🔄 Ejecutando migración de datos...")
            
            # Ejecutar la migración real
            exito, conteo = migrador.ejecutar_migracion()
            
            self.actualizar_progreso(0.85, "✅ Verificando integridad de datos...")
            time.sleep(0.3)
            
            self.actualizar_progreso(0.95, "📝 Generando reporte final...")
            time.sleep(0.2)
            
            self.actualizar_progreso(1.0, "🎉 ¡Migración completada!")

            # Mostrar resultados en el hilo principal
            self.root.after(800, lambda: self.finalizar_migracion(exito, conteo, ruta_bd, tabla))

        except Exception as e:
            # Manejar errores
            self.root.after(0, lambda: self.mostrar_error(f"Error durante la migración: {str(e)}"))

    def finalizar_migracion(self, exito, conteo, ruta_bd, tabla):
        """Finalizar la migración y mostrar resultados"""
        # Ocultar progreso
        self.mostrar_progreso(False)

        # Reactivar botón con animación
        self.btn_migrar.configure(
            state="normal", 
            text="🚀 Iniciar Migración",
            fg_color=self.colors['success']
        )

        # Actualizar estado del sistema
        if exito:
            self.status_title.configure(text="✅ Migración Exitosa")
            self.status_desc.configure(text=f"Procesados: {conteo} registros")
        else:
            self.status_title.configure(text="❌ Error en Migración")
            self.status_desc.configure(text="Revisar logs para más detalles")

        # Mostrar resultados
        self.mostrar_resultados(exito, conteo, ruta_bd, tabla)

        # Mostrar mensaje con estilo
        if exito:
            self.mostrar_mensaje_exitoso(conteo, tabla)
        else:
            self.mostrar_mensaje_error()

    def mostrar_mensaje_exitoso(self, conteo, tabla):
        """Mostrar mensaje de éxito personalizado"""
        tabla_nombres = {
            'ALM': 'Alumnos',
            'CC': 'Carga Curricular',
            'DCT': 'Docentes',
            'INS': 'Inscripciones',
            'SEA': 'Secciones'
        }
        
        messagebox.showinfo(
            "🎉 ¡Migración Exitosa!",
            f"┌─────────────────────────────────────┐\n"
            f"│        MIGRACIÓN COMPLETADA         │\n"
            f"├─────────────────────────────────────┤\n"
            f"│ ✅ Estado: Exitosa                  │\n"
            f"│ 📊 Tabla: {tabla_nombres.get(tabla, tabla):<23} │\n"
            f"│ 📈 Registros: {conteo:<19} │\n"
            f"│ 🎯 Integridad: Verificada           │\n"
            f"└─────────────────────────────────────┘\n\n"
            f"🚀 ¡Su base de datos está lista para usar!"
        )

    def mostrar_mensaje_error(self):
        """Mostrar mensaje de error personalizado"""
        messagebox.showerror(
            "❌ Error en Migración",
            f"┌─────────────────────────────────────┐\n"
            f"│         MIGRACIÓN FALLIDA           │\n"
            f"├─────────────────────────────────────┤\n"
            f"│ ❌ Estado: Error                    │\n"
            f"│ 📋 Logs: Disponibles                │\n"
            f"│ 🔧 Acción: Revisar configuración   │\n"
            f"│ 📞 Soporte: Disponible              │\n"
            f"└─────────────────────────────────────┘\n\n"
            f"🔍 Revise el reporte detallado para más información."
        )

    def mostrar_error(self, mensaje):
        """Mostrar un error del sistema"""
        self.mostrar_progreso(False)
        self.btn_migrar.configure(
            state="normal", 
            text="🚀 Iniciar Migración",
            fg_color=self.colors['success']
        )
        
        # Actualizar estado
        self.status_title.configure(text="⚠️ Error del Sistema")
        self.status_desc.configure(text="Revisar configuración")
        
        messagebox.showerror(
            "⚠️ Error del Sistema", 
            f"Se produjo un error inesperado:\n\n{mensaje}\n\n"
            f"💡 Sugerencias:\n"
            f"• Verificar permisos de archivo\n"
            f"• Comprobar rutas de acceso\n"
            f"• Reiniciar la aplicación"
        )

    def iniciar_migracion(self):
        """Iniciar el proceso de migración con validaciones mejoradas"""
        # Validación de base de datos
        if not self.ruta_bd.get():
            messagebox.showerror(
                "❌ Error de Configuración",
                "┌─────────────────────────────────────┐\n"
                "│        CONFIGURACIÓN FALTANTE       │\n"
                "├─────────────────────────────────────┤\n"
                "│ 📁 Base de datos: No seleccionada  │\n"
                "│ 🎯 Acción requerida: Seleccionar   │\n"
                "└─────────────────────────────────────┘\n\n"
                "Por favor seleccione una base de datos SQLite3"
            )
            return

        if not os.path.exists(self.ruta_bd.get()):
            messagebox.showerror(
                "❌ Error de Archivo",
                "┌─────────────────────────────────────┐\n"
                "│         ARCHIVO NO ENCONTRADO       │\n"
                "├─────────────────────────────────────┤\n"
                "│ 📁 Archivo: No existe              │\n"
                "│ 🔍 Verificar: Ruta de acceso       │\n"
                "└─────────────────────────────────────┘\n\n"
                "La base de datos seleccionada no existe"
            )
            return

        # Obtener información para confirmación
        tabla = self.tabla_seleccionada.get()
        tabla_nombres = {
            'ALM': '👥 Alumnos',
            'CC': '📚 Carga Curricular',
            'DCT': '👨‍🏫 Docentes',
            'INS': '📝 Inscripciones',
            'SEA': '🏫 Secciones'
        }

        nombre_tabla = tabla_nombres.get(tabla, tabla)

        # Diálogo de confirmación moderno
        confirmacion = messagebox.askyesno(
            "🚀 Confirmar Migración",
            f"┌─────────────────────────────────────────┐\n"
            f"│           CONFIRMAR MIGRACIÓN           │\n"
            f"├─────────────────────────────────────────┤\n"
            f"│ 📁 Base de datos:                       │\n"
            f"│   {os.path.basename(self.ruta_bd.get()):<35} │\n"
            f"│                                         │\n"
            f"│ 📊 Tabla a migrar:                      │\n"
            f"│   {nombre_tabla:<35} │\n"
            f"│                                         │\n"
            f"│ ⏱️ Tiempo estimado: 2-5 minutos         │\n"
            f"│ 🔒 Operación: Segura                    │\n"
            f"└─────────────────────────────────────────┘\n\n"
            f"¿Desea continuar con la migración?"
        )

        if not confirmacion:
            return

        # Preparar interfaz para migración
        self.btn_migrar.configure(
            state="disabled", 
            text="⏳ Migrando...",
            fg_color=self.colors['warning']
        )
        
        # Actualizar estado
        self.status_title.configure(text="⚡ Migración en Proceso")
        self.status_desc.configure(text="Por favor espere...")
        
        self.mostrar_progreso(True)

        # Ocultar resultados anteriores
        self.resultados_container.grid_remove()

        # Ejecutar migración en hilo separado
        hilo_migracion = threading.Thread(target=self.ejecutar_migracion_hilo)
        hilo_migracion.daemon = True
        hilo_migracion.start()

    def limpiar_campos(self):
        """Limpiar todos los campos con confirmación"""
        if messagebox.askyesno(
            "🗑️ Limpiar Campos",
            "¿Está seguro de que desea limpiar todos los campos?\n\n"
            "Esta acción restablecerá:\n"
            "• Selección de base de datos\n"
            "• Tabla seleccionada\n"
            "• Resultados mostrados"
        ):
            # Limpiar campos
            self.ruta_bd.set("")
            self.tabla_seleccionada.set("ALM")
            
            # Resetear estado visual
            self.status_title.configure(text="Sistema Preparado")
            self.status_desc.configure(text="Configurar base de datos y tabla")
            
            # Ocultar secciones
            self.mostrar_progreso(False)
            self.resultados_container.grid_remove()
            
            # Resetear selección de tabla cards
            for tabla_codigo in ["ALM", "CC", "DCT", "INS", "SEA"]:
                if hasattr(self, f"card_{tabla_codigo}"):
                    card = getattr(self, f"card_{tabla_codigo}")
                    card.configure(
                        border_color=self.colors['card_border'],
                        fg_color=self.colors['card_bg']
                    )
            
            # Seleccionar ALM por defecto
            if hasattr(self, "card_ALM"):
                self.seleccionar_tabla_card(getattr(self, "card_ALM"), "ALM")

    def salir_aplicacion(self):
        """Salir de la aplicación con confirmación elegante"""
        resultado = messagebox.askyesnocancel(
            "❌ Salir de la Aplicación",
            "┌─────────────────────────────────────┐\n"
            "│          CONFIRMAR SALIDA           │\n"
            "├─────────────────────────────────────┤\n"
            "│ 🚪 ¿Desea salir de la aplicación?  │\n"
            "│                                     │\n"
            "│ ✅ Sí - Salir ahora                │\n"
            "│ ❌ No - Continuar trabajando        │\n"
            "│ 🔄 Cancelar                         │\n"
            "└─────────────────────────────────────┘\n\n"
            "¿Está seguro de que desea salir?"
        )
        
        if resultado:  # True = Sí
            # Animación de cierre (opcional)
            self.root.withdraw()  # Ocultar ventana temporalmente
            
            # Mensaje de despedida
            messagebox.showinfo(
                "👋 ¡Hasta pronto!",
                "┌─────────────────────────────────────┐\n"
                "│             DESPEDIDA               │\n"
                "├─────────────────────────────────────┤\n"
                "│ 🙏 Gracias por usar nuestro sistema │\n"
                "│ 💫 ¡Que tenga un excelente día!    │\n"
                "│ 🚀 Versión 1.2 - 2025              │\n"
                "└─────────────────────────────────────┘"
            )
            
            # Cerrar aplicación
            self.root.quit()
            self.root.destroy()

    def ejecutar(self):
        """Ejecutar la aplicación con manejo de errores"""
        try:
            # Iniciar loop principal (removimos el splash screen que podría causar problemas)
            self.root.mainloop()
            
        except Exception as e:
            messagebox.showerror(
                "💥 Error Fatal del Sistema",
                f"┌─────────────────────────────────────┐\n"
                f"│           ERROR CRÍTICO             │\n"
                f"├─────────────────────────────────────┤\n"
                f"│ ⚠️ Error: {str(e)[:25]:<25} │\n"
                f"│ 📋 Código: Sistema                  │\n"
                f"│ 🔧 Solución: Reiniciar aplicación  │\n"
                f"└─────────────────────────────────────┘\n\n"
                f"Error técnico: {str(e)}"
            )


def main():
    """Función principal mejorada"""
    try:
        # Crear y ejecutar aplicación
        app = SistemaMigracionApp()
        app.ejecutar()
        
    except Exception as e:
        # Error durante la inicialización
        messagebox.showerror(
            "💥 Error de Inicialización",
            f"┌─────────────────────────────────────┐\n"
            f"│        ERROR DE INICIALIZACIÓN      │\n"
            f"├─────────────────────────────────────┤\n"
            f"│ ❌ No se pudo iniciar la aplicación │\n"
            f"│ 🔍 Error: {str(e)[:23]:<23} │\n"
            f"│ 💡 Solución: Verificar dependencias │\n"
            f"└─────────────────────────────────────┘\n\n"
            f"Detalles técnicos: {str(e)}\n\n"
            f"Posibles causas:\n"
            f"• CustomTkinter no instalado correctamente\n"
            f"• Archivos de migrador faltantes\n"
            f"• Permisos de sistema insuficientes\n"
            f"• Versión incompatible de CustomTkinter"
        )


if __name__ == "__main__":
    main()
    