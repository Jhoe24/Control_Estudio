import customtkinter as ctk
from PIL import Image
import os

class Card(ctk.CTkFrame):
    """
    Un widget de tarjeta reutilizable para mostrar un título, una cantidad y un icono.
    """
    def __init__(self, master, title: str, quantity: int, icon_path: str = "", **kwargs):
        super().__init__(master, fg_color="#18244c", corner_radius=10, **kwargs)

        self.grid_columnconfigure(0, weight=1) # Permite que el contenido se expanda horizontalmente
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Frame para el contenido de la tarjeta
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)
        content_frame.grid_rowconfigure(2, weight=1)


        # Título de la tarjeta
        self.title_label = ctk.CTkLabel(
            content_frame,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFFFFF"
        )
        self.title_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

        # Cantidad
        self.quantity_label = ctk.CTkLabel(
            content_frame,
            text=f"{quantity}",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#007bff" # Un color azul para la cantidad
        )
        self.quantity_label.grid(row=1, column=0, sticky="w", pady=(5, 10))

        # Icono
        if icon_path and os.path.exists(icon_path):
            try:
                # Carga la imagen y crea un CTkImage
                image = Image.open(icon_path)
                # Redimensiona el icono si es necesario, por ejemplo a 30x30
                icon_image = ctk.CTkImage(light_image=image, dark_image=image, size=(30, 30))
                self.icon_label = ctk.CTkLabel(content_frame, image=icon_image, text="")
                self.icon_label.grid(row=0, column=1, rowspan=2, sticky="ne") # Posiciona el icono arriba a la derecha
                content_frame.grid_columnconfigure(1, weight=0) # No expandir la columna del icono
            except Exception as e:
                print(f"Error al cargar el icono {icon_path}: {e}")
                self.icon_label = ctk.CTkLabel(content_frame, text="🖼️", font=ctk.CTkFont(size=24)) # Icono de fallback
                self.icon_label.grid(row=0, column=1, rowspan=2, sticky="ne")
        else:
            self.icon_label = ctk.CTkLabel(content_frame, text="🖼️", font=ctk.CTkFont(size=24)) # Icono de fallback
            self.icon_label.grid(row=0, column=1, rowspan=2, sticky="ne")


class CardDisplay(ctk.CTkFrame):
    """
    Un componente que muestra una colección de widgets Card.
    """
    def __init__(self, master, cards_info: list, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs) # Fondo transparente para el frame contenedor

        self.cards_info = cards_info
        self.cards = []

        self._create_cards()

    def _create_cards(self):
        """Crea y empaqueta los widgets Card basados en la información proporcionada."""
        for i, (title, quantity, icon) in enumerate(self.cards_info):
            card = Card(self, title, quantity, icon)
            # Usa grid para un diseño más flexible y responsivo
            card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
            self.grid_columnconfigure(i, weight=1) # Asegura que las columnas se expandan uniformemente
            self.cards.append(card)
