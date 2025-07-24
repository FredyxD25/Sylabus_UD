import os
import tkinter as tk

from func.carpetas import listar_y_clasificar_por_subcarpeta
from func.visualizador_gui import VisualizadorGUI  # asegúrate de que este archivo exista

# Ruta del script actual
carpeta_base = os.path.dirname(__file__)
ruta_syllabus = os.path.abspath(os.path.join(carpeta_base, "..", "Sylabus_Electronica"))

if __name__ == "__main__":
    # Obtener los datos organizados por subcarpeta
    resultado = listar_y_clasificar_por_subcarpeta(ruta_syllabus)

    # Iniciar interfaz gráfica
    root = tk.Tk()
    app = VisualizadorGUI(root, resultado)
    root.mainloop()

