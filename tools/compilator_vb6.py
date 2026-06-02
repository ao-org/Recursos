import subprocess
import os
import sys
import ctypes

def es_administrador():
    """Verifica si el script actual tiene privilegios de administrador."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def compilar_proyecto_vb6(vb6_exe, ruta_vbp, nombre_componente):
    """Ejecuta la compilación de un archivo VBP específico en su propia carpeta."""
    if not os.path.exists(ruta_vbp):
        print(f"❌ Error: No se encontró el archivo de {nombre_componente} en: {ruta_vbp}")
        return False

    print(f"🔨 Compilando {nombre_componente}...")
    comando = [vb6_exe, "/make", ruta_vbp]

    try:
        subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        print(f"✅ {nombre_componente} compilado con éxito junto a su archivo VBP.\n")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al compilar {nombre_componente}.")
        ruta_log = ruta_vbp.replace(".vbp", ".log")
        if os.path.exists(ruta_log):
            print(f"📋 Se generó un registro de errores en {nombre_componente}:")
            with open(ruta_log, 'r', encoding='latin-1') as log_file:
                print(log_file.read())
        else:
            print(f"Detalle del error del sistema: {e.stderr}")
        print("-" * 50)
        return False

def main():
    # --- AUTO-ELEVACIÓN DE PRIVILEGIOS ---
    if not es_administrador():
        print("🔰 El script requiere permisos de administrador. Solicitando elevación...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()
    # -------------------------------------

    rutas_vb6 = [
        r"C:\Program Files (x86)\Microsoft Visual Studio\VB98\VB6.EXE",
        r"C:\Program Files\Microsoft Visual Studio\VB98\VB6.EXE"
    ]
    
    vb6_exe = None
    for ruta in rutas_vb6:
        if os.path.exists(ruta):
            vb6_exe = ruta
            break
            
    if not vb6_exe:
        print("❌ Error crítico: No se encontró VB6.EXE en tu sistema.")
        input("\nPresioná Enter para salir...")
        return

    # --- DETECCIÓN DINÁMICA DE RUTAS RELATIVAS ---
    # __file__ es la ruta de este script: .../GitHub/Recursos/tools/compilator_vb6.py
    ruta_script = os.path.abspath(__file__)
    
    # Subimos 3 niveles para llegar a la carpeta raíz común (ej: 'GitHub' o donde compartan espacio)
    # 1 nivel arriba -> .../GitHub/Recursos/tools
    # 2 niveles arriba -> .../GitHub/Recursos
    # 3 niveles arriba -> .../GitHub (Carpeta contenedora de los repositorios)
    raiz_github = os.path.dirname(os.path.dirname(os.path.dirname(ruta_script)))

    # Armamos los caminos uniendo la raíz detectada con las carpetas de los proyectos
    proyectos = {
        "Servidor AO": os.path.join(raiz_github, "argentum-online-server", "Server.vbp"),
        "Cliente AO": os.path.join(raiz_github, "argentum-online-client", "Argentum20.vbp")
    }
    # ----------------------------------------------

    print("=" * 50)
    print("🚀 INICIANDO COMPILACIÓN DE ARGENTUM ONLINE")
    print(f"📂 Raíz detectada: {raiz_github}")
    print("=" * 50 + "\n")

    for componente, ruta_vbp in proyectos.items():
        compilar_proyecto_vb6(vb6_exe, ruta_vbp, componente)

    print("🏁 Proceso terminado.")
    input("\nPresioná Enter para cerrar...")

if __name__ == "__main__":
    main()