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