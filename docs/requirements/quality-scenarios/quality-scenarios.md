---
title: Escenarios de calidad
parent: Requerimientos
nav_order: 2
---

# Escenarios de calidad — PrimerCraft Pro

> Requerimientos no funcionales del [SRS](../srs.md) (§6). La taxonomía, el significado de cada atributo y la justificación de la selección están en el SRS §6.1–6.3. La tabla resumen (§2) indica los RF y CU con los que se relaciona cada escenario. Registro de uso de IA: [`registro-uso-ia.md`](registro-uso-ia.md).

## 1. Escenarios


> Entornos: 4 de 5 escenarios ocurren en **entorno degradado**; el de mantenibilidad ocurre en un entorno normal de desarrollo porque el atributo se manifiesta en tiempo de desarrollo, no de ejecución.


### 1.1 Pertinencia Funcional (Característica ISO de la que proviene: Adecuación Funcional)


**Qué le exige a la solución y por qué es crítico:** exige que PrimerCraft Pro incorpore el conjunto de funciones indispensables para que el investigador complete todo el flujo de diseño y caracterización de primers dentro de la misma herramienta, evitando que deba recurrir a software externo o realizar ediciones/recortes manuales de secuencias por limitaciones del sistema. Es crítico porque el mayor problema actual es la fragmentación del flujo de trabajo entre múltiples herramientas y pestañas




#### Escenario EC-01


| Componente | Descripción |
|---|---|
| **Explicación de criticidad** | Cuando se trabaja con ensamblados de genomas completos o secuencias cromosómicas donde NCBI no devuelve la tabla de características (GFF) del gen blanco, un sistema sin la pertinencia adecuada obligaría al investigador a abandonar la aplicación, abrir un visor externo (como IGV o UCSC Genome Browser) y mapear manualmente la región para encontrar los números de inicio y fin. Que el sistema resuelva esto internamente es indispensable para mantener el flujo unificado. |
| **Atributo / subcaracterística** | Adecuación funcional / Pertinencia funcional |
| **Estímulo** | El investigador/a inicia una corrida de diseño ingresando el identificador del target, el organismo y los parámetros de diseño. |
| **Fuente del estímulo** | Investigador/a. |
| **Artefacto** | Gestor de Preparación de Datos (P1) y Gestor de Diseño de Candidatos (P2). |
| **Entorno** | Degradado (la consulta recupera la secuencia del genoma/cromosoma de referencia, pero el registro carece de tabla de anotación con las coordenadas delimitadoras del gen de interés). |
| **Respuesta** | El sistema ejecuta de forma autónoma una función interna de localización para identificar las coordenadas del blanco dentro del genoma de referencia, acota la región objetivo y ejecuta la generación de candidatos por ventana deslizante con su caracterización, sin que el usuario haga búsquedas o recortes manuales en herramientas externas. Solo si esa localización interna tampoco encuentra el gen, informa que no se pudo localizar (CU-02 E1) y no genera candidatos. |
| **Medida de la respuesta** | **0** herramientas externas de navegación genómica y **0** pasos manuales de extracción de coordenadas requeridos al usuario para obtener el reporte final de primers caracterizados. |




---


### 1.2 Protección frente a errores del usuario (Característica ISO de la que proviene: Capacidad de interacción)


**Qué le exige a la solución y por qué es crítico:** Exige una interfaz que sea comprensible para un biólogo molecular sin formación en programación, mostrando el scoring como algo transparente (no una "caja negra") y protegiendo al usuario de cometer errores de formato. Es crítico para garantizar la adopción de la herramienta y evitar llamadas inútiles a las APIs externas que consuman la cuota de uso.


#### Escenario EC-02


| Componente | Descripción |
|---|---|
| **Explicación de criticidad** | Validar los datos localmente es vital para no enviar peticiones basura a NCBI, lo cual haría perder tiempo al investigador y consumiría recursos de red innecesariamente. |
| **Atributo / subcaracterística** | Capacidad de interacción / Protección frente a errores del usuario |
| **Estímulo** | Ingreso de un identificador NCBI con formato inválido, o de una secuencia de primer con caracteres fuera del código IUPAC. |
| **Fuente del estímulo** | Investigador/a. |
| **Artefacto** | Módulo de validación de entrada del Gestor de Preparación de Datos (P1). |
| **Entorno** | Degradado: ingreso de datos erróneos o corruptos (p. ej., secuencia pegada desde un PDF con caracteres extraños). |
| **Respuesta** | El sistema intercepta el error en el momento del ingreso, **no** inicia la consulta a NCBI y muestra una alerta que indica qué campo y qué caracteres son inválidos, permitiendo corregirlo **sin perder** el resto de los parámetros ya cargados. |
| **Medida de la respuesta** | **0** peticiones HTTP enviadas a NCBI ante entradas con formato/IUPAC inválido; **100 %** de los demás campos conservados tras el error; tiempo de corrección del usuario **< 10 s** (medido en prueba con usuario). |



---


### 1.3 Modificabilidad (Característica ISO de la que proviene: Mantenibilidad)


**Qué le exige a la solución y por qué es crítico:** Exige una arquitectura modular donde el núcleo termodinámico esté desacoplado de las fuentes de información genómica. Es fundamental debido al ciclo de vida Iterativo e Incremental elegido, dado que integraciones como el cruce de variantes (dbSNP/Ensembl) y los perfiles de scoring se dejaron explícitamente para etapas posteriores o de extensión.


#### Escenario EC-03


| Componente | Descripción |
|---|---|
| **Explicación de criticidad** | A medida que el proyecto evolucione se exigirá integrar nuevos proveedores de datos genómicos (la próxima iteración ya prevé dbSNP o Ensembl, SRS §2.6). Si incorporar un nuevo proveedor obligara a modificar el motor algorítmico, cada incremento pondría en riesgo lo que ya funciona y habría que volver a probar todo el sistema, lo que contradice el ciclo de vida elegido. |
| **Atributo / subcaracterística** | Mantenibilidad / Modificabilidad |
| **Estímulo** | Necesidad de incorporar un nuevo repositorio genómico externo (ya sea para obtener secuencias de referencia, anotaciones o variantes) o reemplazar una API existente por un nuevo proveedor público o privado. |
| **Fuente del estímulo** | Equipo de desarrollo / stakeholders. |
| **Artefacto** | Componentes de integración con servicios externos del Gestor de Preparación de Datos (P1) y del Gestor de Verificación de Variantes Poblacionales (P3). |
| **Entorno** | Normal: entorno de desarrollo/mantenimiento. |
| **Respuesta** | El equipo implementa el nuevo conector y lo integra **sin modificar** el Gestor de Diseño de Candidatos (P2) ni el cálculo termodinámico Nearest-Neighbor. |
| **Medida de la respuesta** | **< 15 horas/persona** para incorporar y validar la nueva fuente; **0** líneas modificadas en el motor de diseño (P2); **0** regresiones en las pruebas existentes. |





---


### 1.4 Interoperabilidad (Característica ISO de la que proviene: Compatibilidad)


**Qué le exige a la solución y por qué es crítico:** Exige que PrimerCraft Pro se comunique e intercambie datos de forma transparente con servicios bioinformáticos externos (NCBI Entrez/BLAST y dbSNP/Ensembl) mediante sus APIs web y formatos estándar (FASTA, VCF, JSON/XML). Es crítico porque el sistema no genera secuencias de referencia ni variantes de forma aislada, sino que su propuesta de valor depende del consumo e interpretación de datos producidos por repositorios públicos externos.


#### Escenario EC-04


| Componente | Descripción |
|---|---|
| **Explicación de criticidad** | Los servicios bioinformáticos públicos (como NCBI Entrez) actualizan periódicamente sus servidores y los esquemas de datos que retornan por HTTP. Si la capa de integración de PrimerCraft Pro utilizara un deserializador rígido, cualquier campo de metadatos nuevo o modificación menor en el encabezado de la respuesta provocará una excepción no controlada en tiempo de ejecución, interrumpiendo la corrida del usuario aunque la secuencia genómica deseada esté presente en el payload. |
| **Atributo / subcaracterística** | Compatibilidad / Interoperabilidad |
| **Estímulo** | La API de NCBI Entrez entrega la secuencia de referencia con un esquema de respuesta actualizado que incluye campos de metadatos no contemplados y variaciones en la cabecera del FASTA. |
| **Fuente del estímulo** | Servicio externo NCBI Entrez. |
| **Artefacto** | Conector con NCBI Entrez del Gestor de Preparación de Datos (P1). |
| **Entorno** | Degradado: incompatibilidad parcial de esquema tras una actualización del servicio externo. |
| **Respuesta** | El sistema procesa la respuesta, extrae la secuencia nucleotídica requerida e ignora los campos no reconocidos, sin interrumpir la corrida. |
| **Medida de la respuesta** | **100 %** de las respuestas que contienen la secuencia solicitada se convierten al formato interno sin excepciones de lectura/deserialización; **0** corridas interrumpidas por campos desconocidos. |







---


### 1.5 Tolerancia a fallos (Característica ISO de la que proviene: Fiabilidad)


**Qué le exige a la solución y por qué es crítico:** Exige que el software sea resiliente ante caídas de red, timeouts o límites de cuota de las APIs públicas, preservando el trabajo ya realizado (los candidatos generados). Es altamente crítico porque NCBI BLAST es un recurso compartido con "límites estrictos" (100 corridas/24hs) que el grupo no controla, lo que representa el principal riesgo técnico del proyecto.


#### Escenario EC-05


| Componente | Descripción |
|---|---|
| **Explicación de criticidad** | Si el sistema corta abruptamente la corrida por un bloqueo temporal de la API, el usuario pierde todo el tiempo invertido y el cálculo termodinámico local se desperdicia. |
| **Atributo / subcaracterística** | Fiabilidad / Tolerancia a fallos |
| **Estímulo** | La API de NCBI BLAST rechaza la conexión por superar la cuota permitida o presentar timeout. |
| **Fuente del estímulo** | API NCBI BLAST. |
| **Artefacto** | Verificación de especificidad del Gestor de Diseño de Candidatos (P2) y módulo de comunicación externa. |
| **Entorno** | Degradado: límite de uso excedido en la API pública. |
| **Respuesta** | El sistema informa el error o la saturación de forma clara, guarda el estado de los candidatos (con su Tm y estructuras ya calculadas) y los pone en una cola para reintentar la verificación de especificidad automáticamente más tarde. |
| **Medida de la respuesta** | **0 %** de pérdida de candidatos ya calculados tras un error HTTP 429 (Too Many Requests) o 500 (Internal Server Error) de NCBI; **100 %** de los candidatos en cola reintentados sin que el usuario vuelva a cargar la corrida. |

## 2. Resumen

| ID | Atributo | Subcaracterística | Entorno | RF / CU |
|---|---|---|---|---|
| AF-1 | Adecuación funcional | Pertinencia funcional | Degradado | RF-10 · CU-02 |
| CI-1 | Capacidad de interacción | Protección frente a errores del usuario | Degradado | RF-01, RF-08 · CU-01, CU-03 |
| MA-1 | Mantenibilidad | Modificabilidad | Normal (desarrollo) | RF-03 · CU-04 |
| CO-1 | Compatibilidad | Interoperabilidad | Degradado | RF-03 · CU-04 |
| FI-1 | Fiabilidad | Tolerancia a fallos | Degradado | RF-06 · CU-05 |

