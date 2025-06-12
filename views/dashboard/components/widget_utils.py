import customtkinter as ctk
import tkinter as tk
from tkcalendar import Calendar

# --- CONSTANTES DE COLOR Y FUENTE ---
COLOR_FONDO_FORMULARIO = "white"
COLOR_TEXTO_PRINCIPAL = "#212529"
COLOR_TEXTO_SECUNDARIO = "#495057"
COLOR_HEADER_SECCION_BG = "#e9ecef"
COLOR_HEADER_SECCION_TEXT = "#343a40"
COLOR_ENTRY_BG = "#FFFFFF"
COLOR_ENTRY_BORDER = "#ced4da"
COLOR_ENTRY_TEXT = "#212529"
COLOR_ENTRY_PLACEHOLDER = "#6c757d"
COLOR_BOTON_PRIMARIO_FG = "#007bff"
COLOR_BOTON_PRIMARIO_HOVER = "#0056b3"
COLOR_BOTON_PRIMARIO_TEXT = "white"
COLOR_BOTON_SECUNDARIO_FG = "#6c757d"
COLOR_BOTON_SECUNDARIO_HOVER = "#545b62"
COLOR_BOTON_SECUNDARIO_TEXT = "white"

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
    return ctk.CTkOptionMenu(master, font=FUENTE_BASE, fg_color=COLOR_ENTRY_BG, button_color=COLOR_BOTON_PRIMARIO_FG, text_color=COLOR_ENTRY_TEXT, dropdown_fg_color=COLOR_ENTRY_PLACEHOLDER, **kwargs)

def crear_check_box(master, **kwargs):
    return ctk.CTkCheckBox(master, font=FUENTE_BASE, text_color=COLOR_TEXTO_PRINCIPAL, border_color=COLOR_ENTRY_BORDER, **kwargs)

def crear_radio_button(master, **kwargs):
    return ctk.CTkRadioButton(master, font=FUENTE_BASE, text_color=COLOR_TEXTO_PRINCIPAL, border_color=COLOR_ENTRY_BORDER, fg_color=COLOR_BOTON_PRIMARIO_FG, hover_color=COLOR_BOTON_PRIMARIO_HOVER, **kwargs)
