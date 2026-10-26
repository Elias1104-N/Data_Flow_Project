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
FUENTE = ("Marco: canciones de reggaetón n.º 1 en Hot Latin Songs o Latin Airplay "
          "(Billboard, vía Wikipedia), 2010–2025.")


def delta_cliff(a, b):
    """Delta de Cliff: P(b > a) − P(b < a). Tamaño de efecto para Mann-Whitney."""
    a, b = np.asarray(a), np.asarray(b)
    return float(((b[:, None] > a).sum() - (b[:, None] < a).sum()) / (len(a) * len(b)))


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


def resumen_num(base, var):
    d = base.groupby("periodo", observed=True)[var].describe()[["count", "mean", "25%", "50%", "75%"]]
    return d.reindex(PERIODOS).rename(columns={"count": "n", "mean": "media", "50%": "mediana"}).round(4)


def caja(grupos, ylabel, titulo, archivo, n_total):
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.boxplot(list(grupos.values()), tick_labels=list(grupos.keys()))
    ax.set_ylabel(ylabel)
    ax.set_title(titulo)
    ax.spines[["top", "right"]].set_visible(False)
    fig.text(0.01, -0.02, f"n = {n_total} canciones. {FUENTE}", fontsize=8)
    fig.savefig(RES / archivo, dpi=200, bbox_inches="tight")
    plt.close(fig)


def grafico_kappas():
    """Kappa de Claude contra el consenso, con IC y el umbral de validez."""
    from src.config import KAPPA_MIN, IC_INF_MIN
    k = pd.read_csv(RES / "tabla_kappas.csv")
    k = k[k.comparacion == "Claude vs consenso"].set_index("categoria")
    h = pd.read_csv(RES / "tabla_kappas.csv")
    h = h[h.comparacion == "humano1 vs humano2"].set_index("categoria")
    y = np.arange(len(k))
    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.errorbar(k.kappa, y, xerr=[k.kappa - k.ic_inf, k.ic_sup - k.kappa], fmt="o",
                capsize=4, color="#1f5aa6", label="Claude vs consenso (IC 95 %)")
    ax.plot(h.kappa.reindex(k.index), y - 0.18, "s", color="#999999", label="Humano 1 vs humano 2")
    ax.axvline(KAPPA_MIN, ls="--", color="#b03a2e", lw=1)
    ax.text(KAPPA_MIN + 0.01, -0.45, f"umbral κ = {KAPPA_MIN}", color="#b03a2e", fontsize=8)
    ax.set_yticks(y, [f"{c} {NOMBRES[c]}" for c in k.index])
    ax.set_xlim(-0.2, 1)
    ax.set_ylim(len(k) - 0.5, -0.6)
    ax.set_xlabel("Kappa de Cohen")
    ax.set_title("Ninguna categoría alcanza el umbral de validez fijado")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=2, frameon=False)
    fig.text(0.01, -0.17, f"Submuestra de validación: n = 50. Regla: κ ≥ {KAPPA_MIN} y límite "
             f"inferior del IC ≥ {IC_INF_MIN}. IC por bootstrap (2000 réplicas).", fontsize=8)
    fig.savefig(RES / "fig_kappas.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def resumen_discrepancias():
    ruta = RES / "discrepancias.csv"
    if not ruta.exists():
        return
    d = pd.read_csv(ruta)
    if d.tipo_final.isna().all():
        print("Discrepancias sin clasificar (columna tipo_final vacía).")
        return
    t = pd.crosstab(d.categoria, d.tipo_final, margins=True, margins_name="Total")
    t.to_csv(RES / "tabla_discrepancias.csv")
    print("\nDiscrepancias Claude-consenso por tipo:\n" + t.to_string())


def grafico(d, c, n_total):
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.errorbar(d.index.astype(str), 100 * d.p,
                yerr=[100 * (d.p - d.ic_inf), 100 * (d.ic_sup - d.p)],
                fmt="o", capsize=4, color="#1f5aa6")
    ax.set_ylabel(f"% de canciones con {NOMBRES[c]}")
    ax.set_ylim(0, 100)
    ax.set_title(f"[Escriban el hallazgo] — {NOMBRES[c]}")
    ax.spines[["top", "right"]].set_visible(False)
    fig.text(0.01, -0.02, f"n = {n_total} canciones. {FUENTE} Barras: IC 95 % de Wilson.", fontsize=8)
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
    # Supuestos: normalidad por periodo (justifica la prueba no paramétrica) y dispersión similar
    # (si las dispersiones son parecidas, Kruskal-Wallis se lee como diferencia de medianas)
    for k, x in grupos.items():
        w, p_sw = stats.shapiro(x)
        anotar("MATTR: supuesto de normalidad", f"Shapiro-Wilk {k}", w, p_sw, "", np.nan,
               nota="p < 0,05 indica que no es normal")
    bf, p_bf = stats.levene(*grupos.values(), center="median")
    anotar("MATTR: supuesto de dispersión", "Brown-Forsythe", bf, p_bf, "", np.nan,
           nota="p > 0,05: dispersiones similares entre periodos")
    H, p = stats.kruskal(*grupos.values())
    anotar("MATTR por periodo", "Kruskal-Wallis", H, p, "épsilon cuadrado", H / (len(base) - 1))
    if p < 0.05:
        pares = [(a, b) for i, a in enumerate(grupos) for b in list(grupos)[i + 1:]]
        ps = [stats.mannwhitneyu(grupos[a], grupos[b]).pvalue for a, b in pares]
        for (a, b), p_holm in zip(pares, multipletests(ps, method="holm")[1]):
            anotar("MATTR por periodo (post hoc)", f"Mann-Whitney {a} vs {b}", np.nan, p_holm,
                   "delta de Cliff", delta_cliff(grupos[a], grupos[b]), nota="p corregido por Holm")
    medianas = base.groupby("anio").mattr.median()
    mkr = mk.original_test(medianas.values)
    ac1 = pd.Series(medianas.values).autocorr(1)
    anotar("MATTR en el tiempo", "Mann-Kendall (mediana anual)", mkr.z, mkr.p,
           "tau de Kendall", mkr.Tau, nota=f"pendiente de Sen = {mkr.slope:.5f} por año; "
           f"autocorrelación de orden 1 = {ac1:.2f}")
    hr = mk.hamed_rao_modification_test(medianas.values)
    anotar("MATTR en el tiempo (robustez)", "Mann-Kendall modificado (Hamed-Rao)", hr.z, hr.p,
           "tau de Kendall", hr.Tau, nota="corrige la autocorrelación de la serie anual")
    # Robustez: ¿la tendencia se explica por más colaboraciones o por letras más largas?
    m = smf.ols("mattr ~ anio_c + colaboracion + np.log(n_palabras)", data=base).fit(cov_type="HC3")
    anotar("MATTR en el tiempo (robustez)", "Regresión lineal con controles (EE robustos HC3)",
           m.tvalues["anio_c"], m.pvalues["anio_c"], "cambio de MATTR por año",
           m.params["anio_c"], m.conf_int().loc["anio_c"].values,
           f"controla colaboración y log(n.º de palabras); R² = {m.rsquared:.3f}")
    resumen_num(base, "mattr").to_csv(RES / "descriptivos_mattr.csv")
    caja(grupos, "MATTR (ventana de 50 palabras)",
         "La riqueza léxica sube en el periodo 2022–25", "fig_mattr_periodo.png", len(base))

    # --- Complementario: léxico (no depende de Claude ni de la validación) ---
    # Mide MENCIONES de vocabulario, no las categorías C1/C2: no responde la pregunta principal.
    for dim, nombre in [("sexual", "léxico sexual"), ("cuerpo", "léxico del cuerpo")]:
        var = f"lex_{dim}_x1000"
        if var not in base.columns:
            continue
        g = {k: x[var].values for k, x in base.groupby("periodo", observed=True)}
        H, p = stats.kruskal(*g.values())
        anotar(f"Complementario: {nombre} por periodo", "Kruskal-Wallis", H, p,
               "épsilon cuadrado", H / (len(base) - 1), nota="menciones por 1000 palabras; exploratorio")
        # media anual: la mediana es 0 en casi todos los años y no sirve para ver tendencia
        mkr = mk.original_test(base.groupby("anio")[var].mean().values)
        anotar(f"Complementario: {nombre} en el tiempo", "Mann-Kendall (media anual)", mkr.z, mkr.p,
               "tau de Kendall", mkr.Tau, nota=f"pendiente de Sen = {mkr.slope:.4f} por año; exploratorio")
        r = resumen_num(base, var)
        r["%_con_alguna_mencion"] = (base.groupby("periodo", observed=True)[f"lex_{dim}"]
                                     .apply(lambda x: 100 * (x > 0).mean()).reindex(PERIODOS).round(1))
        r.to_csv(RES / f"descriptivos_lex_{dim}.csv")
        caja(g, f"Menciones de {nombre} por 1000 palabras", f"Complementario: {nombre} por periodo",
             f"fig_lex_{dim}_periodo.png", len(base))

    grafico_kappas()
    resumen_discrepancias()

    tabla = pd.DataFrame(pruebas)
    tabla.round(4).to_csv(RES / "pruebas.csv", index=False)
    print("\n" + tabla.round(4).to_string(index=False))
    return True


if __name__ == "__main__":   # permite correr este paso solo (clic derecho > Run en PyCharm)
    main()
