import os
import sys

# ============================================================
#  CONFIGURACIÓN
# ============================================================
CARPETA_RAIZ = r"E:\Datos Fredy\Programacion\Sylabus_UD\Syllabus_Electronica"
DRY_RUN = True               # True = solo muestra qué eliminaría, False = elimina de verdad

EXTENSIONES_EXCEL = {".xlsx", ".xls", ".xlsm", ".xlsb"}
# ============================================================

def eliminar_no_excel(carpeta_raiz: str, dry_run: bool = True):
    archivos_eliminados = []
    archivos_omitidos = []
    errores = []

    print(f"{'[SIMULACIÓN]' if dry_run else '[ELIMINACIÓN REAL]'} Procesando: {carpeta_raiz}\n")
    print("=" * 60)

    for dirpath, dirnames, filenames in os.walk(carpeta_raiz):
        for filename in filenames:
            _, ext = os.path.splitext(filename)
            ruta_completa = os.path.join(dirpath, filename)

            if ext.lower() in EXTENSIONES_EXCEL:
                archivos_omitidos.append(ruta_completa)
                print(f"  [CONSERVAR] {ruta_completa}")
            else:
                archivos_eliminados.append(ruta_completa)
                print(f"  [ELIMINAR]  {ruta_completa}")
                if not dry_run:
                    try:
                        os.remove(ruta_completa)
                    except Exception as e:
                        errores.append((ruta_completa, str(e)))
                        print(f"    ⚠ Error al eliminar: {e}")

    print("\n" + "=" * 60)
    print(f"Archivos Excel conservados : {len(archivos_omitidos)}")
    print(f"Archivos a eliminar        : {len(archivos_eliminados)}")

    if dry_run:
        print("\n⚠  MODO SIMULACIÓN activado. Ningún archivo fue eliminado.")
        print("   Cambia DRY_RUN = False para eliminar de verdad.")
    else:
        print(f"Archivos eliminados        : {len(archivos_eliminados) - len(errores)}")
        if errores:
            print(f"Errores                    : {len(errores)}")
            for ruta, error in errores:
                print(f"  - {ruta}: {error}")
        print("\n✅ Proceso completado.")


if __name__ == "__main__":
    # Permite pasar la carpeta como argumento: python eliminar_no_excel.py "C:/mi/carpeta"
    if len(sys.argv) > 1:
        CARPETA_RAIZ = sys.argv[1]

    if not os.path.isdir(CARPETA_RAIZ):
        print(f"Error: '{CARPETA_RAIZ}' no es una carpeta válida.")
        sys.exit(1)

    eliminar_no_excel(CARPETA_RAIZ, dry_run=DRY_RUN)