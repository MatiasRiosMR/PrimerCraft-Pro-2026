---
title: Evaluación heurística — UI-3 Resultados de candidatos (HU-05)
---

# Evaluación heurística — UI-3 · Resultados de candidatos

| | |
|---|---|
| **HU** | HU-05 · Caracterización de candidatos (CU-05, incluido desde CU-02) |
| **Perfil** | [`user_profile.md`](../user_profile.md) |
| **Escenario de uso** | Escenario A — Diseñar primers para un gen |
| **Maqueta** | [`hu-05_resultados-candidatos.html`](../../mockups/hu-05_resultados-candidatos.html) |
| **Herramienta IA** | Claude (generación) · Claude Code (iteración 2: JavaScript y panel) · Gemini (evaluación, en una conversación nueva) |

---

## Ciclo 1 — Generación del maquetado

### Prompt utilizado

```text
Actuá como diseñador/a de interfaces. Generá el maquetado en HTML de UNA pantalla de
"PrimerCraft Pro", una aplicación web para diseñar primers de PCR/qPCR.

CRITERIOS: <los mismos criterios que en UI-1 (ver criterios_generacion.md)>
Importante: el SRS deja FUERA de alcance el scoring/ranking automático. No inventes un
puntaje global: mostrá las métricas desglosadas y dejá que el usuario decida.

USUARIO (perfil): <mismo perfil que en UI-1>. Le molesta que las herramientas actuales
sean una "caja negra" que solo exponen un número final.

ESCENARIO: la corrida de NM_007294 (BRCA1, Homo sapiens) terminó. Laura quiere ver
los pares candidatos con sus métricas y abrir el detalle de uno para ver el amplicón.

HISTORIA HU-05: Como investigador/a, quiero que el sistema caracterice los pares
candidatos según sus propiedades termodinámicas, especificidad y estructuras
secundarias, así como el amplicón esperado, para disponer de candidatos adecuados.
  1. Métricas: Tm real, %GC, GC clamp y penalización por repeticiones de cada primer.
  2. Estructuras secundarias: horquillas, homodímeros y heterodímero F/R con su ΔG.
  3. Amplicón: posición y longitud.
  4. Conjunto final de pares caracterizados.
  Además, CU-02 E1: ningún candidato cumple todos los parámetros.
  La especificidad (BLAST) en el MVP es simulada (mock).
```

> Este prompt se registra tal como se envió. En el SRS actual "ningún candidato cumple todos los parámetros" es CU-02 E2, no E1.

> Los marcadores `<…>` remiten a textos ya transcriptos completos en el prompt de UI-1 y en el perfil; se abrevian para no repetirlos.

### Respuesta obtenida

HTML: [`../../mockups/hu-05_resultados-candidatos.html`](../../mockups/hu-05_resultados-candidatos.html) (v1, iteración 2).

### Vista previa (capturas de la versión actual)

**Con candidatos**

![Con candidatos](../../mockups/capturas/hu-05_resultados-candidatos__1-con-candidatos.png)

**Sin candidatos (CU-02 E2)**

![Sin candidatos (CU-02 E2)](../../mockups/capturas/hu-05_resultados-candidatos__2-sin-candidatos.png)

**Supuestos introducidos por la IA a revisar (iteración 1):**

- Umbrales de semáforo (ΔG horquilla > −3, dímero > −6 kcal/mol, ΔTm ≤ 2 °C, repeticiones ≥ 4 nt). **No están en el SRS.** Son valores habituales en la bibliografía, pero el grupo debe decidir si los adopta y documentarlos.
- Gráfico de "pesas" (dumbbell) con la Tm de F y R sobre la escala 57–63 °C y el objetivo marcado.
- Filtros (todos / sin advertencias / con advertencias), opciones de orden y botón "Copiar" de cada secuencia. Copiar no es exportar, pero tampoco está en el TP1.
- Vista del heterodímero F·R con los enlaces marcados.
- En CU-02 E2: la v1 inicial tenía un embudo con cuántas ventanas descartó cada parámetro y una sugerencia de ajuste. **Se quitó antes de la evaluación** porque es una función de diagnóstico que el TP1 no pide; quedaron el mensaje, los parámetros usados y el botón "Ajustar parámetros".
- La pantalla evita a propósito cualquier puntaje global o "mejor par" (fuera de alcance, SRS §2.6).
- Secuencias y métricas de ejemplo **ilustrativas** (no calculadas); el amplicón mostrado sí mide 184 pb.
- Ilustraciones SVG (cromatograma del encabezado, ícono de filtro sin resultados, par hibridado) embebidas en el HTML.

### Iteración 2 del ciclo 1 (30/09) — Interacción con JavaScript y diseño de panel

Antes de correr la evaluación, el grupo cambió dos criterios de generación (ver [`criterios_generacion.md`](../criterios_generacion.md)) y pidió regenerar la maqueta con **Claude Code** sobre la misma base visual:

- **Tecnología:** HTML + CSS + **JavaScript** sin frameworks ni dependencias; el archivo se sigue abriendo con doble clic. El JavaScript va al final del archivo en dos bloques: `interaccion-nucleo` (igual en las cinco pantallas: datos de la corrida entre pantallas, avisos con "Deshacer", atajos de teclado, validaciones compartidas) e `interaccion-pantalla` (el comportamiento propio de esta pantalla). Sin JavaScript, la maqueta se ve como la versión estática.
- **Diseño de panel:** en escritorio la pantalla ocupa exactamente la ventana y no se desplaza; si una columna no entra, se desplaza solo esa columna. En tablet y teléfono se mantiene el desplazamiento normal.

**Qué cambió en esta pantalla:**

- La lista se arma desde datos: los 4 pares de la versión estática más 20 generados de forma reproducible (mismo resultado en cada apertura). Los contadores de los filtros son reales (24 · 17 · 7).
- Filtros y orden funcionan; "Ver más" agrega de a 6 pares.
- Se elige un par con el mouse o con las flechas ↑ ↓ (atajos <kbd>j</kbd> / <kbd>k</kbd>). El detalle se actualiza con sus secuencias, métricas, umbrales, ubicación y amplicón.
- Las pestañas funcionan: "Estructuras secundarias" dibuja el heterodímero calculado a partir de las secuencias y muestra horquillas y homodímeros.
- "Copiar" deja la secuencia en el portapapeles y lo confirma con un aviso (atajo <kbd>c</kbd>).
- Panel: la lista tiene desplazamiento propio; en el detalle, forward y reverse van lado a lado.

**Supuestos nuevos a revisar:**

- Los 20 pares agregados y sus métricas son datos de ejemplo (GC entre 40 % y 60 %). El dibujo del heterodímero se calcula, pero el valor de ΔG es un dato de ejemplo.
- Por defecto se muestra primero el par con menor diferencia de Tm (es el primer criterio de orden).
- Los casos del botón "Guion demo" (por ejemplo, `NM_999999` → identificador inexistente) son convenciones de la simulación, no reglas del sistema.

> **Al pedir la evaluación:** la pastilla punteada "Estado de la maqueta" y su botón "Guion demo" no son parte de la interfaz. El bloque `<style id="fuentes-embebidas">` (tipografías en base64, ~145 KB) se puede omitir al pegar el HTML.

---

## Ciclo 2 — Evaluación heurística por IA

### Prompt utilizado

```text
Asumí el rol de especialista en interfaz de usuario y usabilidad.
Evaluá esta pantalla de "PrimerCraft Pro" heurística por heurística según las 10
heurísticas de Nielsen, pensando en ESTE usuario y escenario (no uno genérico).
Ignorá la pastilla "Estado de la maqueta" y su botón "Guion demo": no son parte de la
interfaz. La pantalla tiene JavaScript: evaluá también su comportamiento, que está
descrito en los comentarios de los bloques <script>.

PERFIL: <pegar perfil §2>
ESCENARIO: <pegar Escenario A §3.1>
HISTORIA: <pegar HU-05 + CU-02 E2>

Para cada heurística: veredicto (CUMPLE / CUMPLE PARCIALMENTE / NO CUMPLE), por qué
(con referencia al elemento del HTML) y, si corresponde, hallazgo y sugerencia.
Numerá los hallazgos (H1, H2, …).
Respondé únicamente con un documento Markdown, sin texto antes ni después, para
guardarlo como archivo .md. Usá exactamente esta estructura:

# Evaluación heurística — <nombre de la pantalla>

## Resumen
| N.° | Heurística | Veredicto | Hallazgos |
(una fila por cada una de las 10 heurísticas; en Hallazgos, los H… o "—")

## 1. Visibilidad del estado del sistema
**Veredicto:** CUMPLE / CUMPLE PARCIALMENTE / NO CUMPLE
**Por qué:** … (con referencia al elemento concreto del HTML)
**Hallazgos:** H… (o "Ninguno")

(repetir la misma sección para las heurísticas 2 a 10)

## Hallazgos
| Hallazgo | Heurística | Severidad (0–4) | Elemento del HTML | Problema | Sugerencia |

HTML:
<pegar el contenido de hu-05_resultados-candidatos.html, sin el bloque <style id="fuentes-embebidas">>
```

### Respuesta completa de la IA

Respuesta de **Gemini** en una conversación nueva (02/10/2026), pegada sin editar.

<details>
<summary>Ver la respuesta completa</summary>

# Evaluación heurística — Resultados de candidatos (HU-05)

## Resumen
| N.° | Heurística | Veredicto | Hallazgos |
|---|---|---|---|
| 1 | Visibilidad del estado del sistema | CUMPLE PARCIALMENTE | H1, H2 |
| 2 | Coincidencia entre el sistema y el mundo real | CUMPLE | — |
| 3 | Control y libertad del usuario | CUMPLE PARCIALMENTE | H3, H4 |
| 4 | Consistencia y estándares | CUMPLE PARCIALMENTE | H5, H6 |
| 5 | Prevención de errores | CUMPLE | — |
| 6 | Reconocer antes que recordar | CUMPLE | — |
| 7 | Flexibilidad y eficiencia de uso | CUMPLE PARCIALMENTE | H7 |
| 8 | Estética y diseño minimalista | CUMPLE | — |
| 9 | Ayudar a los usuarios a reconocer, diagnosticar y recuperarse de errores | NO CUMPLE | H8, H9 |
| 10 | Ayuda y documentación | CUMPLE PARCIALMENTE | H10 |

---

## 1. Visibilidad del estado del sistema
**Veredicto:** CUMPLE PARCIALMENTE  
**Por qué:** En la vista principal (`.v1`), el sistema indica claramente qué par candidato está seleccionado (`.pair.sel`) y actualiza el panel de detalle (`.det-h`, `.metrics`) de forma inmediata. Sin embargo, en la lista de pares candidatos (`.list .pair`), no se muestra explícitamente el número total de candidatos generados ni la posición del par seleccionado dentro del total (p. ej., "Mostrando 1 de 24 candidatos"). Además, en la vista sin candidatos (`#st2` / `.v2`), se muestra una llamada informativa (`.callout`), pero no se explicita visualmente qué fase o criterio del filtro descartó la totalidad de los pares.  
**Hallazgos:** H1, H2

---

## 2. Coincidencia entre el sistema y el mundo real
**Veredicto:** CUMPLE  
**Por qué:** El lenguaje utilizado respeta plenamente el dominio del usuario (Biólogo/a molecular con alto conocimiento del dominio). Términos como Tm, %GC, GC clamp, ΔG de horquillas y heterodímeros, hebra Forward/Reverse, amplicón y coordenadas de secuencia están expresados con rigor técnico en los bloques `.metrics`, `.dimer` y `.amp`. La representación visual del amplicón y el "dumbbell" de Tm (`.db`) coinciden con modelos mentales habituales en biología molecular.  
**Hallazgos:** Ninguno

---

## 3. Control y libertad del usuario
**Veredicto:** CUMPLE PARCIALMENTE  
**Por qué:** El usuario puede seleccionar libremente cualquier par de la lista (`.pair`), alternar entre las pestañas del detalle (`.tabs span`) y copiar secuencias al portapapeles mediante el botón `.copy`. No obstante, la interfaz no ofrece un mecanismo para reordenar o filtrar los pares candidatos (por ejemplo, ordenar por ΔG, Tm o longitud del amplicón). En la barra de acción inferior (`.actionbar`), si el usuario desea modificar los parámetros de diseño iniciales tras ver los resultados, no dispone de un botón directo de "Ajustar parámetros" o "Volver a diseñar", obligándolo a recurrir a la navegación general del riel (`.rail a`).  
**Hallazgos:** H3, H4

---

## 4. Consistencia y estándares
**Veredicto:** CUMPLE PARCIALMENTE  
**Por qué:** La paleta visual y la estructura general son consistentes con la guía del sistema (`.fwd` en tono verde/azulado, `.rev` en violeta). Sin embargo, se observa una inconsistencia funcional en la interacción con las pestañas de detalle (`.tabs span`): en el marcado HTML estático no se utilizan roles accesibles de ARIA (`role="tablist"`, `role="tab"`, `aria-selected`), y el comportamiento script asociado solo maneja estilos de activación visual sin asegurar la gestión de foco por teclado estándar. Además, la nomenclatura de alertas en métricas usa clases heterogéneas (`.m.ok`, `.m.w`, `.m.e`) respecto al estándar global de insignias (`.b-ok`, `.b-warn`, `.b-err`).  
**Hallazgos:** H5, H6

---

## 5. Prevención de errores
**Veredicto:** CUMPLE  
**Por qué:** Los valores fuera de rango recomendado o que presentan riesgos termodinámicos (como un ΔG muy negativo o una diferencia de Tm elevada) se destacan visualmente con bordes y colores de advertencia (`.m.w`, `.fp .w b`). La copia de secuencias mediante `.copy` previene errores manuales de transcripción o selección de texto al pasar los primers a un pedido de síntesis o a una planilla.  
**Hallazgos:** Ninguno

---

## 6. Reconocer antes que recordar
**Veredicto:** CUMPLE  
**Por qué:** El desglose completo de métricas por par en `.metrics` (Tm, %GC, GC clamp, ΔG horquilla, ΔG homodímero, ΔG heterodímero) evita que el usuario tenga que calcular de memoria o deducir por qué un par recibió determinado puntaje. La alineación del heterodímero (`.dimer`) y la simulación del amplicón (`.amp`) muestran exactamente la secuencia y los sitios de unión con resaltado sintáctico de bases (`.seq .A`, `.C`, `.G`, `.T`), satisfaciendo la necesidad del usuario de ver las métricas desglosadas para confiar en el resultado.  
**Hallazgos:** Ninguno

---

## 7. Flexibilidad y eficiencia de uso
**Veredicto:** CUMPLE PARCIALMENTE  
**Por qué:** La función de copiar secuencia en un clic (`.copy`) acelera el flujo de trabajo de la mesada/oficina. Sin embargo, falta una opción de exportación masiva (por ejemplo, exportar la lista de candidatos o el reporte del par seleccionado a CSV, FASTA o PDF) para alimentar el registro de trabajo del laboratorio sin requerir copiar par por par.  
**Hallazgos:** H7

---

## 8. Estética y diseño minimalista
**Veredicto:** CUMPLE  
**Por qué:** La interfaz aplica una jerarquía visual limpia mediante la tipografía (*Newsreader* y *Instrument Sans* con *JetBrains Mono* para código genético) y tarjetas estructuradas (`.card`, `.split`, `.res`). La información técnica densa está organizada en columnas de resumen y detalle sin sobrecargar la pantalla ni incluir elementos decorativos irrelevantes.  
**Hallazgos:** Ninguno

---

## 9. Ayudar a los usuarios a reconocer, diagnosticar y recuperarse de errores
**Veredicto:** NO CUMPLE  
**Por qué:** Cuando el sistema no genera ningún candidato (`#st2` / `.v2` - CU-02 E2), la pantalla muestra un aviso genérico de que no se encontraron pares que cumplan los parámetros, pero no proporciona un diagnóstico claro sobre qué parámetro fue el más restrictivo (p. ej., Tm, %GC o heterodímeros) ni ofrece acciones directas / atajos para relajar dicho parámetro y reintentar la búsqueda sin perder los datos ingresados.  
**Hallazgos:** H8, H9

---

## 10. Ayuda y documentación
**Veredicto:** CUMPLE PARCIALMENTE  
**Por qué:** Las métricas cuentan con etiquetas claras, pero carecen de contextualización o valor umbral de referencia explicito en la interfaz (por ejemplo, un *tooltip* o texto explicativo sobre el rango óptimo de ΔG aceptable para prevenir estructuras secundarias en qPCR). Si bien el usuario posee alto conocimiento del dominio, disponer del valor límite de referencia directo reduce la carga cognitiva durante la validación.  
**Hallazgos:** H10

---

## Hallazgos

| Hallazgo | Heurística | Severidad (0–4) | Elemento del HTML | Problema | Sugerencia |
|---|---|---|---|---|---|
| H1 | 1. Visibilidad del estado del sistema | 2 | `.toolbar`, `.list` | No se indica la cantidad total de pares candidatos generados ni el total filtrado/mostrado en la cabecera del listado. | Agregar un contador visible en la barra de herramientas (ej. "24 candidatos encontrados"). |
| H2 | 1. Visibilidad del estado del sistema | 2 | `.v2 .callout` | En el estado sin candidatos (`.v2`), la interfaz no informa el motivo específico por el cual la búsqueda finalizó con 0 pares. | Mostrar un resumen de descarte (embudo o filtro) que especifique cuántos pares cayeron por Tm, ΔG, %GC, etc. |
| H3 | 3. Control y libertad del usuario | 2 | `.toolbar` | La lista de pares candidatos no cuenta con opciones de ordenamiento (por Tm, ΔG, scoring) ni filtrado rápido. | Agregar un selector de ordenamiento `<select>` funcional en `.toolbar` para clasificar candidatos por distintos criterios termodinámicos. |
| H4 | 3. Control y libertad del usuario | 3 | `.actionbar` | La barra de acciones inferior no ofrece un botón directo para modificar los parámetros de la corrida e iniciar un nuevo intento. | Incluir un botón secundario "Ajustar parámetros" en `.actionbar` que conserve el identificador NCBI y permita editar las restricciones. |
| H5 | 4. Consistencia y estándares | 1 | `.tabs` | El componente de pestañas (`.tabs span`) no utiliza marcado ni roles ARIA semánticos (`role="tablist"`, `role="tab"`). | Estructurar las pestañas con la semántica WAI-ARIA estándar para garantizar navegación por teclado y accesibilidad. |
| H6 | 4. Consistencia y estándares | 1 | `.m.ok`, `.m.w`, `.m.e` | Inconsistencia en la nomenclatura de clases CSS de estados respecto a los badges globales (`.b-ok`, `.b-warn`, `.b-err`). | Homologar los sufijos de estado CSS a lo largo del stylesheet (`.m-ok`, `.m-warn`, `.m-err`). |
| H7 | 7. Flexibilidad y eficiencia de uso | 2 | `.actionbar`, `.det-h` | No existe una opción para exportar la lista de candidatos o el reporte del par seleccionado a formatos estándar (CSV, FASTA, GenBank). | Añadir un botón "Exportar resultados" en `.actionbar` con opciones de descarga en CSV y FASTA. |
| H8 | 9. Reconocer, diagnosticar y recuperarse de errores | 3 | `.v2` (Estado sin candidatos) | No se brinda una vía de recuperación directa para corregir la falta de candidatos sin reiniciar todo el flujo desde cero. | Incluir un acceso directo promocionado "Relajar restricciones de diseño" dentro del mensaje de alerta de la vista sin candidatos. |
| H9 | 9. Reconocer, diagnosticar y recuperarse de errores | 2 | `.m.w`, `.m.e` | Las métricas con advertencia o error en el panel de detalle destacan el valor en rojo/amarillo pero no explican la causa del fallo termodinámico. | Agregar un mensaje aclaratorio corto bajo el valor (ej. "ΔG < -9 kcal/mol: riesgo alto de horquilla a Tm de reacción"). |
| H10 | 10. Ayuda y documentación | 1 | `.m .k` | Falta indicación de los valores de referencia o umbrales recomendados para las métricas termodinámicascomplejas (ΔG). | Incluir notas breves de rango de referencia o leyendas explicativas (*tooltips*) en los encabezados de cada tarjeta de métrica. |

</details>

---

## Revisión crítica del grupo

> _Pendiente: completar después de la evaluación, con una fila por hallazgo (H1, H2, …)._

| Hallazgo | Heurística | Veredicto de la IA | Decisión | Justificación del grupo |
|---|---|---|---|---|
| H1 | | | Acepta / Rechaza | |
| H2 | | | | |
| H3 | | | | |

**Criterio para decidir:** se acepta si el hallazgo afecta al perfil y al escenario concretos; se rechaza si supone un usuario genérico (por ejemplo, explicar qué es la Tm a alguien con conocimiento de dominio alto), si agrega funciones fuera de la HU o del alcance del SRS, o si contradice el TP1.

---

## Ciclos adicionales

> _Completar solo si, a partir de los hallazgos aceptados, se ajusta la pantalla: cambios pedidos (H…), prompt, archivo resultante (`…_v2.html`, sin pisar la v1) y reevaluación con la misma tabla._
