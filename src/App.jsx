import { useState, useMemo } from "react";

const api = window.api;

const iconos = { pdf: "📄", xlsx: "📊", xls: "📊" };

const formatBytes = (b) => {
  if (b < 1024) return `${b} B`;
  if (b < 1048576) return `${(b / 1024).toFixed(1)} KB`;
  return `${(b / 1048576).toFixed(1)} MB`;
};

const formatFecha = (iso) =>
  new Date(iso).toLocaleDateString("es-CO", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });

export default function App() {
  const [carpeta, setCarpeta] = useState(null);
  const [archivos, setArchivos] = useState([]);
  const [busqueda, setBusqueda] = useState("");
  const [filtroTipo, setFiltroTipo] = useState("todos");
  const [filtroCarpeta, setFiltroCarpeta] = useState("todas");
  const [orden, setOrden] = useState("nombre");
  const [cargando, setCargando] = useState(false);
  const [log, setLog] = useState([]);
  const [panel, setPanel] = useState(null);
  const [nuevaFecha, setNuevaFecha] = useState("");
  const [nombreUnion, setNombreUnion] = useState("union.pdf");
  const [seleccionados, setSeleccionados] = useState(new Set());

  const agregarLog = (msg, tipo = "info") =>
    setLog((prev) => [
      ...prev.slice(-50),
      { msg, tipo, t: new Date().toLocaleTimeString() },
    ]);

  const cargarArchivos = async (dir) => {
    setCargando(true);
    try {
      const lista = await api.listarArchivos(dir);
      setArchivos(lista);
      agregarLog(`${lista.length} archivos cargados`, "ok");
    } catch (e) {
      agregarLog(`Error al cargar: ${e}`, "error");
    } finally {
      setCargando(false);
    }
  };

  const seleccionarCarpeta = async () => {
    const dir = await api.seleccionarCarpeta();
    if (dir) {
      setCarpeta(dir);
      cargarArchivos(dir);
    }
  };

  const carpetasUnicas = useMemo(
    () => ["todas", ...new Set(archivos.map((a) => a.carpeta))],
    [archivos],
  );

  const archivosFiltrados = useMemo(() => {
    let lista = archivos;
    if (filtroTipo !== "todos")
      lista = lista.filter((a) => a.tipo === filtroTipo);
    if (filtroCarpeta !== "todas")
      lista = lista.filter((a) => a.carpeta === filtroCarpeta);
    if (busqueda)
      lista = lista.filter((a) =>
        a.nombre.toLowerCase().includes(busqueda.toLowerCase()),
      );
    return [...lista].sort((a, b) => {
      if (orden === "nombre") return a.nombre.localeCompare(b.nombre);
      if (orden === "fecha") return new Date(b.fecha) - new Date(a.fecha);
      if (orden === "tamaño") return b.tamaño - a.tamaño;
      return 0;
    });
  }, [archivos, filtroTipo, filtroCarpeta, busqueda, orden]);

  const [ultimoClick, setUltimoClick] = useState(null);

  const toggleSeleccion = (ruta, e) => {
    if (e.shiftKey && ultimoClick) {
      const lista = archivosFiltrados.map((a) => a.ruta);
      const indexA = lista.indexOf(ultimoClick);
      const indexB = lista.indexOf(ruta);
      const desde = Math.min(indexA, indexB);
      const hasta = Math.max(indexA, indexB);
      const rango = lista.slice(desde, hasta + 1);
      setSeleccionados((prev) => {
        const s = new Set(prev);
        rango.forEach((r) => s.add(r));
        return s;
      });
    } else {
      setSeleccionados((prev) => {
        const s = new Set(prev);
        s.has(ruta) ? s.delete(ruta) : s.add(ruta);
        return s;
      });
      setUltimoClick(ruta);
    }
  };

  const eliminarSeleccionados = async () => {
    if (!seleccionados.size) return;
    for (const ruta of seleccionados) {
      try {
        await api.eliminarArchivo({ ruta });
        agregarLog(`Eliminado: ${ruta.split("\\").pop()}`, "ok");
      } catch (e) {
        agregarLog(`Error eliminando: ${e}`, "error");
      }
    }
    setSeleccionados(new Set());
    cargarArchivos(carpeta);
  };

  const unirPDFs = async () => {
    const pdfsSeleccionados = [...seleccionados].filter((r) =>
      r.toLowerCase().endsWith(".pdf"),
    );
    if (pdfsSeleccionados.length < 2) {
      agregarLog("Selecciona al menos 2 PDFs para unir", "error");
      return;
    }
    const destino = `${carpeta}\\${nombreUnion.endsWith(".pdf") ? nombreUnion : nombreUnion + ".pdf"}`;
    setCargando(true);
    try {
      await api.unirPdfs({ rutas: pdfsSeleccionados, destino });
      agregarLog(`PDFs unidos → ${nombreUnion}`, "ok");
      setSeleccionados(new Set());
      setPanel(null);
      cargarArchivos(carpeta);
    } catch (e) {
      agregarLog(`Error al unir: ${e}`, "error");
    } finally {
      setCargando(false);
    }
  };

  const actualizarCampos = async () => {
    if (!carpeta || !nuevaFecha) return;
    setCargando(true);
    try {
      await api.actualizarCampos({ carpeta, nuevaFecha });
      agregarLog("Campos actualizados correctamente", "ok");
      cargarArchivos(carpeta);
    } catch (e) {
      agregarLog(`Error: ${e}`, "error");
    } finally {
      setCargando(false);
      setPanel(null);
    }
  };

  const convertirExcelPDF = async () => {
    if (!carpeta) return;
    setCargando(true);
    try {
      await api.convertirExcelPDF({ carpeta });
      agregarLog("Excel convertidos a PDF correctamente", "ok");
      cargarArchivos(carpeta);
    } catch (e) {
      agregarLog(`Error: ${e}`, "error");
    } finally {
      setCargando(false);
      setPanel(null);
    }
  };

  const pdfsSeleccionados = [...seleccionados].filter((r) =>
    r.toLowerCase().endsWith(".pdf"),
  ).length;

  return (
    <div style={s.root}>
      {/* ── Sidebar ── */}
      <aside style={s.sidebar}>
        <div style={s.logo}>
          <span style={s.logoIcon}>◈</span>
          <span style={s.logoText}>
            Syllabus
            <br />
            <b>Gestor UD</b>
          </span>
        </div>

        <button style={s.btnPrimary} onClick={seleccionarCarpeta}>
          📂 Seleccionar carpeta
        </button>

        {carpeta && (
          <div style={s.carpetaChip}>
            <span style={s.muted}>Carpeta activa</span>
            <span style={s.carpetaNombre}>{carpeta.split("\\").pop()}</span>
          </div>
        )}

        <div style={s.seccion}>ACCIONES</div>
        <button
          style={s.btnAccion}
          onClick={() => setPanel("actualizar")}
          disabled={!carpeta}
        >
          🔄 Actualizar versión / fecha
        </button>
        <button
          style={s.btnAccion}
          onClick={() => setPanel("convertir")}
          disabled={!carpeta}
        >
          📄 Convertir Excel → PDF
        </button>

        {seleccionados.size > 0 && (
          <>
            <div style={s.seccion}>SELECCIONADOS ({seleccionados.size})</div>
            {pdfsSeleccionados >= 2 && (
              <button
                style={{ ...s.btnAccion, ...s.btnUnir }}
                onClick={() => setPanel("unir")}
              >
                🔗 Unir PDFs ({pdfsSeleccionados})
              </button>
            )}
            <button
              style={{ ...s.btnAccion, ...s.btnDanger }}
              onClick={eliminarSeleccionados}
            >
              🗑️ Eliminar ({seleccionados.size})
            </button>
            <button
              style={{ ...s.btnAccion, color: "#5a6080" }}
              onClick={() => setSeleccionados(new Set())}
            >
              ✕ Limpiar selección
            </button>
          </>
        )}

        <div style={s.seccion}>FILTRAR POR TIPO</div>
        {["todos", "pdf", "xlsx"].map((t) => (
          <button
            key={t}
            style={filtroTipo === t ? s.filtroActivo : s.filtro}
            onClick={() => setFiltroTipo(t)}
          >
            {t === "todos" ? "🗂 Todos" : t === "pdf" ? "📄 PDF" : "📊 Excel"}
          </button>
        ))}

        <div style={s.seccion}>SUBCARPETA</div>
        <select
          style={s.select}
          value={filtroCarpeta}
          onChange={(e) => setFiltroCarpeta(e.target.value)}
        >
          {carpetasUnicas.map((c) => (
            <option key={c} value={c}>
              {c === "todas" ? "Todas" : c}
            </option>
          ))}
        </select>

        <div style={s.logBox}>
          {log
            .slice()
            .reverse()
            .map((l, i) => (
              <div
                key={i}
                style={{
                  ...s.logLine,
                  color:
                    l.tipo === "error"
                      ? "#e05b5b"
                      : l.tipo === "ok"
                        ? "#3ecf8e"
                        : "#5a6080",
                }}
              >
                <span style={{ opacity: 0.5 }}>{l.t}</span> {l.msg}
              </div>
            ))}
        </div>
      </aside>

      {/* ── Main ── */}
      <main style={s.main}>
        <div style={s.toolbar}>
          <input
            style={s.search}
            placeholder="🔍  Buscar archivo..."
            value={busqueda}
            onChange={(e) => setBusqueda(e.target.value)}
          />
          <div style={s.ordenGroup}>
            <span style={s.muted}>Ordenar:</span>
            {["nombre", "fecha", "tamaño"].map((o) => (
              <button
                key={o}
                style={orden === o ? s.ordenActivo : s.ordenBtn}
                onClick={() => setOrden(o)}
              >
                {o}
              </button>
            ))}
          </div>
          <span style={s.contador}>{archivosFiltrados.length} archivos</span>
          {carpeta && (
            <button
              style={s.btnRefresh}
              onClick={() => cargarArchivos(carpeta)}
            >
              ↻
            </button>
          )}
        </div>

        {cargando ? (
          <div style={s.empty}>⏳ Procesando...</div>
        ) : !carpeta ? (
          <div style={s.empty}>
            <div style={s.emptyIcon}>◈</div>
            <div>Selecciona una carpeta para comenzar</div>
          </div>
        ) : archivosFiltrados.length === 0 ? (
          <div style={s.empty}>Sin archivos que coincidan</div>
        ) : (
          <div style={s.grid}>
            {archivosFiltrados.map((a) => (
              <div
                key={a.ruta}
                style={{
                  ...s.card,
                  ...(seleccionados.has(a.ruta) ? s.cardSel : {}),
                }}
                onClick={(e) => toggleSeleccion(a.ruta, e)}
                onDoubleClick={() => api.abrirArchivo(a.ruta)}
              >
                <div style={s.cardIcon}>{iconos[a.tipo] || "📁"}</div>
                <div style={s.cardNombre} title={a.nombre}>
                  {a.nombre}
                </div>
                <div style={s.cardMeta}>
                  <span
                    style={{
                      ...s.tipoBadge,
                      background: a.tipo === "pdf" ? "#e05b5b22" : "#4f6ef722",
                      color: a.tipo === "pdf" ? "#e05b5b" : "#4f6ef7",
                    }}
                  >
                    {a.tipo.toUpperCase()}
                  </span>
                  <span style={s.muted}>{formatBytes(a.tamaño)}</span>
                </div>
                <div style={s.cardFecha}>{formatFecha(a.fecha)}</div>
                <div style={s.cardCarpeta} title={a.carpeta}>
                  📁 {a.carpeta}
                </div>
                {seleccionados.has(a.ruta) && <div style={s.check}>✓</div>}
              </div>
            ))}
          </div>
        )}
      </main>

      {/* ── Modales ── */}
      {panel && (
        <div style={s.overlay} onClick={() => setPanel(null)}>
          <div style={s.modal} onClick={(e) => e.stopPropagation()}>
            {panel === "actualizar" && (
              <>
                <h2 style={s.modalTitle}>🔄 Actualizar Versión y Fecha</h2>
                <p style={s.muted}>
                  Actualiza "Versión: 01 → 02" y la fecha de aprobación en todos
                  los Excel.
                </p>
                <label style={s.label}>Nueva fecha de aprobación</label>
                <input
                  style={s.input}
                  type="text"
                  placeholder="DD/MM/YYYY"
                  value={nuevaFecha}
                  onChange={(e) => setNuevaFecha(e.target.value)}
                />
                <div style={s.modalBtns}>
                  <button style={s.btnSecondary} onClick={() => setPanel(null)}>
                    Cancelar
                  </button>
                  <button
                    style={s.btnPrimary}
                    onClick={actualizarCampos}
                    disabled={!nuevaFecha}
                  >
                    Ejecutar
                  </button>
                </div>
              </>
            )}

            {panel === "convertir" && (
              <>
                <h2 style={s.modalTitle}>📄 Convertir Excel → PDF</h2>
                <p style={s.muted}>
                  Convierte todos los archivos Excel de la carpeta activa a PDF
                  usando LibreOffice.
                </p>
                <div style={s.modalBtns}>
                  <button style={s.btnSecondary} onClick={() => setPanel(null)}>
                    Cancelar
                  </button>
                  <button style={s.btnPrimary} onClick={convertirExcelPDF}>
                    Convertir todos
                  </button>
                </div>
              </>
            )}

            {panel === "unir" && (
              <>
                <h2 style={s.modalTitle}>🔗 Unir PDFs</h2>
                <p style={s.muted}>
                  Se unirán{" "}
                  <b style={{ color: "#4f6ef7" }}>{pdfsSeleccionados} PDFs</b>{" "}
                  en un solo archivo.
                </p>
                <label style={s.label}>Nombre del archivo resultante</label>
                <input
                  style={s.input}
                  type="text"
                  placeholder="union.pdf"
                  value={nombreUnion}
                  onChange={(e) => setNombreUnion(e.target.value)}
                />
                <p style={{ ...s.muted, fontSize: 11 }}>
                  Se guardará en la carpeta raíz seleccionada.
                </p>
                <div style={s.modalBtns}>
                  <button style={s.btnSecondary} onClick={() => setPanel(null)}>
                    Cancelar
                  </button>
                  <button
                    style={{ ...s.btnPrimary, background: "#3ecf8e" }}
                    onClick={unirPDFs}
                  >
                    Unir PDFs
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

const s = {
  root: {
    display: "flex",
    height: "100vh",
    overflow: "hidden",
    background: "#0a0c12",
  },
  sidebar: {
    width: 240,
    background: "#0f1117",
    borderRight: "1px solid #1e2333",
    display: "flex",
    flexDirection: "column",
    padding: "20px 14px",
    gap: 8,
    overflow: "auto",
  },
  logo: { display: "flex", alignItems: "center", gap: 10, marginBottom: 12 },
  logoIcon: { fontSize: 24, color: "#4f6ef7" },
  logoText: { fontSize: 13, lineHeight: 1.3, color: "#e8eaf0" },
  btnPrimary: {
    background: "#4f6ef7",
    color: "#fff",
    border: "none",
    borderRadius: 8,
    padding: "9px 14px",
    fontWeight: 700,
    fontSize: 13,
    cursor: "pointer",
  },
  btnSecondary: {
    background: "#1e2333",
    color: "#e8eaf0",
    border: "1px solid #2a2f45",
    borderRadius: 8,
    padding: "9px 14px",
    fontWeight: 600,
    fontSize: 13,
    cursor: "pointer",
  },
  btnAccion: {
    background: "#12151f",
    color: "#e8eaf0",
    border: "1px solid #1e2333",
    borderRadius: 8,
    padding: "8px 12px",
    fontSize: 12,
    fontWeight: 600,
    textAlign: "left",
    cursor: "pointer",
  },
  btnDanger: { borderColor: "#e05b5b44", color: "#e05b5b" },
  btnUnir: { borderColor: "#3ecf8e44", color: "#3ecf8e" },
  carpetaChip: {
    background: "#12151f",
    border: "1px solid #1e2333",
    borderRadius: 8,
    padding: "8px 10px",
    display: "flex",
    flexDirection: "column",
    gap: 2,
  },
  carpetaNombre: {
    fontSize: 11,
    color: "#4f6ef7",
    fontFamily: "DM Mono, monospace",
    overflow: "hidden",
    textOverflow: "ellipsis",
    whiteSpace: "nowrap",
  },
  seccion: {
    fontSize: 10,
    fontWeight: 700,
    letterSpacing: 2,
    color: "#3a4060",
    marginTop: 8,
  },
  filtro: {
    background: "transparent",
    color: "#5a6080",
    border: "none",
    borderRadius: 6,
    padding: "6px 10px",
    fontSize: 12,
    textAlign: "left",
    cursor: "pointer",
  },
  filtroActivo: {
    background: "#4f6ef722",
    color: "#4f6ef7",
    border: "none",
    borderRadius: 6,
    padding: "6px 10px",
    fontSize: 12,
    textAlign: "left",
    cursor: "pointer",
    fontWeight: 700,
  },
  select: {
    background: "#12151f",
    color: "#e8eaf0",
    border: "1px solid #1e2333",
    borderRadius: 8,
    padding: "7px 10px",
    fontSize: 11,
    fontFamily: "DM Mono, monospace",
  },
  logBox: {
    marginTop: "auto",
    background: "#080a0f",
    borderRadius: 8,
    padding: 8,
    maxHeight: 140,
    overflow: "auto",
    display: "flex",
    flexDirection: "column",
    gap: 2,
  },
  logLine: { fontSize: 10, fontFamily: "DM Mono, monospace", lineHeight: 1.5 },
  main: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    overflow: "hidden",
  },
  toolbar: {
    display: "flex",
    alignItems: "center",
    gap: 10,
    padding: "14px 20px",
    borderBottom: "1px solid #1e2333",
    background: "#0f1117",
  },
  search: {
    flex: 1,
    background: "#12151f",
    border: "1px solid #1e2333",
    borderRadius: 8,
    padding: "8px 12px",
    color: "#e8eaf0",
    fontSize: 13,
  },
  ordenGroup: { display: "flex", alignItems: "center", gap: 4 },
  ordenBtn: {
    background: "transparent",
    color: "#5a6080",
    border: "none",
    borderRadius: 6,
    padding: "5px 9px",
    fontSize: 12,
    cursor: "pointer",
  },
  ordenActivo: {
    background: "#1e2333",
    color: "#e8eaf0",
    border: "none",
    borderRadius: 6,
    padding: "5px 9px",
    fontSize: 12,
    cursor: "pointer",
    fontWeight: 700,
  },
  contador: {
    fontSize: 12,
    color: "#3a4060",
    fontFamily: "DM Mono, monospace",
  },
  btnRefresh: {
    background: "#12151f",
    color: "#4f6ef7",
    border: "1px solid #1e2333",
    borderRadius: 8,
    padding: "6px 12px",
    fontSize: 16,
    cursor: "pointer",
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(200px,1fr))",
    gap: 12,
    padding: 20,
    overflow: "auto",
    flex: 1,
  },
  card: {
    background: "#0f1117",
    border: "1px solid #1e2333",
    borderRadius: 12,
    padding: 14,
    cursor: "pointer",
    position: "relative",
    transition: "border-color .2s",
    display: "flex",
    flexDirection: "column",
    gap: 6,
  },
  cardSel: { borderColor: "#4f6ef7", background: "#4f6ef710" },
  cardIcon: { fontSize: 28 },
  cardNombre: {
    fontSize: 12,
    fontWeight: 700,
    overflow: "hidden",
    textOverflow: "ellipsis",
    whiteSpace: "nowrap",
  },
  cardMeta: { display: "flex", alignItems: "center", gap: 6 },
  tipoBadge: {
    fontSize: 10,
    fontWeight: 700,
    borderRadius: 4,
    padding: "2px 6px",
  },
  cardFecha: {
    fontSize: 10,
    color: "#3a4060",
    fontFamily: "DM Mono, monospace",
  },
  cardCarpeta: {
    fontSize: 10,
    color: "#3a4060",
    overflow: "hidden",
    textOverflow: "ellipsis",
    whiteSpace: "nowrap",
  },
  check: {
    position: "absolute",
    top: 8,
    right: 8,
    background: "#4f6ef7",
    color: "#fff",
    borderRadius: "50%",
    width: 20,
    height: 20,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: 11,
    fontWeight: 700,
  },
  empty: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    gap: 12,
    color: "#3a4060",
    fontSize: 14,
  },
  emptyIcon: { fontSize: 48, color: "#1e2333" },
  overlay: {
    position: "fixed",
    inset: 0,
    background: "#00000088",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    zIndex: 100,
  },
  modal: {
    background: "#12151f",
    border: "1px solid #1e2333",
    borderRadius: 16,
    padding: 28,
    width: 420,
    display: "flex",
    flexDirection: "column",
    gap: 14,
  },
  modalTitle: { fontSize: 18, fontWeight: 800 },
  modalBtns: {
    display: "flex",
    gap: 10,
    justifyContent: "flex-end",
    marginTop: 8,
  },
  label: { fontSize: 12, color: "#5a6080", fontWeight: 600 },
  input: {
    background: "#0a0c12",
    border: "1px solid #1e2333",
    borderRadius: 8,
    padding: "10px 12px",
    color: "#e8eaf0",
    fontSize: 13,
  },
  muted: { fontSize: 12, color: "#5a6080" },
};
