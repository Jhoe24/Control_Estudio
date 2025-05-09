from models.modeloMaster import ModeloMaster
import time
from datetime import datetime
from util.mensaje import CustomMessageBox


class ControladorMaster:
    def __init__(self, master):
        self.modelo = ModeloMaster()
        self.master = master
        
    
    def obtener_Usuario(self, id_usuario):
        return self.modelo.obtener_nombre_usuario(id_usuario)

    def actualizar_Usuario(self, id_usuario, usuario):
        if len(usuario) == 0:
            CustomMessageBox(self.master, "Mensaje", "El campo del nuevo\n nombre esta vacio","error")
        else:
            CustomMessageBox(self.master, "Mensaje", "El Nombre se cambio\n correctamente","info")
            return self.modelo.actualizar_Usuario(id_usuario, usuario)
    
    def cambiar_clave(self, id_usuario, clave, confi_clave):
        if len(clave)==0 or len(confi_clave)== 0:
            CustomMessageBox(self.master, "Mensaje", "Los campo clave o confirmar\n clave estan vacios","error")
        else:
            if clave == confi_clave:
                CustomMessageBox(self.master, "Mensaje", "La clave se cambio\n correctamente","info")
                return self.modelo.cambiar_clave(id_usuario, clave) 
            else:
                CustomMessageBox(self.master, "Mensaje", "Las claves no coinciden","error")
                
    def agregar_imagen(self, id_usuario, destino):
        self.modelo.agregar_imagen(id_usuario, destino)
        
    def obtener_destino_imagen(self, id_usuario):
        return self.modelo.obtener_destino_imagen(id_usuario)
    
    def actualizar_ruta_imagen(self, id_usuario, destino):
        return self.modelo.actualizar_ruta_imagen(id_usuario, destino)
    
    def existe_imagen(self, id_usuario):
        return self.modelo.existe_imagen(id_usuario)
        
    def insertarhistorial(self, funcion, posicion, palabra, id_usuario):
        fecha = datetime.now().strftime("%Y-%m-%d")
        hora = datetime.now().strftime("%H:%M")
        
        self.modelo.insertarHistorial(funcion, posicion, palabra, fecha, hora, id_usuario)
        
    def obtenerHistorial(self, id_usuario, tabla):
        
        # Limpiar la tabla
        for item in tabla.get_children():
            tabla.delete(item)
            
        filas = self.modelo.obtenerHistorial(id_usuario)


        # Rellenar la tabla con los datos obtenidos
        for fila in filas:
            tabla.insert("", "end", values=fila)



            



   


