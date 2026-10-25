"""Paso 4: medidas de texto y conteos del léxico.

Las letras se leen en memoria desde letras/C001.txt, etc., y de aquí solo salen números.
Entrada:  data/muestra.csv, docs/lexico.csv, letras/*.txt
Salida:   data/base_texto.csv
"""
import re
import unicodedata
import numpy as np
import pandas as pd
from src.config import DATA, DOCS, LETRAS, leer_csv


def normalizar(texto):
    """Minúsculas, sin tildes (pero conserva la ñ), sin signos de puntuación."""
    texto = texto.lower().replace("ñ", "\0")
    texto = "".join(c for c in unicodedata.normalize("NFD", texto)
                    if unicodedata.category(c) != "Mn")
    texto = texto.replace("\0", "ñ")
    texto = re.sub(r"\[[^\]]*\]", " ", texto)          # quita etiquetas tipo [Coro]
    texto = re.sub(r"[^a-zñ0-9' ]+", " ", texto)
    return re.sub(r"\s+", " ", texto).strip()


def mattr(tokens, w=50):
    """Razón tipo-token media en ventanas móviles de w palabras (corrige por longitud)."""
    if len(tokens) < w:
        return len(set(tokens)) / len(tokens)
    return float(np.mean([len(set(tokens[i:i + w])) / w
                          for i in range(len(tokens) - w + 1)]))


def medir(id_, lexico):
    texto = normalizar((LETRAS / f"{id_}.txt").read_text(encoding="utf-8"))
    tokens = texto.split()
    fila = {"id": id_, "n_palabras": len(tokens), "n_tipos": len(set(tokens)),
            "ttr": round(len(set(tokens)) / len(tokens), 4),
            "mattr": round(mattr(tokens), 4)}
    for dim, grupo in lexico.groupby("dimension"):
        patron = r"\b(?:" + "|".join(grupo.patron) + r")\b"
        n = sum(1 for _ in re.finditer(patron, texto))
        fila[f"lex_{dim}"] = n
        fila[f"lex_{dim}_x1000"] = round(1000 * n / len(tokens), 2)
    return fila          # el texto muere aquí: solo salen números


def main():
    if not (DATA / "muestra.csv").exists():
        print("Falta data/muestra.csv (corran el paso 2).")
        return False
    muestra = pd.read_csv(DATA / "muestra.csv")
    # Los metadatos completados a mano viven en registro_letras.csv (muestra.csv no se edita)
    registro = DATA / "registro_letras.csv"
    if registro.exists():
        meta = ["interprete_mujer", "pais_artista_principal", "colaboracion"]
        reg = leer_csv(registro)[["id"] + meta]
        muestra = muestra.drop(columns=meta).merge(reg, on="id", how="left")
    lexico = pd.read_csv(DOCS / "lexico.csv", comment="#").dropna(subset=["patron"])
    def falta(i):  # no existe, o está vacía
        archivo = LETRAS / f"{i}.txt"
        return not archivo.exists() or archivo.stat().st_size <= 50
    faltan = [i for i in muestra.id if falta(i)]
    if faltan:
        print(f"Faltan {len(faltan)} letras en letras/ (por ejemplo: {faltan[:5]}).")
        return False
    medidas = pd.DataFrame([medir(i, lexico) for i in muestra.id])
    base = muestra.merge(medidas, on="id")
    base.to_csv(DATA / "base_texto.csv", index=False)
    print(f"Medidas calculadas para {len(base)} canciones.")
    print(medidas.describe().round(2).T[["mean", "50%", "min", "max"]])
    return True


if __name__ == "__main__":   # permite correr este paso solo (clic derecho > Run en PyCharm)
    main()
