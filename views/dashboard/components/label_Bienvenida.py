import customtkinter as ctk
from PIL import Image
from utils.CargarImagen import UtilImagen

class LabelBienvenida(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.frame_bienvenida = None
        self.label_titulo = None
        self.label_bienvenida = None
        self.icono_label = None

    def configurar(self, titulo, mensaje, icono_path, alineacion="w"):
        # Elimina el frame anterior si existe
        if self.frame_bienvenida:
            self.frame_bienvenida.destroy()

        self.frame_bienvenida = ctk.CTkFrame(
            self,
            fg_color="#eaf0fb",
            corner_radius=20,
            border_width=2,
            border_color="#3556a3"
        )
        self.frame_bienvenida.pack(pady=20, padx=10, fill="x", expand=False)

        icono_bienvenida = UtilImagen().leer_imagen(self, icono_path, (64, 64))
        self.icono_label = ctk.CTkLabel(
            self.frame_bienvenida,
            image=icono_bienvenida,
            text="",
        )
        self.icono_label.image = icono_bienvenida  # Previene el garbage collection
        self.icono_label.pack(side="left", padx=20, pady=20)

        self.label_titulo = ctk.CTkLabel(
            self.frame_bienvenida,
            text=titulo,
            font=("Roboto", 22, "bold"),
            text_color="#3556a3",
            anchor=alineacion,
            wraplength=500
        )
        self.label_titulo.pack(anchor=alineacion, pady=(20, 0), padx=(0, 20))

        self.label_bienvenida = ctk.CTkLabel(
            self.frame_bienvenida,
            text=mensaje,
            font=("Roboto", 16),
            text_color="#222222",
            anchor=alineacion,
            justify={"w": "left", "center": "center", "e": "right"}.get(alineacion, "left"),
            wraplength=500
        )
        self.label_bienvenida.pack(anchor=alineacion, padx=(0, 10), pady=(0, 10))
        self.frame_bienvenida.update_idletasks()

        ancho_inicial = self.frame_bienvenida.winfo_width() - 60
        if ancho_inicial > 100:
            self.label_bienvenida.configure(wraplength=ancho_inicial)

        def ajustar_wrap(event):
            nuevo_ancho = self.frame_bienvenida.winfo_width() - 60
            if nuevo_ancho > 100:
                self.label_bienvenida.configure(wraplength=nuevo_ancho)
        self.frame_bienvenida.bind("<Configure>", ajustar_wrap)