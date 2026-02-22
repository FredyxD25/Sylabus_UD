const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('api', {
  seleccionarCarpeta: () => ipcRenderer.invoke('seleccionar-carpeta'),
  listarArchivos: (carpeta) => ipcRenderer.invoke('listar-archivos', carpeta),
  abrirArchivo: (ruta) => ipcRenderer.invoke('abrir-archivo', ruta),
  actualizarCampos: (datos) => ipcRenderer.invoke('actualizar-campos', datos),
  convertirExcelPDF: (datos) => ipcRenderer.invoke('convertir-excel-pdf', datos),
  eliminarArchivo: (datos) => ipcRenderer.invoke('eliminar-archivo', datos),
  unirPdfs: (datos) => ipcRenderer.invoke('unir-pdfs', datos),
})
