# Gestor Syllabus UD — Electron + React

## Estructura del proyecto
```
SYLABUS_UD/
├── Codigo/
│   └── tools/
│       ├── ActualizarCampos.py
│       ├── ConversorExcelPDF.py
│       └── Eliminar.py
└── gestor-ui/          ← esta carpeta
    ├── main.js
    ├── preload.js
    ├── package.json
    ├── vite.config.js
    ├── index.html
    └── src/
        ├── main.jsx
        ├── index.css
        └── App.jsx
```

## Instalación y ejecución

### 1. Instalar dependencias
```bash
cd gestor-ui
npm install
```

### 2. Modo desarrollo
```bash
npm run dev
```

### 3. Modo producción
```bash
npm run build
npm start
```

## Funcionalidades
- 📂 Seleccionar carpeta base
- 🔍 Buscar archivos por nombre
- 🗂 Filtrar por tipo (PDF / Excel)
- 📁 Filtrar por subcarpeta
- 📅 Ordenar por nombre / fecha / tamaño
- 🔄 Actualizar versión y fecha (llama ActualizarCampos.py)
- 📄 Convertir Excel a PDF (llama ConversorExcelPDF.py)
- 🗑️ Eliminar archivos seleccionados (llama Eliminar.py)
- 👆 Doble clic para abrir archivo
- ✓  Clic para seleccionar/deseleccionar archivos

## Notas
- Requiere Node.js instalado
- Requiere Python instalado
- Requiere LibreOffice para la conversión a PDF
