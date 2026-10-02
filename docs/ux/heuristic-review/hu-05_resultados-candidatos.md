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

> Los marcadores `<…>` remiten a textos ya transcriptos completos en el prompt de UI-1 y en el perfil; se abrevian para no repetirlos.

### Respuesta obtenida

HTML: [`../../mockups/hu-05_resultados-candidatos.html`](../../mockups/hu-05_resultados-candidatos.html) (v1, iteración 2).

### Vista previa (capturas de la versión actual)

**Con candidatos**

![Con candidatos](../../mockups/capturas/hu-05_resultados-candidatos__1-con-candidatos.png)

**Sin candidatos (CU-02 E1)**

![Sin candidatos (CU-02 E1)](../../mockups/capturas/hu-05_resultados-candidatos__2-sin-candidatos.png)

**Supuestos introducidos por la IA a revisar (iteración 1):**

- Umbrales de semáforo (ΔG horquilla > −3, dímero > −6 kcal/mol, ΔTm ≤ 2 °C, repeticiones ≥ 4 nt). **No están en el SRS.** Son valores habituales en la bibliografía, pero el grupo debe decidir si los adopta y documentarlos.
- Gráfico de "pesas" (dumbbell) con la Tm de F y R sobre la escala 57–63 °C y el objetivo marcado.
- Filtros (todos / sin advertencias / con advertencias), opciones de orden y botón "Copiar" de cada secuencia. Copiar no es exportar, pero tampoco está en el TP1.
- Vista del heterodímero F·R con los enlaces marcados.
- En CU-02 E1: la v1 inicial tenía un embudo con cuántas ventanas descartó cada parámetro y una sugerencia de ajuste. **Se quitó antes de la evaluación** porque es una función de diagnóstico que el TP1 no pide; quedaron el mensaje, los parámetros usados y el botón "Ajustar parámetros".
- La pantalla evita a propósito cualquier puntaje global o "mejor par" (fuera de alcance, SRS §2.6).
- Secuencias y métricas de ejemplo **ilustrativas** (no calculadas); el amplicón mostrado sí mide 184 pb.
- Ilustraciones SVG (cromatograma del encabezado, ícono de filtro sin resultados, par hibridado) embebidas en el HTML.

### Iteración 2 del ciclo 1 (30/09) — Interacción con JavaScript y diseño de panel

Antes de correr la evaluación, el grupo cambió dos criterios de generación (ver [`criterios_generacion.md`](../criterios_generacion.md)) y pidió regenerar la maqueta con **Claude Code** sobre la misma base visual:

- **Tecnología:** HTML + CSS + **JavaScript** sin frameworks ni dependencias; el archivo se sigue abriendo con doble clic. El JavaScript va al final del archivo en dos bloques: `interaccion-nucleo` (igual en las cinco pantallas: datos de la corrida entre pantallas, avisos con "Deshacer", atajos de teclado, validaciones compartidas) e `interaccion-pantalla` (el comportamiento propio de esta pantalla). Sin JavaScript, la maqueta se ve como la versión estática.
- **Diseño de panel:** en escritorio la pantalla ocupa exactamente la ventana y no se desplaza; si una columna no entra, se desplaza solo esa columna. En tablet y teléfono se mantiene el desplazamiento normal.

**Pedidos al asistente (texto literal del grupo):**

```text
el maquetado hacelo con html pero metele otro lenguaje para mejorar la experiencia del
usuario mas moderna
```

```text
hay widgets como el de [texto pegado del panel "Próximos pasos"] que tengo que deslizar
para verlos. la idea es que todo este en la misma vision, onda no tener que deslizar.
como un panel digamos
```

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
HISTORIA: <pegar HU-05>

Para cada heurística: veredicto (CUMPLE / CUMPLE PARCIALMENTE / NO CUMPLE), por qué
(con referencia al elemento del HTML) y, si corresponde, hallazgo y sugerencia.
Numerá los hallazgos (H1, H2, …).

HTML:
<pegar el contenido de hu-05_resultados-candidatos.html, sin el bloque <style id="fuentes-embebidas">>
```

### Respuesta completa de la IA

> _Pendiente: pegar la respuesta completa de la IA, sin editar._

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
