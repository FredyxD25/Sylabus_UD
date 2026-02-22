import os
import glob
import re
from openpyxl import load_workbook

# ─── CONFIGURACIÓN ───────────────────────────────────────────
CARPETA = r"E:\Datos Fredy\Programacion\Sylabus_UD\Syllabus_Electronica"
NUEVA_FECHA = "22/02/2025"  # ← cambia esto a la nueva fecha
# ─────────────────────────────────────────────────────────────

REEMPLAZOS = {
    "Versión: 01": "Versión: 02",
    "Version: 01": "Version: 02",
}

PATRON_FECHA = r"Fecha de Aprobación:\s*\d{1,2}/\d{1,2}/\d{4}"
NUEVO_TEXTO_FECHA = f"Fecha de Aprobación:\n{NUEVA_FECHA}"

def procesar_celda(valor):
    if not isinstance(valor, str):
        return valor, False
    modificado = False
    for buscar, reemplazar in REEMPLAZOS.items():
        if buscar in valor:
            valor = valor.replace(buscar, reemplazar)
            modificado = True
    nuevo_valor, n = re.subn(PATRON_FECHA, NUEVO_TEXTO_FECHA, valor)
    if n > 0:
        valor = nuevo_valor
        modificado = True
    return valor, modificado

def procesar_excel(ruta_archivo):
    try:
        wb = load_workbook(ruta_archivo)
        archivo_modificado = False
        for nombre_hoja in wb.sheetnames:
            hoja = wb[nombre_hoja]
            for fila in hoja.iter_rows():
                for celda in fila:
                    nuevo_valor, modificado = procesar_celda(celda.value)
                    if modificado:
                        celda.value = nuevo_valor
                        archivo_modificado = True
        if archivo_modificado:
            wb.save(ruta_archivo)
            print(f"✅ Actualizado: {os.path.basename(ruta_archivo)}")
        else:
            print(f"⏭️  Sin cambios: {os.path.basename(ruta_archivo)}")
    except Exception as e:
        print(f"❌ Error: {os.path.basename(ruta_archivo)} → {e}")

def main():
    excels = glob.glob(os.path.join(CARPETA, "**", "*.xlsx"), recursive=True)
    excels += glob.glob(os.path.join(CARPETA, "**", "*.xls"), recursive=True)

    if not excels:
        print("⚠️  No se encontraron archivos Excel.")
        return

    print(f"📂 Carpeta: {CARPETA}")
    print(f"📊 Excel encontrados: {len(excels)}")
    print(f"🔄 Versión: 01 → 02")
    print(f"📅 Nueva fecha: {NUEVA_FECHA}")
    print("=" * 55)

    for archivo in excels:
        procesar_excel(archivo)

    print("=" * 55)
    print("✔️  Proceso completado.")

if __name__ == "__main__":
    main()