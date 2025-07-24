from func.unidor_pdf import UnidorPDF

class GestorSeleccionPDF:
    def __init__(self):
        self.seleccionados = []

    def actualizar_seleccion(self, seleccionados):
        """Actualiza la lista de archivos seleccionados."""
        self.seleccionados = seleccionados

    def hay_seleccion(self):
        """Retorna True si hay al menos un archivo seleccionado."""
        return len(self.seleccionados) > 0

    def unir_pdfs(self):
        """Une los PDFs seleccionados. Retorna (exito: bool, mensaje: str)."""
        if not self.hay_seleccion():
            return False, "No hay archivos seleccionados."

        return UnidorPDF.unir(self.seleccionados)
