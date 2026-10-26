# Data Flow — Proyecto 3

Análisis estadístico de letras de reggaetón exitosas (canciones que llegaron al n.º 1 de
Hot Latin Songs o Latin Airplay de Billboard, 2010–2025) con validación de Claude como
instrumento de medición.

**Pregunta principal:** ¿ha cambiado entre 2010 y 2025 la proporción de canciones de
reggaetón exitosas con contenido sexual explícito?

**Equipo:** Elias Jose Parra Royero y Maria Monica Murillo Rincon · Estadística Industrial · Universidad del Magdalena

---

## Antes de empezar

- Necesitan **Python 3.10 o superior** y **PyCharm**.
- El repositorio **no incluye el entorno virtual** (la carpeta `.venv` o `venv`, con las
  librerías). Cada persona lo crea en su computador con los pasos de abajo:
  1. Crear el entorno: esto genera la carpeta, solo con Python.
  2. Instalar `requirements.txt`: esto descarga las librerías dentro de esa carpeta.
- La carpeta `resultados/` aparece vacía en GitHub a propósito: tablas y gráficos se
  generan al correr `main.py`.

## Cómo correrlo en PyCharm

1. **File > Open** y elijan la carpeta `Data_Flow_Project` (la carpeta, no un archivo).
2. **Intérprete:** abajo a la derecha, clic en el intérprete > *Add New Interpreter* >
   *Add Local Interpreter* > *Virtualenv Environment* > *New*, con ubicación
   `Data_Flow_Project/.venv`. Acepten.
3. **Librerías:** abran `requirements.txt`; PyCharm muestra un aviso arriba con
   *Install requirements*. Clic ahí. (Alternativa: pestaña *Terminal* de PyCharm →
   `pip install -r requirements.txt`).
4. **Correr todo:** clic derecho en `main.py` > *Run 'main'*. La salida aparece en la pestaña *Run*.
5. **Correr un solo paso:** clic derecho en `src/s01_muestreo.py` (o el que necesiten) > *Run*.
   Si sale `ModuleNotFoundError: No module named 'src'`, vayan a *Run > Edit Configurations*
   y pongan como *Working directory* la carpeta `Data_Flow_Project`.
6. Los CSV se abren directo en PyCharm como tabla, pero para **llenarlos** (marco,
   anotaciones, codificación) es más cómodo Excel o LibreOffice. Al guardar, elijan
   **CSV UTF-8**. Los scripts leen tanto comas como punto y coma (`leer_csv` en `config.py`),
   pero **no abran en Excel** los CSV que genera el código (`marco_muestral.csv`, `muestra.csv`):
   Excel puede cambiarles el formato al guardar.

## Cómo correrlo desde la terminal

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (en Mac/Linux: source .venv/bin/activate)
pip install -r requirements.txt
python main.py
```

`main.py` corre los pasos en orden. Si a alguno le falta algo (letras, anotaciones,
codificación), lo dice y se detiene sin romper nada. Se completa lo pedido y se vuelve
a correr `main.py`.

## Estructura

| Carpeta / archivo | Qué hay |
| --- | --- |
| `main.py` | Script maestro |
| `src/config.py` | Semilla (2026), rutas, tamaños de muestra, modelo y regla de validez |
| `src/s01_muestreo.py` | Muestra estratificada, submuestra de validación y plantillas de anotación |
| `src/s02_texto.py` | Medidas de texto (palabras, TTR, MATTR) y conteos del léxico |
| `src/s03_codificacion_llm.py` | Codificación con Claude (modo manual o API) |
| `src/s04_validacion.py` | Kappas, matrices de confusión, discrepancias y base analítica |
| `src/s05_analisis.py` | Pruebas inferenciales con tamaños de efecto y gráficos |
| `data/` | Marco, muestra, anotaciones, codificación y `base_analitica.csv` |
| `docs/` | Léxico, libro de códigos, prompt y bitácora de IA |
| `resultados/` | Tablas y gráficos que van al informe |
| `letras/` | **Solo local.** Nunca se entrega |

## Flujo de trabajo y orden de llenado

1. **Marco** → llenar `data/marco_muestral.csv` → `python main.py` crea la muestra,
   la submuestra de validación y las plantillas `anotacion_h1.csv` / `anotacion_h2.csv`.
2. **Letras** → copiar cada letra en `letras/C001.txt`, etc. → `python main.py` calcula las medidas de texto.
3. **Anotación humana** (a ciegas, cada uno por su lado) → llenar `anotacion_h1.csv` y `anotacion_h2.csv`.
4. **Codificación con Claude** → `python main.py` crea la plantilla `data/codificacion_llm.csv`.
   Primero se codifican las canciones con `es_validacion = 0`. Las de validación (= 1)
   **solo después** de terminar el punto 3, para que la anotación humana sea ciega.
5. **Consenso** → `python main.py` calcula el kappa entre humanos y crea `data/consenso.csv`
   con los desacuerdos vacíos; se deciden juntos.
6. `python main.py` → kappas de Claude contra el consenso, discrepancias, base analítica y análisis.

### Codificación manual en claude.ai (modo `MODO_LLM = "manual"`)

1. En claude.ai, creen un proyecto llamado "Codificador reggaetón" y peguen el contenido
   completo de `docs/prompt_codificacion.txt` (con el libro de códigos v1.0) como
   instrucciones del proyecto. No lo modifiquen después.
2. Elijan un modelo y úsenlo para todas las canciones. Anoten su nombre en `MODELO`
   (`src/config.py`) y en la columna `modelo`.
3. Por cada canción: **conversación nueva** dentro de ese proyecto → pegar
   `<letra>` + la letra + `</letra>` → copiar los valores del JSON a la fila de esa
   canción en `data/codificacion_llm.csv` (y la fecha).
4. Limitación que se reporta: en claude.ai no se puede fijar la temperatura.

## Regla sobre las letras

El texto completo de las letras no aparece en ningún entregable ni en el repositorio.
Las letras se guardan solo en la carpeta local `letras/`, que el `.gitignore` excluye
(se sube únicamente `LEEME.txt`). Los commits se hacen con GitHub Desktop, que respeta el
`.gitignore`; **no se suben archivos arrastrándolos a la web de GitHub**, porque la web no
lo respeta. `s04_validacion.py` verifica además que la base analítica no tenga columnas de
texto largo.

## Fuentes

- Marco: listas anuales de Wikipedia de las canciones n.º 1 de Hot Latin Songs y Latin Airplay
  de Billboard, 2010–2025 (URL y fecha de consulta por año en `data/listas_por_anio.csv`).
  La lista de fin de año de Billboard se descartó porque requiere suscripción.
- Género de cada canción: página de Wikipedia de la canción (criterio en `docs/pregunta.md`).
- Letras: Letras.com, consultadas y copiadas a mano (URL y fecha por canción en
  `data/registro_letras.csv`). Las letras nunca salen de la carpeta local `letras/`.

## Resultados principales

- **Validación:** ninguna categoría alcanzó la regla fijada antes de ver los datos (κ ≥ 0,61 y
  límite inferior del IC ≥ 0,40). Por eso la pregunta principal (C1) y la secundaria 1 (C2) no
  se responden con inferencia. Ver `resultados/tabla_kappas.csv` y `resultados/discrepancias.csv`.
- **Riqueza léxica (secundaria 2):** el MATTR sube con el tiempo (Kruskal-Wallis, ε² = 0,16;
  Mann-Kendall τ = 0,78, pendiente de Sen ≈ +0,0076 por año). El cambio se concentra en 2022–25.

## Reproducir desde cero (sesión limpia)

Un clon limpio del repositorio corre completo con `python main.py`, sin letras: el paso de
medidas de texto detecta que `letras/` está vacía y usa la `data/base_texto.csv` versionada.
La muestra no se vuelve a sortear porque `data/muestra.csv` existe; si se borra, el sorteo con
la semilla 2026 reproduce exactamente la misma muestra y la misma submuestra de validación.
