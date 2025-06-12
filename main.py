"""
Sistema de Control de Estudio para la Universidad Politecnica Territorial "Jose Felix Ribas"

Aplicacion Principal para la gestion de los datos de los estudiantes, profesores, cursos Y mas ...

Autores:
# -
# - 
# -
# -

"""

import customtkinter as ctk
from views.main_windows import MainWindow
from config.app_config import AppConfig


def main():
    # Configuramos la aplicacion, con los parametros del AppConfig para los colores, tema, etc.
    color_thema = AppConfig().color_tema
    ctk.set_default_color_theme(color_thema)  # Configuramos el tema de color
    
    #Inicializamos la ventana principal de la aplicacion
    app = MainWindow()
    app.run()
    
if __name__ == "__main__":
    main()
    
    