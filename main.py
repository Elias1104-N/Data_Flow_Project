"""Script maestro: corre todo el proyecto en orden.

Uso:  python main.py

Cada paso revisa si tiene lo que necesita. Si falta algo (por ejemplo, las letras
o la anotación humana), lo dice y el flujo se detiene ahí sin romper nada.
"""
from src import s01_muestreo, s02_texto, s03_codificacion_llm, s04_validacion, s05_analisis

# (nombre, módulo, ¿detiene el flujo si no está listo?)
# La codificación con Claude NO detiene el flujo: la anotación humana y el consenso
# (paso 6) deben poder avanzar antes de codificar con Claude las canciones de validación.
PASOS = [
    ("Paso 2 · Muestreo", s01_muestreo, True),
    ("Paso 4 · Medidas de texto", s02_texto, True),
    ("Paso 5 · Codificación con Claude", s03_codificacion_llm, False),
    ("Paso 6 · Validación (kappa)", s04_validacion, True),
    ("Paso 7 · Análisis", s05_analisis, True),
]

if __name__ == "__main__":
    for nombre, paso, bloquea in PASOS:
        print(f"\n=== {nombre} ===")
        if paso.main() is False and bloquea:
            print(f"\n>> El flujo se detuvo en «{nombre}». Completen lo indicado y vuelvan a correr main.py.")
            break
    else:
        print("\n>> Todo el flujo corrió completo. Resultados en la carpeta resultados/.")
