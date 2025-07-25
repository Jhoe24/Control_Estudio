import tkinter.messagebox as messagebox
import customtkinter as ctk
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase
from ..DatosPersonales import DatosPersonalesFrame

class FrameNotaEstudiante(SectionFrameBase):
    def __init__(self, master, controller_estudiante, tupla, unidad_curricular_id):
        super().__init__(master, header_text="Gestión de Notas de Estudiantes")
        self.controller_estudiante = controller_estudiante
        self.unidad_curricular_id = unidad_curricular_id
        self.seccion_id = tupla[5]  # id de la sección que esta en la posicion de la tupla nuemero 5 
        print("\n\n=========================================================")
        print(f'tupla es :{tupla}')
        print(f"seccion_id recibido: {self.seccion_id}")
        self.lista_estudiantes = self.controller_estudiante.obtener_estudiantes_por_seccion(self.seccion_id)
        print(f"lista_estudiantes obtenida: {self.lista_estudiantes}")
        
        # si la lista de estudiantes está vacía, mostrar un mensaje
        # y no continuar con la carga de notas
        if self.lista_estudiantes == []:
            label = ctk.CTkLabel(self, text="No hay estudiantes inscritos en esta sección.", font=FUENTE_LABEL_CAMPO, text_color=COLOR_TEXTO_PRINCIPAL)
            label.pack(pady=20, padx=20, anchor="w")
        # si la lista de estudiantes no está vacía, es decir di hay datos, entonces
        # crear los frames para cada estudiante
        elif self.lista_estudiantes != []:   
            self.frames_estudiantes = []
            self.cargar_notas_estudiante()
            

    def cargar_notas_estudiante(self):
        """Crear frame por estudiante para cargar notas"""

        for idx, estudiante in enumerate(self.lista_estudiantes):
            frame = ctk.CTkFrame(self, fg_color="white", corner_radius=8)
            frame.pack(fill="x", padx=10, pady=5)

            # Grid horizontal para cada elemento
            frame.grid_columnconfigure(0, weight=0)
            frame.grid_columnconfigure(1, weight=1)
            frame.grid_columnconfigure(2, weight=0)
            frame.grid_columnconfigure(3, weight=0)
            frame.grid_columnconfigure(4, weight=0)

            # Labels
            label_documento = ctk.CTkLabel(frame, text=f"Documento: {estudiante['documento_identidad']}",font=FUENTE_LABEL_CAMPO, text_color=COLOR_TEXTO_PRINCIPAL, anchor="w")
            label_documento.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="w")

            label_nombre = ctk.CTkLabel(frame, text=f"Nombres: {estudiante['nombres']}",font=FUENTE_LABEL_CAMPO, text_color=COLOR_TEXTO_PRINCIPAL, anchor="w")
            label_nombre.grid(row=0, column=1, padx=(20, 5), pady=10, sticky="w")

            label_nota = ctk.CTkLabel(frame, text="Ingrese Nota:",font=FUENTE_LABEL_CAMPO, text_color=COLOR_TEXTO_PRINCIPAL, anchor="w")
            label_nota.grid(row=0, column=3, padx=5, pady=10, sticky="w")

            # Entry para nota
            entry_nota = ctk.CTkEntry(frame, width=80, fg_color=COLOR_ENTRY_BG, text_color=COLOR_TEXTO_PRINCIPAL,font=FUENTE_LABEL_CAMPO)
            entry_nota.grid(row=0, column=4, padx=5, pady=10, sticky="w")

            # Buscar inscripcion_id para este estudiante y sección
            inscripcion_id = self.controller_estudiante.obtener_inscripcion_id(estudiante['id'], self.seccion_id)
            print(f"Inscripción ID para {estudiante['nombres']}: {inscripcion_id}")
            
            btn_guardar = ctk.CTkButton(
                frame, width=150, text="Cargar Nota",
                command=lambda e=entry_nota, insc_id=inscripcion_id: self.guardar_nota(insc_id, self.unidad_curricular_id, e)
            )
            btn_guardar.grid(row=0, column=5, padx=10, pady=10, sticky="w")

        #label = Documento    label = Nombre del estudiante    label = ingrese nota : entry    boton: cargar notas

    def guardar_nota(self, inscripcion_id, unidad_curricular_id, entry_widget):
        valor = entry_widget.get()
        try:
            valor = float(valor)
            self.controller_estudiante.guardar_nota(inscripcion_id, unidad_curricular_id, valor)
            messagebox.showinfo("Éxito", "Nota guardada correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la nota: {e}")
