import win32com.client
import os
#pip install pywin32

# Rutas
archivo_excel = os.path.abspath("archivo1.xlsx")
archivo_pdf = os.path.abspath("archivo1.pdf")

# Inicializar Excel
excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = False

# Abrir el archivo
wb = excel.Workbooks.Open(archivo_excel)

# Exportar a PDF
wb.ExportAsFixedFormat(0, archivo_pdf)  # 0 = PDF
wb.Close(False)
excel.Quit()

print(f"Archivo exportado a PDF: {archivo_pdf}")
