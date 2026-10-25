# Libro de códigos — v1.0 (congelado)

> Versión congelada el 25/10/2026 después de la prueba piloto (ver historial).
> No se modifica durante la codificación. Cualquier cambio posterior se registra
> como versión nueva y obliga a recodificar.

## Reglas generales

1. **Unidad:** la canción completa, incluidos coros, puentes y versos de artistas invitados.
2. **Escala:** cada categoría es binaria: 1 = presente, 0 = ausente.
3. **Lectura dominante:** se codifica 1 solo si una persona hispanohablante que conoce el
   género entendería esa lectura como la principal. Ante una duda real: 0.
4. **Basta una mención clara** que cumpla la definición. No se exige que el tema se repita.
5. **Se codifica el texto**, no el video, la portada ni lo que se sepa del artista.
6. **Las categorías son independientes y miden cosas distintas.** En particular, una
   canción puede ser sexualmente explícita (C1 = 1) sin describir partes del cuerpo de
   la mujer (C2 = 0), y al revés.
7. **Columna `ambiguo`** (solo codificadoras humanas): 1 si dudaron en al menos una
   categoría. En `nota` se indica cuál y por qué, sin copiar versos.
8. **Ninguna celda de C1 a C4 ni de `ambiguo` queda vacía.**
9. **No se copian versos** en este documento ni en las notas: los ejemplos se parafrasean.

---

## C1 — Contenido sexual explícito (pregunta principal)

**Definición operativa:** la letra describe o alude de forma inequívoca a un acto sexual,
ya sea directamente o mediante dobles sentidos cuya lectura sexual es la dominante.

**Se incluye:**
- Descripción de un acto sexual pasado, presente o propuesto.
- Invitación explícita a tener relaciones sexuales.
- **Acumulación de dobles sentidos:** cuando varias expresiones de la misma canción apuntan
  a un acto sexual, la lectura sexual se considera dominante, aunque ninguna sea explícita
  por sí sola.
- Desnudez o recorrido del cuerpo descrito dentro de un encuentro sexual.

**Se excluye (→ 0):**
- Baile o perreo, aunque sea intenso, sin referencia a un acto sexual.
- Deseo, atracción o coqueteo sin referencia a un acto.
- Besos, abrazos o caricias sin más.
- **Una sola expresión de doble sentido, aislada**, cuando el resto de la canción no la
  refuerza (→ 0 y `ambiguo` = 1).

**Ejemplos (de la prueba piloto, parafraseados):**
1. La canción combina varias metáforas (un tren que pasa por la vía de ella, subirse por las
   paredes) que juntas describen un encuentro sexual → 1. (P04)
2. En un contexto de perreo, ella pide toques y azotes, junto con otras referencias más
   directas → 1. (P02)

**Contraejemplos:**
1. La invita a bailar pegados toda la noche → 0.
2. Le dice que la desea y que quiere volver a verla → 0.

**Casos límite:**
- "Perreo intenso" o "duro" por sí solo es baile → 0.
- Una única metáfora que podría ser sexual en una canción por lo demás de fiesta → 0, `ambiguo` = 1.

---

## C2 — Cuerpo de la mujer como atributo (secundaria 1)

**Definición operativa:** la letra **nombra partes específicas** del cuerpo de una mujer
(caderas, cintura, trasero, pecho, piernas, labios, etc.), su figura o intervenciones
estéticas, como objeto de elogio o de deseo.

**Se incluye:**
- Al menos una mención clara de una parte específica del cuerpo como motivo de elogio o deseo.
- Referencias a la figura o a medidas.
- Cirugías o intervenciones estéticas presentadas como atributo.
- Comparación del cuerpo con objetos o productos.

**Se excluye (→ 0):**
- **Referencias genéricas** ("tu cuerpo", "tu piel") dentro de la descripción de un acto
  sexual: cuentan para C1, no para C2.
- Contenido sexual explícito que no nombra partes del cuerpo de la mujer (puede ser C1 = 1).
- Elogio general a la belleza ("eres hermosa", "la más linda").
- Foco en la ropa, la actitud o la forma de bailar.
- Una mujer que habla en primera persona de su propio cuerpo (puede ser C3 = 1).

**Ejemplos (parafraseados):**
1. El narrador dice que se fijó en ella por su cintura y sus caderas → 1.
2. Presume que ella "se operó" y la describe por esas partes → 1.

**Contraejemplos:**
1. Quiere recorrer con los labios toda su piel durante el encuentro: es una referencia
   genérica dentro de un acto sexual → C2 = 0 (cuenta para C1). (P01)
2. La canción es sexualmente explícita, con muchas metáforas, pero no nombra ninguna parte
   del cuerpo de ella → C2 = 0. (P10)

---

## C3 — Agencia femenina (descriptiva)

**Definición operativa:** una mujer aparece como sujeto que expresa su propio deseo o toma
sus propias decisiones (sobre relaciones, sexualidad, fiesta, dinero o su vida), en primera
persona o descrita así, y el texto presenta ese deseo o esa decisión como suyos.

**Se incluye:**
- Una mujer habla en primera persona y dice lo que quiere, elige o rechaza.
- Una mujer es descrita tomando la iniciativa o decidiendo sin depender del narrador.
- Una mujer es descrita como independiente (económica o afectivamente), como rasgo propio.

**Se excluye (→ 0):**
- La mujer aparece solo como objeto del deseo o de la acción de otro.
- **Proyección del narrador:** él afirma que ella lo desea, pero el texto no le da voz ni
  decisión propia.
- Que la intérprete sea mujer no basta: se codifica lo que dice el texto.

**Ejemplos (parafraseados):**
1. Ella cuenta que salió con sus amigas, que no necesita a nadie y que decide con quién baila → 1.
2. Él reconoce que ella lo dejó porque así lo quiso → 1.

**Contraejemplos:**
1. Él asegura que ella se muere por él, sin que ella diga ni decida nada → 0.
2. Él describe lo que le haría a ella esta noche → 0.

---

## C4 — Violencia

**Definición operativa:** la letra hace referencias **literales** a armas, agresión física,
amenazas o muerte.

**Se incluye:**
- Armas mencionadas por su nombre o por su función, en sentido literal.
- Amenazas de causar daño a alguien.
- Descripción de disparos, golpes o muertes.

**Se excluye (→ 0):**
- Metáforas: "me matas", "está que mata", "rompe la disco", "es una bomba".
- **Armas usadas como metáfora sexual** (cuentan para C1 si cumplen su definición).
- Lenguaje de baile o de fiesta.
- Contar un pasado difícil sin violencia física.

**Ejemplos (parafraseados):**
1. Advierte a un rival que anda armado y que le va a disparar si se acerca → 1.
2. Cuenta que en su barrio mataron a un amigo → 1.

**Contraejemplos:**
1. Le dice que con ese baile lo mata → 0.
2. Compara su desempeño sexual con una pistola que no sirve sin balas → C4 = 0. (P02)

---

## Historial de versiones

| Versión | Fecha | Cambio | Motivo |
| --- | --- | --- | --- |
| v0.1 | 22/10/2026 | Borrador inicial | — |
| v0.2 | 24/10/2026 | Definiciones, inclusiones, exclusiones y ejemplos completos de C1 a C4 | Preparación de la prueba piloto |
| v1.0 | 25/10/2026 | C1: regla de acumulación de dobles sentidos; C2: exige partes específicas y excluye referencias genéricas; regla general 6 (C1 y C2 son distintas); C4: armas como metáfora sexual → 0 | Prueba piloto con 10 canciones fuera de la muestra (`data/practica.csv`), codificadas por separado. Acuerdo inicial: C1 80 % (κ = 0,60), C2 70 % (κ = 0,44), C3 100 % (κ = 1,00), C4 90 % (κ = 0,00 por baja prevalencia). Los 6 desacuerdos se discutieron y llevaron a los cambios de esta versión |