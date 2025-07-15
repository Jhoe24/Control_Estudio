import tkinter.messagebox as messagebox

class ControllerSecciones:
    def __init__(self, modelo_secciones):
        pass

    def obtener_datos_vista(self, vista):
        datos = {
            "codigo": vista.codigo_entry.get(),
            "docente": vista.var_docente.get(),
            "cupo_maximo": vista.cupo_maximo_entry.get(),
            "turno": vista.var_turno.get(),
            "modalidad": vista.var_modalidad.get(),
            "aula": vista.aula_entry.get(),
            "estado": vista.var_estado.get(),
            "pnf_id": vista.pnf_id_por_nombre[vista.var1.get()],
            "trayecto_id": vista.trayecto_id_por_nombre[vista.var_trayecto.get()],
            "tramo_id": vista.tramo_id_por_nombre[vista.var_tramo.get()]
        }