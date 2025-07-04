import tkinter.messagebox as messagebox
from models.PNF.modelo_pnf import ModeloPNF
from datetime import datetime
from pprint import pprint
class ControllerPNF:
    
    def __init__(self):
        self.modelo = ModeloPNF()
        self.listado_pnf = self.modelo.obtner_lista_pnf()

        # Obtener el primer PNF válido, si existe
        if self.listado_pnf and len(self.listado_pnf) > 0:
            primer_pnf_id = self.listado_pnf[0][0]
            self.listado_trayecto = self.modelo.obtener_lista_trayecto(primer_pnf_id)
        else:
            self.listado_trayecto = []
        
        # Obtener el primer trayecto válido, si existe
        if self.listado_trayecto and len(self.listado_trayecto) > 0:
            primer_trayecto_id = self.listado_trayecto[0][0]
            self.listado_tramo = self.modelo.obtener_lista_tramo(primer_trayecto_id)
        else:
            self.listado_tramo = []

    def registrar_pnf(self, dic_pnf, vista_formulario=None):
        try:
            fecha_actual = self.obtener_fecha_actual()
            lista_trayectos = dic_pnf["lista_trayectos"]
            id_pnf = self.modelo.registrar_pnf(dic_pnf, fecha_actual)

            if not id_pnf:
                messagebox.showerror("Error", "No se pudo registrar el PNF.", parent=vista_formulario)
                return False

            for trayecto in lista_trayectos:
                lista_tramos = trayecto["lista_tramos"]
                id_trayecto = self.modelo.registrar_trayecto(trayecto, id_pnf)

                if not id_trayecto:
                    messagebox.showerror("Error", f"No se pudo registrar el trayecto {trayecto.get('numero', '')}.", parent=vista_formulario)
                    continue

                for tramo in lista_tramos:
                    exito_tramo = self.modelo.registrar_tramos(tramo, id_trayecto)
                    if exito_tramo is not True:
                        messagebox.showerror("Error", f"Error al registrar el tramo {tramo.get('numero', '')} del trayecto {trayecto.get('numero', '')}.", parent=vista_formulario)

            messagebox.showinfo("Éxito", "PNF registrado correctamente.", parent=vista_formulario)
            # Actualizar el listado de PNF en el modelo
            self.listado_pnf = self.modelo.obtner_lista_pnf()
            return True

        except Exception as e:
            print(f"Error inesperado al registrar el PNF: {e}")
            messagebox.showerror("Error inesperado", f"Ocurrió un error: {e}", parent=vista_formulario)
            return False

    def actualizar_listado(self):
        self.listado_pnf = self.modelo.obtner_lista_pnf()

    def obtener_datos_completos(self,id):
        dic_pnf = self.modelo.obtener_pnf(id)
        list_dic_trayectos =self.modelo.obtener_trayecto(id)
        #dic_pnf["lista_trayectos"] = list_dic_trayectos
        new_trayetos = []

        if list_dic_trayectos:
            for trayecto in list_dic_trayectos:
                if trayecto:
                    dic_tramo = self.modelo.obtener_tramo(trayecto["id"])
                    if dic_tramo:
                        trayecto["lista_tramos"] = dic_tramo
                    else:
                        trayecto["lista_tramos"] = []
                    new_trayetos.append(trayecto)
            dic_pnf["lista_trayectos"] = new_trayetos
        else:
            dic_pnf["lista_trayectos"] = []
        #pprint(dic_pnf)
        return dic_pnf
    
    def update_pnf(self,dic_pnf,dic_id,top,nuevos_trayectos = None):
        exito = self.modelo.update_pnf(dic_pnf,dic_id["id_pnf"])
        if exito:
            if dic_pnf["lista_trayectos"]:
                for trayectos,id_trayecto in zip(dic_pnf["lista_trayectos"],dic_id["ids_trayectos"]):
                    exito = self.modelo.update_trayecto(trayectos,id_trayecto[0])
                    if exito:
                        if trayectos["lista_tramos"]:
                            for tramos,id in zip(trayectos["lista_tramos"],id_trayecto[1]):
                                exito = self.modelo.update_tramo(tramos,id)
                                if exito == False:
                                    messagebox.showinfo("Error", f"tramo {tramos['numero']} no se puedo actualizar.", parent=top)
                        if trayectos["lista_tramos_nuevos"]:
                            for tramos in trayectos["lista_tramos_nuevos"]:
                                exito = self.modelo.registrar_tramos(tramos, id_trayecto[0])
                                if exito is not True:
                                    messagebox.showerror("Error", f"tramo {tramos['numero']} no se pudo registrar.", parent=top)
                    else:
                        messagebox.showinfo("Error", f"trayecto {trayectos['numero']} no se puedo actualizar.", parent=top)

            messagebox.showinfo("Éxito","PNF actualizado correctamente.", parent=top)

            if nuevos_trayectos:
                for trayecto in nuevos_trayectos:
                    lista_tramos = trayecto["lista_tramos"]
                    id_trayecto = self.modelo.registrar_trayecto(trayecto, dic_id["id_pnf"])

                    if not id_trayecto:
                        messagebox.showerror("Error", f"No se pudo actualizar el nuevo trayecto {trayecto.get('numero', '')}.", parent=top)
                        continue

                    for tramo in lista_tramos:
                        exito_tramo = self.modelo.registrar_tramos(tramo, id_trayecto)
                        if exito_tramo is not True:
                            messagebox.showerror("Error", f"Error al actualizar el nuevo tramo {tramo.get('numero', '')} del trayecto {trayecto.get('numero', '')}.", parent=top)



            self.listado_pnf = self.modelo.obtner_lista_pnf()
            return True
        else: 
            messagebox.showinfo("Error", f"El PNF no se puedo actualizar.", parent=top)
            return False

    def obtener_id(self, dic_pnf):
        dic_id = {}
        dic_id["id_pnf"] = dic_pnf["id"]

        if dic_pnf["lista_trayectos"]:
            list_id_trayectos = []
            for trayecto in dic_pnf["lista_trayectos"]:
                id_trayecto = trayecto["id"]
                ids_tramos = []
                if trayecto["lista_tramos"]:
                    for tramo in trayecto["lista_tramos"]:
                        ids_tramos.append(tramo["id"])
                list_id_trayectos.append([id_trayecto, ids_tramos])
            dic_id['ids_trayectos'] = list_id_trayectos
        return dic_id



    def getTramos(self,vista_tramos):
        try:
            # Verifica que los widgets existen antes de acceder
            if not (vista_tramos.numero_entry.winfo_exists() and
                    vista_tramos.nombre_entry.winfo_exists() and
                    vista_tramos.duracion_semanas_entry.winfo_exists() and
                    vista_tramos.duracion_horas_entry.winfo_exists() and
                    vista_tramos.creditos_entry.winfo_exists() and
                    vista_tramos.objetivos_entry.winfo_exists() and
                    vista_tramos.estado_option_menu.winfo_exists()):
                return None

            return {
                "numero": vista_tramos.numero_entry.get(),
                "nombre": vista_tramos.nombre_entry.get(),
                "duracion_semanas": vista_tramos.duracion_semanas_entry.get(),
                "duracion_horas": vista_tramos.duracion_horas_entry.get(),
                "creditos": vista_tramos.creditos_entry.get(),
                "objetivos": vista_tramos.objetivos_entry.get(),
                "estado": vista_tramos.estado_option_menu.get(),
            }
        except Exception as e:
            print(f"Error al obtener datos del tramo: {e}")
            return None
        
    def getTrayectos(self,vista_trayectos, lista_tramos):
        #diccinario para guardar los datos de los trayectos
        dic_trayectos = {
            "numero": vista_trayectos.numero_entry.get(),
            "nombre": vista_trayectos.nombre_entry.get(),
            "tipo": vista_trayectos.tipo_trayecto,
            "duracion_semanas": vista_trayectos.duracion_semanas_entry.get(),
            "duracion_horas": vista_trayectos.duracion_horas_entry.get(),
            "creditos_minimos": vista_trayectos.creditos_minimos_entry.get(),
            "creditos_maximos": vista_trayectos.creditos_maximos_entry.get(),
            "numero_tramos": vista_trayectos.numero_tramos_menu.get(),
            "objetivos": vista_trayectos.objetivos_entry.get(),
            "perfil_egreso": vista_trayectos.perfil_egreso_menu.get(),
            "obligatorio": vista_trayectos.obligatorio_menu.get(),
            "secuencial": vista_trayectos.secuencial_menu.get(),
            "estado": vista_trayectos.estado_option_menu.get(),
            "lista_tramos": lista_tramos
        }
        
        return dic_trayectos 

    def getPNF(self,vista_pnf, lista_trayectos):
        #diccinario para guardar el pnf completo
        dic_pnf = {
            "codigo": vista_pnf.codigo_entry.get(),
            "codigo_nacional": vista_pnf.codigo_nacional_entry.get(),
            "nombre_pnf": vista_pnf.nombre_entry.get(),
            "siglas": vista_pnf.siglas_entry.get(),
            "tipo_pnf": vista_pnf.tipo_pnf_menu.get(),
            "area_conocimiento": vista_pnf.area_conocimiento_entry.get(),
            "cantidad_trayectos": vista_pnf.get_trayecto(),
            "duracion_semana": vista_pnf.duracion_semanas_entry.get(),
            "duracion_creditos": vista_pnf.duracion_creditos_entry.get(),
            "duracion_horas": vista_pnf.duracion_horas_entry.get(),

            "fecha_resolucion": vista_pnf.fecha_resolucion,
            "titulo_otorga": vista_pnf.titulo_otorga_entry.get(),
            "perfil_egreso": vista_pnf.perfil_egreso_entry.get(),
            "resolucion": vista_pnf.resolucion_entry.get(),
            "version_pensum": vista_pnf.version_pensum_entry.get(),
            "coordinador_nacional": vista_pnf.coordinador_nacional_entry.get(),
            "estado": vista_pnf.estado_menu.get(),
            "lista_trayectos": lista_trayectos  
        }
        return dic_pnf

    def _solo_numeros(self, char_input):
        return char_input.isdigit()

    def _numeros_y_barras(self, char_input):
        return char_input.isdigit() or char_input in "-/"

    def _solo_decimal(self, valor_actual, char_input):
        if char_input in "0123456789":
            return True
        if char_input == "." and "." not in valor_actual:
            return True
        if char_input == "":
            return True  # Permitir borrar
        return False

    def validar_campos_obligatorios_tramos(self, datos_tramos, vista_formulario):
        try:
            campos_a_validar = [
                ("numero", "Número"),
                ("nombre", "Nombre"),
                ("duracion_semanas", "Duración en Semanas"),
                ("duracion_horas", "Duración en Horas"),
                ("creditos", "Créditos"),
                ("objetivos", "Objetivos"),
                ("estado", "Estado"),
            ]   
            
            for campo, nombre_campo in campos_a_validar:
                valor_campo = datos_tramos.get(campo, "").strip()

                if not valor_campo:
                    messagebox.showwarning("Campo Vacío", f"El campo '{nombre_campo}' es obligatorio.", parent=vista_formulario)
                    return False

            return True

        except Exception as e:
            print(e)

    def validar_campos_obligatorios_trayectos(self, datos_trayectos, vista_formulario):
        try:
            campos_a_validar = [
                ("numero", "Número"),
                ("nombre", "Nombre"),
                ("tipo", "Tipo"),
                ("duracion_semanas", "Duración en Semanas"),
                ("duracion_horas", "Duración en Horas"),
                ("creditos_minimos", "Créditos Mínimos"),
                ("creditos_maximos", "Créditos Máximos"),
                ("numero_tramos", "Número de Tramos"),
                ("objetivos", "Objetivos"),
                ("perfil_egreso", "Perfil de Egreso"),
                ("obligatorio", "Obligatorio"),
                ("secuencial", "Secuencial"),
                ("estado", "Estado"),
            ]   
            
            for campo, nombre_campo in campos_a_validar:
                valor_campo = datos_trayectos.get(campo, "").strip()

                if not valor_campo:
                    messagebox.showwarning("Campo Vacío", f"El campo '{nombre_campo}' es obligatorio.", parent=vista_formulario)
                    return False

            return True

        except Exception as e:
            print(e)       

    def validar_campos_obligatorios_pnf(self, datos_pnf, vista_formulario):
        try:
            campos_a_validar = [
                ("codigo", "Código"),
                ("codigo_nacional", "Código Nacional"),
                ("nombre", "Nombre del PNF"),
                ("siglas", "Siglas"),
                ("tipo_pnf", "Tipo de PNF"),
                ("area_conocimiento", "Área de Conocimiento"),
                ("duracion_horas", "Duración en Horas"),
                ("creditos", "Créditos"),
                ("fecha_resolucion", "Fecha de Resolución"),
                ("titulo_otorga", "Título que Otorga"),
                ("perfil_egreso", "Perfil de Egreso"),
                ("resolucion", "Resolución"),
                ("version_pensum", "Versión del Pensum"),
                ("coordinador_nacional", "Coordinador Nacional"),
                ("estado", "Estado")
            ]

            for campo, nombre_campo in campos_a_validar:
                valor_campo = datos_pnf.get(campo, "").strip()
                
                if not valor_campo:
                    messagebox.showwarning("Campo Vacío", f"El campo '{nombre_campo}' es obligatorio.", parent=vista_formulario)
                    return False
            return True
        except Exception as e:
            print(e)

    def obtener_fecha_actual(self):
        return datetime.now().strftime("%Y-%m-%d")
    
    def existe_codigo(self, codigo):
        return self.modelo.existe_campo("codigo", codigo)
    
    def existe_codigo_nacional(self, codigo_nacional):
        return self.modelo.existe_campo("codigo_nacional", codigo_nacional)
    
    #Metodos para el controlador de unidades Curriculares
    def registrar_unidad_curricular(self, datos_uc, vista_formulario=None):
        try:
            fecha_actual = self.obtener_fecha_actual()
            id_uc = self.modelo.registrar_unidad_curricular(datos_uc, fecha_actual)
            if not id_uc:
                messagebox.showerror("Error", "No se pudo registrar la Unidad Curricular.", parent=vista_formulario)
                return False
            messagebox.showinfo("Éxito", "Unidad Curricular registrada correctamente.", parent=vista_formulario)
            return True
        except Exception as e:
            print(f"Error inesperado al registrar la Unidad Curricular: {e}")
            messagebox.showerror("Error inesperado", f"Ocurrió un error: {e}", parent=vista_formulario)
            return False
        
    def obtener_datos_completos_uc(self, id_uc):
        return self.modelo.obtener_unidad_curricular(id_uc)
    
    def update_unidad_curricular(self, datos_uc, id_uc, top):
        try:
            exito = self.modelo.update_unidad_curricular(datos_uc, id_uc)
            if exito:
                messagebox.showinfo("Éxito", "Unidad Curricular actualizada correctamente.", parent=top)
                return True
            else:
                messagebox.showinfo("Error", "La Unidad Curricular no se pudo actualizar.", parent=top)
                return False
        except Exception as e:
            print(f"Error al actualizar la Unidad Curricular: {e}")
            messagebox.showerror("Error", "La Unidad Curricular no se pudo actualizar.", parent=top)
            return False
        
    def getUnidadCurricular(self, vista_uc):
        # Diccionario para guardar los datos de la U.C
        dic_uc = {
            "codigo": vista_uc.codigo_entry.get(),
            "nombre": vista_uc.nombre_entry.get(),
            "nombre_corto": vista_uc.nombre_corto_entry.get(),
            "area": vista_uc.area_entry.get(),
            "subarea": vista_uc.subarea_entry.get(),
            "eje_formativo": vista_uc.eje_formativo_entry.get(),
            "horas_teoricas": vista_uc.horas_teoricas_entry.get(),
            "horas_practicas": vista_uc.horas_practicas_entry.get(),
            "horas_laboratorio": vista_uc.horas_laboratorio_entry.get(),
            "horas_trabajo_independiente": vista_uc.horas_trabajo_independiente_entry.get(),
            "horas_totales": vista_uc.horas_totales_entry.get(),
            "unidades_credito": vista_uc.unidades_credito_entry.get(),
            "tipo": vista_uc.tipo_menu.get(),
            "caracter": vista_uc.caracter_menu.get(),
            "modalidad": vista_uc.modalidad_menu.get(),
            "complejidad": vista_uc.complejidad_menu.get(),
            "prelaciones": vista_uc.prelaciones_entry.get(),
            "competencias_genericas": vista_uc.competencias_genericas_entry.get(),
            "competencias_especificas": vista_uc.competencias_especificas_entry.get(),
            "saberes_cognitivos": vista_uc.saberes_cognitivos_entry.get(),
            "saberes_procedimentales": vista_uc.saberes_procedimentales_entry.get(),
            "saberes_actitudinales": vista_uc.saberes_actitudinales_entry.get(),
            "estrategias_ensenanza": vista_uc.estrategias_ensenanza_entry.get(),
            "recursos_didacticos": vista_uc.recursos_didacticos_entry.get(),
            "evaluacion": vista_uc.evaluacion_entry.get(),
            "bibliografia": vista_uc.bibliografia_entry.get(),
            "homologacion_clave": vista_uc.homologacion_clave_entry.get(),
            "clave_especial": vista_uc.clave_especial_entry.get(),
            "estado": vista_uc.estado_menu.get(),
            # "fecha_creacion": vista_uc.fecha_creacion_entry.get(),
            # "fecha_actualizacion": vista_uc.fecha_actualizacion_entry.get(),
        }
        return dic_uc
    
    def validar_campos_obligatorios_uc(self, datos_uc, vista):
        """
        Valida campos obligatorios y gestiona el estado del botón de grabar:
        - Deshabilita el botón si falta algún campo o si no se selecciona un tramo válido.
        - Habilita el botón si todo está completo.
        """
        campos_obligatorios = [
            'codigo', 'nombre', 'nombre_corto', 'area', 'subarea',
            'eje_formativo', 'horas_teoricas', 'horas_practicas',
            'horas_laboratorio', 'horas_trabajo_independiente', 'horas_totales',
            'unidades_credito', 'prelaciones', 'competencias_genericas',
            'competencias_especificas', 'saberes_cognitivos', 'saberes_procedimentales',
            'saberes_actitudinales', 'estrategias_ensenanza', 'recursos_didacticos',
            'evaluacion', 'bibliografia', 'homologacion_clave', 'clave_especial'
            # 'fecha_creacion', 'fecha_actualizacion'
        ]

        campos_faltantes = []
        for campo in campos_obligatorios:
            valor = datos_uc.get(campo, "").strip()
            if not valor:
                campos_faltantes.append(campo)

        # Validar selección de Tramo
        id_tramo = datos_uc.get('id_tramo')
        tramo_valido = id_tramo is not None

        if campos_faltantes or not tramo_valido:
            # Deshabilitar botón
            vista.btn_guardar.configure(state="disabled")
            return False
        else:
            # Habilitar botón
            vista.btn_guardar.configure(state="normal")
            return True
    
    def obtener_trayectos_por_pnf(self, id_pnf):
        return self.modelo.obtener_lista_trayecto(id_pnf)

    def obtener_tramos_por_trayecto(self, id_trayecto):
        return self.modelo.obtener_lista_tramo(id_trayecto)
    
    def obtener_UC(self):
        return self.modelo.obtener_UC()
