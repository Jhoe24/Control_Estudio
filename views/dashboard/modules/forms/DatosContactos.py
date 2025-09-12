import customtkinter as ctk
from views.dashboard.components.widget_utils import *
from views.dashboard.components.SectionFrameBase import SectionFrameBase
from views.dashboard.modules.forms.DatosPersonales import DatosPersonalesFrame



class DatosContactosFrame(SectionFrameBase):

    def __init__(self, master, telefonos, correo):
        super().__init__(master, header_text="Datos Contactos")
        self.lista_widget_tlf = []
        self.telefono = telefonos
        self.correo = correo
        self.vcmd = self.register(solo_numeros)
        self._crear_fila_widgets([
            ("Correo Electrónico:", crear_entry, {"width":300}, 1, self, 'correo_electronico_entry')
        ])
        self.correo_electronico_entry.configure(state="normal")  # Asegurar que esté habilitado
        self.correo_electronico_entry.delete(0, ctk.END)
        if self.correo:  # Solo insertar si hay contenido
            self.correo_electronico_entry.insert(0, self.correo)
        self.correo_electronico_entry.configure(state="disabled")

        self.btn = ctk.CTkButton(self,text="Añadir Telefonos",command =self.anadir_telefono)
        self.btn.pack(anchor="w", pady=5)
        self.crear_widget_tlf()
    _crear_fila_widgets = DatosPersonalesFrame._crear_fila_widgets

    def anadir_telefono(self, telefono = None):
        fila = ctk.CTkFrame(self, fg_color="transparent")
        fila.pack(fill="x", pady=2)

        var_tipo = ctk.StringVar(value="movil")

        tipo_menu = crear_option_menu(
            fila,
            values=['movil', 'casa', 'trabajo', 'otro'],
            variable=var_tipo
        )
        tipo_menu.pack(side="left", padx=(0, 5))

        entry_num = crear_entry(
            fila,
            width=150,
            validate="key",
            validatecommand=(self.vcmd, "%S")
        )
        
        btn_eliminar = ctk.CTkButton(
            fila,
            text="Eliminar",
            width=70,
            command=lambda: self.eliminar_telefono(fila)
        )

        if telefono:
            var_tipo.set(telefono[0])
            entry_num.insert(0,str(telefono[1]))

        entry_num.pack(side="left", padx=(0, 5))
        btn_eliminar.pack(side="left", padx=(0, 5))
        self.lista_widget_tlf.append((var_tipo,tipo_menu,entry_num))

    def eliminar_telefono(self, fila):
        """
        Elimina una fila de teléfono de la interfaz y de la lista.
        """
        fila.destroy()
        self.telefono_widgets = [
            t for t in self.lista_widget_tlf if t[0] != fila
        ]

    def crear_widget_tlf(self):
        for telefono in self.telefono:
            self.anadir_telefono(telefono)

    def get_datos(self):
       
        result = []
        for telefono in self.telefono:
            result.append(telefono[0].get(),telefono[1].get())
        
        return {
           "telefono":result,
           "correo":self.correo_electronico_entry.get()
        }
        
       
