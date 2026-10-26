# Pregunta de investigación e hipótesis

## Pregunta principal
¿Ha cambiado entre 2010 y 2025 la proporción de canciones de reggaetón exitosas
(canciones que alcanzaron el n.º 1 en Hot Latin Songs o Latin Airplay de Billboard) que contienen contenido sexual
explícito, según la definición de la categoría C1 del libro de códigos?

- Unidad de análisis: la canción.
- Qué se cuenta: canciones con C1 = 1.
- Sobre qué muestra: 160 canciones (2010–13: 16 y 2014–17: 44, ambos por censo; 2018–21: 50; 2022–25: 50).

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

## Definición de "intérprete mujer"
interprete_mujer = 1 si al menos una mujer está acreditada como intérprete (principal o
invitada) en la lista de Billboard; 0 si solo hay hombres.

## Marco muestral
Canciones que alcanzaron el n.º 1 de Hot Latin Songs o Latin Airplay de Billboard al menos
una semana entre 2010 y 2025, según las listas anuales de Wikipedia (`data/listas_por_anio.csv`).
En 2010 y 2011 solo existía Hot Latin Songs, que entonces medía la radio; Latin Airplay se
creó en octubre de 2012 con esa misma metodología. El año de cada canción es el de su primera
semana en n.º 1, y cada canción cuenta una sola vez.

Una canción es reggaetón si su página de Wikipedia (en español o en inglés) incluye
"reguetón" o "reggaeton" entre sus géneros; las fusiones cuentan. Resultado: 459 canciones
n.º 1, de las cuales 264 son reggaetón (2010–13: 16; 2014–17: 44; 2018–21: 129; 2022–25: 75).

Se descartó la lista de fin de año de Billboard porque requiere suscripción.

## Alcance
Los resultados describen las canciones de reggaetón más exitosas en la lista de
Billboard (Estados Unidos), no todo el género. El estudio mide asociaciones, no
efectos sobre las audiencias.

El tamaño por estrato se fijó en 50 para alcanzar una muestra total de al menos 150
canciones; los estratos con menos de 50 canciones en el marco se toman completos (censo).

## Condición
Las preguntas que dependen de C1 o C2 solo se responden si esas categorías
superan la validación (κ ≥ 0,61 y límite inferior del IC ≥ 0,40).

## Decisión de diseño registrada
Se evaluó como alternativa una pregunta sobre agencia femenina según el género del
intérprete (2015–2025). Se descartó por dos riesgos estadísticos: pocas canciones con
intérprete mujer en los primeros años (estratos pequeños) y menor probabilidad de que la
categoría de agencia alcanzara un kappa aceptable. La agencia femenina (C3) se sigue
codificando como variable descriptiva.