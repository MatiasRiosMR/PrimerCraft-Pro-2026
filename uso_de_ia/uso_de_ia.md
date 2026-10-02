---
title: Uso de IA — PrimerCraft Pro
---

# Uso de IA generativa — PrimerCraft Pro

| | |
|---|---|
| **Proyecto** | PrimerCraft Pro |
| **Integrantes** | Barbara Sara · Vergara Emilia · Rios Matias |
| **Institución** | Licenciatura en Bioinformática, Facultad de Ingeniería, Universidad Nacional de Entre Ríos (FIUNER) |

Archivo único, actualizado TP a TP, con una entrada por uso, siguiendo el procedimiento definido por la cátedra (`docs/uso-de-ia.md`). El uso de IA en este TP se limitó a tres funciones de apoyo: **corroborar** datos técnicos puntuales, **elaborar borradores** a partir de decisiones ya tomadas por el grupo, y **sugerir estructuras** de Markdown/Mermaid para ordenar el contenido. El contenido técnico, las decisiones de alcance y la redacción final quedaron a cargo del equipo en todos los casos.


---

## [TP1] Corroboración del planteo del problema

| | |
|---|---|
| **Herramienta** | Claude |
| **Tarea** | Corroborar si el argumento inicial del grupo sobre el problema a resolver ("hoy se calcula la Tm a mano") era técnicamente sostenible. |
| **Resultado** | La IA señaló que la afirmación era imprecisa, porque existen herramientas gratuitas de uso extendido (Primer3, NCBI Primer-BLAST) que ya resuelven ese cálculo. |
| **Modificado/descartado** | El equipo descartó el argumento original y lo reemplazó por uno propio, más ajustado a la realidad: el problema es la fragmentación del flujo entre varias herramientas y la falta de soporte para automatizar el diseño a escala (esto último corroborado contra la documentación pública de NCBI sobre los límites de uso de su API de BLAST). |
| **Error detectado** | La afirmación sobre el cálculo manual de la Tm. |

---

## [TP1] Borrador inicial de la comparación con plataformas existentes

| | |
|---|---|
| **Herramienta** | Claude |
| **Tarea** | Elaborar un borrador de tabla comparativa de plataformas existentes (Primer3, NCBI Primer-BLAST, IDT PrimerQuest, Thermo OligoPerfect, Benchling, SnapGene/Geneious) como punto de partida para discutir en el grupo. |
| **Resultado** | Un borrador de tabla con motor, fortaleza y punto débil de cada plataforma. |
| **Modificado/descartado** | El equipo revisó y corrigió el borrador, agregando una observación propia que la IA no había incluido: varias suites pagas (Benchling, Geneious) ya integran diseño, especificidad e historial en un mismo lugar, por lo que la "fragmentación" no es una debilidad universal del mercado sino principalmente de las herramientas gratuitas. También se sumó, por iniciativa del equipo, la idea de diferenciarse cruzando los primers contra bases de datos de variantes poblacionales (dbSNP/Ensembl). |
| **Error detectado** | Ninguno de datos; sí se corrigió una generalización que el equipo consideró injusta con las suites pagas. |

---

## [TP1] Estructura Markdown/Mermaid del SRS

| | |
|---|---|
| **Herramienta** | Claude |
| **Tarea** | Sugerir una estructura de encabezados en Markdown para consolidar el SRS (`docs/requirements/srs.md`) y la sintaxis de Mermaid para el diagrama de contexto (DFD nivel 0) y el modelo de dominio, a partir del contenido ya definido por el grupo. |
| **Resultado** | Una propuesta de organización en ocho secciones y los bloques `mermaid` correspondientes para ambos diagramas. |
| **Modificado/descartado** | Se aceptó la estructura general de secciones; el contenido de cada diagrama (entidades, flujos, relaciones) fue definido por el equipo a partir de su propio entendimiento del dominio. |
| **Error detectado** | Ninguno. |

---


---

## [TP1] Formato de archivos Markdown

| | |
|---|---|
| **Herramienta** | Claude |
| **Tarea** | Dar formato a los archivos Markdown del repositorio (tablas, encabezados, índices), a partir del contenido ya redactado por el equipo. |
| **Resultado** | Archivos reformateados con tablas para los campos estructurados, encabezados consistentes entre documentos, e índices de navegación donde correspondía. |
| **Modificado/descartado** | El contenido y la redacción no se modificaron — solo la presentación. El equipo revisó que el formato no alterara el sentido de lo ya escrito antes de comitear. |
| **Error detectado** | Ninguno. |


---

## [TP1] Chequeo de consistencia de los casos de uso

| | |
|---|---|
| **Herramienta** | Gemini |
| **Tarea** | Revisar los casos de uso (CU-01 a CU-05) redactados por el equipo, chequeando consistencia interna (numeración de RF/HU/CU, cardinalidad de las precondiciones, clasificación de slices alternativos vs. de excepción) y cobertura de escenarios de error no contemplados. |
| **Resultado** | Se detectaron varias inconsistencias: colisión de identificadores entre una versión anterior del SRS y la nueva (RF-01, HU-01 y CU-01 duplicados con contenido distinto); la disponibilidad de la API de NCBI Entrez estaba modelada como precondición en vez de como riesgo gestionable; faltaban slices de excepción para timeout y límite de tasa de NCBI Entrez; varios slices "A" (alternativos) en realidad describían fallos y correspondía clasificarlos como "E" (excepción); un paso de CU-03 incluía por error un fragmento de otro caso de uso en vez de un caso de uso completo (`<<include>>` mal formado). |
| **Modificado/descartado** | El equipo decidió, para cada punto señalado, si corregía el documento o mantenía la redacción original con una justificación propia. La reconciliación final de numeración de RF y la definición de qué caso de uso reemplazaba a cuál quedó a criterio del equipo, no de la IA. |
| **Error detectado** | Los listados en la columna Resultado — en particular, la colisión de IDs entre versiones fue el hallazgo más relevante, porque afectaba la trazabilidad de todo el documento. |

---

## [TP1] Chequeo del diagrama de modelo de dominio (Mermaid)

| | |
|---|---|
| **Herramienta** | Gemini |
| **Tarea** | Revisar el diagrama de clases del modelo de dominio en Mermaid, chequeando sintaxis válida, cardinalidades consistentes con los casos de uso, y correspondencia entre las relaciones del diagrama y el comportamiento descrito en los CU. |
| **Resultado** | Se detectaron errores de sintaxis (typos que generaban clases duplicadas fantasma al renderizar; uso de `<--` en vez de `<|--` para relaciones de generalización, que no dibuja la herencia) y errores de cardinalidad (una relación `1..*` que impedía representar el caso "no se encontraron candidatos" ya descrito en una historia de usuario; una relación que no permitía que un `CandidatoPrimer` existiera sin su par, contradiciendo el caso de uso de validación manual de un primer suelto). |
| **Modificado/descartado** | El equipo aplicó las correcciones de sintaxis y evaluó cada cambio de cardinalidad contra el comportamiento real que querían modelar, antes de aceptarlo. |
| **Error detectado** | Los de sintaxis (typos, símbolo de generalización incorrecto) y los dos de cardinalidad mencionados arriba. |



---

## [TP1] Discusión sobre relaciones `<<include>>` entre casos de uso

| | |
|---|---|
| **Herramienta** | Claude |
| **Tarea** | Consultar si un paso de CU-03 (validar un primer ingresado manualmente), que repetía lógica ya escrita en CU-01, ameritaba modelarse como una relación `<<include>>` directa hacia ese paso puntual. |
| **Resultado** | Se explicó que `<<include>>` en UML/Cockburn solo puede apuntar a un caso de uso completo (con su propio objetivo, flujo y postcondición), nunca a un fragmento o paso suelto de otro caso de uso. Como la lógica de localizar el gen dentro de la secuencia de referencia sí tenía entidad propia y ya se reutilizaba en más de un lugar, se sugirió extraerla como un caso de uso de soporte nuevo (sin actor humano directo), en vez de forzar una inclusión mal formada. |
| **Modificado/descartado** | El equipo aceptó extraer el caso de uso de soporte y lo incorporó al documento, reescribiendo CU-02 y CU-03 para que lo incluyeran correctamente en vez de duplicar la lógica. En una revisión posterior, el equipo reformuló y renumeró estos casos de uso de soporte de manera distinta a la sugerida inicialmente (ver entrada "Ordenamiento y consolidación de un documento reformulado"). |
| **Error detectado** | Una relación `<<include>>` mal formada, que apuntaba a un paso de otro caso de uso en vez de a un caso de uso completo. |

---

## [TP1] Ordenamiento y consolidación de un documento reformulado (canvas, RF y casos de uso)

| | |
|---|---|
| **Herramienta** | Claude |
| **Tarea** | Ordenar y dar formato a una versión nueva y más extensa del canvas de descubrimiento, el catálogo de requerimientos funcionales y los casos de uso (con CU-04 y CU-05 redefinidos respecto de una iteración anterior del documento), para dejarlos listos como archivos separados según la estructura del repositorio (`docs/requirements/srs.md`, `docs/architecture/`). |
| **Resultado** | Los tres documentos reformateados y separados según su ubicación final en el repo. Al ordenar el contenido, se detectó una inconsistencia entre la sección "Elección de Procesos" (que declaraba pospuesto el Proceso 3, dependiente de NCBI BLAST y variantes poblacionales) y el flujo principal de CU-05 (incluido tanto por CU-02 como por CU-03), que sí ejecutaba una verificación de especificidad vía BLAST como parte de su lógica central. |
| **Modificado/descartado** | Se aceptó el ordenamiento y formato propuesto. La inconsistencia detectada quedó señalada para que el equipo la revise y decida cómo reconciliarla; no fue resuelta unilateralmente por la IA. |
| **Error detectado** | La inconsistencia entre la Elección de Procesos y el flujo de CU-05 respecto del alcance real de la verificación por BLAST. |

---

## [TP1] Redacción de mensajes de commit

| | |
|---|---|
| **Herramienta** | Claude |
| **Tarea** | Redactar, en formato Conventional Commits, los mensajes correspondientes a las tareas de entrega repartidas entre las integrantes del equipo (diagramas, modelo de dominio, elección de procesos, casos de uso, actualizaciones del canvas y del catálogo de RF). |
| **Resultado** | Mensajes de commit con tipo, alcance y descripción para cada entrega, además de una advertencia sobre posibles conflictos de merge cuando dos personas editaban el mismo archivo (`docs/requirements/srs.md`) en la misma sesión de trabajo. |
| **Modificado/descartado** | Se completaron a mano los detalles que la IA no podía conocer por sí sola (nombres reales de casos de uso, contenido exacto de documentos externos referenciados). El orden de commiteo y la coordinación entre integrantes quedó a criterio del equipo. |
| **Error detectado** | Ninguno de contenido; se recibieron advertencias preventivas (colisión de numeración entre versiones del SRS, riesgo de conflicto de merge) que el equipo tuvo en cuenta antes de comitear. |
---

## [TP2] Revisión de links y organización de la documentación

| | |
|---|---|
| **Herramienta** | Claude Code |
| **Tarea** | Revisar todos los links a archivos y secciones del repositorio y la organización de la documentación, después de subir las maquetas, el perfil, los criterios y las evaluaciones heurísticas. |
| **Resultado** | Se encontraron rutas que apuntaban a nombres viejos (`perfil-investigador.md`, `criterios-generacion.md`, `docs/ui/…`) y rutas relativas mal armadas hacia las maquetas y capturas. La IA corrigió las rutas, armó índices para `docs/ux/` y `docs/architecture/`, actualizó el README principal y adaptó la portada del sitio, que seguía siendo la plantilla de la cátedra. |
| **Modificado/descartado** | El grupo pidió quitar de las evaluaciones los pedidos al asistente escritos en lenguaje informal, y subir la carpeta de la marca, que faltaba. Cada cambio se commiteó por separado con mensajes revisados por el grupo. |
| **Error detectado** | 36 links rotos en las evaluaciones heurísticas, el perfil y los criterios; una referencia a una carpeta de marca que no existía en el repositorio; una inconsistencia de colores entre la marca y la interfaz. |

---

## [TP2] Preparación de los prompts de evaluación heurística y alineación con el SRS

| | |
|---|---|
| **Herramienta** | Claude Code |
| **Tarea** | Completar los prompts del ciclo 2 (perfil, escenario, historias de usuario y HTML de cada maqueta) para pegarlos en Gemini, y pedir que la respuesta llegue como documento Markdown con una estructura fija. |
| **Resultado** | Cinco prompts listos para pegar, uno por pantalla. Al armarlos, la IA detectó que las evaluaciones citaban escenarios y códigos de casos de uso que ya no coincidían con el SRS: HU-01.1 esc. 3 y HU-04 esc. 3 y 4 se habían quitado el 14/09, y los códigos de CU-02 habían cambiado (A1 → E1 y E1 → E2). |
| **Modificado/descartado** | El grupo decidió que la evaluación la hiciera otra IA (Gemini) en conversaciones nuevas, como establece el método, y no la misma IA que generó la iteración 2 de las maquetas. Se corrigieron las referencias en los textos descriptivos; los prompts del ciclo 1 se dejaron como se enviaron, con una nota que explica cómo se corresponden con el SRS actual. |
| **Error detectado** | Las referencias desactualizadas al SRS. Además, en una sustitución automática la IA cambió mal un código (dejó "sin candidatos" como CU-02 E1); lo detectó en la revisión y lo corrigió a E2. |

---

## [TP2] Evaluación heurística de las cinco pantallas

| | |
|---|---|
| **Herramienta** | Gemini |
| **Tarea** | Evaluar cada maqueta (UI-1 a UI-5) con las 10 heurísticas de Nielsen, en una conversación nueva por pantalla, pensando en el perfil y el escenario del grupo. |
| **Resultado** | Cinco evaluaciones en Markdown con 37 hallazgos en total, cada uno con heurística, severidad (0–4), elemento del HTML, problema y sugerencia. Las respuestas se pegaron sin editar en cada evaluación. |
| **Modificado/descartado** | No se volvió a correr la evaluación para obtener otra respuesta: se conservó la primera, que es la evaluación real. Cada hallazgo se verificó contra el HTML antes de decidir (ver la entrada siguiente). |
| **Error detectado** | 19 de los 37 hallazgos describían problemas que la maqueta no tiene (por ejemplo, decía que "Cancelar corrida" no hace nada, cuando abre un diálogo de confirmación) y 4 eran parcialmente ciertos. Gemini también citó elementos inexistentes (`#input-ncbi`, un botón "Iniciar corrida", el organismo *Arabidopsis*), aunque el prompt indicaba que la pantalla tenía JavaScript. |

---

## [TP2] Verificación de los hallazgos y borrador de la revisión crítica

| | |
|---|---|
| **Herramienta** | Claude Code |
| **Tarea** | Verificar cada hallazgo de Gemini contra el HTML y el JavaScript de su maqueta y proponer, para cada uno, aceptarlo o rechazarlo según el criterio de la evaluación. |
| **Resultado** | Una tabla por pantalla con la verificación y una justificación por hallazgo. Se propuso aceptar 3: avisar demoras de NCBI (UI-2), agregar "Ajustar parámetros" con resultados (UI-3) e informar las condiciones del cálculo de Tm y ΔG (UI-5). El resto se propuso rechazar, por ser incorrecto o por agregar funciones fuera de la HU o del alcance. |
| **Modificado/descartado** | A pedido del grupo, la propuesta se pasó a la sección "Revisión crítica del grupo" de cada evaluación. Las decisiones quedan sujetas a la revisión del grupo antes de la entrega. |
| **Error detectado** | Los de Gemini listados en la entrada anterior. Además, el texto visible de la maqueta UI-3 muestra "(CU-02 E1)" para el estado sin candidatos, que en el SRS es CU-02 E2. Se dejó sin corregir porque el grupo pidió no modificar el código de las maquetas. |

---

## [TP2] Publicación del sitio con GitHub Pages y rediseño

| | |
|---|---|
| **Herramienta** | Claude Code |
| **Tarea** | Publicar la documentación con GitHub Pages, según el instructivo de la cátedra, y rediseñar el sitio con el logo y los colores de la marca. |
| **Resultado** | Sitio publicado desde `main` en `/docs`, con menú lateral por secciones, portada, galería de maquetas, página de identidad visual, textos en español y un visor para ampliar los diagramas. La IA armó el sitio localmente y revisó cada página en el navegador antes del push. |
| **Modificado/descartado** | El grupo pidió un diseño más moderno, con el logo y los colores de la marca. Los colores de los nodos de los diagramas se ajustan solo en el sitio; el código Mermaid de los documentos conserva sus colores. |
| **Error detectado** | El modelo de dominio no se dibujaba ("Syntax error") por una línea `---` repetida y por clases vacías escritas `class X {}`. Se corrigió sin cambiar clases ni relaciones. Los diagramas grandes se veían demasiado chicos para leerse. La configuración de `_config.yml` copiada del instructivo (`theme: just-the-docs`) no funciona en GitHub Pages y se reemplazó por `remote_theme`. En la portada, la IA usó al principio una secuencia de ejemplo cuyo reverse era el complemento del forward, que no es un par de primers válido; se reemplazó por un motivo gráfico. |

---

## [TP2] Redacción de mensajes de commit

| | |
|---|---|
| **Herramienta** | Claude Code |
| **Tarea** | Redactar los mensajes de commit, en el formato que ya usa el repositorio, para cada grupo de cambios de esta etapa. |
| **Resultado** | Un mensaje por cambio, con los archivos de cada uno separados para commitearlos de a uno. |
| **Modificado/descartado** | Los commits los hizo el grupo, en el orden que eligió. |
| **Error detectado** | Ninguno. |
