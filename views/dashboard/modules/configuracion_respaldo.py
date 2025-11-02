import os
from tkinter import filedialog, messagebox
import webbrowser
import threading
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image
from datetime import datetime

from config.settings import Settings
from views.dashboard.components.widget_utils import *
from views.dashboard.components.tooltip import Tooltip

class ConfiguracionRespaldo(ctk.CTkFrame):
    def __init__(self, master, controllers):
        super().__init__(master, fg_color="transparent")

        self.controllerSolicitud = controllers["Solicitud"]


        header_label = ctk.CTkLabel(self, text=f" Respaldo y Restauración", text_color=COLOR_HEADER_SECCION_TEXT,
                                        fg_color=COLOR_HEADER_SECCION_BG_2, font=FUENTE_HEADER_SECCION,
                                        height=30, corner_radius=6)
        header_label.pack(fill="x", pady=(0, 10), padx=0)

        self.componentesVista()
     

    def componentesVista(self):
        #Componentes de impotacion y respaldo
        frameContenido = ctk.CTkFrame(self, fg_color="transparent")
        frameContenido.pack(pady=(20, 10), padx=20, fill="x", anchor="n")

        rutaIconoInfo = Settings().rutas_iconos.get("advertencia_icon")
        imagenInfo = Image.open(rutaIconoInfo)
        
        iconoInfo = CTkImage(light_image=imagenInfo, dark_image=imagenInfo, size=(24, 24))
        
        ###############COMPONENTES DE EXPORTACION###############

        frameFilaExportacion = ctk.CTkFrame(frameContenido, fg_color="transparent")
        frameFilaExportacion.pack(pady=20, fill="x", anchor="w")

        ctk.CTkLabel(
            frameFilaExportacion,
            text="Exportar Información del Sistema",
            font=FUENTE_TITULO_FORMULARIO,
            text_color=COLOR_TEXTO_PRINCIPAL
        ).pack(pady=(10, 20), anchor="w")

        #Mostrar icono de advertencia

        infoExportLabel = ctk.CTkLabel(
            frameFilaExportacion,
            image=iconoInfo,
            text="",
        )
        infoExportLabel.pack(side="left", padx=16)

        tooltip_text = "⚠️ Tener extremo cuidado con la información que desee Exportar\nSe recomienda resguardarla en una unidad de almacenamiento seguro\nPara no comprometer la información de los usuarios"
        Tooltip(infoExportLabel, tooltip_text)

        self.varTipoExpor = ctk.StringVar(value="*.xlxs")

        self.menuTipoExpor = create_option_menu_row(
            frameFilaExportacion,
            label_text="Seleccione el formato del archivo",
            options=  ["*.xlxs","*.sql"],
            variable=self.varTipoExpor,
            side_="left",
            crear_frame=False,
            width=180
            )

        self.btn_exportar = ctk.CTkButton(
            frameFilaExportacion,
            text="Realizar Exportación",
            width=140,
            font=FUENTE_BOTON,
            fg_color=COLOR_BOTON_PRIMARIO_FG,
            hover_color=COLOR_BOTON_PRIMARIO_HOVER,
            text_color=COLOR_BOTON_PRIMARIO_TEXT,
            command=self.iniciar_proceso_exportacion
        )
        self.btn_exportar.pack(side="left", padx=(10, 0))
        
        # --- Barra de progreso y etiqueta de estado (inicialmente ocultas) ---
        self.progress_bar = ctk.CTkProgressBar(frameFilaExportacion, width=250)
        self.progress_bar.set(0)
        
        self.progress_label = ctk.CTkLabel(frameFilaExportacion, text="", font=("Segoe UI", 12))

        ###############COMPONENTES DE IMPORTACION###############
        # Separador visual
        ctk.CTkFrame(frameContenido, height=2, fg_color="gray80").pack(fill="x", padx=20, pady=20)

        frameFilaImportacion = ctk.CTkFrame(frameContenido, fg_color="transparent")
        frameFilaImportacion.pack(pady=20, fill="x", anchor="w")

        ctk.CTkLabel(
            frameFilaImportacion,
            text="Importar Información del Sistema",
            font=FUENTE_TITULO_FORMULARIO,
            text_color=COLOR_TEXTO_PRINCIPAL
        ).pack(pady=(10, 20), anchor="w")

        #Mostrar icono de advertencia

        infoImportLabel = ctk.CTkLabel(
            frameFilaImportacion,
            image=iconoInfo,
            text="",
        )
        infoImportLabel.pack(side="left", padx=16)

        tooltip_text = "⚠️ Tener extremo cuidado con la información que desee importar\npara no comprometer la integridad del Sistema"
        Tooltip(infoImportLabel, tooltip_text)

        self.btn_importar = ctk.CTkButton(
            frameFilaImportacion,
            text="Realizar Importación",
            width=140,
            font=FUENTE_BOTON,
            fg_color=COLOR_BOTON_PRIMARIO_FG,
            hover_color=COLOR_BOTON_PRIMARIO_HOVER,
            text_color=COLOR_BOTON_PRIMARIO_TEXT,
            command=lambda: messagebox.showinfo("En desarrollo", "La funcionalidad de importación aún no ha sido implementada.", parent=self)
        )
        self.btn_importar.pack(side="left", padx=(10, 0))


    def iniciar_proceso_exportacion(self):
        """
        Inicia el proceso de exportación según el formato seleccionado.
        Actúa como un despachador para los métodos específicos de exportación.
        """
        tipoFormato = self.varTipoExpor.get()
        if tipoFormato == "*.xlxs":
            self._iniciar_exportacion_excel()
        elif tipoFormato == "*.sql":
            self._iniciar_exportacion_sql()
        else:
            messagebox.showwarning("Advertencia", "Formato no implementado", parent=self)

    def _preparar_ui_para_exportacion(self):
        """Muestra la barra de progreso y deshabilita los botones."""
        self.progress_bar.pack(side="left", padx=(10, 5), pady=5)
        self.progress_label.pack(side="left", padx=5, pady=5)
        self.btn_exportar.configure(state="disabled")
        self.btn_importar.configure(state="disabled")

    def update_progress(self, current, total):
        """Actualiza la barra de progreso. Se llama desde el hilo principal."""
        progress = current / total
        self.progress_bar.set(progress)
        self.progress_label.configure(text=f"Procesando {current}/{total}...")
        self.update_idletasks()

    def _iniciar_exportacion_excel(self):
        """Maneja la lógica de exportación para archivos Excel."""
        ruta_carpeta = filedialog.askdirectory(title="Seleccione la carpeta para guardar la exportación Excel")
        if not ruta_carpeta:
            return

        nombre_archivo = f"exportacion_sistema_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        ruta_completa_destino = os.path.join(ruta_carpeta, nombre_archivo)

        self._preparar_ui_para_exportacion()
        
        def worker_exportar():
            ruta_final = self.controllerSolicitud.exportarAExcel(
                ruta_archivo=ruta_completa_destino,
                progress_callback=lambda c, t: self.after(0, self.update_progress, c, t)
            )
            self.after(0, self.finalizar_exportacion, ruta_final)

        thread = threading.Thread(target=worker_exportar)
        thread.start()

    def _iniciar_exportacion_sql(self):
        """Maneja la lógica de exportación para archivos SQL."""
        directorio_destino = filedialog.askdirectory(title="Seleccione la carpeta para guardar el respaldo SQL")
        if not directorio_destino:
            return

        self._preparar_ui_para_exportacion()

        def worker_exportar_sql():
            """Función que se ejecuta en un hilo para la exportación SQL."""
            ruta_final = self.controllerSolicitud.exportarSQL(
                directorio_destino=directorio_destino,
                progress_callback=lambda c, t: self.after(0, self.update_progress, c, t)
            )
            self.after(0, self.finalizar_exportacion, ruta_final)

        thread = threading.Thread(target=worker_exportar_sql)
        thread.start()

    def finalizar_exportacion(self, ruta_final):
        """
        Se ejecuta en el hilo principal para actualizar la UI después de cualquier exportación.
        Oculta la barra de progreso, reactiva los botones y muestra el resultado.
        
        Args:
            ruta_final (str|None): La ruta del archivo generado o None si hubo un error.
        """
        self.progress_bar.pack_forget()
        self.progress_label.pack_forget()
        self.btn_exportar.configure(state="normal")
        self.btn_importar.configure(state="normal")

        if ruta_final:
            respuesta = messagebox.askyesno(
                "Éxito",
                f"Exportación completada.\nArchivo guardado en:\n{ruta_final}\n\n¿Desea abrir la carpeta de destino?"
            )
            if respuesta:
                webbrowser.open(os.path.dirname(ruta_final))
        else:
            messagebox.showerror("Error", "Ocurrió un error durante la exportación.")
        