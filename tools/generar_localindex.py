import os
import configparser
import re

def main():
    # === CONFIGURACIÓN ===
    # Get the script's directory and navigate to find the correct base folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # If running from tools folder, go up to Recursos folder (where Dat and init are located)
    if os.path.basename(script_dir) == "tools":
        CARPETA_BASE = os.path.dirname(script_dir)  # This is the Recursos folder
    else:
        # Fallback to original logic
        CARPETA_BASE = os.path.abspath(os.path.join(os.getcwd(), ".."))
    
    CARPETA_DAT = os.path.join(CARPETA_BASE, "Dat")
    CARPETA_INIT = os.path.join(CARPETA_BASE, "init")
    
    # Debug: Print paths to verify they're correct
    print(f"Script directory: {script_dir}")
    print(f"Base directory: {CARPETA_BASE}")
    print(f"Dat directory: {CARPETA_DAT}")
    print(f"Init directory: {CARPETA_INIT}")
    
    # Check if directories exist
    if not os.path.exists(CARPETA_DAT):
        print(f"ERROR: Dat directory not found at {CARPETA_DAT}")
        return
    if not os.path.exists(CARPETA_INIT):
        print(f"ERROR: Init directory not found at {CARPETA_INIT}")
        return
    IDIOMAS = ["sp", "en", "pt", "fr", "it"]
    ARCHIVOS_IDIOMA = {
        "msg": "LocalMsg.dat",
        "sugerencias": "sugerencias.ini"
    }
    ARCHIVOS_BASE_DAT = ["obj.dat", "npcs.dat", "quests.dat", "hechizos.dat"]
    ARCHIVOS_BASE_INIT = ["NameMapa.dat"]

    # === ORDEN DE SECCIONES FIJO ===
    ORDEN_SECCIONES = (
        ["INIT", "SUGERENCIAS", "MODRAZA", "ES_MSG", "EN_MSG", "PT_MSG", "FR_MSG", "IT_MSG"]
        + [f"QUEST{i}" for i in range(1, 3000)]
        + [f"NPC{i}" for i in range(1, 3000)]
        + [f"HECHIZO{i}" for i in range(1, 3000)]
        + [f"OBJ{i}" for i in range(1, 3000)]
        + ["NAMEMAPA"]
    )

    # === CLAVES PERMITIDAS POR SECCIÓN (lista blanca; comparación case-insensitive) ===
    INCLUIR_CLAVES_POR_SECCION = {
        "NPC": [
            "Name", "Desc",  "Body", "BodyIdle", "Ataque1","BodyOnLand","BodyOnWater","BodyOnWaterIdle","Ataque2", "Head","DescClose",
            "EXP", "GiveEXPClan", "ORO", "HP", "MaxHIT", "MinHIT","IsGlobalQuestBoss",
            "NoMapInfo", "NumQuiza", "PuedeInvocar",
            "QuizaDropea1", "QuizaDropea2", "QuizaDropea3", "QuizaDropea4", "QuizaDropea5",
            "QuizaDropea6", "QuizaDropea7", "QuizaDropea8", "QuizaDropea9",
            "QuizaDropea10", "QuizaDropea11", "QuizaDropea12", "QuizaDropea13",
            "QuizaDropea14", "QuizaDropea15", "QuizaDropea16",
            "QuizaProb", "NROITEMS", "Obj1", "Obj2", "Obj3", "NpcType", "Comercia","Nivel"
        ],
        "OBJ": [
            "Name", "GrhIndex", "ObjType", "Agarrable", "Texto", "Llave", "Valor", "MaxDef", "MinDef", "MinHit", "MaxHit","MaxArmorPenetrationFlat","MinArmorPenetrationFlat","ExtraCritAndStabChance",
            "CD", "CDType", "Coal", "ColaDeZorro", "CreaGRH", "Destruye",
            "FlorOceano", "FlorRoja", "FrascoAlq", "Hechizo", "HongoDeLuz", "Info", "LingH",
            "LingO", "LingP", "Madera", "MaderaElfica", "Mortero", "Municiones",
            "PielLobo", "PielLoboNegro", "PielOsoPardo", "PielOsoPolar", "PielTigre",
            "PielTigreBengala", "Proyectil", "Raices", "SemillasPros", "SKHerreria",
            "SKPociones", "SKSastreria", "Tuna", "Blodium","ElementalTags","FireEssence","WaterEssence",
            "EarthEssence", "WindEssence","Cala","RequiereObjeto", "RopajeElfa", "RopajeElfaOscura", "RopajeElfo",
            "RopajeElfoOscuro", "RopajeEnana", "RopajeEnano", "RopajeGnoma", "RopajeGnomo", "RopajeHumana", "RopajeHumano",        "RopajeOrca",
            "RopajeOrco"
        ],
        "QUE": [
            "Name", "Desc", "DescFinal", "NextQuest", "Nombre", "PosMap", "Repetible", "RequiredLevel"
        ],
        "HEC": [
            "Nombre", "Desc", "Texto", "GrhIndex", "ManaRequerido", "HechizoTipo", "MinSkill",
            "MaxSkill", "HechizeroMsg", "Cooldown", "IconoIndex", "PalabrasMagicas", "PropioMsg",
            "StaRequerido", "TargetMsg"
        ]
    }

    # === RENOMBRADOS (aplican case-insensitive sobre la clave de origen) ===
    RENOMBRAR_CLAVES = {
        "NPC": {
            "GiveEXP": "EXP",
            "MaxHP": "HP",
            "GiveGLD": "ORO"
        },
        "HEC": {
            "Name": "Nombre"
        }
    }

    # === ORDEN PREFERIDO DE CLAVES EN LA SALIDA ===
    PRIORIDAD_CLAVES = {
        "NPC": ["Name", "Desc","DescClose", "Body","Head",  "BodyIdle", "Ataque1", "HP"],
    }

    # === EXCEPCIONES PARA ELIMINAR COMENTARIOS (se respeta el texto tras comillas) ===
    EXCEPTION_KEYS = {
        "palabrasmagicas",
        "name", "texto", "desc", "descfinal", "nombre",
        "en_name", "pt_name", "fr_name", "it_name",
        "en_texto", "pt_texto", "fr_texto", "it_texto",
        "propiomsg", "targetmsg"
    }
    MSG_OR_SUG_REGEX = re.compile(r'^(msg|sugerencia)\d+$', re.IGNORECASE)

    # === FUNCIONES AUXILIARES ===
    def buscar_archivo_sin_case(carpeta, nombre_esperado):
        if not os.path.isdir(carpeta):
            return None
        for archivo in os.listdir(carpeta):
            if archivo.lower() == nombre_esperado.lower():
                return os.path.join(carpeta, archivo)
        return None

    def normalizar_idioma(clave):
        clave = clave.strip()
        for lang in IDIOMAS:
            pref = f"{lang}_"
            if clave.lower().startswith(pref):
                return lang, clave[len(pref):]
        return None, clave

    def cargar_ini(ruta):
        config = configparser.ConfigParser(strict=False, delimiters=("="), interpolation=None)
        config.optionxform = str  # mantener caso
        with open(ruta, encoding="latin-1") as f:
            config.read_file(f)
        return config

    def cargar_ini_balance(ruta):
        config = configparser.ConfigParser(strict=False, delimiters=("="), interpolation=None)
        config.optionxform = str
        with open(ruta, encoding="latin-1") as f:
            lineas_validas = [linea for linea in f if not linea.lstrip().startswith("'")]
            config.read_string("".join(lineas_validas))
        return config

    def extraer_valor_txt(archivo, clave_buscada):
        if not os.path.exists(archivo):
            return "0"
        clave_buscada = clave_buscada.upper()
        with open(archivo, encoding="latin-1") as f:
            dentro = False
            for linea in f:
                linea = linea.strip()
                if linea.startswith("[INIT]"):
                    dentro = True
                elif linea.startswith("[") and dentro:
                    break
                elif dentro and "=" in linea:
                    clave, valor = linea.split("=", 1)
                    if clave.strip().upper() == clave_buscada:
                        return valor.strip()
        return "0"

    def obtener_valor_sugerencias(archivo):
        if not archivo or not os.path.exists(archivo):
            return "0"
        config = cargar_ini(archivo)
        for section in config.sections():
            if section.upper().endswith("_SUGERENCIAS") or section.upper() == "SUGERENCIAS":
                sec = config[section]
                return sec.get("NumSugerencias", "0")
        return "0"

    def contar_secciones(archivo, prefijo):
        if not os.path.exists(archivo):
            return 0
        with open(archivo, encoding="latin-1") as f:
            pref = f"[{prefijo}"
            return sum(1 for linea in f if linea.strip().startswith(pref))

    def procesar_archivo(ruta, secciones_dict):
        """Parseo tolerante: '[NPC601] 'coment' → usa 'NPC601' y descarta comentario."""
        if not os.path.exists(ruta):
            print(f"Archivo no encontrado: {ruta}")
            return
        with open(ruta, encoding="latin-1") as f:
            seccion = None
            claves_por_idioma = {lang: {} for lang in IDIOMAS}
            for cruda in f:
                linea = cruda.strip()
                if not linea:
                    continue
                if linea.startswith("["):
                    cierra = linea.find("]")
                    if cierra > 0:
                        if seccion:
                            for lang in IDIOMAS:
                                secciones_dict[lang][seccion] = claves_por_idioma[lang]
                            claves_por_idioma = {lang: {} for lang in IDIOMAS}
                        seccion = linea[1:cierra].strip()
                        continue
                if "=" in linea and seccion:
                    clave, valor = linea.split("=", 1)
                    clave = clave.strip()
                    valor = valor.strip()
                    idioma, clave_limpia = normalizar_idioma(clave)
                    if idioma:
                        claves_por_idioma[idioma][clave_limpia] = valor
                    else:
                        for lang in IDIOMAS:
                            claves_por_idioma[lang][clave] = valor
            if seccion:
                for lang in IDIOMAS:
                    secciones_dict[lang][seccion] = claves_por_idioma[lang]

    def ordenar_por_prioridad(claves, tipo_sec, renombrar_lower):
        prefer = PRIORIDAD_CLAVES.get(tipo_sec, [])
        prefer_lower = [p.lower() for p in prefer]
        finales = [renombrar_lower.get(k.lower(), k) for k in claves]
        orden_indices, usados = [], set()
        for pref in prefer_lower:
            for i, kf in enumerate(finales):
                if i in usados:
                    continue
                if kf.lower() == pref:
                    orden_indices.append(i)
                    usados.add(i)
        for i in range(len(claves)):
            if i not in usados:
                orden_indices.append(i)
        return [claves[i] for i in orden_indices]

    def sanitizar_valor(clave_final_lower: str, valor_original: str) -> str:
        """Quita comentarios inline salvo excepciones y recorta espacios."""
        valor = (valor_original or "").strip()
        if (clave_final_lower not in EXCEPTION_KEYS
            and not MSG_OR_SUG_REGEX.match(clave_final_lower)):
            valor = valor.split("'", 1)[0].rstrip()
        return valor

    # === INICIO ===
    datos_idioma = {lang: {} for lang in IDIOMAS}

    # Procesar bases /Dat y /Init
    for archivo in ARCHIVOS_BASE_DAT:
        ruta = os.path.join(CARPETA_DAT, archivo)
        procesar_archivo(ruta, datos_idioma)

    for archivo in ARCHIVOS_BASE_INIT:
        ruta = os.path.join(CARPETA_INIT, archivo)
        procesar_archivo(ruta, datos_idioma)

    # Procesar archivos por idioma
    for lang in IDIOMAS:
        for _, nombre_base in ARCHIVOS_IDIOMA.items():
            nombre_buscado = f"{lang}_{nombre_base}"
            ruta = buscar_archivo_sin_case(CARPETA_INIT, nombre_buscado)
            if ruta:
                config = cargar_ini(ruta)
                for seccion in config.sections():
                    if seccion not in datos_idioma[lang]:
                        datos_idioma[lang][seccion] = {}
                    for clave in config[seccion]:
                        if clave.strip().lower() == "numsugerencias":
                            continue
                        datos_idioma[lang][seccion][clave] = config[seccion][clave]

        ruta_balance = os.path.join(CARPETA_DAT, "Balance.dat")
        if os.path.exists(ruta_balance):
            balance = cargar_ini_balance(ruta_balance)
            if "MODRAZA" in balance:
                datos_idioma[lang]["MODRAZA"] = dict(balance["MODRAZA"])

    # Inyectar INIT (contadores)
    for lang in IDIOMAS:
        ruta_msg = buscar_archivo_sin_case(CARPETA_INIT, f"{lang}_LocalMsg.dat")
        ruta_sug = buscar_archivo_sin_case(CARPETA_INIT, f"{lang}_sugerencias.ini")
        ruta_mapa = os.path.join(CARPETA_INIT, "NameMapa.dat")
        mapas_valor = extraer_valor_txt(ruta_mapa, "NumMapas")
        if mapas_valor == "0":
            mapas_valor = "750"

        datos_idioma[lang]["INIT"] = {
            "NUMEROHECHIZO": extraer_valor_txt(os.path.join(CARPETA_DAT, "hechizos.dat"), "NumeroHechizos"),
            "NUMLOCALEMSG": extraer_valor_txt(ruta_msg, f"NumLocale{lang.upper()}_Msg") if ruta_msg else "0",
            "NUMMAPAS": mapas_valor,
            "NUMNPCS": extraer_valor_txt(os.path.join(CARPETA_DAT, "npcs.dat"), "NumNPCs"),
            "NUMOBJS": extraer_valor_txt(os.path.join(CARPETA_DAT, "obj.dat"), "NumOBJs"),
            "NUMQUESTS": extraer_valor_txt(os.path.join(CARPETA_DAT, "quests.dat"), "NumQuests"),
            "NUMSUGERENCIAS": obtener_valor_sugerencias(ruta_sug) if ruta_sug else "0"
        }

    # Guardar resultados (secciones en MAYÚSCULAS) — SIN secciones vacías
    for lang in IDIOMAS:
        archivo_salida = os.path.join(CARPETA_INIT, f"{lang}_localindex.dat")
        with open(archivo_salida, "w", encoding="latin-1") as f:
            secciones_ordenadas = list(ORDEN_SECCIONES) + [s for s in datos_idioma[lang] if s not in ORDEN_SECCIONES]
            for seccion in secciones_ordenadas:
                if seccion not in datos_idioma[lang]:
                    continue

                # Tipo (NPC/OBJ/QUE/HEC...) por prefijo
                tipo_sec = seccion[:3].upper()
                incluir = INCLUIR_CLAVES_POR_SECCION.get(tipo_sec, None)
                renombrar = RENOMBRAR_CLAVES.get(tipo_sec, {})
                incluir_normalizado = set(k.lower() for k in incluir) if incluir else None
                renombrar_lower = {k.lower(): v for k, v in renombrar.items()}

                claves_fuente = list(datos_idioma[lang][seccion].keys())

                # 1) Filtrar por whitelist
                claves_a_escribir = [
                    k for k in claves_fuente
                    if not incluir_normalizado or renombrar_lower.get(k.lower(), k).lower() in incluir_normalizado
                ]
                if not claves_a_escribir:
                    continue  # no hay nada permitido para esta sección

                # 2) Ordenar por prioridad
                claves_a_escribir = ordenar_por_prioridad(claves_a_escribir, tipo_sec, renombrar_lower)

                # 3) Preparar líneas con valores sanitizados; descartar vacíos
                lineas_claves = []
                for clave_original in claves_a_escribir:
                    clave_final = renombrar_lower.get(clave_original.lower(), clave_original)
                    clave_final_lower = clave_final.lower()
                    valor_raw = datos_idioma[lang][seccion].get(clave_original, "")
                    valor_ok = sanitizar_valor(clave_final_lower, valor_raw)
                    if valor_ok != "":
                        lineas_claves.append(f"{clave_final}={valor_ok}")

                # 4) Si después de limpiar no queda ninguna línea, NO escribir la sección
                if not lineas_claves:
                    continue

                # 5) Escribir sección + claves
                f.write(f"[{seccion.upper()}]\n")
                for linea in lineas_claves:
                    f.write(linea + "\n")
                f.write("\n")

        print(f"Archivo generado: {archivo_salida}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("X Ocurrio un error inesperado:")
        print(e)
