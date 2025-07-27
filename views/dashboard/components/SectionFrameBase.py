import customtkinter as ctk
from .widget_utils import *

class SectionFrameBase(ctk.CTkFrame):

    def __init__(self, master, header_text, fg_color_label=COLOR_HEADER_SECCION_BG):
        super().__init__(master, fg_color="transparent")
        self.pack(fill="x", pady=(0, 15), padx=10, expand="True")

        if header_text:
            header_label = ctk.CTkLabel(self, text=f" {header_text} ", text_color=COLOR_HEADER_SECCION_TEXT,
                                        fg_color=fg_color_label, font=FUENTE_HEADER_SECCION,
                                        height=30, corner_radius=6)
            header_label.pack(fill="x", pady=(0, 10), padx=0)

    def _crear_fila_widgets(self, widgets_info):
        frame_fila = ctk.CTkFrame(self, fg_color="transparent")
        frame_fila.pack(fill="x", pady=PADY_FILA, padx=15)

        col_index = 0
        for label_text, widget_creator_func, widget_creator_args, widget_span in widgets_info:
            widget_obj = widget_creator_func(frame_fila, **widget_creator_args)

            if label_text:
                label = ctk.CTkLabel(frame_fila, text=label_text, font=FUENTE_LABEL_CAMPO, text_color=COLOR_TEXTO_PRINCIPAL, anchor="w")
                label.grid(row=0, column=col_index, sticky="w", padx=PADX_LABEL)
                col_index += 1

            widget_obj.grid(row=0, column=col_index, sticky="ew", columnspan=widget_span, padx=PADX_ENTRY)
            col_index += widget_span

            if widget_span > 0 :
                for i in range(widget_span):
                    frame_fila.grid_columnconfigure(col_index - widget_span + i, weight=1 if widget_span > 1 else 0)
