import tkinter.messagebox as messagebox
import customtkinter as ctk
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase
from ..DatosPersonales import DatosPersonalesFrame

class FrameNotaEstudiante(SectionFrameBase):
    def __init__(self, master, controller_estudiante, tupla, unidad_curricular_id, solo_lectura=False):
        super().__init__(master, header_text="Gestión de Notas de Estudiantes", fg_color_label=COLOR_HEADER_SECCION_BG_2)
        self.controller_estudiante = controller_estudiante
        self.unidad_curricular_id = unidad_curricular_id
        self.solo_lectura = solo_lectura
        self.seccion_id = tupla[5]  # id de la sección que esta en la posicion de la tupla nuemero 5 
        #print("\n\n=========================================================")
        #print(f'tupla es :{tupla}')
        #print(f"seccion_id recibido: {self.seccion_id}")
        self.lista_estudiantes = self.controller_estudiante.obtener_estudiantes_por_seccion(self.seccion_id)
        #print(f"lista_estudiantes obtenida: {self.lista_estudiantes}")
        
        # si la lista de estudiantes está vacía, mostrar un mensaje
        # y no continuar con la carga de notas
        if self.lista_estudiantes == []:
            label = ctk.CTkLabel(self, text="No hay estudiantes inscritos en esta sección.", font=FUENTE_LABEL_CAMPO, text_color=COLOR_TEXTO_PRINCIPAL)
            label.pack(pady=20, padx=20, anchor="w")
        # si la lista de estudiantes no está vacía, es decir di hay datos, entonces
        # crear los frames para cada estudiante
        elif self.lista_estudiantes != []:   
            self.frames_estudiantes = []
            self.cargar_o_ver_notas_estudiante()
            

    def cargar_o_ver_notas_estudiante(self):
        """Crear frame por estudiante para cargar notas"""

        self.frame_tabla = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        # Encabezado (fila 0)
        headers = ["Documento", "Nombres", "Nota", "Acción"]
        for col, header in enumerate(headers):
            celda = ctk.CTkFrame(self.frame_tabla, fg_color="#e0e0e0", corner_radius=4)
            celda.grid(row=0, column=col, padx=1, pady=1, sticky="nsew")
            label = ctk.CTkLabel(celda, text=header, font=ctk.CTkFont(weight="bold"), text_color="#222")
            label.pack(padx=10, pady=5)
        for i in range(len(headers)):
            self.frame_tabla.grid_columnconfigure(i, weight=1)

        self.filas_datos = []

        # Listar Estudiantes (desde la fila 1)
        for i, estudiante in enumerate(self.lista_estudiantes, start=1):
            fila_widgets = []
            # Documento
            fila_widgets.append(self._crear_celda_tabla(i, 0, estudiante['documento_identidad']))
            # Nombres
            fila_widgets.append(self._crear_celda_tabla(i, 1, estudiante['nombres']))

            # Nota (Entry en celda)
            celda_nota = ctk.CTkFrame(self.frame_tabla, fg_color="#f5f5f5", corner_radius=4)
            celda_nota.grid(row=i, column=2, padx=1, pady=1, sticky="nsew")

            vcmd = self.register(solo_decimal)
            entry_nota = ctk.CTkEntry(
                celda_nota, width=80, fg_color=COLOR_ENTRY_BG,
                text_color=COLOR_TEXTO_PRINCIPAL, font=FUENTE_LABEL_CAMPO,
                validate = "key", validatecommand = (vcmd, "%P")
            )
            entry_nota.pack(padx=10, pady=5)
            # Si es solo lectura, mostrar la nota y deshabilitar
            inscripcion_id = self.controller_estudiante.obtener_inscripcion_id(estudiante['id'], self.seccion_id)

            valor = self.controller_estudiante.obtener_nota(inscripcion_id, self.unidad_curricular_id)
            state_actualizar = "disabled"
            state_guardar = "normal"

            if valor:
                entry_nota.insert(0, valor)
                entry_nota.configure(state="disabled", border_color=COLOR_HEADER_SECCION_BG_2)
                state_actualizar = "normal"
                state_guardar = "disabled"
                
                
            # if self.solo_lectura:
            #     valor = str(self.controller_estudiante.obtener_nota(inscripcion_id, self.unidad_curricular_id) or "No asignada")
            #     entry_nota.insert(0, valor)
            #     entry_nota.configure(state="disabled")

            fila_widgets.append(celda_nota)

            # Acción (botón)
            celda_btn = ctk.CTkFrame(self.frame_tabla, fg_color="#f5f5f5", corner_radius=4)
            celda_btn.grid(row=i, column=3, padx=1, pady=1, sticky="nsew")
            # Frame interno para centrar los botones
            frame_botones = ctk.CTkFrame(celda_btn, fg_color="transparent")
            frame_botones.pack(expand=True)

            if not self.solo_lectura:
                btn_guardar = ctk.CTkButton(
                    frame_botones,
                    width=110,
                    text="Cargar Nota",
                    state=state_guardar,
                    command=lambda e=entry_nota, insc_id=inscripcion_id: self.guardar_nota(insc_id, self.unidad_curricular_id, e)
                )
                btn_update = ctk.CTkButton(
                    frame_botones,
                    width=110,
                    text="Actualizar Nota",
                    state=state_actualizar,
                    fg_color=COLOR_BOTON_FONDO,
                    hover_color=COLOR_BOTON_FONDO_HOVER,
                    command=lambda btn = btn_guardar, ent = entry_nota: self.habilitar_carga_notas(btn,ent)
                )
                btn_guardar.pack(side="left", padx=(0, 4), pady=5)
                btn_update.pack(side="left", pady=5)
            fila_widgets.append(celda_btn)

            self.filas_datos.append(fila_widgets)
        

    def guardar_nota(self, inscripcion_id, unidad_curricular_id, entry_widget):
        valor = entry_widget.get()
        if valor == "":
            messagebox.showerror("Error","El campo esta vacio",parent=self)
            return
        try:
            valor = float(valor)
            self.controller_estudiante.guardar_nota(inscripcion_id, unidad_curricular_id, valor)
            messagebox.showinfo("Éxito", "Nota guardada correctamente",parent=self)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la nota: {e}",parent=self)

    def _crear_celda_tabla(self, row, col, texto):
        celda = ctk.CTkFrame(self.frame_tabla, fg_color="#f5f5f5", corner_radius=4)
        celda.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
        label = ctk.CTkLabel(celda, text=texto, text_color="#222")
        label.pack(padx=10, pady=5)
        return celda
    
    def habilitar_carga_notas(self,btn_guardar,entry_nota):
        btn_guardar.configure(state="normal")
        entry_nota.configure(state="normal")