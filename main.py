# importacion de la libreria customTkinter
import customtkinter as ctk

# importacion el controlador principal
from controllers.controlador import ControladorPrincipal

if __name__ == "__main__":
    app = ControladorPrincipal() # instanciamos el controlador
    app.run() # ejecutamos la funcion que esta dentro del controlador principal para que se muestre la ventana
                      