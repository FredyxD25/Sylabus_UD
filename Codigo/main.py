import os
import sys  # Importa sys para acceder a _MEIPASS
import tkinter as tk

from func.carpetas import listar_y_clasificar_por_subcarpeta
from func.visualizador_gui import VisualizadorGUI

if getattr(sys, 'frozen', False):

    carpeta_base_app = sys._MEIPASS
else:
    carpeta_base_app = os.path.dirname(__file__)

ruta_syllabus = os.path.abspath(os.path.join(carpeta_base_app, "Syllabus_Electronica"))



if __name__ == "__main__":
    if not os.path.exists(ruta_syllabus):
        print(f"Error: La carpeta Syllabus_Electronica no fue encontrada en: {ruta_syllabus}")
        # Considera mostrar un mensaje de error en la GUI o salir elegantemente
        sys.exit(1) # Salir si la carpeta no se encuentra

    # Obtener los datos organizados por subcarpeta
    resultado = listar_y_clasificar_por_subcarpeta(ruta_syllabus)

    # Iniciar interfaz gráfica
    root = tk.Tk()
    app = VisualizadorGUI(root, resultado)
    root.mainloop()