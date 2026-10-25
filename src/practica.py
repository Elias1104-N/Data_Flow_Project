"""Paso 3: sortea 10 canciones de práctica para la prueba piloto del libro de códigos.

Son canciones de reggaetón del marco que NO están en la muestra, para que la prueba
no contamine las canciones que se van a analizar.
Salida: data/practica.csv
"""
import pandas as pd
from src.config import DATA, SEMILLA


def main():
    marco = pd.read_csv(DATA / "marco_muestral.csv")
    muestra = pd.read_csv(DATA / "muestra.csv")
    clave = lambda df: df.titulo.str.lower().str.strip() + "|" + df.artista.str.lower().str.strip()
    fuera = marco[(marco.es_reggaeton == 1) & ~clave(marco).isin(clave(muestra))]
    practica = fuera.sample(n=10, random_state=SEMILLA)[["anio", "titulo", "artista"]]
    practica = practica.sort_values("anio").reset_index(drop=True)
    practica.insert(0, "id", [f"P{i:02d}" for i in range(1, 11)])
    practica.to_csv(DATA / "practica.csv", index=False)
    print(f"Canciones fuera de la muestra disponibles: {len(fuera)}")
    print(practica.to_string(index=False))


if __name__ == "__main__":
    main()