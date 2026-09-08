---
title: Uso de IA — PrimerCraft Pro
---

# Uso de IA generativa — PrimerCraft Pro

Archivo único, actualizado TP a TP, con una entrada por uso, siguiendo el procedimiento definido por la cátedra (`docs/uso-de-ia.md`). El uso de IA en este TP se limitó a tres funciones de apoyo: **corroborar** datos técnicos puntuales, **elaborar borradores** a partir de decisiones ya tomadas por el grupo, y **sugerir estructuras** de Markdown/Mermaid para ordenar el contenido. El contenido técnico, las decisiones de alcance y la redacción final quedaron a cargo del equipo en todos los casos.

---

### [TP1] Corroboración del planteo del problema

**Herramienta:** Claude
**Tarea:** corroborar si el argumento inicial del grupo sobre el problema a resolver ("hoy se calcula la Tm a mano") era técnicamente sostenible.
**Resultado:** la IA señaló que la afirmación era imprecisa, porque existen herramientas gratuitas de uso extendido (Primer3, NCBI Primer-BLAST) que ya resuelven ese cálculo.
**Modificado/descartado:** el equipo descartó el argumento original y lo reemplazó por uno propio, más ajustado a la realidad: el problema es la fragmentación del flujo entre varias herramientas y la falta de soporte para automatizar el diseño a escala (esto último corroborado contra la documentación pública de NCBI sobre los límites de uso de su API de BLAST).
**Error detectado:** la afirmación sobre el cálculo manual de la Tm.

---

### [TP1] Borrador inicial de la comparación con plataformas existentes

**Herramienta:** Claude
**Tarea:** elaborar un borrador de tabla comparativa de plataformas existentes (Primer3, NCBI Primer-BLAST, IDT PrimerQuest, Thermo OligoPerfect, Benchling, SnapGene/Geneious) como punto de partida para discutir en el grupo.
**Resultado:** un borrador de tabla con motor, fortaleza y punto débil de cada plataforma.
**Modificado/descartado:** el equipo revisó y corrigió el borrador, agregando una observación propia que la IA no había incluido: varias suites pagas (Benchling, Geneious) ya integran diseño, especificidad e historial en un mismo lugar, por lo que la "fragmentación" no es una debilidad universal del mercado sino principalmente de las herramientas gratuitas. También se sumó, por iniciativa del equipo, la idea de diferenciarse cruzando los primers contra bases de datos de variantes poblacionales (dbSNP/Ensembl).
**Error detectado:** ninguno de datos; sí se corrigió una generalización que el equipo consideró injusta con las suites pagas.

---

### [TP1] Estructura Markdown/Mermaid del SRS

**Herramienta:** Claude
**Tarea:** sugerir una estructura de encabezados en Markdown para consolidar el SRS (`docs/requirements/srs.md`) y la sintaxis de Mermaid para el diagrama de contexto (DFD nivel 0) y el modelo de dominio, a partir del contenido ya definido por el grupo.
**Resultado:** una propuesta de organización en ocho secciones y los bloques `mermaid` correspondientes para ambos diagramas.
**Modificado/descartado:** se aceptó la estructura general de secciones; el contenido de cada diagrama (entidades, flujos, relaciones) fue definido por el equipo a partir de su propio entendimiento del dominio.
**Error detectado:** ninguno.

---

### [TP1] Corroboración de la distinción entre requerimientos funcionales y atributos de calidad

**Herramienta:** Claude
**Tarea:** corroborar si el SRS cumplía con el pedido de la cátedra de distinguir con precisión los requerimientos funcionales de los atributos de calidad.
**Resultado:** se identificó que el SRS dejaba los requerimientos funcionales implícitos solo dentro de las historias de usuario, sin un catálogo numerado independiente.
**Modificado/descartado:** el equipo agregó la sección de requerimientos funcionales (RF-01 a RF-05) y decidió cómo mapearlos contra las historias de usuario existentes.
**Error detectado:** una omisión de estructura, no un error de contenido técnico.

---

### [TP1] Corroboración de la estructura de los escenarios de calidad (ISO/IEC 25010)

**Herramienta:** Gemini
**Tarea:** corroborar que las seis dimensiones usadas para redactar los escenarios de calidad del SRS (fuente → estímulo → artefacto → entorno → respuesta → medida) se correspondieran con el modelo de atributos de calidad de la norma ISO/IEC 25010, y que los cuatro atributos elegidos (eficiencia de desempeño, fiabilidad, usabilidad, mantenibilidad) fueran categorías válidas de esa norma.
**Resultado:** confirmó que la estructura de seis dimensiones y los cuatro atributos elegidos son consistentes con ISO/IEC 25010, y sugirió no dejar ningún atributo sin al menos dos escenarios con distinta condición de entorno.
**Modificado/descartado:** el equipo redactó el contenido específico de cada escenario (fuente, estímulo, medida concreta) a partir del propio conocimiento del sistema; de Gemini solo se tomó la confirmación de la estructura, no redacción de contenido.
**Error detectado:** ninguno; sirvió como chequeo de que no faltara ninguna dimensión del escenario antes de darlo por cerrado.

