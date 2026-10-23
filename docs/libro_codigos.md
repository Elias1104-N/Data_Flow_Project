# Libro de códigos — v0.1 (BORRADOR)

> Estado: borrador. Se congela como **v1.0** después de la prueba con 10 canciones de práctica (paso 3 de la guía).
> Cada cambio posterior se registra en el historial al final del archivo.

**Unidad de codificación:** la canción completa.
**Escala:** cada categoría es binaria: 1 = presente, 0 = ausente.
**Regla general de duda:** ante la duda, 0. Se codifica 1 solo si esa lectura es la dominante.
**Columna `ambiguo`** (solo para codificadores humanos): 1 si dudaron en al menos una categoría por doble sentido, ironía o jerga.

---

## C1 — Contenido sexual explícito

**Definición operativa:** la letra describe o alude de forma inequívoca a un acto sexual, ya sea directamente o mediante un doble sentido cuya lectura sexual es la dominante.

**Se incluye:**
- Descripción de actos sexuales, aunque sea con eufemismos.
- Doble sentido cuya única lectura razonable es sexual.

**Se excluye:**
- Baile (perreo) sin referencia a un acto sexual.
- Coqueteo, deseo o atracción sin referencia a un acto.
- Besos o caricias sin más.

**Ejemplos (parafraseados, sin copiar versos):**
1. Canción que narra un encuentro sexual en un hotel después de una fiesta → 1
2. [completar]

**Contraejemplos:**
1. Canción que invita a bailar pegados toda la noche → 0
2. [completar]

**Casos límite conocidos:** [completar después de la prueba con 10 canciones]

---

## C2 — Cuerpo de la mujer como atributo principal

**Definición operativa:** se describe el cuerpo de una mujer (partes, medidas, intervenciones estéticas) como lo que se valora de ella.

**Se incluye:** [completar]
**Se excluye:** elogio general ("eres linda") sin foco en el cuerpo; el foco está en su actitud o personalidad.
**Ejemplos:** [2, parafraseados]
**Contraejemplos:** [2, parafraseados]
**Casos límite conocidos:** [completar]

---

## C3 — Agencia femenina

**Definición operativa:** una mujer aparece como sujeto que expresa su propio deseo o toma decisiones, en primera persona o descrita así.

**Se incluye:** [completar]
**Se excluye:** la mujer aparece solo como objeto del deseo o de la acción de otro.
**Ejemplos:** [2, parafraseados]
**Contraejemplos:** [2, parafraseados]
**Casos límite conocidos:** canciones cantadas por un hombre que describe a una mujer que decide → [decidir regla]

---

## C4 — Violencia

**Definición operativa:** hay referencias a armas, agresión física, amenazas o muerte con sentido literal.

**Se incluye:** [completar]
**Se excluye:** lenguaje violento metafórico ("me matas" como halago, "está que mata").
**Ejemplos:** [2, parafraseados]
**Contraejemplos:** [2, parafraseados]
**Casos límite conocidos:** [completar]

---

## Historial de versiones

| Versión | Fecha | Cambio | Motivo |
| --- | --- | --- | --- |
| v0.1 | 22/10/2026 | Borrador inicial | — |
