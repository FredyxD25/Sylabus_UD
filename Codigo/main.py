import os
import sys
import tkinter as tk

from func.carpetas import listar_y_clasificar_por_subcarpeta
from func.visualizador_gui import VisualizadorGUI

if __name__ == "__main__":
    base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    posible_ruta_1 = os.path.join(base_path, "Syllabus_Electronica")
    posible_ruta_2 = os.path.abspath(os.path.join(base_path, "..", "Syllabus_Electronica"))

    # Variable para almacenar la ruta final encontrada
    ruta_syllabus_encontrada = None

    # Primero, intentamos la ruta más probable para el ejecutable (al mismo nivel)
    if os.path.exists(posible_ruta_1):
        ruta_syllabus_encontrada = posible_ruta_1
    # Si la primera no existe, intentamos la segunda (un nivel arriba)
    elif os.path.exists(posible_ruta_2):
        ruta_syllabus_encontrada = posible_ruta_2

    # Si no se encontró en ninguna de las rutas
    if ruta_syllabus_encontrada is None:
        root = tk.Tk()
        root.withdraw()
        tk.messagebox.showerror("Error de Ruta",
                                f"La carpeta 'Syllabus_Electronica' no se encuentra.\n"
                                f"Por favor, asegúrese de que esté en:\n{ruta_syllabus_encontrada}")
        sys.exit(1)

    # Si la carpeta fue encontrada, proceder con la lógica principal
    try:
        resultado = listar_y_clasificar_por_subcarpeta(ruta_syllabus_encontrada)
    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        tk.messagebox.showerror("Error de Ruta",
                                f"La carpeta 'Syllabus_Electronica' no se encuentra.\n"
                                f"Por favor, asegúrese de que esté en:\n{ruta_syllabus_encontrada}")
        sys.exit(1)

    root = tk.Tk()
    app = VisualizadorGUI(root, resultado)
    root.mainloop()