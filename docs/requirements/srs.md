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
## 7. Casos de uso / Historias de usuario

### Actores

- **Primario:** Investigador/a (biólogo/a molecular que diseña primers para su propio experimento).
- **Secundarios (sistemas externos):** NCBI Entrez / BLAST.

---

### CU-01 · Preparar target y secuencia de referencia

- **Actor:** Investigador/a
- **Objetivo:** Validar la información de entrada de un target.
- **RF que realiza:** RF-01, RF-02
- **Precondición:** El sistema está disponible para que el investigador/a genere una corrida de diseño.

**Flujo principal:**

**Slice 1:**
1. El Investigador/a selecciona la opción de iniciar una nueva corrida de diseño.
2. El Investigador/a ingresa el identificador NCBI del target, el organismo de interés y los parámetros de corrida (longitud del primer, %GC y Tm objetivo).
3. El sistema valida que los campos de entrada cumplan con el formato esperado.

**Slice 2:** → `<<include>>` CU-04

**Postcondición:** La secuencia de referencia, la anotación y los parámetros de corrida quedan validados y disponibles para que el Proceso 2 los tome como entrada.

**Slices secundarios nombrados:**
- **A1:** Carga masiva mediante archivo `.txt` con lista de identificadores (RF-02).
- **E1:** Identificador NCBI inexistente o no encontrado en NCBI Entrez (RF-09).
- **E2:** Incompatibilidad entre el identificador NCBI y el organismo ingresado.
- **E3:** Parámetros de corrida fuera de los rangos válidos.

#### HU-01.1 · Iniciar diseño individual de primers

*Deriva de: CU-01, Slice 1.*

> **Como** investigador/a, **quiero** ingresar el identificador NCBI de mi target, su organismo y los parámetros de corrida, **para** que el sistema valide que los datos ingresados tienen un formato válido antes de realizar la búsqueda de la secuencia de referencia.

```gherkin
Escenario: Datos de entrada válidos
  Given que el investigador/a seleccionó la opción de iniciar una nueva corrida de diseño
  When ingresa un identificador NCBI (NM_007294), un organismo y parámetros de corrida con formato válido (Tm 60°C, %GC 50%, longitud 20 nt)
  Then el sistema valida correctamente los datos y permite continuar con la consulta de la referencia

Escenario: Identificador con formato inválido
  Given que el investigador/a se encuentra ingresando los datos de una nueva corrida
  When ingresa un identificador NCBI cuyo formato no es válido
  Then el sistema informa que el identificador ingresado no cumple con el formato esperado y solicita su corrección

Escenario: Parámetros de corrida inválidos
  Given que el investigador/a ingresó un identificador NCBI y un organismo
  When uno o más parámetros de corrida no cumplen con los rangos o formatos establecidos
  Then el sistema informa cuáles parámetros son inválidos y solicita su corrección antes de continuar

Escenario: Datos válidos habilitan la consulta
  Given que todos los datos ingresados cumplen con las validaciones establecidas
  When el sistema finaliza la validación
  Then los datos quedan disponibles para realizar la consulta de la secuencia de referencia en NCBI Entrez
```

---

### CU-02 · Generar y caracterizar candidatos de primers

- **Actor:** Investigador/a (interacción indirecta — se dispara automáticamente al finalizar CU-01, sin una acción nueva del usuario).
- **Objetivo:** Generar pares de primers candidatos que cumplan los parámetros de diseño y caracterizarlos termodinámicamente, dejándolos listos para la verificación de especificidad y variantes.
- **RF que realiza:** RF-10
- **Precondición:** CU-01 finalizó exitosamente; el sistema cuenta con la secuencia de referencia, su anotación y los parámetros de corrida.

**Flujo principal:**

**Slice 1:**
1. El sistema localiza el gen objetivo dentro de la anotación del genoma de referencia, utilizando su identificador o nombre.
2. El sistema obtiene las coordenadas de inicio y fin de la región génica.
3. El sistema determina la hebra en la que se codifica.

**Slice 2:** → `<<include>>` CU-05

**Postcondición:** Existe un conjunto de candidatos de primers caracterizados (con métricas termodinámicas, estructuras secundarias y amplicón simulado), listo para la verificación de especificidad.

**Slices secundarios nombrados:**
- **A1:** No se encuentra ninguna coincidencia del gen en la anotación (localización fallida).
- **E1:** Ningún candidato generado cumple simultáneamente todos los parámetros de diseño dentro de la región del gen.

#### HU-02.1 · Localización del gen objetivo

*Deriva de: CU-02, Slice 1.*

> **Como** investigador/a, **quiero** que el sistema localice automáticamente el gen objetivo dentro de la secuencia de referencia y determine la hebra en la que se encuentra codificado, **para** asegurar que la generación de primers se realice sobre la región correcta del gen.

```gherkin
Escenario: Localización exitosa del gen
  Given que el sistema dispone de la secuencia de referencia y su anotación obtenidas en CU-01
  When busca el gen objetivo utilizando su identificador o nombre
  Then el sistema localiza correctamente el gen dentro del genoma de referencia

Escenario: Determinación de coordenadas
  Given que el sistema localizó correctamente el gen objetivo
  When consulta la información correspondiente en la anotación
  Then obtiene y registra las coordenadas de inicio y fin de la región del gen

Escenario: Determinación de la hebra
  Given que el sistema identificó las coordenadas del gen
  When analiza la información de la anotación
  Then determina correctamente la hebra en la que se encuentra codificado el gen
```

---
### CU-03 · Validar un primer ingresado manualmente

- **Actor:** Investigador/a
- **Objetivo:** Verificar que un par de primers ya diseñado por otro medio hibride correctamente en el target de interés y obtener sus métricas, sin pasar por la generación automática de candidatos.
- **RF que realiza:** RF-08
- **Precondición:** El investigador/a cuenta con una secuencia de primer (o par forward/reverse) ya diseñada, y el sistema está disponible para generar una corrida de validación.
- **Relaciones con otros casos de uso:**
  - `<<include>>` CU-01 — para validar el identificador de target/organismo y obtener la secuencia de referencia y anotación.
  - `<<include>>` CU-04 — para localizar el gen dentro de la secuencia de referencia.

**Flujo principal:**

**Slice 1 — Ingreso y validación del primer:**
1. El investigador/a selecciona la opción de validar un primer existente.
2. El investigador/a ingresa las secuencias forward/reverse, el organismo y el identificador del target.
3. El sistema valida que los datos de entrada cumplan con el formato requerido.

**Slice 2 — Localización del gen:**
1. `<<include>>` CU-04 — el sistema valida el target y obtiene la secuencia de referencia y su anotación.
2. El sistema localiza el gen objetivo y obtiene sus coordenadas y hebra.

**Slice 3 — Verificación de hibridación y caracterización:**
1. El sistema ubica las secuencias de los primers dentro de la región del gen.
2. El sistema verifica que hibriden en las posiciones y orientaciones esperadas.
3. `<<include>>` CU-05 — el sistema caracteriza el par de primers.

**Postcondición:** Existe un primer validado, con sus métricas termodinámicas y estructurales calculadas, disponible para su revisión por el investigador/a.

**Slices secundarios nombrados:**
- **A1:** El par ingresado no hibrida en la región esperada del gen indicado.
- **E1:** La secuencia ingresada contiene caracteres fuera del alfabeto IUPAC válido.

#### HU-03.1 · Ingreso y validación del primer

*Deriva de: CU-03, Slice 1.*

> **Como** investigador/a, **quiero** ingresar las secuencias de los primers que diseñé externamente junto con el organismo y el identificador del target, **para** que el sistema valide que los datos tienen un formato correcto antes de realizar su verificación.

```gherkin
Escenario: Ingreso de datos
  Given que el investigador/a desea validar un par de primers diseñado externamente
  When ingresa las secuencias forward y reverse, el organismo y el identificador del target
  Then el sistema recibe correctamente los datos ingresados

Escenario: Validación del formato
  Given que el investigador/a ingresó las secuencias y los datos del target
  When el sistema valida los datos de entrada
  Then verifica que las secuencias de los primers y los demás campos cumplan con el formato requerido y permite continuar con la validación
```

#### HU-03.2 · Localización del gen

*Deriva de: CU-03, Slice 2.*

> **Como** investigador/a, **quiero** que el sistema obtenga la secuencia de referencia y localice automáticamente el gen objetivo, **para** asegurar que la validación de los primers se realice sobre la región correcta.

```gherkin
Escenario: Obtención de la referencia
  Given que los datos del target ingresados son válidos
  When el sistema ejecuta <<include>> CU-04
  Then obtiene la secuencia de referencia y la anotación correspondientes al target

Escenario: Localización del gen
  Given que la secuencia de referencia y su anotación están disponibles
  When el sistema localiza el gen objetivo
  Then identifica correctamente la región del gen dentro de la secuencia de referencia

Escenario: Coordenadas y hebra
  Given que el gen objetivo fue localizado correctamente
  When el sistema analiza su información genómica
  Then obtiene las coordenadas de inicio y fin y determina la hebra en la que se encuentra codificado
```

#### HU-03.3 · Verificación de hibridación y caracterización

*Deriva de: CU-03, Slice 3.*

> **Como** investigador/a, **quiero** que el sistema verifique que mi par de primers hibrida correctamente en la región objetivo y lo caracterice, **para** conocer si es adecuado para amplificar el target de interés.

```gherkin
Escenario: Localización de los primers
  Given que el gen objetivo fue localizado y se dispone de sus coordenadas y hebra
  When el sistema busca las secuencias de los primers dentro de la región del gen
  Then identifica las posiciones correspondientes de los primers forward y reverse

Escenario: Verificación de posición y orientación
  Given que las secuencias de los primers fueron localizadas en la región objetivo
  When el sistema analiza sus posiciones y orientaciones
  Then confirma que ambos primers hibridan en las posiciones y orientaciones esperadas para la amplificación del gen

Escenario: Caracterización del par
  Given que el par de primers hibrida correctamente en la región objetivo
  When el sistema ejecuta <<include>> CU-05
  Then obtiene la caracterización del par, incluyendo sus métricas termodinámicas, estructuras secundarias, valores de ΔG y el amplicón esperado
```

---
### CU-04 · Obtener secuencia de referencia del target

- **Actor:** Investigador/a
- **Actor secundario:** API NCBI
- **Objetivo:** Obtener la secuencia de referencia y anotación para habilitar el diseño de primers.
- **RF que realiza:** RF-03, RF-09
- **Precondición:** El sistema cuenta con acceso y conectividad a la API pública de NCBI Entrez.

**Flujo principal:**
1. El sistema consulta internamente la API de NCBI Entrez enviando el identificador y el organismo.
2. El sistema obtiene la secuencia FASTA y la anotación del genoma de referencia desde NCBI Entrez.
3. El sistema notifica al Investigador/a si el target fue validado correctamente o no.

**Postcondición:** La secuencia FASTA y la anotación del genoma de referencia correspondientes al identificador NCBI y organismo ingresados quedan obtenidas y disponibles internamente para que los casos de uso de diseño y validación de primers puedan utilizarlas.

#### HU-04 · Obtener la secuencia de referencia del target

*Deriva de: CU-04.*

> **Como** investigador/a, **quiero** que el sistema consulte automáticamente NCBI Entrez utilizando el identificador NCBI y el organismo ingresados, **para** obtener la secuencia FASTA y la anotación de referencia necesarias para continuar con el diseño de primers.

```gherkin
Escenario: Consulta exitosa a NCBI Entrez
  Given que los datos de entrada fueron validados correctamente
  When el sistema consulta NCBI Entrez utilizando el identificador NCBI y el organismo ingresados
  Then el sistema obtiene la secuencia FASTA y la anotación correspondientes al target

Escenario: Datos disponibles internamente
  Given que NCBI Entrez devuelve correctamente la secuencia FASTA y la anotación
  When el sistema finaliza la consulta
  Then almacena o deja disponibles internamente estos datos para el proceso de diseño de primers

Escenario: Confirmación al investigador
  Given que la secuencia y la anotación fueron obtenidas correctamente
  When finaliza la preparación del target
  Then el sistema informa al investigador/a que el target fue validado correctamente y que la secuencia de referencia quedó disponible para el diseño

Escenario: No requiere intervención manual
  Given que NCBI Entrez proporcionó correctamente la referencia
  When el sistema finaliza la consulta
  Then el investigador/a no necesita descargar ni cargar manualmente el archivo FASTA para continuar con el diseño
```

---
### CU-05 · Caracterizar par de primers

- **Actor:** Investigador/a
- **Objetivo:** Generar y caracterizar pares de primers candidatos para el gen objetivo, evaluando sus propiedades termodinámicas, estructuras secundarias, especificidad y amplicón esperado.
- **RF que realiza:** RF-04, RF-05, RF-06, RF-07
- **Precondición:** La región del gen objetivo ha sido localizada correctamente, se dispone de la secuencia de referencia y de los parámetros de diseño establecidos.

**Flujo principal (slice principal):**
1. El sistema recorre la región del gen con una ventana deslizante, generando pares de primers forward/reverse candidatos que cumplen la longitud, %GC y Tm objetivo.
2. El sistema calcula, para cada candidato, sus métricas termodinámicas (Tm real, %GC real, GC clamp, penalización por repeticiones).
3. El sistema verifica la especificidad de cada par de primers mediante BLAST.
4. El sistema evalúa cada candidato en busca de estructuras secundarias (horquillas y dímeros, internos y entre el par forward/reverse) y calcula su ΔG.
5. El sistema genera la simulación del amplicón esperado para cada par candidato.

**Postcondición:** Existe un conjunto de pares de primers candidatos caracterizados, cada uno con sus métricas termodinámicas, evaluación de especificidad, estructuras secundarias, valores de ΔG y amplicón esperado, disponibles para su revisión y selección por parte del investigador/a.

#### HU-05 · Generación y caracterización de candidatos

*Deriva de: CU-05.*

> **Como** investigador/a, **quiero** que el sistema genere pares de primers candidatos y los caracterice según sus propiedades termodinámicas, especificidad y estructuras secundarias, así como el amplicón esperado, **para** disponer de candidatos adecuados para la amplificación del target.

```gherkin
Escenario: Generación de candidatos
  Given que el sistema localizó correctamente la región del gen y dispone de los parámetros de diseño
  When recorre la región mediante una ventana deslizante
  Then genera pares de primers forward/reverse candidatos que cumplen con los parámetros de longitud, %GC y Tm objetivo establecidos

Escenario: Cálculo de métricas
  Given un par de primers candidato generado
  When el sistema realiza su caracterización
  Then calcula para cada primer su Tm real, %GC, GC clamp y penalización por repeticiones

Escenario: Evaluación de estructuras secundarias
  Given un par de primers candidato
  When el sistema analiza sus posibles estructuras secundarias
  Then evalúa la formación de horquillas y homodímeros de cada primer, así como heterodímeros entre forward y reverse, calculando los valores de ΔG correspondientes

Escenario: Simulación del amplicón
  Given un par de primers candidato localizado sobre la región objetivo
  When el sistema simula la amplificación
  Then determina el amplicón esperado y su información de posición y longitud

Escenario: Candidatos caracterizados
  Given que se completó la caracterización de los pares candidatos
  When finaliza el proceso
  Then el sistema dispone de un conjunto de pares de primers caracterizados con sus métricas termodinámicas, estructuras secundarias y amplicón esperado
```

---
