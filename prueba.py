import ctypes

try:
    # Intenta hacer que la aplicación sea DPI-aware para obtener el valor real
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except AttributeError:
    # Esto puede fallar en versiones de Windows anteriores a 8.1
    ctypes.windll.user32.SetProcessDPIAware()

# La función GetScaleFactorForDevice(0) devuelve el factor de escala para el monitor principal
# El valor devuelto es un entero (ej. 125 para 125%)
scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0)

print(f"El factor de escala de la pantalla es: {scale_factor}%")