from tkinter import ttk, messagebox
from func.unidor_pdf import UnidorPDF
from func.gestor_seleccion_pdf import GestorSeleccionPDF
from func.conversor_excel_pdf import ConversorExcelPDF

import tkinter as tk
import os

class VisualizadorGUI:
    def __init__(self, root, datos_archivos):
        self.root = root
        self.gestor = GestorSeleccionPDF()
        self.conversor_excel = ConversorExcelPDF()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.modo_columnas = False  # Vista por defecto: una columna
        self.root = root
        self.datos = datos_archivos
        self.check_vars = {}  # Diccionario para variables de Checkbutton

        self.root.title("Visualizador de Archivos por Subcarpetas")
        self.root.state('zoomed')  # Para Windows, pantalla completa sin bordes negros
        
        # --- Frame superior para controles (filtro, búsqueda, botón1, botón2) ---
        frame_controles = ttk.Frame(root)
        frame_controles.pack(fill="x", padx=10, pady=5)

        # Filtro a la izquierda
        self.filtro_var = tk.StringVar(value="Todos")
        opciones = ["Todos", "pdf", "excel", "otros"]
        self.menu_filtro = ttk.Combobox(frame_controles, textvariable=self.filtro_var, values=opciones, state="readonly", width=10)
        self.menu_filtro.pack(side="left", padx=(0, 10))
        self.menu_filtro.bind("<<ComboboxSelected>>", self.actualizar_vista)

        # Barra de búsqueda al centro (expandible)
        self.buscador_var = tk.StringVar()
        self.entry_busqueda = ttk.Entry(frame_controles, textvariable=self.buscador_var)
        self.entry_busqueda.pack(side="left", expand=True, fill="x", padx=(0, 10))
        self.buscador_var.trace_add("write", lambda *args: self.actualizar_vista())

        # Botón a la derecha
        self.boton_unir = ttk.Button(frame_controles, text="Unir PDFs seleccionados", command=self.unir_pdfs, state="disabled")
        self.boton_unir.pack(side="right")
        
        '''self.boton_vista = ttk.Button(frame_controles, text="Cambiar vista", command=self.toggle_modo_vista)
        self.boton_vista.pack(side="right", padx=10)'''


        # -----------------Canvas con scrollbar para mostrar archivos
        self.canvas = tk.Canvas(root)
        self.frame_scroll = ttk.Frame(self.canvas)
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.frame_scroll, anchor="nw")

        self.frame_scroll.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.actualizar_vista()
        
    def toggle_modo_vista(self):
        self.modo_columnas = not self.modo_columnas
        self.actualizar_vista()

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def actualizar_vista(self, event=None):
        # Ocultar todo lo actual
        for widget in self.frame_scroll.winfo_children():
            widget.pack_forget()

        filtro = self.filtro_var.get()
        texto_busqueda = self.buscador_var.get().lower()

        ya_mostradas = set()
        widgets_mostrados = set()  # Para saber qué Checkbuttons se usaron esta vez

        if self.modo_columnas:
            columnas = [ttk.Frame(self.frame_scroll) for _ in range(3)]
            for col in columnas:
                col.pack(side="left", fill="both", expand=True, padx=10)

            subcarpetas = list(self.datos.items())
            partes_por_columna = len(subcarpetas) // 3 + 1

            for idx_col, col in enumerate(columnas):
                for subcarpeta, tipos in subcarpetas[idx_col * partes_por_columna : (idx_col + 1) * partes_por_columna]:
                    self.mostrar_subcarpeta(col, subcarpeta, tipos, texto_busqueda, filtro, ya_mostradas, widgets_mostrados)
        else:
            for subcarpeta, tipos in self.datos.items():
                self.mostrar_subcarpeta(self.frame_scroll, subcarpeta, tipos, texto_busqueda, filtro, ya_mostradas, widgets_mostrados)

    def mostrar_subcarpeta(self, parent_frame, subcarpeta, tipos, texto_busqueda, filtro, ya_mostradas, widgets_mostrados):
        partes = subcarpeta.split(os.sep)

        ruta_actual = ""
        for i, parte in enumerate(partes):
            ruta_actual = os.path.join(ruta_actual, parte)
            if ruta_actual not in ya_mostradas:
                sangria = "    " * i
                label = ttk.Label(parent_frame, text=f"{sangria}📁 {parte}", font=("Arial", 10, "bold"))
                label.pack(anchor="w", pady=(0 if i == 0 else 2, 0))
                ya_mostradas.add(ruta_actual)

        for tipo, archivos in tipos.items():
            if filtro != "Todos" and tipo != filtro:
                continue
            for archivo in archivos:
                nombre = os.path.basename(archivo)

                if texto_busqueda and texto_busqueda not in nombre.lower():
                    continue  # No coincide con búsqueda

                sangria_px = 20 + len(partes) * 10

                if tipo == "pdf":
                    if archivo not in self.check_vars:
                        var = tk.IntVar()
                        chk = ttk.Checkbutton(parent_frame, text=nombre, variable=var, command=self.verificar_seleccion_pdf)
                        self.check_vars[archivo] = (var, chk)
                        chk.pack_forget()
                    else:
                        var, chk = self.check_vars[archivo]

                    chk.pack(anchor="w", padx=sangria_px)
                    widgets_mostrados.add(chk)
                else:
                    lbl = ttk.Label(parent_frame, text=nombre)
                    lbl.pack(anchor="w", padx=sangria_px)

    def on_closing(self):
        if hasattr(self, 'conversor_excel'):
            self.conversor_excel.cerrar()
        self.root.destroy()

    def verificar_seleccion_pdf(self):
        seleccionados = [ruta for ruta, (var, _) in self.check_vars.items() if var.get() == 1]
        self.gestor.actualizar_seleccion(seleccionados)

        self.boton_unir["state"] = "normal" if self.gestor.hay_seleccion() else "disabled"
        
        seleccionados = []

    def unir_pdfs(self):
        seleccionados = []

        for ruta_pdf, (var, _) in self.check_vars.items():
            if var.get() == 1:
                # Si existe un Excel con el mismo nombre, convertirlo a PDF
                ruta_final = self.conversor_excel.convertir_si_existe(ruta_pdf)
                seleccionados.append(ruta_final)

        self.gestor.actualizar_seleccion(seleccionados)

        if not self.gestor.hay_seleccion():
            messagebox.showwarning("Advertencia", "No hay archivos seleccionados para unir.")
            return

        exito, mensaje = self.gestor.unir_pdfs()

        if not exito:
            messagebox.showwarning("Advertencia", mensaje)
        else:
            messagebox.showinfo("Éxito", f"PDFs unidos correctamente en:\n{mensaje}")

