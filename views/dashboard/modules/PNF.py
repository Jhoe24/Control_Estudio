import customtkinter as ctk
import tkinter.messagebox as messagebox
from views.dashboard.components.widget_utils import *
from views.dashboard.modules.forms.DatosPersonales import DatosPersonalesFrame
from views.dashboard.modules.forms.DatosUbicacion import DatosUbicacionFrame
from views.dashboard.modules.forms.PNF.FormPNF import DatosPNFPensumFrame
from views.dashboard.modules.forms.PNF.frameTrayecto import FrameTrayecto
import pprint


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

        self.dict_trayectos_invertido = {
            1: "I",
            2: "II",
            3: "III",
            4: "IV",
            5: "V"
        }

        self.dict_trayectos = {
            "I": 1,
            "II": 2,
            "III": 3,
            "IV": 4,
            "V": 5
        }
        
        try:
            toplevel = self.winfo_toplevel()
            self.vcmd_num_val = toplevel.register(self.controlador._solo_numeros)
            self.vcmd_fecha_val = toplevel.register(self.controlador._numeros_y_barras)
            self.vcmd_decimal_val = toplevel.register(self.controlador.solo_decimal)
        except Exception: # Fallback si no es un toplevel (ej. si el master es el root)
            self.vcmd_num_val = master.register(self.controlador._solo_numeros)
            self.vcmd_fecha_val = master.register(self.controlador._numeros_y_barras)
            self.vcmd_decimal_val = master.register(self.controlador._solo_decimal)


        # Instanciar los frames de sección, pasando las validaciones
        self.datos_pnf = DatosPNFPensumFrame(self, self.vcmd_num_val, self.vcmd_fecha_val)

        for entry in self.datos_pnf.entries_a_validar:
            entry.bind("<KeyRelease>", lambda event: self.validar_campos_trayecto())
        
        self.button_siguiente = ctk.CTkButton(
            self,
            text="Grabar trayecto",
            width=140,
            font=FUENTE_BOTON,
            fg_color=COLOR_BOTON_PRIMARIO_FG,
            hover_color=COLOR_BOTON_PRIMARIO_HOVER,
            text_color=COLOR_BOTON_PRIMARIO_TEXT,
            command=self.comando_trayecto,
            state="disabled"  # Deshabilitar al inicio
        )
        self.button_siguiente.pack(pady=(20, 0))

        # Empacar los frames
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=(25, 20))

        self.btn_guardar = ctk.CTkButton(self.button_frame, text="Grabar Datos", width=140, command=self.obtener_datos_trayecto,
                                        font=FUENTE_BOTON, fg_color=COLOR_BOTON_SECUNDARIO_FG, hover_color=COLOR_BOTON_PRIMARIO_HOVER, text_color=COLOR_BOTON_PRIMARIO_TEXT,
                                        state="disabled")
        self.btn_guardar.pack(side="left", padx=10)

        self.btn_cancelar = ctk.CTkButton(self.button_frame, text="Limpiar Campos", width=140, command=self.limpiar_formulario_completo,
                                        font=FUENTE_BOTON, fg_color=COLOR_BOTON_SECUNDARIO_FG, hover_color=COLOR_BOTON_SECUNDARIO_HOVER, text_color=COLOR_BOTON_SECUNDARIO_TEXT,
                                        state="normal")
        self.btn_cancelar.pack(side="left", padx=10)
      
       
        
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

    def comando_trayecto(self):
        # Verificar_codigo
        codigo = self.datos_pnf.codigo_entry.get().strip()
        if self.controlador.existe_codigo(codigo):
            messagebox.showerror("Error", "El código ingresado ya existe. Por favor, ingrese un código único.")
            return
        codigo_nacional = self.datos_pnf.codigo_nacional_entry.get().strip()
        if self.controlador.existe_codigo_nacional(codigo_nacional):
            messagebox.showerror("Error", "El código nacional ingresado ya existe. Por favor, ingrese un código único.")
            return
        self.datos_pnf.deshabilitar_campos()
        self.actualizar_cantidad_trayecto()
    
    def actualizar_cantidad_trayecto(self):
        self.datos_cantidad_trayecto = self.datos_pnf.get_trayecto()
        
        if self.listado_trayectos:
            for frame in self.listado_trayectos:
                frame.destroy()
        self.listado_trayectos = []

        if self.datos_cantidad_trayecto > 0:
            for i in range(self.datos_cantidad_trayecto):
                self.listado_trayectos.append(FrameTrayecto(self, self.controlador, self.vcmd_num_val, self.vcmd_fecha_val, titulo=f"Trayecto #{i+1}"))

                self.listado_trayectos[i].pack(fill="x", padx=10, pady=(10, 0))

                
        # SIEMPRE repack el frame de botones al final
        self.btn_guardar.configure(state="normal")
        self.button_frame.pack_forget()
        self.button_frame.pack(pady=(25, 20))
    
    def obtener_datos_trayecto(self):
        list_dic_trayectos = []
        if self.listado_trayectos:
            for frame_trayectos in self.listado_trayectos:
                list_dic_trayectos.append(frame_trayectos.obtener_datos_trayectos())
        
        dato_completos = self.controlador.getPNF(self.datos_pnf,list_dic_trayectos)
        if dato_completos:
            self.controlador.registrar_pnf(dato_completos,self)
        print("Datos del PNF:", dato_completos)
    
    def validar_campos_trayecto(self):
    # Verifica que todos los entries tengan datos
        todos_llenos = all(entry.get().strip() for entry in self.datos_pnf.entries_a_validar)
        fecha_ok = self.datos_pnf.fecha_resolucion is not None and str(self.datos_pnf.fecha_resolucion).strip() != ""
        if todos_llenos and fecha_ok:
            self.button_siguiente.configure(state="normal", fg_color=COLOR_BOTON_PRIMARIO_FG, hover_color=COLOR_BOTON_PRIMARIO_HOVER)
        else:
            self.button_siguiente.configure(state="disabled")
    
    def actualizar_cantidad_trayecto(self):
        self.datos_cantidad_trayecto = self.datos_pnf.get_trayecto()
        
        if self.listado_trayectos:
            for frame in self.listado_trayectos:
                frame.destroy()
        self.listado_trayectos = []

        if self.datos_cantidad_trayecto > 0:
            for i in range(self.datos_cantidad_trayecto):
                self.listado_trayectos.append(FrameTrayecto(self, self.controlador, self.vcmd_num_val, self.vcmd_fecha_val, titulo=f"Trayecto #{i+1}"))
                self.listado_trayectos[i].numero_entry.insert(0,i+1)
                self.listado_trayectos[i].nombre_entry.insert(0,f"Trayecto {self.dict_trayectos_invertido[i+1]}")
                self.listado_trayectos[i].nombre_entry.configure(state="disabled")
                self.listado_trayectos[i].numero_entry.configure(state="disabled")
                self.listado_trayectos[i].numero_tramos_menu.set(str(self.dict_trayectos[self.datos_pnf.duracion_tramos_entry.get()]))  
                self.listado_trayectos[i].numero_tramos_menu.configure(state="disabled")
                self.listado_trayectos[i].pack(fill="x", padx=10, pady=(10, 0))
                
        # Habilita los botones después de grabar trayecto
        self.btn_guardar.configure(state="normal")
        self.btn_cancelar.configure(state="normal")
        self.button_frame.pack_forget()
        self.button_frame.pack(pady=(25, 20))

    def validar_todo_completo(self):
        # Verifica campos principales
        todos_llenos = all(entry.get().strip() for entry in self.datos_pnf.entries_a_validar)
        fecha_ok = self.datos_pnf.fecha_resolucion is not None and str(self.datos_pnf.fecha_resolucion).strip() != ""
        # Verifica trayectos
        trayectos_ok = True
        if self.listado_trayectos:
            for frame in self.listado_trayectos:
                if not frame.todos_campos_llenos():  
                    trayectos_ok = False
                    break
        # Habilita o deshabilita el botón
        if todos_llenos and fecha_ok and trayectos_ok and self.listado_trayectos != []:
            self.btn_guardar.configure(state="normal")
        else:
            self.btn_guardar.configure(state="disabled")

    

    def limpiar_formulario_completo(self):
        """
        Limpia todos los campos del formulario.
        """
        if self.listado_trayectos:
            self.datos_pnf.limpiar_fomulario()
            for trayecto in self.listado_trayectos:
                trayecto.destroy()
            self.listado_trayectos = []
            self.datos_cantidad_trayecto = 0
            self.button_siguiente.configure(state="disabled")
            self.btn_guardar.configure(state="disabled")
        self.datos_pnf.limpiar_fomulario()
        self._parent_canvas.yview_moveto("0.0")
           