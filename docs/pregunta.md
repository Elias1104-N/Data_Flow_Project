# Pregunta de investigación e hipótesis

## Pregunta principal
¿Ha cambiado entre 2010 y 2025 la proporción de canciones de reggaetón exitosas
(listas de fin de año Billboard Hot Latin Songs) que contienen contenido sexual
explícito, según la definición de la categoría C1 del libro de códigos?

- Unidad de análisis: la canción.
- Qué se cuenta: canciones con C1 = 1.
- Sobre qué muestra: 160 canciones, 40 por periodo (2010–13, 2014–17, 2018–21, 2022–25).

H0: la probabilidad de que una canción tenga contenido sexual explícito no cambia con el año (β_año = 0).
H1: esa probabilidad cambia con el año (β_año ≠ 0).

## Pregunta secundaria 1
¿Difiere la proporción de canciones que describen el cuerpo de una mujer como su
atributo principal (C2) entre canciones con y sin una intérprete mujer acreditada?

H0: C2 es independiente de que haya una intérprete mujer.
H1: C2 y la presencia de una intérprete mujer están asociadas.

## Pregunta secundaria 2
¿Ha cambiado la riqueza léxica de las letras (MATTR, ventana de 50 palabras) entre 2010 y 2025?

H0: la distribución de MATTR es igual en los cuatro periodos y no hay tendencia monótona anual.
H1: al menos un periodo difiere, o hay una tendencia monótona.

## Variables y pruebas

| Pregunta | Respuesta | Explicativa | Prueba | Tamaño de efecto |
| --- | --- | --- | --- | --- |
| Principal | C1 (0/1) | Año y periodo | Regresión logística + tendencia lineal por periodos + Mann-Kendall | OR por año con IC 95 % |
| Secundaria 1 | C2 (0/1) | Intérprete mujer (sí/no) | Chi-cuadrado, o Fisher si alguna esperada < 5 | OR con IC 95 % y phi |
| Secundaria 2 | MATTR | Periodo | Kruskal-Wallis + Mann-Kendall sobre la mediana anual | Épsilon cuadrado y tau de Kendall |

## Alcance
Los resultados describen las canciones de reggaetón más exitosas en la lista de
Billboard (Estados Unidos), no todo el género. El estudio mide asociaciones, no
efectos sobre las audiencias.

## Condición
Las preguntas que dependen de C1 o C2 solo se responden si esas categorías
superan la validación (κ ≥ 0,61 y límite inferior del IC ≥ 0,40).

## Decisión de diseño registrada
Se evaluó como alternativa una pregunta sobre agencia femenina según el género del
intérprete (2015–2025). Se descartó por dos riesgos estadísticos: pocas canciones con
intérprete mujer en los primeros años (estratos pequeños) y menor probabilidad de que la
categoría de agencia alcanzara un kappa aceptable. La agencia femenina (C3) se sigue
codificando como variable descriptiva.