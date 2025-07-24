import os
from collections import defaultdict

# Ruta del script actual (carpeta donde se ejecuta este archivo)
carpeta_base = os.path.dirname(__file__)
ruta_syllabus = os.path.join(carpeta_base, "..", "..", "Sylabus_Electronica")  

# Normalizar la ruta por si estás en Windows
ruta_syllabus = os.path.abspath(ruta_syllabus)

def listar_y_clasificar_por_subcarpeta(ruta_base):
    estructura = defaultdict(lambda: {"pdf": [], "excel": [], "otros": []})

    for carpeta_actual, subcarpetas, archivos in os.walk(ruta_base):
        subcarpeta_relativa = os.path.relpath(carpeta_actual, ruta_base)

        for archivo in archivos:
            ruta_completa = os.path.join(carpeta_actual, archivo)
            extension = os.path.splitext(archivo)[1].lower()

            if extension == ".pdf":
                estructura[subcarpeta_relativa]["pdf"].append(ruta_completa)
            elif extension in [".xlsx", ".xls"]:
                estructura[subcarpeta_relativa]["excel"].append(ruta_completa)
            else:
                estructura[subcarpeta_relativa]["otros"].append(ruta_completa)

    return dict(estructura)

def imprimir_clasificados(resultado):
    for subcarpeta, tipos in resultado.items():
        print(f"\n📁 Subcarpeta: {subcarpeta}")
        for tipo, archivos in tipos.items():
            if archivos:
                print(f"  📌 {tipo.upper()} ({len(archivos)} archivos):")
                for archivo in archivos:
                    nombre = os.path.basename(archivo)
                    print(f"     - {nombre}")
            else:
                print(f"  📌 {tipo.upper()}: (vacío)")

if __name__ == "__main__":
    resultado = listar_y_clasificar_por_subcarpeta(ruta_syllabus)
    imprimir_clasificados(resultado)
