import customtkinter as ctk
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase

class ListaAsignacionUC(ctk.CTkFrame):
    def __init__(self, master, controller_pnf, docente):
        super().__init__(master, fg_color="white")
        self.controller_pnf = controller_pnf
        self.docente = docente

        docente_id = self.docente.get("id")
        # Obtener el PNF asignado al docente
        pnf_asignados = self.controller_pnf.modelo.obtener_nombre_pnf_asignado_docente(docente_id)
        if not pnf_asignados or len(pnf_asignados) == 0:
            label = ctk.CTkLabel(self, text="El docente no tiene PNF asignado.", text_color="black")
            label.pack(pady=20)
            self.pack(fill="both", expand=True)
            return
        
        # tomar el primer pnf asignado
        pnf_id = pnf_asignados[0]['pnf_id']
        nombre_pnf = pnf_asignados[0].get('nombre_pnf', 'Desconocido')

        # buscar las UC asociadas 
        unidades_curriculares = self.controller_pnf.obtener_uc_por_pnf(pnf_id)

        label = ctk.CTkLabel(self, text=f"Unidades Curriculares del PNF: {nombre_pnf}", text_color="black", font=("Roboto", 16))
        label.pack(pady=10)

        self.uc_vars = []
        for uc in unidades_curriculares:
            var = ctk.BooleanVar()
            chk = ctk.CTkCheckBox(self, text=uc['nombre'], variable=var, text_color="black")
            chk.pack(anchor="w", padx=20)
            self.uc_vars.append((uc, var))

        btn_inscribir = ctk.CTkButton(
            self, 
            text="Inscribir Docente en U.C.", 
            command=self.inscribir_docente_uc)
        btn_inscribir.pack(pady=20)

        self.pack(fill="both", expand=True)

    def inscribir_docente_uc(self):
        seleccionadas = [uc for uc, var in self.uc_vars if var.get()]
        # preguntar
        print(f"Docente inscrito en las siguientes UC: {[uc['nombre'] for uc in seleccionadas]}")
        