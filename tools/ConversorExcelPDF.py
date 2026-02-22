import os
import glob
import subprocess
import time

LIBREOFFICE_PATH = r"C:\Program Files\LibreOffice\program\soffice.exe"

class ConversorExcelPDF:
    """
    Convierte archivos Excel (.xlsx, .xls) a PDF usando LibreOffice.
    Si LibreOffice no está abierto, lo abre automáticamente.
    """

    def __init__(self, carpeta):
        self.carpeta = carpeta
        self._asegurar_libreoffice_activo()

    def _libreoffice_instalado(self):
        return os.path.exists(LIBREOFFICE_PATH)

    def _libreoffice_corriendo(self):
        resultado = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq soffice.exe"],
            capture_output=True, text=True
        )
        return "soffice.exe" in resultado.stdout

    def _asegurar_libreoffice_activo(self):
        if not self._libreoffice_instalado():
            print("❌ LibreOffice no está instalado.")
            print("   Descárgalo en: https://www.libreoffice.org/download/download/")
            raise FileNotFoundError("LibreOffice no encontrado.")

        if not self._libreoffice_corriendo():
            print("🚀 Iniciando LibreOffice...")
            subprocess.Popen([LIBREOFFICE_PATH, "--headless"])
            time.sleep(3)  # espera a que arranque
            print("✅ LibreOffice iniciado correctamente.")
        else:
            print("✅ LibreOffice ya está activo.")

    def convertir_archivo(self, ruta_excel):
        try:
            carpeta_destino = os.path.dirname(ruta_excel)

            subprocess.run([
                LIBREOFFICE_PATH,
                "--headless",
                "--convert-to", "pdf",
                "--outdir", carpeta_destino,
                ruta_excel
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            nombre_pdf = os.path.splitext(os.path.basename(ruta_excel))[0] + ".pdf"
            ruta_pdf = os.path.join(carpeta_destino, nombre_pdf)
            print(f"✅ Convertido: {os.path.basename(ruta_excel)} → {nombre_pdf}")
            return ruta_pdf

        except subprocess.CalledProcessError as e:
            print(f"❌ Error al convertir: {os.path.basename(ruta_excel)} → {e}")
            return None

    def convertir_todos(self):
        excels = glob.glob(os.path.join(self.carpeta, "**", "*.xlsx"), recursive=True)
        excels += glob.glob(os.path.join(self.carpeta, "**", "*.xls"), recursive=True)

        if not excels:
            print("⚠️  No se encontraron archivos Excel.")
            return []

        print(f"📂 Carpeta: {self.carpeta}")
        print(f"📊 Excel encontrados: {len(excels)}")
        print("=" * 55)

        pdfs_generados = []
        for archivo in excels:
            pdf = self.convertir_archivo(archivo)
            if pdf:
                pdfs_generados.append(pdf)

        print("=" * 55)
        print(f"✔️  PDFs generados: {len(pdfs_generados)} de {len(excels)}")
        return pdfs_generados


# ── USO ──────────────────────────────────────────────────────
if __name__ == "__main__":
    CARPETA = r"E:\Datos Fredy\Programacion\Sylabus_UD\Syllabus_Electronica"

    conversor = ConversorExcelPDF(CARPETA)
    conversor.convertir_todos()