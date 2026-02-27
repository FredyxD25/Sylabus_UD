import os
import sys
import glob
import zipfile
import shutil

REEMPLAZOS = {
    "Código: AA-FR-003": "Código: CC-FR-003",
    "Codigo: AA-FR-003": "Codigo: CC-FR-003",
}

def reemplazar_en_xml(contenido_bytes):
    try:
        texto = contenido_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return contenido_bytes, False
    modificado = False
    for buscar, reemplazar in REEMPLAZOS.items():
        if buscar in texto:
            texto = texto.replace(buscar, reemplazar)
            modificado = True
    return texto.encode("utf-8"), modificado

def procesar_excel(ruta_archivo):
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
            nuevo, mod = reemplazar_en_xml(contenidos[fn])
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

def main(carpeta):
    excels  = glob.glob(os.path.join(carpeta, "**", "*.xlsx"), recursive=True)
    excels += glob.glob(os.path.join(carpeta, "**", "*.xls"),  recursive=True)
    if not excels:
        print("No se encontraron archivos Excel.")
        return
    print(f"Carpeta: {carpeta}")
    print(f"Excel encontrados: {len(excels)}")
    print("Codigo: AA-FR-003 -> CC-FR-003")
    print("=" * 55)
    for archivo in excels:
        procesar_excel(archivo)
    print("=" * 55)
    print("Proceso completado.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python ActualizarCodigo.py <carpeta>")
        sys.exit(1)
    carpeta = sys.argv[1]
    if not os.path.isdir(carpeta):
        print(f"La carpeta no existe: {carpeta}")
        sys.exit(1)
    main(carpeta)
