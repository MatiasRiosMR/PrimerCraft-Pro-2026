# SRS — PrimerCraft Pro

**Especificación de Requerimientos del Software**
Ingeniería de Software 2026 · FIUNER · TP1 — Instancia 1

| | |
|---|---|
| **Proyecto** | PrimerCraft Pro |
| **Integrantes** | Sara Barbará, Emilia Vergara, Matias Rios |
| **Versión del documento** | 1.0.0 (línea base TP1) |
| **Estado** | En revisión para presentación 01/09 |

---

## 1. Introducción

### 1.1 Propósito

Este documento especifica los requerimientos de PrimerCraft Pro para la primera iteración del proyecto (TP1). Consolida la visión y el alcance surgidos de la actividad de descubrimiento, el contexto del sistema, el modelo de dominio conceptual, los requerimientos funcionales, los casos de uso e historias de usuario de los procesos elegidos para desarrollar en profundidad, y los atributos de calidad según ISO/IEC 25010.

### 1.2 Alcance del producto

PrimerCraft Pro diseña, puntúa y valida primers para PCR/qPCR en un flujo único e integrado, conectándose por API a las bases y motores que ya usa la comunidad (NCBI Entrez, NCBI BLAST, dbSNP/Ensembl). No reemplaza la termodinámica de diseño existente (Primer3, Nearest-Neighbor / SantaLucia 1998), sino que **cierra los huecos de las herramientas actuales**: la fragmentación entre pestañas, la falta de automatización en lote, la opacidad del criterio de puntaje y la falta de trazabilidad de las decisiones de diseño.

### 1.3 Definiciones, acrónimos y abreviaturas

| Término | Definición |
|---|---|
| **Primer** | Oligonucleótido corto que sirve de punto de inicio para la síntesis de ADN en una PCR. |
| **Par de primers** | Primer forward + primer reverse que delimitan la región a amplificar. |
| **Tm** | Temperatura de fusión (melting temperature) del primer. |
| **%GC** | Proporción de bases G y C en la secuencia. |
| **GC clamp** | Presencia de G o C en el extremo 3' del primer, que favorece un anclaje estable. |
| **Estructura secundaria** | Plegamiento no deseado: horquilla (hairpin) intramolecular, homodímero o heterodímero entre primers. |
| **ΔG** | Energía libre de Gibbs asociada a una estructura secundaria; más negativa = estructura más estable = más problemática. |
| **Amplicón** | Fragmento de ADN resultante de la amplificación por PCR. |
| **Especificidad** | Grado en que el primer se une únicamente a la región blanco y no a otras regiones del genoma. |
| **SNP** | Polimorfismo de un solo nucleótido (variante puntual en la población). |
| **Región de anclaje** | Zona del genoma donde hibrida el primer; una variante allí, sobre todo en el extremo 3', puede provocar el fallo de la PCR. |
| **Nearest-Neighbor** | Modelo termodinámico para calcular la Tm considerando pares de bases adyacentes (SantaLucia 1998). |
| **IUPAC** | Código de nucleótidos ambiguos (A, C, G, T, más R, Y, N, etc.). |
| **FASTA** | Formato de texto para secuencias biológicas. |
| **VCF** | Variant Call Format; estándar de dbSNP/Ensembl para representar variantes con posición y frecuencia. |
| **NCBI Entrez (E-utilities)** | API pública de NCBI para recuperar secuencias y metadatos. |
| **NCBI BLAST (Common URL API)** | API pública de NCBI para búsquedas de similitud de secuencias; recurso compartido con límites de uso. |
| **dbSNP / Ensembl** | Bases de datos públicas de variantes genéticas poblacionales. |
| **RF / RNF** | Requerimiento Funcional / Requerimiento No Funcional. |
| **CU / HU** | Caso de Uso / Historia de Usuario. |
| **GWT** | Given-When-Then; formato de criterios de aceptación. |
| **SRS** | Software Requirements Specification. |

### 1.4 Referencias

- Guía de TP1 — Ingeniería de Software 2026, FIUNER.
- Instructivo de cátedra: Diagrama de Flujo de Datos (DFD) — Contexto y Niveles.
- Cockburn, A. *Writing Effective Use Cases* (2000), cap. 1–3.
- Jacobson, I. et al. *Use Case 2.0* (2011) — marco de slices.
- SantaLucia, J. (1998) — parámetros termodinámicos Nearest-Neighbor.
- ISO/IEC 25010 — modelo de calidad del producto de software.
- NCBI — política de uso de las E-utilities y de la Common URL API de BLAST.

---

## 2. Visión y alcance

*(Esta sección proviene del canvas de descubrimiento — Semana 2 — y es la instancia formal de selección y validación del proyecto para todo el cuatrimestre.)*

### 2.1 Área de dolencia u oportunidad

El área elegida es el **diseño de primers para PCR/qPCR** en laboratorios de biología molecular. Hoy el diseño de un solo par de primers exige alternar entre múltiples sitios e interfaces (NCBI para traer y descargar el FASTA a mano, Primer3 o Primer-BLAST para el diseño, una planilla propia para documentar el criterio), y ese copiar y pegar entre pestañas no escala cuando hay que diseñar primers para varios targets a la vez (un panel de diagnóstico multiplex, un panel de vigilancia, un genotipado de varios genes).

La propia NCBI advierte en su documentación que su BLAST público es un recurso compartido pensado para uso interactivo, con límites estrictos para quien quiera automatizarlo; no hay hoy una alternativa gratuita y simple para diseñar primers en lote respetando esos límites.

### 2.2 Dominio y problema

**Problema real:** el diseño de primers está fragmentado entre herramientas, no se puede automatizar en lote de forma gratuita y respetuosa de los límites de uso, y el criterio de puntaje de las herramientas existentes es una **caja negra** que además no queda registrada de forma versionada.

**Quién lo sufre hoy:** laboratorios chicos y grupos de investigación sin presupuesto para suites pagas integradas (Benchling, Geneious), y en general cualquier investigador que deba diseñar primers para varios targets.

**Cómo se resuelve actualmente:** saltando entre pestañas (NCBI → Primer3/Primer-BLAST → planilla propia), o pagando herramientas comerciales que tampoco resuelven todo (no consideran variantes poblacionales, no exponen el criterio de scoring).

### 2.3 Datos que maneja el sistema

Datos biológicos **públicos**, sin información de pacientes:

| Dato | Origen | Formato |
|---|---|---|
| Secuencia de referencia del target | NCBI Entrez (E-utilities) | FASTA |
| Anotación de genes (ubicar el target dentro del gen) | NCBI / GenBank | GFF / GenBank |
| Variantes poblacionales (SNPs, frecuencia alélica) | dbSNP, Ensembl | VCF |
| Parámetros termodinámicos de referencia | Tablas Nearest-Neighbor (SantaLucia 1998) | Constantes del sistema |
| Parámetros de diseño (Tm objetivo, %GC, tamaño de amplicón) | Ingresados por el usuario, con valores por defecto | — |
| Resultado de especificidad | NCBI BLAST (Common URL API) | Reporte BLAST |

### 2.4 Usuarios y stakeholders

| Rol | Tipo | Por qué le importa el sistema |
|---|---|---|
| **Investigador/a de biología molecular** | Usuario principal / actor primario | Diseña primers para sus propios experimentos. Quiere pasar de horas de cálculo manual y copia-pega a una sugerencia automática en segundos, con la seguridad de un diseño robusto. |
| **Docente / director/a de laboratorio** | Stakeholder indirecto | Tiene que confiar en que el criterio de diseño usado fue riguroso y poder auditarlo; el diseño lo aprueba él/ella antes de comprar la síntesis. |
| **Bioinformático/a de soporte** | Stakeholder indirecto | Necesita que el resultado se pueda exportar e integrar a un análisis o pipeline más grande (formatos estándar: FASTA, CSV, VCF). |
| **Laboratorio de síntesis de oligonucleótidos** | Stakeholder indirecto | Recibe la secuencia final y necesita que no tenga ambigüedades ni errores de transcripción. |
| **Cátedra de Ingeniería de Software (FIUNER)** | Stakeholder del contexto académico | El proyecto se construye como trabajo de la materia; evalúa el proceso, no solo el producto. |

> No hay "perfiles" de usuario distintos por tipo de PCR: el sistema es el mismo para cualquier investigador, y el tipo de ensayo (PCR simple, qPCR, panel) es un **parámetro de la corrida**, no un rol de usuario distinto.

### 2.5 Valor

Si el sistema funciona:

- Bajan los **fallos experimentales** en PCR/qPCR causados por un mal diseño de primer.
- Se ahorran **reactivos**: menos oligonucleótidos sintetizados que terminan sin usarse porque fallan.
- El diseño pasa de **horas de cálculo manual** a **segundos de sugerencia automática**.
- Queda un registro **trazable y reproducible** de qué criterios se usaron para elegir cada par de primers — útil tanto para una publicación como para una auditoría interna del laboratorio.
- El investigador puede diseñar **paneles completos en lote** en vez de repetir el proceso target por target.

### 2.6 Alcance realista

**Lo mínimo que ya demuestra el valor central (MVP del cuatrimestre):**

- Cargar / ingresar un target (identificador de gen/región o secuencia FASTA propia, con validación de caracteres IUPAC).
- Traer la secuencia de referencia por API (NCBI Entrez).
- Calcular propiedades termodinámicas reales: Tm por Nearest-Neighbor, %GC, GC clamp en el extremo 3', penalización por repeticiones.
- Chequear estructuras secundarias básicas (horquillas y dímeros) calculando su ΔG.
- Verificar especificidad contra el genoma (NCBI BLAST), respetando los límites de uso públicos mediante cola y aviso de espera.
- Cruzar la región de anclaje contra variantes poblacionales conocidas (dbSNP/Ensembl) — **este cruce es el diferencial frente al resto del mercado, así que se prioriza dentro del MVP**.
- Puntuar y sugerir automáticamente los mejores pares Forward/Reverse, con **scoring desglosado y configurable**.
- Simular el amplicón in silico de forma básica (secuencia teórica y tamaño esperado en pb).
- Diseñar primers **en lote** para una lista de targets (panel), vía la API propia de PrimerCraft Pro.
- Validar un primer ya diseñado (ingresado manualmente) y devolver sus métricas, especificidad y exposición a variantes.
- Registrar de forma versionada los parámetros, umbrales y versión de datos de variantes usados en cada corrida.

**Lo que queda deliberadamente afuera:**

| Fuera de alcance | Motivo |
|---|---|
| Integración *en vivo* con la API de NCBI BLAST | Manejar bien sus límites de uso lleva tiempo; en el MVP se usa una simulación local (mock) documentada. La integración real llega en TP3. |
| Módulo de diseño de Multiplex PCR | Complejidad alta; candidato para el Trabajo Integrador. |
| Diseño de sondas fluorescentes TaqMan para qPCR | Fuera del núcleo de valor de la primera iteración. |
| Diseño en lote de paneles grandes con retroalimentación de laboratorio real (CU-04) | Requiere modelar el historial de corridas y un circuito de aprendizaje; candidato para TP3 en adelante. |
| Perfiles de scoring pre-armados (exploratorio / qPCR / diagnóstico) | Extensión posterior; el MVP fija un único perfil por defecto con pesos ajustables. |
| Explicación del resultado en lenguaje natural | Extensión posterior. |
| Aviso de superposición entre primers de distintos ensayos del mismo laboratorio | Extensión posterior. |
| Modo "para aprender" (mostrar el cálculo intermedio de Tm/ΔG paso a paso) | Extensión posterior; diferencial académico, no de valor central. |

### 2.7 Riesgos de fracaso y mitigación

De los problemas típicos de requerimientos (visión poco clara de los stakeholders, incertidumbre al inicio, cambio de requerimientos, negociación entre stakeholders con intereses distintos), el más probable en este proyecto es:

**Negociación de requerimientos entre stakeholders con intereses distintos.** El investigador quiere rapidez y automatización; el director/a de laboratorio quiere rigurosidad y trazabilidad auditable. Esa tensión tira del diseño del scoring: ¿cuánto se automatiza vs. cuánto queda a criterio manual del director?

**Mitigación:** el MVP fija el scoring por defecto con **pesos documentados y ajustables** (no fijos en el código), y valida el criterio de variantes con un caso de uso concreto y acotado (una sola fuente —dbSNP *o* Ensembl, no ambas desde el inicio) antes de sumar más complejidad.

**Riesgo secundario — incertidumbre al inicio:** no está claro cuánto valor real agrega el cruce con variantes poblacionales frente al costo de implementarlo bien (un falso positivo en la alerta de riesgo podría generar desconfianza en la herramienta). Se mitiga acotando ese cruce a una sola fuente y un caso de uso puntual en la primera iteración.

**Riesgo técnico — dependencia de servicio externo:** la API pública de NCBI BLAST es un punto de falla que el grupo no controla. Se mantiene un mock local documentado como respaldo, y la integración real recién se hace en TP3.

### 2.8 Datos sensibles y ética profesional

El sistema, en su alcance actual, maneja **únicamente datos biológicos públicos** (secuencias de referencia y variantes poblacionales agregadas): **no hay datos personales identificables ni vinculables a pacientes**.

No obstante, el Código de Ética IEEE/ACM exige proteger la privacidad de los usuarios como parte del interés público. Si en algún momento el sistema llegara a manejar datos vinculables a personas (por ejemplo, en un contexto de diagnóstico clínico), habría que revisar esta sección antes de sumar esa funcionalidad: minimización de datos, consentimiento, control de acceso y confidencialidad del almacenamiento pasan a ser requerimientos de primera clase. Se deja escrito desde ahora, aunque el sistema no se implemente todavía.

---