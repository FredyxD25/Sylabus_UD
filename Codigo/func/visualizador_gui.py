from tkinter import ttk
from PyPDF2 import PdfMerger
import os
import tkinter as tk

class UnidorPDF:
    @staticmethod
    def unir(archivos, salida="PDF_unido.pdf"):
        try:
            combinador = PdfMerger()
            for archivo in archivos:
                combinador.append(archivo)
            combinador.write(salida)
            combinador.close()
            return True, salida
        except Exception as e:
            return False, str(e)
        
class VisualizadorGUI:
    def __init__(self, root, datos_archivos):
        self.root = root
        self.datos = datos_archivos

        self.root.title("Visualizador de Archivos por Subcarpetas")

        # Filtro desplegable
        self.filtro_var = tk.StringVar(value="Todos")
        opciones = ["todos", "pdf", "excel", "otros"]
        self.menu_filtro = ttk.Combobox(root, textvariable=self.filtro_var, values=opciones, state="readonly")
        self.menu_filtro.pack(pady=5)
        self.menu_filtro.bind("<<ComboboxSelected>>", self.actualizar_vista)

        # Árbol para mostrar archivos
        self.tree = ttk.Treeview(root)
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        self.tree["columns"] = ("Tipo",)
        self.tree.heading("#0", text="Archivo")
        self.tree.heading("Tipo", text="Tipo")

        self.actualizar_vista()

    def actualizar_vista(self, event=None):
        filtro = self.filtro_var.get()
        self.tree.delete(*self.tree.get_children())  # Limpiar vista

        for subcarpeta, tipos in self.datos.items():
            nodo = self.tree.insert("", "end", text=f"📁 {subcarpeta}", open=True)

            for tipo, archivos in tipos.items():
                if filtro != "todos" and tipo != filtro:
                    continue

                for archivo in archivos:
                    nombre = os.path.basename(archivo)
                    self.tree.insert(nodo, "end", text=nombre, values=(tipo.upper(),))
