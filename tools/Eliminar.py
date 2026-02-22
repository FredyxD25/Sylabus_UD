import os
import sys

def eliminar_archivo(ruta):
    if not os.path.exists(ruta):
        print(f"⚠️  No existe: {ruta}")
        return False
    try:
        os.remove(ruta)
        print(f"✅ Eliminado: {os.path.basename(ruta)}")
        return True
    except Exception as e:
        print(f"❌ Error al eliminar {os.path.basename(ruta)}: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Uso: python Eliminar.py <ruta_archivo>")
        sys.exit(1)

    ruta = sys.argv[1]
    ok = eliminar_archivo(ruta)
    sys.exit(0 if ok else 1)