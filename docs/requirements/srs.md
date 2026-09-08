# SRS — PrimerCraft Pro

**Especificación de Requerimientos del Software**
Ingeniería de Software 2026 · FIUNER · TP1 — Instancia 1

| | |
|---|---|
| **Proyecto** | PrimerCraft Pro |
| **Integrantes** | Sara Barbará, Emilia Vergara, Matias Rios |
| **Versión del documento** | 1.0.0 (línea base TP1) |


---

## 1. Introducción

### 1.1 Propósito

Este documento especifica los requerimientos de PrimerCraft Pro para la primera iteración del proyecto (TP1). Consolida la visión y el alcance surgidos de la actividad de descubrimiento, el contexto del sistema, el modelo de dominio conceptual, los requerimientos funcionales, los casos de uso e historias de usuario de los procesos elegidos para desarrollar en profundidad, y los atributos de calidad según ISO/IEC 25010.

### 1.2 Propuesta

PrimerCraft Pro diseña, puntúa y valida primers para PCR/qPCR en un flujo único e integrado, teniendo enc uenta información que se encuentra presente en bases y motores que ya usa la comunidad (NCBI Entrez, NCBI BLAST, dbSNP/Ensembl). No reemplaza la termodinámica ni la lógica del diseño existente, sino que **cierra los huecos de las herramientas actuales**: la fragmentación entre pestañas, la falta de claridad en como se descompone el scoring (funciona como caja engra en al que solo se expone la métrica) y la falta de trazabilidad de las decisiones de diseño.

### 1.3 Definiciones, acrónimos y abreviaturas

| Término | Definición |
|---|---|
| **Primer** | Oligonucleótido corto que sirve de punto de inicio para la síntesis de ADN en una PCR. |
| **Par de primers** | Primer forward + primer reverse que delimitan la región a amplificar. |
| **Tm** | Temperatura de melting del primer. |
| **%GC** | Proporción de bases G y C en la secuencia. |
| **GC clamp** | Presencia de G o C en el extremo 3' del primer, que favorece un anclaje estable. |
| **Estructura secundaria** | Plegamiento no deseado: horquilla (hairpin) intramolecular, homodímero o heterodímero entre primers. |
| **ΔG** | Energía libre de Gibbs asociada a una estructura secundaria; más negativa = estructura más estable = más probable que los primers hibriden entre sí = más problemática. |
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


---

## 2. Visión y alcance



### 2.1 Área de dolencia u oportunidad

El área elegida es el **diseño de primers para PCR/qPCR** en laboratorios de biología molecular. Hoy el diseño de un solo par de primers exige alternar entre múltiples sitios e interfaces (NCBI para traer y descargar el FASTA a mano, Primer3 o Primer-BLAST para el diseño, una planilla propia para documentar el criterio), y ese copiar y pegar entre pestañas no escala cuando hay que diseñar primers para varios targets a la vez (un panel de diagnóstico multiplex, un panel de vigilancia, un genotipado de varios genes).

La propia NCBI advierte en su documentación que su BLAST público es un recurso compartido pensado para uso interactivo, con límites estrictos para quien quiera automatizarlo; no hay hoy una alternativa gratuita y simple para diseñar primers en lote respetando esos límites.

### 2.2 Dominio y problema

**Problema real:** el diseño de primers está fragmentado entre herramientas, no se puede automatizar en lote de forma gratuita y respetando los límites de uso, y el criterio de puntaje de las herramientas existentes es una **caja negra** que además no queda registrada de forma versionada.

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
| **Bioinformático/a** | Stakeholder directo | Necesita poder integrar esta herramienta en su pipeline de análisis, puede actuar como investigador tambien pero ademas necesita poder utilizar el sistema como ingresa secuencia target y sale primers. |


> No hay "perfiles" de usuario distintos por tipo de PCR: el sistema es el mismo para cualquier investigador, y el tipo de ensayo (PCR simple, qPCR, panel) es un **parámetro de la corrida**, no un rol de usuario distinto.

### 2.5 Valor

Si el sistema funciona:

- Bajan los **fallos experimentales** en PCR/qPCR causados por un mal diseño de primer.
- Se ahorran **reactivos**: menos oligonucleótidos sintetizados que terminan sin usarse porque fallan.
- El diseño pasa de **horas de cálculo manual** a **segundos de sugerencia automática**.
- Queda un registro **trazable y reproducible** de qué criterios se usaron para elegir cada par de primers — útil tanto para una publicación como para una auditoría interna del laboratorio.
- El investigador puede diseñar **paneles completos en lote** en vez de repetir el proceso target por target.


### 2.6 Alcance realista en el marco de la materia

**Incluido:**

- Cargar / ingresar un target o lista de ellos (identificador de gen/región o secuencia FASTA propia, con validación de caracteres IUPAC).
- Traer la secuencia de referencia por API (NCBI Entrez).
- Calcular propiedades termodinámicas reales: Tm por Nearest-Neighbor, %GC, GC clamp en el extremo 3', penalización por repeticiones.
- Chequear estructuras secundarias básicas (horquillas y dímeros) calculando su ΔG.
- Verificar especificidad contra el genoma (NCBI BLAST), respetando los límites de uso públicos mediante cola y aviso de espera.
- Simular el amplicón in silico de forma básica (secuencia teórica y tamaño esperado en pb).
- Diseñar primers **en lote** para una lista de targets (panel), vía la API propia de PrimerCraft Pro.
- Validar un primer ya diseñado (ingresado manualmente) y devolver sus métricas, especificidad y exposición a variantes.

**Fuera de alcance:**

| Fuera de alcance | Motivo |
|---|---|
| Integración *en vivo* con la API de NCBI BLAST | Manejar bien sus límites de uso lleva tiempo; en el MVP se usa una simulación local (mock) documentada. |
| Módulo de aprendizaje | Definir una función de scoring que involucre aprendizaje llevaría un trabajo extra que podría comprometer los tiempos actuales. |
| Diseño de sondas fluorescentes TaqMan para qPCR | Fuera del núcleo de valor de la primera iteración. |
| Diseño en lote de paneles grandes con retroalimentación de laboratorio real | Requiere modelar el historial de corridas y un circuito de aprendizaje. |
| Perfiles de scoring pre-armados (exploratorio / qPCR / diagnóstico) | El MVP fija un único perfil por defecto con pesos ajustables. |
| Explicación del resultado en lenguaje natural | Extensión posterior. |
| Aviso de superposición entre primers de distintos ensayos del mismo laboratorio | Extensión posterior. |
| Registro versionado de parámetros, umbrales y versión de datos de variantes por corrida | Extensión posterior. |
| Scoring desglosado y configurable (puntuación y sugerencia automática de mejores pares) | Extensión posterior. |
| Cruce de la región de anclaje contra variantes poblacionales (dbSNP/Ensembl) | *(Nota: el canvas original lo marca como "se prioriza dentro del MVP" — pendiente de que el equipo lo reconcilie contra esta tabla, que lo lista como fuera de alcance).* |



### 2.7 Riesgos de fracaso y mitigación


**Mitigación:** el MVP fija el scoring por defecto con **pesos documentados y ajustables** (no fijos en el código), y valida el criterio de variantes con un caso de uso concreto y acotado (una sola fuente —dbSNP *o* Ensembl, no ambas desde el inicio) antes de sumar más complejidad.

**Riesgo secundario — incertidumbre al inicio:** no está claro cuánto valor real agrega el cruce con variantes poblacionales frente al costo de implementarlo bien (un falso positivo en la alerta de riesgo podría generar desconfianza en la herramienta). Se mitiga acotando ese cruce a una sola fuente y un caso de uso puntual en la primera iteración.

**Riesgo técnico — dependencia de servicio externo:** la API pública de NCBI BLAST es un punto de falla que el grupo no controla. Se mantiene documentación local como respaldo, y la integración real recién se hace en TP3.

### 2.8 Datos sensibles y ética profesional

El sistema, en su alcance actual, maneja **únicamente datos biológicos públicos** (secuencias de referencia y variantes poblacionales agregadas): **no hay datos personales identificables ni vinculables a pacientes**.

---

## 3. Requerimientos funcionales

| RF | Descripción |
|---|---|
| **RF-01** | El sistema debe permitir al investigador ingresar un identificador de gen/región o una secuencia propia, junto con parámetros de diseño (Tm objetivo, %GC, tamaño de primers), con valores por defecto sugeridos. |
| **RF-02** | El sistema debe permitir al investigador ingresar una lista de identificadores de gen/región o secuencias propias, junto con parámetros de diseño, con valores por defecto sugeridos. |
| **RF-03** | El sistema debe consultar la API de NCBI Entrez y obtener la secuencia FASTA correspondiente al target ingresado, sin intervención manual del usuario. |
| **RF-04** | El sistema debe generar candidatos de primers forward/reverse y calcular su termodinámica (Tm, %GC) según el modelo Nearest-Neighbor (SantaLucia 1998). |
| **RF-05** | El sistema debe evaluar cada candidato en busca de horquillas (hairpins) y dímeros, tanto internos como entre el par forward/reverse. |
| **RF-06** | El sistema debe consultar NCBI BLAST para cada candidato y determinar su especificidad contra el genoma completo, respetando el límite de uso público (100 corridas/24hs) mediante cola y aviso de espera al usuario. |
| **RF-07** | El sistema debe generar una simulación del amplicón resultante para cada par de primers sugerido. |
| **RF-08** | El sistema debe permitir al usuario ingresar una secuencia de primer ya existente y devolver sus métricas, especificidad y exposición a variantes, sin necesidad de haber sido diseñado por el sistema. |
| **RF-09** | Ante un identificador de gen/región inexistente en NCBI, el sistema debe informar el error y solicitar al investigador que lo verifique. |
| **RF-10** | Ante un gen target de interés, el sistema debe localizar información específica desde la anotación del genoma de referencia (coordenadas de inicio y fin, hebra, etc.). |
---

## 6. Elección del modelo de procesos

Para el desarrollo prioritario en lo que resta del cuatrimestre se seleccionaron el **Proceso 1 (Preparar target y secuencia de referencia)** y el **Proceso 2 (Generar y caracterizar candidatos de primers)**.

Esta elección se fundamenta en que el Proceso 1 establece la puerta de entrada indispensable del sistema, resolviendo la validación de los datos ingresados y la obtención de la secuencia mediante la API de NCBI Entrez. Por su parte, el Proceso 2 representa el verdadero motor algorítmico del proyecto, ya que ejecuta de manera completamente local la lógica de diseño por ventana deslizante, el cálculo de propiedades termodinámicas como la Tm por Nearest-Neighbor y la evaluación de estructuras secundarias mediante ΔG, garantizando un alto valor del dominio y desarrollo técnico sin depender de limitaciones externas.

En contraste, se decidió no priorizar el **Proceso 3** debido a su fuerte dependencia de servicios de terceros como NCBI BLAST y bases de variantes poblacionales, sujetos a restricciones de cuota y tiempos de respuesta que es preferible gestionar mediante simulaciones (mocks) en las primeras entregas. La profundización del **Proceso 4** se postergó para una etapa posterior, ya que su función principal es aplicar el esquema de scoring y orquestar el ciclo de reintentos basándose en los resultados de especificidad y variantes que genera el Proceso 3, lo que hace indispensable tener consolidadas las etapas previas antes de abordar su lógica completa.

---
