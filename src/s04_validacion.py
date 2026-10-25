"""Paso 6: validación del instrumento (kappa) y base analítica final.

Flujo:
 1. h1 y h2 llenan data/anotacion_h1.csv y data/anotacion_h2.csv por separado y a ciegas.
 2. Este script calcula el kappa humano-humano y crea data/consenso.csv: las celdas
    donde coinciden vienen llenas; donde no, quedan vacías para que las decidan juntos.
 3. Cuando consenso.csv y codificacion_llm.csv están completos, calcula el kappa
    Claude-consenso, las matrices de confusión, las discrepancias y la decisión de validez,
    y arma data/base_analitica.csv (entregable 1).
"""
import numpy as np
import pandas as pd
from sklearn.metrics import cohen_kappa_score, confusion_matrix
from src.config import DATA, RES, SEMILLA, CATS, KAPPA_MIN, IC_INF_MIN, leer_csv


def kappa_ic(a, b, B=2000):
    rng = np.random.default_rng(SEMILLA)
    a, b = np.asarray(a), np.asarray(b)
    ks = []
    for _ in range(B):
        i = rng.integers(0, len(a), len(a))
        if len(set(a[i]) | set(b[i])) > 1:
            ks.append(cohen_kappa_score(a[i], b[i]))
    return np.nanpercentile(ks, [2.5, 97.5]) if ks else (np.nan, np.nan)


def resumen(a, b):
    a, b = np.asarray(a, dtype=int), np.asarray(b, dtype=int)
    po = float(np.mean(a == b))
    k = cohen_kappa_score(a, b) if len(set(a) | set(b)) > 1 else np.nan
    lo, hi = kappa_ic(a, b)
    return {"n": len(a), "kappa": k, "ic_inf": lo, "ic_sup": hi, "acuerdo_%": 100 * po,
            "pabak": 2 * po - 1, "prevalencia_%": 100 * float(np.mean(a))}


def leer_completo(ruta, columnas):
    if not ruta.exists():
        return None
    df = leer_csv(ruta).sort_values("id").reset_index(drop=True)
    if "ambiguo" in df.columns:  # ambiguo vacío = no fue ambigua
        df["ambiguo"] = df["ambiguo"].fillna(0)
    if df[columnas].isna().any().any():
        return None
    return df


def main():
    h1 = leer_completo(DATA / "anotacion_h1.csv", CATS + ["ambiguo"])
    h2 = leer_completo(DATA / "anotacion_h2.csv", CATS + ["ambiguo"])
    if h1 is None or h2 is None:
        print("La anotación humana no está completa (anotacion_h1.csv y anotacion_h2.csv).")
        return False
    if list(h1.id) != list(h2.id):
        print("h1 y h2 no tienen las mismas canciones.")
        return False

    # --- Kappa humano-humano y plantilla de consenso -----------------------
    filas = [{"categoria": c, "comparacion": "humano1 vs humano2", **resumen(h1[c], h2[c])}
             for c in CATS]
    ruta_cons = DATA / "consenso.csv"
    if not ruta_cons.exists():
        cons = h1[["id"]].copy()
        for c in CATS:
            cons[c] = h1[c].where(h1[c] == h2[c]).astype("Int64")
        cons["ambiguo"] = ((h1.ambiguo == 1) | (h2.ambiguo == 1)).astype(int)
        cons.to_csv(ruta_cons, index=False)
        pd.DataFrame(filas).round(3).to_csv(RES / "tabla_kappas_humanos.csv", index=False)
        print(pd.DataFrame(filas).round(3).to_string(index=False))
        print("\nSe creó data/consenso.csv: decidan juntos las celdas vacías (desacuerdos).")
        return False

    cons = leer_completo(ruta_cons, CATS)
    if cons is None:
        print("data/consenso.csv tiene celdas vacías: decidan juntos esos desacuerdos.")
        return False
    llm_todo = leer_completo(DATA / "codificacion_llm.csv", [f"llm_{c}" for c in CATS])
    if llm_todo is None:
        print("Consenso listo. Falta completar data/codificacion_llm.csv (paso 5) "
              "para calcular el kappa de Claude.")
        return False
    llm = llm_todo.set_index("id").loc[cons.id].reset_index()

    # --- Kappa Claude-consenso ---------------------------------------------
    for c in CATS:
        filas.append({"categoria": c, "comparacion": "Claude vs consenso",
                      **resumen(cons[c], llm[f"llm_{c}"])})
        m = confusion_matrix(cons[c].astype(int), llm[f"llm_{c}"].astype(int), labels=[0, 1])
        pd.DataFrame(m, index=["humano=0", "humano=1"], columns=["Claude=0", "Claude=1"]) \
          .to_csv(RES / f"confusion_{c}.csv")
    kap = pd.DataFrame(filas)
    kap["valida"] = np.where(kap.comparacion == "Claude vs consenso",
                             (kap.kappa >= KAPPA_MIN) & (kap.ic_inf >= IC_INF_MIN), np.nan)
    kap.round(3).to_csv(RES / "tabla_kappas.csv", index=False)
    print(kap.round(3).to_string(index=False))

    # --- Tabla de discrepancias (para clasificar a mano la causa) ----------
    disc = []
    for c in CATS:
        for i in cons.index:
            if int(cons.at[i, c]) != int(llm.at[i, f"llm_{c}"]):
                dudoso = (h1.at[i, c] != h2.at[i, c]) or cons.at[i, "ambiguo"] == 1
                disc.append({"id": cons.at[i, "id"], "categoria": c,
                             "consenso": int(cons.at[i, c]), "claude": int(llm.at[i, f"llm_{c}"]),
                             "h1": int(h1.at[i, c]), "h2": int(h2.at[i, c]),
                             "ambiguo": int(cons.at[i, "ambiguo"]),
                             "justificacion_claude": llm.at[i, "llm_justificacion"],
                             "tipo_sugerido": "ambigüedad genuina" if dudoso else
                             ("error del modelo: falso positivo" if llm.at[i, f"llm_{c}"] == 1
                              else "error del modelo: falso negativo"),
                             "tipo_final": "", "causa": ""})
    ruta_disc = RES / "discrepancias.csv"
    if not ruta_disc.exists():   # no se sobrescribe si ya clasificaron causas
        pd.DataFrame(disc).to_csv(ruta_disc, index=False)
    print(f"\nDiscrepancias Claude-consenso: {len(disc)} (ver resultados/discrepancias.csv).")

    # --- Base analítica final (entregable 1) --------------------------------
    base = pd.read_csv(DATA / "base_texto.csv")
    base = base.merge(llm_todo[["id"] + [f"llm_{c}" for c in CATS]], on="id", how="left")
    base["en_validacion"] = base.id.isin(cons.id).astype(int)
    texto = base.select_dtypes(["object", "string"])
    assert (texto.apply(lambda s: s.astype(str).str.len().max()) < 100).all(), \
        "¡Hay una columna con texto largo! Revisen que no se haya colado una letra."
    base.to_csv(DATA / "base_analitica.csv", index=False)
    validas = list(kap.loc[kap.valida == True, "categoria"])  # noqa: E712
    print(f"Categorías válidas según la regla: {validas or 'ninguna'}")
    return True


if __name__ == "__main__":   # permite correr este paso solo (clic derecho > Run en PyCharm)
    main()
