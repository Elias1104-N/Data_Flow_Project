"""Parámetros fijos del proyecto. Lo que está aquí NO se cambia entre corridas."""
from pathlib import Path

# --- Reproducibilidad -------------------------------------------------------
SEMILLA = 2026

# --- Rutas ------------------------------------------------------------------
RAIZ = Path(__file__).resolve().parents[1]
DATA = RAIZ / "data"
LETRAS = RAIZ / "letras"          # SOLO LOCAL: nunca se entrega ni se comparte
DOCS = RAIZ / "docs"
RES = RAIZ / "resultados"
for carpeta in (DATA, LETRAS, DOCS, RES):
    carpeta.mkdir(exist_ok=True)

# --- Diseño muestral (paso 2) -----------------------------------------------
CORTES = [2009, 2013, 2017, 2021, 2025]
PERIODOS = ["2010-13", "2014-17", "2018-21", "2022-25"]
N_POR_ESTRATO = 50
N_VALIDACION = 50                 # max(50, 20 % de la muestra)

# --- Instrumento (pasos 3 y 5) ----------------------------------------------
CATS = ["C1", "C2", "C3", "C4"]   # C1 sexual explícito, C2 cuerpo, C3 agencia femenina, C4 violencia
# "manual": se codifica en claude.ai y se llena data/codificacion_llm.csv a mano.
# "api":    se codifica con la API de Anthropic (requiere ANTHROPIC_API_KEY en .env).
MODO_LLM = "manual"
MODELO = "claude-opus-5-5"      # modelo exacto usado; es parte del instrumento

# --- Regla de validez (paso 6), fijada ANTES de ver resultados --------------
KAPPA_MIN = 0.61
IC_INF_MIN = 0.40


import pandas as pd


def leer_csv(ruta):
    """Lee un CSV separado por comas o por punto y coma (como lo guarda Excel en español)."""
    return pd.read_csv(ruta, sep=None, engine="python", encoding="utf-8-sig")
