"""Paso 3.3: compara la prueba piloto de las dos codificadoras.

Entradas: data/piloto_h1.csv y data/piloto_h2.csv (las 10 canciones de practica.csv)
Salida:   resultados/piloto_comparacion.csv (y un resumen en pantalla)

Con 10 canciones el kappa es muy inestable: aquí lo importante es VER EN QUÉ
canciones y categorías no coinciden, para corregir el libro de códigos.
"""
import pandas as pd
from sklearn.metrics import cohen_kappa_score
from src.config import DATA, RES, CATS, leer_csv


def main():
    h1 = leer_csv(DATA / "piloto_h1.csv").sort_values("id").reset_index(drop=True)
    h2 = leer_csv(DATA / "piloto_h2.csv").sort_values("id").reset_index(drop=True)
    faltan = [f for f, h in (("h1", h1), ("h2", h2)) if h[CATS].isna().any().any()]
    if faltan:
        print(f"Hay celdas vacías en: {faltan}. Completen 0 o 1 en todas las categorías.")
        return False

    print("Acuerdo por categoría (10 canciones):")
    for c in CATS:
        acuerdo = (h1[c] == h2[c]).mean() * 100
        if len(set(h1[c]) | set(h2[c])) > 1:
            k = f"{cohen_kappa_score(h1[c], h2[c]):.2f}"
        else:
            k = "no se puede calcular (todas iguales)"
        print(f"  {c}: {acuerdo:.0f} % de acuerdo · kappa = {k}")

    filas = []
    for i in h1.index:
        for c in CATS:
            if h1.at[i, c] != h2.at[i, c]:
                filas.append({"id": h1.at[i, "id"], "categoria": c,
                              "h1": int(h1.at[i, c]), "h2": int(h2.at[i, c]),
                              "nota_h1": h1.at[i, "nota"], "nota_h2": h2.at[i, "nota"],
                              "decision": "", "cambio_en_libro": ""})
    tabla = pd.DataFrame(filas)
    tabla.to_csv(RES / "piloto_comparacion.csv", index=False)
    print(f"\nDesacuerdos: {len(tabla)} (detalle en resultados/piloto_comparacion.csv)")
    if len(tabla):
        print(tabla[["id", "categoria", "h1", "h2"]].to_string(index=False))
    return True


if __name__ == "__main__":
    main()