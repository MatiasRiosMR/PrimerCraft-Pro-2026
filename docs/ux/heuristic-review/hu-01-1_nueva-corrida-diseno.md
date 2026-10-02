---
title: Evaluación heurística — UI-1 Nueva corrida de diseño (HU-01.1)
---

# Evaluación heurística — UI-1 · Nueva corrida de diseño

| | |
|---|---|
| **HU** | HU-01.1 · Iniciar diseño individual de primers (CU-01, Slice 1) |
| **Perfil** | [`user_profile.md`](../user_profile.md) |
| **Escenario de uso** | Escenario A — Diseñar primers para un gen |
| **Maqueta** | [`hu-01-1_nueva-corrida-diseno.html`](../../mockups/hu-01-1_nueva-corrida-diseno.html) |
| **Herramienta IA** | Claude (generación) · Claude Code (iteración 2: JavaScript y panel) · Gemini (evaluación, en una conversación nueva) |

---

## Ciclo 1 — Generación del maquetado

### Prompt utilizado

```text
Actuá como diseñador/a de interfaces. Generá el maquetado en HTML de UNA pantalla de
"PrimerCraft Pro", una aplicación web para diseñar primers de PCR/qPCR.

CRITERIOS (obligatorios):
- Un único archivo HTML5 + CSS embebido, sin frameworks, sin dependencias externas y
  sin JavaScript. Es un maquetado estático; los estados alternativos se muestran con un
  selector hecho solo con CSS, que no es parte de la interfaz.
- Español. Términos técnicos sin traducir (Tm, %GC, nt).
- Escritorio como diseño principal (≥1280 px), responsive: que se adapte a tablet y
  teléfono sin agregar ni quitar funciones.
- Accesible: foco de teclado visible, etiquetas en cada campo, errores vinculados al
  campo y estado del proceso anunciado a lectores de pantalla.
- Estética sobria y formal, a la altura de una herramienta científica: riel lateral
  claro, encabezado con el nombre del producto, tarjetas con bordes suaves, SOLO modo
  claro (sin fondos oscuros). Tipografía formal: serif para títulos (Newsreader),
  sans serif para texto (Instrument Sans) y monoespaciada para secuencias e IDs
  (JetBrains Mono), embebidas en el mismo archivo. Tono impersonal y técnico.
- Imágenes: solo ilustraciones SVG del dominio embebidas (cromatograma, ideograma del
  cromosoma, mapa del gen, doble hélice). Visualizaciones propias del dominio (bases
  coloreadas, mapas del gen, alineamientos) en lugar de tablas planas. Los estados
  siempre con texto o ícono además del color.
- Navegación: riel lateral con "Diseñar" y "Validar" (los dos puntos de entrada).
- Mostrá el estado normal Y los estados de error de la historia. Como no hay JavaScript,
  se alternan con un selector hecho solo con CSS ("Estado de la maqueta").
- NO agregues funciones que no estén en la historia (login, historial, exportar, ranking).

USUARIO (perfil): investigador/a de biología molecular de un laboratorio chico sin
presupuesto para suites pagas. Conocimiento de dominio alto (Tm, ΔG, GC clamp), uso
técnico medio (herramientas web, no programa). Usa computadora de escritorio. Su
frustración: saltar entre NCBI, Primer3 y una planilla, y descargar el FASTA a mano.

ESCENARIO: Laura quiere diseñar primers para BRCA1. Elige "Nueva corrida de diseño",
escribe NM_007294, elige Homo sapiens y deja los parámetros sugeridos
(Tm 60 °C, %GC 50 %, longitud 20 nt).

HISTORIA DE USUARIO (HU-01.1):
Como investigador/a, quiero ingresar el identificador NCBI de mi target, su organismo y
los parámetros de corrida, para que el sistema valide que los datos ingresados tienen un
formato válido antes de realizar la búsqueda de la secuencia de referencia.
Criterios de aceptación:
1. Datos válidos → el sistema valida y permite continuar con la consulta de la referencia.
2. Identificador con formato inválido → informa que no cumple el formato y pide corregirlo.
3. Parámetros inválidos → informa CUÁLES parámetros son inválidos y pide corregirlos.
Además, RF-01 pide valores por defecto sugeridos.
```

### Respuesta obtenida

El HTML generado es el archivo [`../../mockups/hu-01-1_nueva-corrida-diseno.html`](../../mockups/hu-01-1_nueva-corrida-diseno.html) (v1, iteración 2).

### Vista previa (capturas de la versión actual)

**Datos válidos**

![Datos válidos](../../mockups/capturas/hu-01-1_nueva-corrida-diseno__1-datos-validos.png)

**Errores de formato (HU-01.1 esc. 2 y 3)**

![Errores de formato (HU-01.1 esc. 2 y 3)](../../mockups/capturas/hu-01-1_nueva-corrida-diseno__2-errores-de-formato.png)

**Supuestos introducidos por la IA a revisar (iteración 1):**

- Rangos válidos de los parámetros (longitud 15–35 nt, %GC 30–70 %, Tm 50–72 °C). **El SRS no los define.**
- Organismos frecuentes como chips (*H. sapiens*, *M. musculus*, *R. norvegicus*, *D. rerio*) + "Otro organismo…". El SRS no dice si el organismo es una lista cerrada.
- Detección del tipo de accession ("RefSeq de ARNm, prefijo NM_") mientras se escribe.
- Parámetros con botones −/+ y una barra que muestra el valor dentro del rango válido.
- Panel "Primer objetivo" (esquema de 20 nt coloreado por G/C) y panel "Próximos pasos" con los 4 pasos siguientes.
- Ilustración "del cromosoma al par de primers": ideograma del cromosoma 17 con la banda 17q21.31, mapa de exones de BRCA1 (hebra −, chr17: 43 044 295 – 43 125 483, GRCh38) y doble hélice con F y R. Las coordenadas son reales, pero el número y la posición de los exones son esquemáticos.
- Atajo de teclado <kbd>Ctrl</kbd>+<kbd>Enter</kbd>.
- Mensaje que interpreta el error ("¿Quisiste poner la temperatura de desnaturalización?") y resumen de errores con enlaces a cada campo.
- Panel "Lo que ya está bien" en el estado de error.

### Iteración 2 del ciclo 1 (30/09) — Interacción con JavaScript y diseño de panel

Antes de correr la evaluación, el grupo cambió dos criterios de generación (ver [`criterios_generacion.md`](../criterios_generacion.md)) y pidió regenerar la maqueta con **Claude Code** sobre la misma base visual:

- **Tecnología:** HTML + CSS + **JavaScript** sin frameworks ni dependencias; el archivo se sigue abriendo con doble clic. El JavaScript va al final del archivo en dos bloques: `interaccion-nucleo` (igual en las cinco pantallas: datos de la corrida entre pantallas, avisos con "Deshacer", atajos de teclado, validaciones compartidas) e `interaccion-pantalla` (el comportamiento propio de esta pantalla). Sin JavaScript, la maqueta se ve como la versión estática.
- **Diseño de panel:** en escritorio la pantalla ocupa exactamente la ventana y no se desplaza; si una columna no entra, se desplaza solo esa columna. En tablet y teléfono se mantiene el desplazamiento normal.

**Qué cambió en esta pantalla:**

- El identificador se valida mientras se escribe: indica el tipo de accession (NM_, NC_, GenBank…) y da un mensaje específico si parece un nombre de gen, si le falta el guion bajo o si le faltan dígitos (HU-01.1 esc. 2).
- Los parámetros se editan escribiendo o con −/+ (mantener apretado repite). Los botones se deshabilitan en los límites del rango y la etiqueta pasa de "sugerido" a "ajustado". Un valor fuera de rango muestra cuál es el problema en el mismo parámetro (HU-01.1 esc. 3).
- El esquema "Primer objetivo" se actualiza con la longitud y el %GC elegidos.
- La barra inferior resume la corrida o, si hay errores, lista los campos a corregir con un enlace a cada uno. El botón indica por qué está deshabilitado.
- "Restablecer sugeridos" y "Cancelar" se pueden deshacer.
- Los datos pasan a UI-2 y se conservan al volver: si UI-2 o UI-3 detectan un problema, UI-1 lo explica arriba y pone el foco en el campo a corregir.
- Panel: identificador y organismo lado a lado; "Próximos pasos" y "Primer objetivo" siempre a la vista. En ventanas de menos de 900 px de alto se oculta la ilustración decorativa.

**Supuestos nuevos a revisar:**

- Aviso al ingresar un cromosoma completo (`NC_`): puede impedir delimitar el gen. Deriva del supuesto de UI-2 sobre CU-02 A1.
- Los casos del botón "Guion demo" (por ejemplo, `NM_999999` → identificador inexistente) son convenciones de la simulación, no reglas del sistema.

> **Al pedir la evaluación:** la pastilla punteada "Estado de la maqueta" y su botón "Guion demo" no son parte de la interfaz. El bloque `<style id="fuentes-embebidas">` (tipografías en base64, ~145 KB) se puede omitir al pegar el HTML.

---

## Ciclo 2 — Evaluación heurística por IA

> Se hace en una **conversación nueva**, con otra IA (Gemini), pegando el HTML completo.

### Prompt utilizado

```text
Asumí el rol de especialista en interfaz de usuario y usabilidad.

Te paso el HTML de una pantalla de "PrimerCraft Pro" (aplicación web para diseñar primers
de PCR/qPCR). Evaluala heurística por heurística según las 10 heurísticas de usabilidad
de Nielsen.

Evaluá pensando en ESTE usuario y ESTE escenario, no en un usuario genérico.
Ignorá la pastilla "Estado de la maqueta" y su botón "Guion demo": no son parte de la
interfaz. La pantalla tiene JavaScript: evaluá también su comportamiento, que está
descrito en los comentarios de los bloques <script>.

PERFIL: <pegar la tabla del perfil de user_profile.md §2>
ESCENARIO: <pegar Escenario A de user_profile.md §3.1>
HISTORIA: <pegar HU-01.1 con sus criterios de aceptación>

Para cada una de las 10 heurísticas indicá:
- Veredicto: CUMPLE / CUMPLE PARCIALMENTE / NO CUMPLE
- Por qué (con referencia al elemento concreto del HTML)
- Si no cumple o cumple parcialmente: hallazgo concreto y sugerencia de mejora.

Numerá los hallazgos (H1, H2, …) para poder referenciarlos.

HTML:
<pegar el contenido de hu-01-1_nueva-corrida-diseno.html, sin el bloque <style id="fuentes-embebidas">>
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
