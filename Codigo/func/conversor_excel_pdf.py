import os
import win32com.client

class ConversorExcelPDF:
    def __init__(self):
        self.excel = win32com.client.Dispatch("Excel.Application")
        self.excel.Visible = False
        self.excel.DisplayAlerts = False  # <-- MUY IMPORTANTE
        self.excel.ScreenUpdating = False # <-- MUY IMPORTANTE
    
    def convertir_excel_a_pdf(self, ruta_excel, ruta_salida_pdf):
        try:
            libro = self.excel.Workbooks.Open(ruta_excel, UpdateLinks=False) # No actualizar enlaces
            libro.ExportAsFixedFormat(0, ruta_salida_pdf)
            libro.Close(False) # False = no guardar cambios
            print(f"[→] PDF creado: {ruta_salida_pdf}")
        except Exception as e:
            print(f"[!] Error al convertir Excel a PDF: {e}")
        finally: # Asegúrate de que el libro se cierre incluso si hay un error
            try:
                if libro:
                    libro.Close(False)
            except:
                pass # Ignorar errores al cerrar si ya está cerrado o no existe

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
        libro = None # Inicializa libro para asegurar que esté definido
        try:
            # UpdateLinks=False evita que Excel intente actualizar vínculos a fuentes externas,
            # lo que puede causar diálogos o congelamientos.
            libro = self.excel.Workbooks.Open(ruta_excel, UpdateLinks=False)
            # xlTypePDF = 0, xlQualityStandard = 0 (valores predeterminados)
            # Para exportar hojas específicas, necesitarías iterar:
            # for sheet in libro.Sheets:
            #    sheet.ExportAsFixedFormat(0, "ruta_salida_para_hoja.pdf")
            libro.ExportAsFixedFormat(0, ruta_salida_pdf)
            libro.Close(False) # False = No guardar cambios al cerrar el libro
            print(f"[→] PDF creado: {ruta_salida_pdf}")
            return True # Indica que la conversión fue exitosa
        except Exception as e:
            print(f"[!] Error al convertir Excel a PDF: {e}")
            return False # Indica que la conversión falló
        finally:
            # Asegúrate de cerrar el libro y liberar recursos, incluso si hay un error
            if libro is not None:
                try:
                    libro.Close(False) # Asegúrate de cerrar sin guardar
                except Exception as close_e:
                    print(f"[!] Advertencia: Error al intentar cerrar el libro de Excel: {close_e}")
            # Resetear la configuración de Excel al estado original
            self.excel.DisplayAlerts = True
            self.excel.ScreenUpdating = True

    def cerrar(self):
        try:
            self.excel.Quit()
            # Asegúrate de liberar completamente el objeto COM
            del self.excel
        except Exception as e:
            print(f"[!] Error al cerrar Excel: {e}")
        # pythoncom.CoUninitialize() # Necesario si CoInitialize fue llamado

