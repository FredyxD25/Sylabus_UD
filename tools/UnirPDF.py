import sys
import os
from pypdf import PdfWriter

def unir_pdfs(ruta_destino, rutas_pdfs):
    writer = PdfWriter()

    for ruta in rutas_pdfs:
        if not os.path.exists(ruta):
            print(f"No encontrado: {ruta}")
            continue
        if not ruta.lower().endswith('.pdf'):
            print(f"No es PDF: {ruta}")
            continue
        writer.append(ruta)
        print(f"Agregado: {os.path.basename(ruta)}")

    with open(ruta_destino, 'wb') as f:
        writer.write(f)

    print(f"\nPDF unido guardado en: {ruta_destino}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python UnirPDF.py <destino.pdf> <archivo1.pdf> <archivo2.pdf> ...")
        sys.exit(1)

    destino = sys.argv[1]
    archivos = sys.argv[2:]
    unir_pdfs(destino, archivos)