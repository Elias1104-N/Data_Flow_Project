"""Paso 5: codificación de todo el corpus con Claude.

Dos modos (se elige en src/config.py, variable MODO_LLM):

- "manual": codifican en claude.ai con el prompt fijo (ver README) y copian la respuesta
  en data/codificacion_llm.csv. Este script crea la plantilla y revisa que esté completa.
- "api":    llama a la API de Anthropic. Se ejecuta UNA sola vez; si el CSV ya existe,
  no vuelve a llamar.

REGLA DE CIEGO (equipo de 2): las 50 canciones de validación se codifican con Claude
solo DESPUÉS de que ambos terminen anotacion_h1.csv y anotacion_h2.csv.
"""
import json
import re
from datetime import date
import pandas as pd
from src.config import DATA, DOCS, LETRAS, MODELO, MODO_LLM, CATS, leer_csv

SALIDA = DATA / "codificacion_llm.csv"
COLS = ["id", "es_validacion"] + [f"llm_{c}" for c in CATS] + ["llm_justificacion", "modelo", "fecha"]


def crear_plantilla():
    muestra = pd.read_csv(DATA / "muestra.csv")
    val = set(pd.read_csv(DATA / "submuestra_validacion.csv").id)
    p = pd.DataFrame({"id": muestra.id, "es_validacion": muestra.id.isin(val).astype(int)})
    for c in COLS[2:]:
        p[c] = ""
    # primero las que NO son de validación: esas se pueden codificar ya
    p.sort_values(["es_validacion", "id"]).to_csv(SALIDA, index=False)


def revisar_completa():
    cod = leer_csv(SALIDA)
    llm = cod[[f"llm_{c}" for c in CATS]]
    faltan = cod[llm.isna().any(axis=1)]
    malos = cod[~llm.isin([0, 1]).all(axis=1) & ~llm.isna().any(axis=1)]
    if len(malos):
        print(f"Valores distintos de 0/1 en: {list(malos.id)}")
        return False
    if len(faltan):
        n_val = int(faltan.es_validacion.sum())
        print(f"Faltan {len(faltan)} canciones por codificar con Claude "
              f"({len(faltan) - n_val} normales y {n_val} de validación).")
        if n_val:
            print("Recuerden: las de validación se codifican solo cuando h1 y h2 hayan terminado.")
        return False
    print(f"Codificación completa: {len(cod)} canciones.")
    return True


def codificar_api(cliente, prompt, id_):
    letra = (LETRAS / f"{id_}.txt").read_text(encoding="utf-8")
    r = cliente.messages.create(
        model=MODELO, max_tokens=400, temperature=0, system=prompt,
        messages=[{"role": "user", "content": f"<letra>\n{letra}\n</letra>"}])
    texto = re.sub(r"^```(json)?|```$", "", r.content[0].text.strip()).strip()
    salida = json.loads(texto)
    return {"id": id_, **{f"llm_{c}": int(salida[c]) for c in CATS},
            "llm_justificacion": salida["justificacion"], "modelo": r.model,
            "fecha": date.today().isoformat()}


def main():
    if not (DATA / "submuestra_validacion.csv").exists():
        print("Falta la muestra (corran el paso 2).")
        return False

    if MODO_LLM == "manual":
        if not SALIDA.exists():
            crear_plantilla()
            print(f"Plantilla creada en {SALIDA.relative_to(SALIDA.parents[1])}. "
                  "Llénenla con las respuestas de Claude (ver README, paso 5).")
            return False
        return revisar_completa()

    # --- modo API ---
    if SALIDA.exists():
        print("La codificación ya existe; no se vuelve a llamar a la API.")
        return revisar_completa()
    import anthropic
    from dotenv import load_dotenv
    load_dotenv()
    cliente = anthropic.Anthropic()
    prompt = (DOCS / "prompt_codificacion.txt").read_text(encoding="utf-8")
    val = set(pd.read_csv(DATA / "submuestra_validacion.csv").id)
    filas, errores = [], []
    for id_ in pd.read_csv(DATA / "muestra.csv").id:
        try:
            filas.append({**codificar_api(cliente, prompt, id_), "es_validacion": int(id_ in val)})
        except Exception as e:  # se registra y se sigue
            errores.append((id_, str(e)[:120]))
    pd.DataFrame(filas)[COLS].to_csv(SALIDA, index=False)
    print(f"Codificadas: {len(filas)}. Con error: {errores}")
    return not errores


if __name__ == "__main__":   # permite correr este paso solo (clic derecho > Run en PyCharm)
    main()
