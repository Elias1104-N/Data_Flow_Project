"""Paso 7: análisis inferencial, SOLO sobre las categorías que pasaron la validación.

Entradas: data/base_analitica.csv, resultados/tabla_kappas.csv, resultados/tabla_muestreo.csv
Salidas:  resultados/descriptivos_*.csv, resultados/pruebas.csv, resultados/fig_*.png
"""
import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pymannkendall as mk
import statsmodels.formula.api as smf
from scipy import stats
from statsmodels.stats.contingency_tables import Table, Table2x2
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.proportion import proportion_confint
from src.config import DATA, RES, PERIODOS

NOMBRES = {"C1": "contenido sexual explícito", "C2": "cuerpo como atributo principal",
           "C3": "agencia femenina", "C4": "violencia"}
pruebas = []   # cada prueba se agrega aquí con su tamaño de efecto


def anotar(pregunta, prueba, estadistico, p, efecto, valor_efecto, ic=None, nota=""):
    pruebas.append({"pregunta": pregunta, "prueba": prueba, "estadistico": estadistico,
                    "p": p, "efecto": efecto, "valor_efecto": valor_efecto,
                    "ic95": "" if ic is None else f"[{ic[0]:.3f}; {ic[1]:.3f}]", "nota": nota})


def descriptivos(base, var, W):
    d = base.groupby("periodo", observed=True).agg(n=(var, "size"), k=(var, "sum")).reindex(PERIODOS)
    d["p"] = d.k / d.n
    d["ic_inf"], d["ic_sup"] = proportion_confint(d.k, d.n, method="wilson")
    d.round(4).to_csv(RES / f"descriptivos_{var}.csv")
    p_pond = float((W * d.p).sum())
    return d, p_pond


def tendencia(base, var, c):
    preg = f"Tendencia de {NOMBRES[c]}"
    # a) logística: OR por año
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            m = smf.logit(f"{var} ~ anio_c", data=base).fit(disp=0)
        or_ = float(np.exp(m.params["anio_c"]))
        ic = np.exp(m.conf_int().loc["anio_c"]).values
        anotar(preg, "Regresión logística (año)", m.params["anio_c"], m.pvalues["anio_c"],
               "OR por año", or_, ic, f"OR por 10 años = {or_ ** 10:.2f}")
    except Exception as e:
        anotar(preg, "Regresión logística (año)", np.nan, np.nan, "", np.nan, nota=f"no convergió: {e}")
    # b) tendencia lineal entre periodos ordenados (tipo Cochran-Armitage)
    t = pd.crosstab(base.periodo, base[var]).reindex(PERIODOS)
    r = Table(t).test_ordinal_association()
    anotar(preg, "Asociación lineal por periodos", r.statistic, r.pvalue, "z", r.zscore)
    # c) Mann-Kendall sobre la proporción anual
    anual = base.groupby("anio")[var].mean()
    mkr = mk.original_test(anual.values)
    anotar(preg, "Mann-Kendall (proporción anual)", mkr.z, mkr.p, "tau de Kendall", mkr.Tau,
           nota=f"pendiente de Sen = {mkr.slope:.4f} por año; {len(anual)} años")


def grafico(d, c, n_total):
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.errorbar(d.index.astype(str), 100 * d.p,
                yerr=[100 * (d.p - d.ic_inf), 100 * (d.ic_sup - d.p)],
                fmt="o", capsize=4, color="#1f5aa6")
    ax.set_ylabel(f"% de canciones con {NOMBRES[c]}")
    ax.set_ylim(0, 100)
    ax.set_title(f"[Escriban el hallazgo] — {NOMBRES[c]}")
    ax.spines[["top", "right"]].set_visible(False)
    fig.text(0.01, -0.02, f"n = {n_total} canciones. Fuente: Billboard Hot Latin Songs, "
             "listas de fin de año 2010–2025. Barras: IC 95 % de Wilson.", fontsize=8)
    fig.savefig(RES / f"fig_tendencia_{c}.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def main():
    if not (DATA / "base_analitica.csv").exists():
        print("Falta data/base_analitica.csv (paso 6).")
        return False
    base = pd.read_csv(DATA / "base_analitica.csv")
    base["periodo"] = pd.Categorical(base.periodo, categories=PERIODOS, ordered=True)
    base["anio_c"] = base.anio - 2010
    kap = pd.read_csv(RES / "tabla_kappas.csv")
    validas = list(kap.loc[kap.valida == True, "categoria"])  # noqa: E712
    print(f"Categorías válidas: {validas or 'ninguna'}")
    tm = pd.read_csv(RES / "tabla_muestreo.csv", index_col=0)
    W = tm.loc[PERIODOS, "peso_W_h"].astype(float)

    # --- Pregunta principal y descriptivos de cada categoría válida ----------
    for c in validas:
        var = f"llm_{c}"
        d, p_pond = descriptivos(base, var, W)
        print(f"\n{c} ({NOMBRES[c]}) por periodo:\n{d.round(3)}\n"
              f"Proporción 2010-2025 ponderada: {p_pond:.3f}")
        tendencia(base, var, c)
        grafico(d, c, len(base))

    # --- Secundaria 1: C2 según intérprete mujer ---------------------------
    if "C2" in validas:
        t = pd.crosstab(base.interprete_mujer, base.llm_C2).reindex(index=[0, 1], columns=[0, 1], fill_value=0)
        chi2, p, _, esperadas = stats.chi2_contingency(t, correction=False)
        prueba = "Chi-cuadrado"
        if (esperadas < 5).any():
            _, p = stats.fisher_exact(t)
            prueba = "Exacta de Fisher (esperadas < 5)"
        tt = Table2x2(t.values, shift_zeros=True)
        anotar("C2 según intérprete mujer", prueba, chi2, p, "OR", tt.oddsratio,
               tt.oddsratio_confint(), f"phi = {np.sqrt(chi2 / t.values.sum()):.3f}")

    # --- Secundaria 2: riqueza léxica (MATTR) por periodo --------------------
    grupos = {k: g.mattr.values for k, g in base.groupby("periodo", observed=True)}
    H, p = stats.kruskal(*grupos.values())
    anotar("MATTR por periodo", "Kruskal-Wallis", H, p, "épsilon cuadrado", H / (len(base) - 1))
    if p < 0.05:
        pares = [(a, b) for i, a in enumerate(grupos) for b in list(grupos)[i + 1:]]
        ps = [stats.mannwhitneyu(grupos[a], grupos[b]).pvalue for a, b in pares]
        for (a, b), p_holm in zip(pares, multipletests(ps, method="holm")[1]):
            anotar("MATTR por periodo (post hoc)", f"Mann-Whitney {a} vs {b}", np.nan, p_holm,
                   "", np.nan, nota="p corregido por Holm")
    mkr = mk.original_test(base.groupby("anio").mattr.median().values)
    anotar("MATTR en el tiempo", "Mann-Kendall (mediana anual)", mkr.z, mkr.p,
           "tau de Kendall", mkr.Tau, nota=f"pendiente de Sen = {mkr.slope:.5f} por año")
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.boxplot(list(grupos.values()), tick_labels=list(grupos.keys()))
    ax.set_ylabel("MATTR (ventana de 50 palabras)")
    ax.set_title("[Escriban el hallazgo] — riqueza léxica por periodo")
    ax.spines[["top", "right"]].set_visible(False)
    fig.savefig(RES / "fig_mattr_periodo.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

    tabla = pd.DataFrame(pruebas)
    tabla.round(4).to_csv(RES / "pruebas.csv", index=False)
    print("\n" + tabla.round(4).to_string(index=False))
    return True


if __name__ == "__main__":   # permite correr este paso solo (clic derecho > Run en PyCharm)
    main()
