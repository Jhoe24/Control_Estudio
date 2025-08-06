import customtkinter as ctk
from views.dashboard.components.widget_utils import *
from datetime import datetime


class CTKFecha(ctk.CTkFrame):
    def __init__(self, master, info_label):
        super().__init__(master, fg_color="white")
        self.master = master
        self.anio_actual = datetime.now().year
        
        self.info_label = ctk.CTkLabel(self, text=info_label, text_color=COLOR_TEXTO_PRINCIPAL,font=FUENTE_HEADER_SECCION)
        self.info_label.pack(side = "top", padx=10, pady=(10,0), anchor="w")
        
        #Frame para optionesMenu  que simulan un calendario
        self.frame_fecha = ctk.CTkFrame(self, fg_color="white")
        self.frame_fecha.pack(side = "top", padx=10, pady=(10,0), anchor="w")
        
        #Se crea el campo para el anio que esta desde el anio actual hasta 70 anios menos 
        self.year_values = [str(self.anio_actual - i) for i in range(0, 71)]
        self.var_year = ctk.StringVar(value=self.year_values[0])

        self.year_menu = create_option_menu_row(self.frame_fecha, 
                                                label_text="Año", 
                                                options=self.year_values, 
                                                variable=self.var_year, 
                                                width=50, 
                                                font_size=12, 
                                                funcion=self.validate_day,
                                                side_="left", 
                                                fill_=None,
                                                crear_frame=False)   

        #Se crea el campo para el mes
        self.month_values = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        self.var_month = ctk.StringVar(value=self.month_values[0])
        self.month_menu = create_option_menu_row(self.frame_fecha,
                                                label_text="Mes",
                                                options=self.month_values, 
                                                variable=self.var_month, 
                                                width=50, font_size=12 ,
                                                funcion=self.validate_day,
                                                side_="left", 
                                                fill_=None,
                                                crear_frame=False)

        #Se crea el campo para el dia
        self.day_values = [str(i) for i in range(1, 32)]
        self.var_day = ctk.StringVar(value=self.day_values[0])
        self.day_menu = create_option_menu_row(self.frame_fecha,
                                               label_text="Día",
                                               options=self.day_values, 
                                               variable=self.var_day, width=50, 
                                               font_size=12,
                                               side_="left", 
                                               fill_=None,
                                               crear_frame=False)

    def validate_day(self, *args):
        """ Este metodo define cuantos dias se pueden mostrar segun el mes y año, si es bisiesto """

        if self.var_month.get() in ("Enero", "Marzo", "Mayo", "Julio", "Agosto", "Octubre", "Diciembre"):
            self.day_values = [str(i) for i in range(1, 32)]

        elif self.var_month.get() in ("Abril", "Junio", "Septiembre", "Noviembre"):
            self.day_values = [str(i) for i in range(1, 31)]

        elif self.var_month.get() == "Febrero":
            if self.isLeapYear(int(self.var_year.get())):
                self.day_values = [str(i) for i in range(1, 30)]
            else:
                self.day_values = [str(i) for i in range(1, 29)]

        self.day_menu.configure(values=self.day_values)
        self.var_day.set(self.day_values[0])

    def isLeapYear(self, year):
        if (year % 4) == 0:
            if (year % 100) == 0:
                if (year % 400) == 0:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False
    
    def get_date(self):
        anio = self.var_year.get()
        mes = self.var_month.get()
        mes = self.month_values.index(mes) + 1
        dia = self.var_day.get()
        return f"{anio}-{mes}-{dia}"
        
    def set_date(self, fecha: str):
        fecha = fecha.split("-")
        self.var_year.set(fecha[0])
        self.var_month.set(self.month_values[int(fecha[1])-1])
        self.var_day.set(fecha[2])
        self.year_menu.configure(state="disabled")
        self.month_menu.configure(state="disabled")
        self.day_menu.configure(state="disabled")

    def enable(self):
        self.year_menu.configure(state="normal")
        self.month_menu.configure(state="normal")
        self.day_menu.configure(state="normal")
