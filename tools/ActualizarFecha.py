import os
import sys
import glob
import re
import zipfile
import shutil

PATRON_FECHA = r"Fecha de Aprobaci&#xF3;n:(?:&#10;|\n| )?\s*\d{1,2}/\d{1,2}/\d{4}"
PATRON_FECHA2 = r"Fecha de Aprobaci\u00f3n:(?:&#10;|\n| )?\s*\d{1,2}/\d{1,2}/\d{4}"

def reemplazar_en_xml(contenido_bytes, nueva_fecha):
    try:
        texto = contenido_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return contenido_bytes, False

    # El XML puede tener la ó como &#xF3; o como ó directamente
    nuevo_texto_fecha = f"Fecha de Aprobaci\u00f3n:&#10;{nueva_fecha}"

    # Intentar con ó como entidad XML
    patron1 = r"Fecha de Aprobaci&#xF3;n:(?:&#10;|\n| )?\s*\d{1,2}/\d{1,2}/\d{4}"
    # Intentar con ó como unicode directo
    patron2 = r"Fecha de Aprobaci\u00f3n:(?:&#10;|\n| )?\s*\d{1,2}/\d{1,2}/\d{4}"
    patron2 = "Fecha de Aprobaci\u00f3n:(?:&#10;|\n| )?\\s*\\d{1,2}/\\d{1,2}/\\d{4}"

    nuevo1, n1 = re.subn(patron1, nuevo_texto_fecha.replace("\u00f3", "&#xF3;"), texto)
    if n1 > 0:
        return nuevo1.encode("utf-8"), True

    nuevo2, n2 = re.subn(patron2, nuevo_texto_fecha, texto)
    if n2 > 0:
        return nuevo2.encode("utf-8"), True

    return contenido_bytes, False

def procesar_excel(ruta_archivo, nueva_fecha):
    nombre = os.path.basename(ruta_archivo)
    tmp_zip = ruta_archivo + ".tmp_repack.xlsx"
    try:
        with zipfile.ZipFile(ruta_archivo, "r") as zin:
            infolist   = zin.infolist()
            contenidos = {info.filename: zin.read(info.filename) for info in infolist}

        archivos_a_procesar = [
            fn for fn in contenidos
            if (fn == "xl/sharedStrings.xml" or fn.startswith("xl/worksheets/"))
            and fn.endswith(".xml")
        ]

        archivo_modificado = False
        for fn in archivos_a_procesar:
            nuevo, mod = reemplazar_en_xml(contenidos[fn], nueva_fecha)
            if mod:
                contenidos[fn] = nuevo
                archivo_modificado = True

        if not archivo_modificado:
            print(f"Sin cambios: {nombre}")
            return

        with zipfile.ZipFile(tmp_zip, "w", allowZip64=True) as zout:
            for info in infolist:
                zi = zipfile.ZipInfo(info.filename)
                zi.compress_type  = info.compress_type
                zi.external_attr  = info.external_attr
                zi.create_system  = info.create_system
                zi.create_version = info.create_version
                zi.date_time      = info.date_time
                zi.flag_bits      = info.flag_bits & ~0x8
                zout.writestr(zi, contenidos[info.filename])

        shutil.move(tmp_zip, ruta_archivo)
        print(f"Actualizado: {nombre}")

    except Exception as e:
        print(f"Error: {nombre} -> {e}")
        if os.path.exists(tmp_zip):
            os.remove(tmp_zip)

def main(carpeta, nueva_fecha):
    excels  = glob.glob(os.path.join(carpeta, "**", "*.xlsx"), recursive=True)
    excels += glob.glob(os.path.join(carpeta, "**", "*.xls"),  recursive=True)
    if not excels:
        print("No se encontraron archivos Excel.")
        return
    print(f"Carpeta: {carpeta}")
    print(f"Excel encontrados: {len(excels)}")
    print(f"Nueva fecha: {nueva_fecha}")
    print("=" * 55)
    for archivo in excels:
        procesar_excel(archivo, nueva_fecha)
    print("=" * 55)
    print("Proceso completado.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python ActualizarFecha.py <carpeta> <nueva_fecha>")
        print("Ejemplo: python ActualizarFecha.py C:\\mis\\excels 15/03/2024")
        sys.exit(1)
    carpeta     = sys.argv[1]
    nueva_fecha = sys.argv[2]
    if not os.path.isdir(carpeta):
        print(f"La carpeta no existe: {carpeta}")
        sys.exit(1)
    main(carpeta, nueva_fecha)
