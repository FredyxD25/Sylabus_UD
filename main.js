const {
  app,
  BrowserWindow,
  ipcMain,
  dialog,
  shell,
  Menu,
} = require("electron");
const path = require("path");
const { spawn } = require("child_process");
const fs = require("fs");

const PYTHON = "python";
const TOOLS_PATH = path.join(__dirname, "tools");

function createWindow() {
  const win = new BrowserWindow({
    width: 1280,
    height: 800,
    minWidth: 900,
    minHeight: 600,
    backgroundColor: "#0f1117",
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });
  Menu.setApplicationMenu(null);
  const isDev = process.env.NODE_ENV === "development";
  if (isDev) {
    win.loadURL("http://localhost:5173");
    win.webContents.openDevTools();
  } else {
    win.loadFile(path.join(__dirname, "dist", "index.html"));
  }
}

ipcMain.handle("seleccionar-carpeta", async () => {
  const result = await dialog.showOpenDialog({ properties: ["openDirectory"] });
  return result.canceled ? null : result.filePaths[0];
});

ipcMain.handle("listar-archivos", async (_, carpeta) => {
  const archivos = [];
  function recorrer(dir) {
    if (!fs.existsSync(dir)) return;
    const items = fs.readdirSync(dir, { withFileTypes: true });
    for (const item of items) {
      const rutaCompleta = path.join(dir, item.name);
      if (item.isDirectory()) {
        recorrer(rutaCompleta);
      } else {
        const ext = path.extname(item.name).toLowerCase();
        if ([".pdf", ".xlsx", ".xls"].includes(ext)) {
          const stat = fs.statSync(rutaCompleta);
          archivos.push({
            nombre: item.name,
            ruta: rutaCompleta,
            carpeta: path.relative(carpeta, dir) || ".",
            tipo: ext.replace(".", ""),
            tamaño: stat.size,
            fecha: stat.mtime.toISOString(),
          });
        }
      }
    }
  }
  recorrer(carpeta);
  return archivos;
});

ipcMain.handle("abrir-archivo", async (_, ruta) => {
  await shell.openPath(ruta);
});

function ejecutarPython(script, args = []) {
  return new Promise((resolve, reject) => {
    const scriptPath = path.join(TOOLS_PATH, script);
    const proc = spawn(PYTHON, [scriptPath, ...args]);
    let salida = "";
    let error = "";
    proc.stdout.on("data", (d) => (salida += d.toString()));
    proc.stderr.on("data", (d) => (error += d.toString()));
    proc.on("close", (code) => {
      if (code === 0) resolve(salida);
      else reject(error || `Error código ${code}`);
    });
  });
}

ipcMain.handle("actualizar-version", async (_, { carpeta }) =>
  ejecutarPython("ActualizarVersion.py", [carpeta]),
);

ipcMain.handle("actualizar-fecha", async (_, { carpeta, nuevaFecha }) =>
  ejecutarPython("ActualizarFecha.py", [carpeta, nuevaFecha]),
);

ipcMain.handle("convertir-excel-pdf", async (_, { carpeta }) =>
  ejecutarPython("ConversorExcelPDF.py", [carpeta]),
);

ipcMain.handle("eliminar-archivo", async (_, { ruta }) =>
  ejecutarPython("Eliminar.py", [ruta]),
);

ipcMain.handle("unir-pdfs", async (_, { rutas, destino }) =>
  ejecutarPython("UnirPDF.py", [destino, ...rutas]),
);

app.whenReady().then(createWindow);
app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});
