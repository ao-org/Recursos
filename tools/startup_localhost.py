import subprocess
import time
import os

def ejecutar_secuencia():
    print("Iniciando script desde Recursos/tools...")
    
    # 5 segundos de espera inicial
    print("Esperando 5 segundos antes de iniciar...")
    time.sleep(5)
    
    # --- DETECCIÓN DE RUTAS RELATIVAS ---
    # os.path.dirname(__file__) obtiene la ubicación actual de este script (Recursos\tools)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Subimos dos niveles para llegar a la raíz (\GitHub)
    github_dir = os.path.abspath(os.path.join(base_dir, "..", ".."))
    
    # Construimos las rutas dinámicamente a partir de la raíz de GitHub
    server_path = os.path.join(github_dir, "argentum-online-server", "Server.exe")
    script_path = os.path.join(github_dir, "Recursos", "tools", "generar_localindex.py")
    client_path = os.path.join(github_dir, "argentum-online-client", "Argentum.exe")
    # ------------------------------------

    # 1. Ejecutar Server.exe
    print(f"Ejecutando: {server_path}")
    subprocess.Popen(server_path, cwd=os.path.dirname(server_path))
    
    # Pausa 5 segundos
    print("Pausa de 5 segundos...")
    time.sleep(5)
    
    # 2. Ejecutar generar_localindex.py
    print(f"Ejecutando: {script_path}")
    subprocess.run(["python", script_path], cwd=os.path.dirname(script_path))
    
    # Pausa 5 segundos
    print("Pausa de 5 segundos...")
    time.sleep(5)
    
    # 3. Ejecutar Argentum.exe
    print(f"Ejecutando: {client_path}")
    subprocess.Popen(client_path, cwd=os.path.dirname(client_path))
    
    print("Secuencia completada con éxito.")

if __name__ == "__main__":
    ejecutar_secuencia()