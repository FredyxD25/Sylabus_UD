from tkinter import ttk, messagebox
from func.unidor_pdf import UnidorPDF
import tkinter as tk
import os

class VisualizadorGUI:
    def __init__(self, root, datos_archivos):
        self.root = root
        self.datos = datos_archivos
        self.check_vars = {}  # Diccionario para variables de Checkbutton

        self.root.title("Visualizador de Archivos por Subcarpetas")

        # Filtro desplegable
        self.filtro_var = tk.StringVar(value="Todos")
        opciones = ["Todos", "pdf", "excel", "otros"]
        self.menu_filtro = ttk.Combobox(root, textvariable=self.filtro_var, values=opciones, state="readonly")
        self.menu_filtro.pack(pady=5)
        self.menu_filtro.bind("<<ComboboxSelected>>", self.actualizar_vista)

        # Canvas con scrollbar para mostrar archivos
        self.canvas = tk.Canvas(root)
        self.frame_scroll = ttk.Frame(self.canvas)
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.frame_scroll, anchor="nw")

        self.frame_scroll.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Botón para unir PDFs
        self.boton_unir = ttk.Button(root, text="Unir PDFs seleccionados", command=self.unir_pdfs, state="disabled")
        self.boton_unir.pack(pady=10)

        self.actualizar_vista()

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def actualizar_vista(self, event=None):
        for widget in self.frame_scroll.winfo_children():
            widget.destroy()

        self.check_vars.clear()
        filtro = self.filtro_var.get()

        ya_mostradas = set()

        for subcarpeta, tipos in self.datos.items():
            partes = subcarpeta.split(os.sep)

            ruta_actual = ""
            for i, parte in enumerate(partes):
                ruta_actual = os.path.join(ruta_actual, parte)
                if ruta_actual not in ya_mostradas:
                    sangria = "    " * i
                    label = ttk.Label(self.frame_scroll, text=f"{sangria}📁 {parte}", font=("Arial", 10, "bold"))
                    label.pack(anchor="w", pady=(0 if i == 0 else 2, 0))
                    ya_mostradas.add(ruta_actual)

            for tipo, archivos in tipos.items():
                if filtro != "Todos" and tipo != filtro:
                    continue
                for archivo in archivos:
                    nombre = os.path.basename(archivo)

                    if tipo == "pdf":
                        var = tk.IntVar()
                        self.check_vars[archivo] = var
                        chk = ttk.Checkbutton(self.frame_scroll, text=nombre, variable=var, command=self.verificar_seleccion_pdf)
                        chk.pack(anchor="w", padx=20 + len(partes)*10)  # Sangría dinámica
                    else:
                        lbl = ttk.Label(self.frame_scroll, text=nombre)
                        lbl.pack(anchor="w", padx=20 + len(partes)*10)


        self.verificar_seleccion_pdf()

    def verificar_seleccion_pdf(self):
        seleccionados = [ruta for ruta, var in self.check_vars.items() if var.get() == 1]
        self.boton_unir["state"] = "normal" if seleccionados else "disabled"

    def unir_pdfs(self):
        seleccionados = [ruta for ruta, var in self.check_vars.items() if var.get() == 1]

        if not seleccionados:
            messagebox.showwarning("Advertencia", "Selecciona al menos un PDF.")
            return

        exito, resultado = UnidorPDF.unir(seleccionados)

        if exito:
            messagebox.showinfo("Éxito", f"PDFs unidos correctamente en:\n{resultado}")
        else:
            messagebox.showerror("Error", f"Ocurrió un error:\n{resultado}")