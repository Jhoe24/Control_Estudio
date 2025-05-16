import pandas as pd
from dbfread import DBF
import tkinter as tk
from tkinter import filedialog, messagebox

def dbf_to_txt(dbf_file_path, txt_file_path):
    try:
        table = DBF(dbf_file_path)
        df = pd.DataFrame(iter(table))
        df.to_csv(txt_file_path, index=False, sep='\t')
        messagebox.showinfo("Éxito", "Archivo convertido a .txt exitosamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al convertir a .txt: {e}")

def dbf_to_excel(dbf_file_path, excel_file_path):
    try:
        table = DBF(dbf_file_path)
        df = pd.DataFrame(iter(table))
        df.to_excel(excel_file_path, index=False)
        messagebox.showinfo("Éxito", "Archivo convertido a .xlsx exitosamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al convertir a .xlsx: {e}")

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("DBF files", "*.dbf")])
    if file_path:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, file_path)

def select_output_path():
    output_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("Excel files", "*.xlsx")])
    if output_path:
        entry_output_path.delete(0, tk.END)
        entry_output_path.insert(0, output_path)

def convert_file():
    dbf_file_path = entry_file_path.get()
    output_path = entry_output_path.get()

    if not dbf_file_path or not output_path:
        messagebox.showerror("Error", "Por favor, selecciona un archivo .dbf y una ruta de salida.")
        return

    if output_path.endswith('.txt'):
        dbf_to_txt(dbf_file_path, output_path)
    elif output_path.endswith('.xlsx'):
        dbf_to_excel(dbf_file_path, output_path)
    else:
        messagebox.showerror("Error", "Formato de salida no soportado.")

# Crear la ventana principal
root = tk.Tk()
root.title("Conversor de DBF a TXT/Excel")

# Widgets
label_file_path = tk.Label(root, text="Selecciona el archivo .dbf:")
label_file_path.pack()

entry_file_path = tk.Entry(root, width=50)
entry_file_path.pack()

button_select_file = tk.Button(root, text="Seleccionar archivo", command=select_file)
button_select_file.pack()

label_output_path = tk.Label(root, text="Selecciona la ruta de salida:")
label_output_path.pack()

entry_output_path = tk.Entry(root, width=50)
entry_output_path.pack()

button_select_output = tk.Button(root, text="Seleccionar ruta de salida", command=select_output_path)
button_select_output.pack()

button_convert = tk.Button(root, text="Convertir", command=convert_file)
button_convert.pack()

# Iniciar la aplicación
root.mainloop()
