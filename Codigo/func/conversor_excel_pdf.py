# utils/conversor_excel_pdf.py

import os
import win32com.client

class ConversorExcelPDF:
    def __init__(self):
        self.excel = win32com.client.Dispatch("Excel.Application")
        self.excel.Visible = False

    def convertir_si_existe(self, ruta_pdf):
        """
        Verifica si existe un archivo Excel con el mismo nombre base del PDF.
        Si lo encuentra, lo convierte a PDF y devuelve la nueva ruta.
        Si no lo encuentra, devuelve la ruta original del PDF.
        """
        dir_actual = os.path.dirname(ruta_pdf)
        nombre_base = os.path.splitext(os.path.basename(ruta_pdf))[0]

        posibles_excel = [
            os.path.join(dir_actual, f"{nombre_base}.xlsx"),
            os.path.join(dir_actual, f"{nombre_base}.xls"),
        ]

        for ruta_excel in posibles_excel:
            if os.path.exists(ruta_excel):
                print(f"[✓] Excel encontrado: {ruta_excel}")
                ruta_salida_pdf = os.path.join(dir_actual, f"{nombre_base}_from_excel.pdf")
                self.convertir_excel_a_pdf(ruta_excel, ruta_salida_pdf)
                return ruta_salida_pdf

        return ruta_pdf  # No se encontró Excel, retorna el PDF original

    def convertir_excel_a_pdf(self, ruta_excel, ruta_salida_pdf):
        try:
            libro = self.excel.Workbooks.Open(ruta_excel)
            libro.ExportAsFixedFormat(0, ruta_salida_pdf)
            libro.Close(False)
            print(f"[→] PDF creado: {ruta_salida_pdf}")
        except Exception as e:
            print(f"[!] Error al convertir Excel a PDF: {e}")

    def cerrar(self):
        self.excel.Quit()
