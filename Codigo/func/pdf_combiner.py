from PyPDF2 import PdfMerger

class PDFCombiner:
    def __init__(self, lista_archivos):
        self.archivos = lista_archivos

    def combinar(self, nombre_salida="unido.pdf"):
        if not self.archivos:
            raise ValueError("La lista de archivos está vacía")

        combinador = PdfMerger()
        for archivo in self.archivos:
            combinador.append(archivo)

        combinador.write(nombre_salida)
        combinador.close()
        return nombre_salida
