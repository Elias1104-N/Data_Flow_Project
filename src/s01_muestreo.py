"""Paso 2: muestra estratificada por periodo + submuestra de validación.

Entrada:  data/marco_muestral.csv (lo llenan ustedes desde las listas de Billboard)
Salidas:  data/muestra.csv
          data/submuestra_validacion.csv
          data/anotacion_h1.csv y data/anotacion_h2.csv (plantillas vacías, solo si no existen)
          resultados/tabla_muestreo.csv (tabla para el Avance 1)
"""
import unicodedata
import pandas as pd
from src.config import (DATA, RES, SEMILLA, CORTES, PERIODOS, N_POR_ESTRATO,
                        N_VALIDACION, CATS)

COLUMNAS_MARCO = ["anio", "posicion", "titulo", "artista", "es_reggaeton",
                  "interprete_mujer", "pais_artista_principal", "colaboracion",
                  "fuente", "fecha_consulta"]


def clave(texto):
    """Normaliza títulos y artistas para detectar duplicados."""
    t = unicodedata.normalize("NFD", str(texto).lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    for basura in (" feat.", " ft.", " featuring", " (remix)", "(", ")", "'", "’", "."):
        t = t.replace(basura, " ")
    return " ".join(t.split())


def main():
    ruta = DATA / "marco_muestral.csv"
    marco = pd.read_csv(ruta)
    faltan = set(COLUMNAS_MARCO) - set(marco.columns)
    if faltan:
        print(f"Faltan columnas en {ruta.name}: {sorted(faltan)}")
        return False
    if marco.empty:
        print(f"{ruta.name} está vacío: llénenlo con las listas de fin de año (paso 2.1 de la guía).")
        return False

    # 1. Solo reggaetón; cada canción una sola vez (la primera aparición)
    marco = marco[marco.es_reggaeton == 1].copy()
    marco["_clave"] = marco.titulo.map(clave) + " | " + marco.artista.map(clave)
    marco = (marco.sort_values(["anio", "posicion"])
                  .drop_duplicates("_clave", keep="first"))
    marco["periodo"] = pd.cut(marco.anio, bins=CORTES, labels=PERIODOS)
    marco = marco.dropna(subset=["periodo"])

    # 2. Muestreo estratificado con asignación igual
    partes = []
    for periodo in PERIODOS:
        estrato = marco[marco.periodo == periodo]
        n = min(N_POR_ESTRATO, len(estrato))
        if n < N_POR_ESTRATO:
            print(f"Aviso: el estrato {periodo} solo tiene {len(estrato)} canciones; se toman todas.")
        partes.append(estrato.sample(n=n, random_state=SEMILLA))
    muestra = pd.concat(partes).drop(columns="_clave").reset_index(drop=True)
    muestra.insert(0, "id", [f"C{i:03d}" for i in range(1, len(muestra) + 1)])
    muestra.to_csv(DATA / "muestra.csv", index=False)

    # 3. Tabla de muestreo para el Avance 1
    N_h = marco.periodo.value_counts().reindex(PERIODOS)
    n_h = muestra.periodo.value_counts().reindex(PERIODOS)
    tabla = pd.DataFrame({"N_h": N_h, "n_h": n_h, "fraccion_%": (100 * n_h / N_h).round(1),
                          "peso_W_h": (N_h / N_h.sum()).round(4)})
    tabla.loc["Total"] = [N_h.sum(), n_h.sum(), round(100 * n_h.sum() / N_h.sum(), 1), 1.0]
    tabla.to_csv(RES / "tabla_muestreo.csv")
    print(tabla)

    # 4. Submuestra de validación (aleatoria, misma semilla) + plantillas de anotación
    val = muestra.sample(n=min(N_VALIDACION, len(muestra)), random_state=SEMILLA)[["id"]]
    val = val.sort_values("id")
    val.to_csv(DATA / "submuestra_validacion.csv", index=False)
    for quien in ("h1", "h2"):
        ruta_h = DATA / f"anotacion_{quien}.csv"
        if not ruta_h.exists():   # nunca se sobrescribe una anotación ya hecha
            plantilla = val.copy()
            for c in CATS + ["ambiguo"]:
                plantilla[c] = ""
            plantilla["nota"] = ""
            plantilla.to_csv(ruta_h, index=False)
    print(f"Muestra: {len(muestra)} canciones. Submuestra de validación: {len(val)}.")
    return True


if __name__ == "__main__":   # permite correr este paso solo (clic derecho > Run en PyCharm)
    main()
