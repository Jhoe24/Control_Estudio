# controllers/estudiante_controller.py

# Importar el futuro ModeloEstudiante y cualquier utilidad necesaria (ej. mensajes)
# from models.modelo_estudiante import ModeloEstudiante # Descomenta cuando lo crees
# from util.mensaje import CustomMessageBox # Si necesitas mostrar mensajes desde aquí

class EstudianteController:
    def __init__(self, controlador_principal):
        """
        Constructor del EstudianteController.

        Args:
            controlador_principal: Instancia del ControladorPrincipal para posible
                                   navegación o acceso a otros controladores/servicios.
        """
        self.controlador_principal = controlador_principal
        # self.modelo_estudiante = ModeloEstudiante() # Instancia del modelo de estudiante
        print("INFO: EstudianteController inicializado.")
        # Puedes pasarle self.controlador_principal.root a CustomMessageBox si lo usas aquí.
        # self.vista_raiz_para_mensajes = self.controlador_principal.root

    def procesar_guardado_estudiante(self, datos_estudiante, vista_formulario):
        """
        Procesa la solicitud de guardar (crear o actualizar) un estudiante.
        Este método será llamado desde FormularioEstudianteView.

        Args:
            datos_estudiante (dict): Un diccionario con todos los datos del formulario.
            vista_formulario (FormularioEstudianteView): La instancia de la vista del formulario,
                                                        para poder interactuar con ella (ej. mostrar errores específicos).
        """
        print(f"DEBUG: EstudianteController - Recibidos datos para guardar: {datos_estudiante}")

        # 1. Validación de Reglas de Negocio (más allá de campos vacíos que hace la vista)
        #    Ejemplos:
        #    - ¿La cédula ya existe para un nuevo estudiante?
        #    - ¿El formato de las fechas es correcto (dd/mm/aaaa)? (Podría hacerse en la vista también)
        #    - ¿Combinaciones de campos válidas? (ej. si es profesional, debe tener título)

        # --- EJEMPLO DE VALIDACIÓN DE CÉDULA (requiere el modelo) ---
        # if not datos_estudiante.get("id_estudiante"): # Asumiendo que 'id_estudiante' existe si es una edición
        #     cedula_existente = self.modelo_estudiante.verificar_cedula_existente(datos_estudiante["cedula"])
        #     if cedula_existente:
        #         # CustomMessageBox(self.vista_raiz_para_mensajes, "Error de Validación", f"La cédula {datos_estudiante['cedula']} ya está registrada.", "error")
        #         # vista_formulario.marcar_error_cedula() # Método hipotético en la vista
        #         print(f"ERROR: Cédula {datos_estudiante['cedula']} ya existe.")
        #         # Podrías usar el messagebox de tkinter directamente si CustomMessageBox no está adaptado para parent
        #         tkinter.messagebox.showerror("Error de Validación", f"La cédula {datos_estudiante['cedula']} ya está registrada.", parent=vista_formulario)
        #         return False # Indica que el guardado falló

        # 2. Preparar datos para el modelo (si es necesario)
        #    Ej. convertir fechas a objetos datetime, booleanos a 0/1 si la BD lo requiere.
        #    datos_para_db = self._preparar_datos_para_db(datos_estudiante)

        # 3. Llamar al Modelo para guardar/actualizar
        #    Aquí distinguirías si es una creación o una actualización.
        #    Podrías tener un campo oculto 'id_estudiante' en el formulario si estás editando.
        #    O determinarlo por si la cédula ya existe y se está editando ese registro.

        # try:
        #     if datos_estudiante.get("modo_edicion_id"): # Un campo que indique que se está editando
        #         # exito = self.modelo_estudiante.actualizar(datos_estudiante.get("modo_edicion_id"), datos_para_db)
        #         print(f"SIMULACIÓN: Actualizando estudiante ID {datos_estudiante.get('modo_edicion_id')}")
        #     else:
        #         # exito = self.modelo_estudiante.crear(datos_para_db)
        #         print("SIMULACIÓN: Creando nuevo estudiante")
        #     exito = True # Simulación de éxito

        #     if exito:
        #         # CustomMessageBox(self.vista_raiz_para_mensajes, "Éxito", "Datos del estudiante guardados correctamente.", "info")
        #         print("INFO: Datos del estudiante guardados (simulación).")
        #         tkinter.messagebox.showinfo("Éxito", "Datos del estudiante guardados correctamente (simulación).", parent=vista_formulario)
        #         vista_formulario.limpiar_formulario_completo() # Limpiar el formulario después de guardar
        #         # Opcional: Navegar a otra vista, como la lista de estudiantes
        #         # self.controlador_principal.mostrar_vista_lista_estudiantes()
        #         return True
        #     else:
        #         # CustomMessageBox(self.vista_raiz_para_mensajes, "Error", "No se pudieron guardar los datos del estudiante.", "error")
        #         print("ERROR: No se pudieron guardar los datos (simulación).")
        #         tkinter.messagebox.showerror("Error", "No se pudieron guardar los datos del estudiante (simulación).", parent=vista_formulario)

        #         return False
        # except Exception as e:
        #     # CustomMessageBox(self.vista_raiz_para_mensajes, "Error Crítico", f"Ocurrió un error inesperado: {e}", "error")
        #     print(f"EXCEPCIÓN: Ocurrió un error inesperado: {e}")
        #     tkinter.messagebox.showerror("Error Crítico", f"Ocurrió un error inesperado: {e}", parent=vista_formulario)
        #     return False
        
        # ----- SIMULACIÓN SIMPLE POR AHORA -----
        # Esta simulación asume que el proceso fue exitoso
        # (Quita esto cuando implementes la lógica real con el modelo)
        # vista_formulario hace su propio messagebox por ahora en procesar_formulario
        print(f"INFO: EstudianteController - Procesamiento de guardado para {datos_estudiante['nombre']} finalizado (simulación).")
        return True # Indica éxito a la vista para que pueda reaccionar (ej. limpiar campos)


    def cargar_estudiante_para_edicion(self, id_estudiante, vista_formulario):
        """
        Carga los datos de un estudiante por su ID y le dice a la vista que llene los campos.
        (Esta función es para cuando tengas una lista de estudiantes y selecciones uno para editar)

        Args:
            id_estudiante: El ID del estudiante a cargar.
            vista_formulario (FormularioEstudianteView): La instancia de la vista.
        """
        print(f"DEBUG: EstudianteController - Solicitud para cargar estudiante ID: {id_estudiante}")
        # datos_estudiante = self.modelo_estudiante.obtener_por_id(id_estudiante)
        # if datos_estudiante:
        #     vista_formulario.llenar_campos_para_edicion(datos_estudiante) # Método a crear en la vista
        # else:
        #     # CustomMessageBox(self.vista_raiz_para_mensajes, "Error", f"No se encontró el estudiante con ID {id_estudiante}.", "error")
        #     print(f"ERROR: No se encontró estudiante con ID {id_estudiante}.")
        #     tkinter.messagebox.showerror("Error", f"No se encontró el estudiante con ID {id_estudiante}.", parent=vista_formulario)
        pass # Implementar cuando tengas la lista y el modelo

    def obtener_lista_estudiantes(self, criterios_busqueda=None):
        """
        Obtiene una lista de estudiantes del modelo, posiblemente filtrada.
        (Para una vista que muestre una tabla de estudiantes)

        Args:
            criterios_busqueda (dict, optional): Diccionario con criterios para filtrar. Defaults to None.

        Returns:
            list: Lista de objetos/diccionarios de estudiantes.
        """
        print(f"DEBUG: EstudianteController - Obteniendo lista de estudiantes. Criterios: {criterios_busqueda}")
        # return self.modelo_estudiante.obtener_todos(criterios_busqueda)
        return [] # Simulación

    # Otros métodos que podrías necesitar:
    # - eliminar_estudiante(id_estudiante)
    # - generar_reporte_estudiante(id_estudiante)
    # - _preparar_datos_para_db(datos_vista): Método privado para transformar datos si es necesario.