from tkcalendar import Calendar
import customtkinter as ctk
import tkinter as tk
from tkcalendar import Calendar
import re

# --- CONSTANTES DE COLOR Y FUENTE ---
COLOR_FONDO_FORMULARIO = "white"
COLOR_TEXTO_PRINCIPAL = "#212529"
COLOR_TEXTO_SECUNDARIO = "#495057"
COLOR_HEADER_SECCION_BG = "#e9ecef"
COLOR_HEADER_SECCION_BG_2 = "#64da7e" 
COLOR_HEADER_SECCION_TEXT = "#343a40"
COLOR_ENTRY_BG = "#FFFFFF"
COLOR_ENTRY_BORDER = "#ced4da"
COLOR_ENTRY_TEXT = "#212529"
COLOR_ENTRY_PLACEHOLDER = "#6c757d"
COLOR_BOTON_PRIMARIO_FG = "#007bff"
COLOR_BOTON_FONDO = "#bf2121"
COLOR_BOTON_FONDO2 = "#d4e725"
COLOR_BOTON_FONDO_HOVER = "#b15c5c"
COLOR_BOTON_PRIMARIO_HOVER = "#0056b3"
COLOR_BOTON_PRIMARIO_TEXT = "white"
COLOR_BOTON_SECUNDARIO_FG = "#6c757d"
COLOR_BOTON_SECUNDARIO_HOVER = "#545b62"
COLOR_BOTON_SECUNDARIO_TEXT = "white"
COLOR_AVERTENCIA_TEXT = "#c74511"

FUENTE_BASE = ("Roboto", 13)
FUENTE_TITULO_FORMULARIO = ("Roboto", 18, "bold")
FUENTE_HEADER_SECCION = ("Roboto", 14, "bold")
FUENTE_LABEL_CAMPO = ("Roboto", 13)
FUENTE_BOTON = ("Roboto", 13, "bold")

PADX_LABEL = (0, 5)
PADX_ENTRY = (0, 0)
PADY_FILA = (5, 5)

# --- Funciones creadoras de widgets ---
def crear_entry(master, **kwargs):
    return ctk.CTkEntry(master, font=FUENTE_BASE, text_color=COLOR_ENTRY_TEXT, fg_color=COLOR_ENTRY_BG, border_color=COLOR_ENTRY_BORDER, placeholder_text_color=COLOR_ENTRY_PLACEHOLDER, **kwargs)

def crear_option_menu(master, **kwargs):
    return ctk.CTkOptionMenu(master,font=FUENTE_BASE, fg_color=COLOR_ENTRY_BG, button_color=COLOR_BOTON_PRIMARIO_FG, text_color=COLOR_ENTRY_TEXT, dropdown_fg_color=COLOR_ENTRY_PLACEHOLDER, **kwargs)

def crear_check_box(master, **kwargs):
    return ctk.CTkCheckBox(master, font=FUENTE_BASE, text_color=COLOR_TEXTO_PRINCIPAL, border_color=COLOR_ENTRY_BORDER, **kwargs)

def crear_radio_button(master, **kwargs):
    return ctk.CTkRadioButton(master, font=FUENTE_BASE, text_color=COLOR_TEXTO_PRINCIPAL, border_color=COLOR_ENTRY_BORDER, fg_color=COLOR_BOTON_PRIMARIO_FG, hover_color=COLOR_BOTON_PRIMARIO_HOVER, **kwargs)

def create_option_menu_row(parent_frame, label_text, options, variable, width=350, font_size=15, funcion = None, side_ = "right", fill_ = "x",crear_frame = True, text_color_=COLOR_TEXTO_PRINCIPAL):
    """
    Crea una fila con una etiqueta y un CTkOptionMenu con tamaños ajustados.
    """
    if crear_frame:
        frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        frame.pack(pady=10, fill="x", anchor="center")
    else:
        frame = parent_frame

    # Fuente para la etiqueta
    label_font = ("Roboto", font_size) # Usar la misma fuente y tamaño que el optionmenu para consistencia

    label = ctk.CTkLabel(frame, text=label_text, font=label_font,text_color=text_color_)
    label.pack(side="left", padx=(20, 10)) # Aumentar padx para más espacio horizontal

    # Fuente para el OptionMenu
    optionmenu_font = ("Roboto", font_size)

    if funcion:
        optionmenu = ctk.CTkOptionMenu(
            frame,
            values=options,
            variable=variable,
            command=funcion,
            width=width,  # Aumentar el ancho fijo para los OptionMenu
            height=font_size + 20, # Aumentar la altura basada en el tamaño de la fuente
            font=optionmenu_font,
            dropdown_font=optionmenu_font, # También el tamaño de la fuente del desplegable
            dropdown_fg_color=("lightgray", "gray25"),
            dropdown_hover_color=("gray75", "gray40"),
            dropdown_text_color=("black", "white"),
            fg_color="SkyBlue",
            button_color="#1074ad",
            button_hover_color="steelblue",
            text_color="black",
            corner_radius=8, # Un poco más redondeado para un look más moderno si lo deseas
        )
    else:
        optionmenu = ctk.CTkOptionMenu(
        frame,
        values=options,
        variable=variable,
        width=width,  # Aumentar el ancho fijo para los OptionMenu
        height=font_size + 20, # Aumentar la altura basada en el tamaño de la fuente
        font=optionmenu_font,
        dropdown_font=optionmenu_font, # También el tamaño de la fuente del desplegable
        dropdown_fg_color=("lightgray", "gray25"),
        dropdown_hover_color=("gray75", "gray40"),
        dropdown_text_color=("black", "white"),
        fg_color="SkyBlue",
        button_color="#1074ad",
        button_hover_color="steelblue",
        text_color="black",
        corner_radius=8, # Un poco más redondeado para un look más moderno si lo deseas
        )

    optionmenu.pack(side=side_, expand=False, fill=fill_, padx=(0, 10)) # Aumentar padx en el lado derecho del optionmenu

    return optionmenu

def solo_decimal(new_text):
        """
        Función de validación para asegurar que solo se ingresen números (enteros o reales).
        Permite:
        - Dígitos (0-9)
        - Un punto decimal opcional
        - Un signo negativo opcional al principio
        - Cadena vacía (para permitir borrar el contenido)
        """
        if new_text == "":  # Permite borrar el contenido del entry
            return True
        
        # Expresión regular para números enteros o flotantes
        # ^: inicio de la cadena
        # -?: un signo negativo opcional
        # \d+: uno o más dígitos
        # (\.\d*)?: un punto seguido de cero o más dígitos, opcionalmente
        # $: fin de la cadena
        pattern = r"^-?\d*\.?\d*$"
        
        if re.fullmatch(pattern, new_text):
            return True
        else:
            return False


def solo_numeros(new_text):
        if new_text == "":  # Permite borrar el contenido del entry
                return True
        
        pattern = r"^\d+$"
            
        if re.fullmatch(pattern, new_text):
            return True
        else:
            return False