# func/unidor_pdf.py
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

