import customtkinter as ctk
import tkinter.messagebox as messagebox
from views.dashboard.components.widget_utils import *
from views.dashboard.modules.forms.DatosPersonales import DatosPersonalesFrame
from views.dashboard.modules.forms.DatosUbicacion import DatosUbicacionFrame
from views.dashboard.modules.forms.PNF.FormPNF import DatosPNFPensumFrame
from views.dashboard.modules.forms.PNF.frameTrayecto import FrameTrayecto
from views.dashboard.modules.forms.PNF.frameTramos import FrameTramos

from config.app_config import AppConfig

class FormularioPNFPensumView(ctk.CTkScrollableFrame):

    def __init__(self, master, controlador):
        super().__init__(master, fg_color=COLOR_FONDO_FORMULARIO, label_text="")
        self.master = master
        self.controlador = controlador
        self.datos_pnf = None
        self.datos_trayecto = None
        self.datos_cantidad_trayecto = 0
        self.listado_trayectos = []
        self.evento_mouse()
        
        try:
            toplevel = self.winfo_toplevel()
            self.vcmd_num_val = toplevel.register(self.controlador._solo_numeros)
            self.vcmd_fecha_val = toplevel.register(self.controlador._numeros_y_barras)
            self.vcmd_decimal_val = toplevel.register(self.controlador._solo_decimal)
        except Exception: # Fallback si no es un toplevel (ej. si el master es el root)
            self.vcmd_num_val = master.register(self.controlador._solo_numeros)
            self.vcmd_fecha_val = master.register(self.controlador._numeros_y_barras)
            self.vcmd_decimal_val = master.register(self.controlador._solo_decimal)


        # Instanciar los frames de sección, pasando las validaciones
        self.datos_pnf = DatosPNFPensumFrame(self, self.vcmd_num_val, self.vcmd_fecha_val)
        
        print(self.datos_pnf.get_trayecto())
        button_siguiente = ctk.CTkButton(
            self,
            text="Grabar trayecto",
            width=140,
            font=FUENTE_BOTON,
            fg_color=COLOR_BOTON_PRIMARIO_FG,
            hover_color=COLOR_BOTON_PRIMARIO_HOVER,
            text_color=COLOR_BOTON_PRIMARIO_TEXT,
            command=self.actualizar_cantidad_trayecto
        )
        button_siguiente.pack(pady=(20, 0))

        # Empacar los frames
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=(25, 20))

        self.btn_guardar = ctk.CTkButton(self.button_frame, text="Grabar Datos", width=140,#command=self.procesar_formulario,
                                        font=FUENTE_BOTON, fg_color=COLOR_BOTON_PRIMARIO_FG, hover_color=COLOR_BOTON_PRIMARIO_HOVER, text_color=COLOR_BOTON_PRIMARIO_TEXT)
        self.btn_guardar.pack(side="left", padx=10)

        self.btn_cancelar = ctk.CTkButton(self.button_frame, text="Limpiar Campos", width=140, #command=self.limpiar_formulario_completo,
                                        font=FUENTE_BOTON, fg_color=COLOR_BOTON_SECUNDARIO_FG, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, text_color=COLOR_BOTON_SECUNDARIO_TEXT)
        self.btn_cancelar.pack(side="left", padx=10)
        self.btn_guardar.configure(state="desabled")  # Deshabilitar el botón de guardar al inicio
        
        
    def evento_mouse(self):
        # Accede al canvas interno de CTkScrollableFrame
        canvas = self._parent_canvas  # atributo privado, pero funciona
        # Para Windows y Mac
        canvas.bind_all("<MouseWheel>", self.movimiento_mouse)
        # Para Linux
        canvas.bind_all("<Button-4>", self.movimiento_mouse)
        canvas.bind_all("<Button-5>", self.movimiento_mouse)
    
    def movimiento_mouse(self, event):
        
        canvas = self._parent_canvas
        if event.num == 4:  # Linux scroll up
            canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # Linux scroll down
            canvas.yview_scroll(1, "units")
        else:  # Windows/Mac
            canvas.yview_scroll(int(-1*(event.delta/2)), "units")
    
    def actualizar_cantidad_trayecto(self):
        self.datos_cantidad_trayecto = self.datos_pnf.get_trayecto()
        
        if self.listado_trayectos:
            for frame in self.listado_trayectos:
                frame.destroy()
        self.listado_trayectos = []

        if self.datos_cantidad_trayecto > 0:
            for i in range(self.datos_cantidad_trayecto):
                self.listado_trayectos.append(FrameTrayecto(self, self.vcmd_num_val, self.vcmd_fecha_val, titulo=f"Trayecto #{i+1}"))
                self.listado_trayectos[i].pack(fill="x", padx=10, pady=(10, 0))

                

        # SIEMPRE repack el frame de botones al final
        self.btn_guardar.configure(state="normal")
        self.button_frame.pack_forget()
        self.button_frame.pack(pady=(25, 20))
    
    