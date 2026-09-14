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

## Índice de entradas

| TP | Entrada | Herramienta |
|---|---|---|
| TP1 | [Corroboración del planteo del problema](#tp1-corroboración-del-planteo-del-problema) | Claude |
| TP1 | [Borrador inicial de la comparación con plataformas existentes](#tp1-borrador-inicial-de-la-comparación-con-plataformas-existentes) | Claude |
| TP1 | [Estructura Markdown/Mermaid del SRS](#tp1-estructura-markdownmermaid-del-srs) | Claude |
| TP1 | [Corroboración de RF vs. atributos de calidad](#tp1-corroboración-de-la-distinción-entre-requerimientos-funcionales-y-atributos-de-calidad) | Claude |
| TP1 | [Corroboración de escenarios de calidad ISO/IEC 25010](#tp1-corroboración-de-la-estructura-de-los-escenarios-de-calidad-isoiec-25010) | Gemini |

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

## [TP1] Corroboración de la distinción entre requerimientos funcionales y atributos de calidad

| | |
|---|---|
| **Herramienta** | Claude |
| **Tarea** | Corroborar si el SRS cumplía con el pedido de la cátedra de distinguir con precisión los requerimientos funcionales de los atributos de calidad. |
| **Resultado** | Se identificó que el SRS dejaba los requerimientos funcionales implícitos solo dentro de las historias de usuario, sin un catálogo numerado independiente. |
| **Modificado/descartado** | El equipo agregó la sección de requerimientos funcionales (RF-01 a RF-05) y decidió cómo mapearlos contra las historias de usuario existentes. |
| **Error detectado** | Una omisión de estructura, no un error de contenido técnico. |



---

## [TP1] Formato de archivos Markdown

| | |
|---|---|
| **Herramienta** | Claude |
| **Tarea** | Dar formato a los archivos Markdown del repositorio (tablas, encabezados, índices), a partir del contenido ya redactado por el equipo. |
| **Resultado** | Archivos reformateados con tablas para los campos estructurados, encabezados consistentes entre documentos, e índices de navegación donde correspondía. |
| **Modificado/descartado** | El contenido y la redacción no se modificaron — solo la presentación. El equipo revisó que el formato no alterara el sentido de lo ya escrito antes de comitear. |
| **Error detectado** | Ninguno. |