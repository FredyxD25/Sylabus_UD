import tkinter as tk
from tkinter import ttk, messagebox
import os
from PyPDF2 import PdfMerger

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
        self.archivos_radio = {}  # clave: nombre archivo, valor: tk.IntVar
        self.subcarpeta_paths = {}  # para encontrar ruta completa

        self.root.title("Visualizador de Archivos por Subcarpetas")

        # Filtro desplegable
        self.filtro_var = tk.StringVar(value="Todos")
        opciones = ["Todos", "pdf", "excel", "otros"]
        self.menu_filtro = ttk.Combobox(root, textvariable=self.filtro_var, values=opciones, state="readonly")
        self.menu_filtro.pack(pady=5)
        self.menu_filtro.bind("<<ComboboxSelected>>", self.actualizar_vista)
        
        # Frame contenedor para árbol y scrollbar
        frame_arbol = ttk.Frame(root)
        frame_arbol.pack(expand=True, fill="both", padx=10, pady=10)

        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(frame_arbol, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # Árbol para mostrar archivos
        self.tree = ttk.Treeview(frame_arbol, selectmode="extended", yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", expand=True, fill="both")

        scrollbar.config(command=self.tree.yview)

        self.tree["columns"] = ("Tipo",)
        self.tree.heading("#0", text="Archivo")
        self.tree.bind("<<TreeviewSelect>>", self.verificar_seleccion_pdf)


        # Botón para unir PDFs
        self.boton_unir = ttk.Button(root, text="Unir PDFs seleccionados", command=self.unir_pdfs, state="disabled")
        self.boton_unir.pack(pady=10)

        self.actualizar_vista()

    def actualizar_vista(self, event=None):
        filtro = self.filtro_var.get()
        self.tree.delete(*self.tree.get_children())

        for subcarpeta, tipos in self.datos.items():
            nodo = self.tree.insert("", "end", text=f"📁 {subcarpeta}", open=True)

            for tipo, archivos in tipos.items():
                if filtro != "todos" and tipo != filtro:
                    continue
                for archivo in archivos:
                    nombre = os.path.basename(archivo)
                    self.tree.insert(nodo, "end", text=nombre, values=(tipo,), tags=(archivo,))

        # Activar o desactivar botón si cambia el filtro
        self.boton_unir["state"] = "normal" if self.filtro_var.get() == "pdf" else "disabled"

    def verificar_seleccion_pdf(self, event=None):
        if self.filtro_var.get() != "pdf":
            self.boton_unir["state"] = "disabled"
            return

        seleccion = self.tree.selection()
        archivos_pdf = [self.tree.item(i, "tags")[0] for i in seleccion if self.tree.item(i, "values")[0] == "pdf"]

        self.boton_unir["state"] = "normal" if archivos_pdf else "disabled"

    def unir_pdfs(self):
        seleccion = self.tree.selection()
        archivos = [self.tree.item(i, "tags")[0] for i in seleccion if self.tree.item(i, "values")[0] == "pdf"]

        if not archivos:
            messagebox.showwarning("Advertencia", "Selecciona al menos un PDF.")
            return

        exito, resultado = UnidorPDF.unir(archivos)

        if exito:
            messagebox.showinfo("Éxito", f"PDFs unidos correctamente en:\n{resultado}")
        else:
            messagebox.showerror("Error", f"Ocurrió un error:\n{resultado}")
