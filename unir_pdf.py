from PyPDF2 import PdfMerger
#pip install PyPDF2

# Lista de archivos PDF que quieres unir (en orden)
archivos_pdf = ["archivo1.pdf", "archivo2.pdf"]

# Crear objeto combinador
combinador = PdfMerger()

# Agregar cada PDF al combinador
for archivo in archivos_pdf:
    combinador.append(archivo)

# Guardar el PDF combinado
combinador.write("unido.pdf")
combinador.close()

print("PDFs unidos correctamente en 'unido.pdf'")
