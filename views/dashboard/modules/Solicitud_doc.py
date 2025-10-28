import customtkinter as ctk
from tkinter import filedialog
import tkinter as tk
import tkinter.messagebox as messagebox
import os
import shutil
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

        ctk.CTkLabel(
            button_container,
            text="Plantillas de Servicio Comunitario",
            font=("Segoe UI", 16, "bold"),
            text_color=COLOR_TEXTO_PRINCIPAL
        ).pack(pady=(20, 0))

        # --- Fila 2 ---
        row2 = ctk.CTkFrame(button_container, fg_color="transparent")
        row2.pack(pady=10)

        self.btn_serv_comunitario = ctk.CTkButton(
            row2, text="Planilla de inscripción\nServicio Comunitario", 
            command=self.plantillaIncripcionServiCumuni,
            **card_btn_style
        )
        self.btn_serv_comunitario.pack(side="left", padx=20)

        self.btn_infomeFinal = ctk.CTkButton(
            row2, text="Informe Final de Servicio\nComunitario", 
            command=self.informeFinalSC,
            **card_btn_style
        )
        self.btn_infomeFinal.pack(side="left", padx=20)

        #---- Fila 3 ---
        row3 = ctk.CTkFrame(button_container, fg_color="transparent")
        row3.pack(pady=10)

        self.btn_informe_avances_sc = ctk.CTkButton(
            row3, text="Informe de avance de\nServicio Comunitario", 
            command=self.informeAvanceSC,
            **card_btn_style
        )
        self.btn_informe_avances_sc.pack(side="left", padx=20)

        self.btn_control_actividades = ctk.CTkButton(
            row3, text="Control de actividades de\nServicio Comunitario", 
            command=self.controlActividadesSC,
            **card_btn_style
        )
        self.btn_control_actividades.pack(side="left", padx=20)   
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
        #listNotas = self.controllerNotas.obtener_historial_academico_completo(self.id)
        listNotas = self.controllerNotas.modelo_notas.listar_notas_estudiante(self.id)
        listAsistencias = self.controllerNotas.modelo_notas.obtener_historial_asistencias(self.id)

        # # For para calcular el promedio de las asistencias
        # --- Construir un diccionario de asistencias por unidad curricular ---
        mapeo_asistencia = {}

        for a in listAsistencias:
            uc_nombre = a.get("unidad_curricular")
            asistencia_valor = a.get("asistencia_promedio", 0)
            if not uc_nombre:
                continue

            if uc_nombre not in mapeo_asistencia:
                mapeo_asistencia[uc_nombre] = {
                    "total": 0,
                    "count": 0
                }

            mapeo_asistencia[uc_nombre]["total"] += asistencia_valor
            mapeo_asistencia[uc_nombre]["count"] += 1

        # Ahora convertir totales a promedios
        for uc in mapeo_asistencia:
            total = mapeo_asistencia[uc]["total"]
            count = mapeo_asistencia[uc]["count"]
            mapeo_asistencia[uc] = round(total / count, 2) if count > 0 else 0

        uc_data = {}

        for nota in listNotas:
            uc = nota["unidad_curricular"]
            trayecto = nota["trayecto"]
            insc_id = nota["inscripcion_id"]
            valor = nota["valor"]
            uc_creditos = nota["unidades_credito"]
            asistencia = mapeo_asistencia.get(uc, 0)

            if uc not in uc_data:
                uc_data[uc] = {
                    "trayecto": trayecto,
                    "notas": [],
                    "asistencias": [],
                    "unidades_credito": uc_creditos
                }

            if valor is not None:
                uc_data[uc]["notas"].append(valor)
            uc_data[uc]["asistencias"].append(asistencia)
        print(listNotas)
        if not listNotas:
            messagebox.showwarning("Advertencia", "No se encontraron notas para calcular el índice académico.")
            dictDatosSolicitud["indiceAcademico"] = 0
        else:
            listaMapeada = []
            total_notas = 0
            count_notas = 0

            for uc, datos in uc_data.items():
                promedio_nota = sum(datos["notas"]) / len(datos["notas"]) if datos["notas"] else 0
                promedio_asistencia = sum(datos["asistencias"]) / len(datos["asistencias"]) if datos["asistencias"] else 0

                listaMapeada.append({
                    "periodo_academico": "2025",  # o el actual
                    "nombre_trayecto": datos["trayecto"],
                    "nombre_unidad_curricular": uc,
                    "nota": round(promedio_nota, 2),
                    "asistencia": round(promedio_asistencia, 2),
                    "unidades_credito": datos["unidades_credito"],
                    "promedio": promedio_nota
                })

                total_notas += promedio_nota
                count_notas += 1

            dictDatosSolicitud["indiceAcademico"] = total_notas / count_notas if count_notas > 0 else 0
       
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
        #return
           


    def plantillaIncripcionServiCumuni(self):
        rutaDocumento = "reportes/plantillas/PLANILLA DE INSCRIPCION DE SERVICIO COMUNITARIO.docx"
        self.guardarDocumento(rutaDocumento,sugerenciaNombre="PLANTILLA DE INSCRIPCIÓN DE SERVICIO COMUNITARIO")

    def informeFinalSC(self):
        rutaDocumento = "reportes/plantillas/INFORME_FINAL_PSC.docx"
        self.guardarDocumento(rutaDocumento,sugerenciaNombre="INFORME FINAL DE SERVICIO COMUNITARIO")
    
    def informeAvanceSC(self):
        rutaDocumento = "reportes/plantillas/AVANCE_PSC(planilla diaria de actividades).docx"
        self.guardarDocumento(rutaDocumento,sugerenciaNombre="INFORME DE AVANCES")
    
    def controlActividadesSC(self):
        rutaDocumento = "reportes/plantillas/CONTROL_TOTAL_DE_ACTIVIDADES_PSC.docx"
        self.guardarDocumento(rutaDocumento,sugerenciaNombre="CONTROL TOTAL DE ACTIVIDADES")

    def guardarDocumento(self, documentoGuardar, sugerenciaNombre="Servicio Comunitario"):
       
        # 1. Verificar si el archivo de origen (la plantilla) realmente existe
        if not os.path.exists(documentoGuardar):
            messagebox.showerror("Error", f"No se encontró el archivo")
            return

        tipos_archivo = [
            ("Documento de Word", "*.docx"),
            ("Todos los archivos", "*.*")

        ]

        # 2. Abrir el diálogo "Guardar como" para que el usuario elija el destino
        ruta_destino = filedialog.asksaveasfilename(
            title="Seleccionar dónde guardar el documento",
            initialfile=sugerenciaNombre, # Sugerir un nombre de archivo
            defaultextension=".docx",
            filetypes=tipos_archivo
        )

        # 3. Si el usuario seleccionó una ruta (no canceló)
        if ruta_destino:
            try:
                # 4. Copiar el archivo desde el origen al destino
                # shutil.copy2() es ideal porque copia el archivo y sus metadatos
                shutil.copy2(documentoGuardar, ruta_destino)
                
                # 5. Informar al usuario que todo salió bien
                respuesta = messagebox.askyesno(
                    "Éxito",
                    f"El documento se ha guardado correctamente en:\n{ruta_destino}\n\n¿Desea abrir la carpeta origen?"
                )
                if respuesta:
                    # Abre el explorador de archivos en la carpeta donde se guardó el documento
                    webbrowser.open(os.path.dirname(ruta_destino))

            except Exception as e:
                # Informar si ocurre un error durante la copia (ej: permisos)
                messagebox.showerror("Error al Guardar", f"No se pudo guardar el archivo.\n\nError: {e}")
        else:
            # El usuario presionó "Cancelar" en el diálogo
            print("Operación de guardado cancelada por el usuario.")
            
