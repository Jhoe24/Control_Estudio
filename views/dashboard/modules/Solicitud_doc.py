import customtkinter as ctk
import tkinter as tk
import tkinter.messagebox as messagebox
import os
import webbrowser

from views.dashboard.components.SectionFrameBase import SectionFrameBase
from views.dashboard.components.widget_utils import *

class SolicitudDoc(SectionFrameBase):
    def __init__(self, master, controllers, rol, id, username):
        super().__init__(master, header_text="Solicitud de Documentos")
        self.master = master
        self.controllerEstudiante = controllers["Estudiantes"]
        self.controllerPNF = controllers["PNF"]
        self.controllerSolicitud = controllers["Solicitud"]
        self.controllerUser = controllers["Usuario"]
        self.controllerSede = controllers["Sedes"]
        self.controllerNotas = controllers["Notas"]
        self.rol = rol
        self.id = id
        self.username = username
        self.personaId = self.controllerUser.obtener_persona_id(self.username)

        card_btn_style = {
            "width": 250,
            "height": 100,
            "corner_radius": 16,
            "fg_color": "#23272f",
            #"hover_color": "#31343c",
            "text_color": "#fff",
            "font": ("Segoe UI", 16, "bold"),
            #"border_width": 2,
            #"border_color": "#444857"
        }

        # Contenedor principal para centrar los botones
        button_container = ctk.CTkFrame(self, fg_color="transparent")
        button_container.pack(pady=(40, 20), padx=20, fill="x", anchor="n")

        # --- Fila 1 ---
        row1 = ctk.CTkFrame(button_container, fg_color="transparent")
        row1.pack(pady=20)

        self.btn_cons_est = ctk.CTkButton(
            row1, text="Constancia de Estudios", 
            command=self.contanciaEstudio,
            **card_btn_style
        )
        self.btn_cons_est.pack(side="left", padx=20)

        self.btn_sit_academica = ctk.CTkButton(
            row1, text="Situación Académica", 
            command=self.situacionAcademica,
            **card_btn_style
        )
        self.btn_sit_academica.pack(side="left", padx=20)

        # --- Fila 2 ---
        row2 = ctk.CTkFrame(button_container, fg_color="transparent")
        row2.pack(pady=20)

        self.btn_hist_academico = ctk.CTkButton(
            row2, text="Historial Académico", 
            #command=...
            **card_btn_style
        )
        self.btn_hist_academico.pack(side="left", padx=20)

        self.btn_serv_comunitario = ctk.CTkButton(
            row2, text="Carta de Servicio Comunitario", 
            #command=...
            **card_btn_style
        )
        self.btn_serv_comunitario.pack(side="left", padx=20)

    def contanciaEstudio(self):
        if self.rol.lower() == "estudiante":
            frase_a_quitar = "Programa Nacional de Formación"
            datos = self.controllerEstudiante.modelo.obtener_datos_para_constancia(self.id)

            if not datos:
                messagebox.showerror("Error", "No se encontraron datos para la constancia.")
                return

            # Si la consulta principal no trajo datos de inscripción, busca en estudiante_pnf
            if not datos.get('pnf_nombre') or not datos.get('trayecto_nombre'):
                datos_faltantes = self.controllerEstudiante.modelo.obtener_datos_faltantes(self.id)
                if datos_faltantes:
                    # Actualiza el diccionario 'datos' con la información encontrada
                    datos.update(datos_faltantes)

            # Ahora, verifica y procesa el nombre del PNF de forma segura
            nombre_pnf = datos.get('pnf_nombre')
            if nombre_pnf and nombre_pnf.startswith(frase_a_quitar):
                datos['pnf_nombre'] = nombre_pnf.replace(frase_a_quitar, "").strip()

            if not datos.get('periodo_academico_nombre'):
                datos['periodo_academico_nombre']='Actual'

            #try:
                # El controlador devuelve la ruta del archivo generado
            ruta_docx = self.controllerSolicitud.generar_constancia(datos)

            if ruta_docx and os.path.exists(ruta_docx):
                messagebox.showinfo("Éxito", f"Constancia DOCX generada en:\n{ruta_docx}")

                # Intentar convertir a PDF
                ruta_pdf = self.controllerSolicitud.convertir_a_pdf(ruta_docx)
                if ruta_pdf and os.path.exists(ruta_pdf):
                    respuesta = messagebox.askyesno("Éxito", f"Constancia PDF generada en:\n{ruta_pdf}\n\n¿Desea abrir el archivo ahora?")
                    if respuesta:
                        # Abrir el archivo PDF en el navegador o visor predeterminado
                        webbrowser.open_new_tab(ruta_pdf)
                else:
                    messagebox.showwarning("Advertencia", "No se pudo convertir el archivo a PDF. Asegúrate de tener MS Word instalado.")
            else:
                messagebox.showerror("Error", "No se pudo generar el archivo de la constancia.")

    def situacionAcademica(self):
        if not self.personaId:
            messagebox.showerror("Error", "Ocurrió un error con inesperado")
            return
        dictDatosPersonales = self.controllerUser.obtener_datos_personales(self.personaId)
        if not dictDatosPersonales:
            messagebox.showerror("Error", "Ocurrió un error con inesperado")
            return
        
        datosPNF = self.controllerPNF.modelo.obtener_pnf_asignado(self.id)

        if not datosPNF:
            messagebox.showerror("Error", "Ocurrió un error con inesperado")
            return

        nombrePNF =  self.controllerPNF.modelo.obtener_nombres_por_id("pnf",datosPNF["pnf_id"])
        nombreSede = self.controllerSede.obtenerSedeEstudiante(self.id)
        
        dictDatosSolicitud = {
            'documento_identidad': dictDatosPersonales["documento_identidad"],
            'tipo_documento': "V" if dictDatosPersonales["nacionalidad"] == "Venezolano" else "E",
            'nombres': dictDatosPersonales["nombres"],
            'apellidos': dictDatosPersonales["apellidos"],
            'pnf_nombre':nombrePNF[0],
            'sede_nombre':nombreSede
        }

        # For para calcular el indiceAcademico
        listNotas = self.controllerNotas.obtener_lista_notas_historialAcademico(self.id)
        #print(listNotas)
        # For para calcular el promedio de las assistencias
        listaMapeada = []
        asistencia = 0
        for dicNotas in listNotas:
            if dicNotas["valor"]:
                asistencia = asistencia + dicNotas["valor"]
            listaMapeada.append({
                "periodo_academico":dicNotas['periodo_academico'],
                "nombre_trayecto":dicNotas['trayecto'],
                "nombre_unidad_curricular":dicNotas['unidad_curricular'],
                "nota":dicNotas['valor'],
                "asistencia":dicNotas['asistencia'],
                "unidades_credito":dicNotas['unidades_credito'],
            })
        dictDatosSolicitud["indiceAcademico"] = asistencia/len(listNotas)


        reporte_generator = self.controllerSolicitud.generarSituacionAcademica(dictDatosSolicitud, listaMapeada)
        ruta_pdf = reporte_generator.generar_pdf()

        # 4. Mostrar resultado y abrir el archivo
        if ruta_pdf:
            respuesta = messagebox.askyesno("Éxito", f"Situación Académica PDF generada en:\n{ruta_pdf}\n\n¿Desea abrir el archivo ahora?")
            if respuesta:
                # Abrir el archivo PDF en el navegador o visor predeterminado
                webbrowser.open_new_tab(ruta_pdf)
            return
        else:
            messagebox.showerror("Error", "Ocurrió un error con inesperado")
            return
           


    def historialAcademico(self):
        pass

    def servicioComunitario(self):
        pass
