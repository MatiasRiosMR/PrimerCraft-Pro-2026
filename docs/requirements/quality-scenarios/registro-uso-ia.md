---
title: Registro de uso de IA (escenarios de calidad)
parent: Requerimientos
nav_order: 3
---

# Registro de uso de IA — Parte A

> Mismo formato que `uso_de_ia/uso_de_ia.md`. Una entrada por cada interacción con IA de la Parte A, en el orden en que ocurrieron.

## Punto de partida: trabajo del grupo (sin IA)

Antes de usar cualquier herramienta de IA, el grupo armó en conjunto un **borrador propio** con las ideas centrales de la Parte A:

- la taxonomía a usar (ISO/IEC 25010:2023);
- los cinco atributos que consideramos más críticos para PrimerCraft Pro y por qué, a partir de los riesgos que ya habíamos identificado en el SRS (dependencia de NCBI/BLAST, límites de uso, errores de formato del usuario, extensiones previstas como dbSNP/Ensembl);
- los atributos que dejamos afuera (seguridad de la información, portabilidad, eficiencia llevada al extremo) con su motivo;
- un primer escenario por atributo, con sus seis componentes, pensado en condiciones degradadas (registro sin anotación, entrada inválida, nuevo proveedor de datos, cambio de esquema de NCBI, cuota de BLAST excedida).

Las decisiones de **qué** atributos elegir y **qué** situaciones modelar son del grupo. La IA se usó después, para revisar ese borrador contra la consigna y la norma, y para corroborar la terminología.

---

## [TP2] Revisión del borrador de escenarios contra la consigna y la ISO/IEC 25010:2023

| | |
|---|---|
| **Herramienta** | Claude |
| **Tarea** | Revisar el borrador del grupo (taxonomía, 5 atributos, justificación y 5 escenarios) contra la consigna del TP2 y la ISO/IEC 25010:2023, señalar inconsistencias y pasarlo a Markdown con trazabilidad al SRS. |
| **Resultado** | Una lista de observaciones y el documento `quality-scenarios.md` con el contenido del grupo y estos cambios propuestos: <br>1. "Usabilidad" → **Capacidad de interacción** (nombre de la edición 2023). <br>2. "Portabilidad" (en los excluidos) → **Flexibilidad**. <br>3. "Modificabilidad / Extensibilidad" → **Modificabilidad** (*extensibilidad* no es subcaracterística ISO). <br>4. Dejar en cada atributo solo las subcaracterísticas que algún escenario pone a prueba. <br>5. Sacar de la criticidad de MA-1 la referencia a "patrones de desacoplamiento", porque el checklist pide la criticidad **sin** decisiones de arquitectura. <br>6. FI-1: el artefacto "Gestor de Verificación de Variantes y Especificidad" no existe en el DFD; el que consulta BLAST es el Gestor de Diseño de Candidatos (P2).  <br>7. Agregar medidas verificables complementarias (CI-1: campos conservados; MA-1: 0 líneas modificadas en P2; FI-1: reintento sin recarga). <br>8. Agregar un escenario **FI-2** (Capacidad de recuperación), porque Fiabilidad nombraba esa subcaracterística y ningún escenario la ponía a prueba. |
| **Modificado/descartado** | **Aceptados:** 1, 2 y 3; 4; 5; 6 y 7. <br>**Modificado:** el 8. Nos quedamos con FI-2 porque tapaba un hueco real de nuestro borrador, y lo atamos a RF-09 y HU-04: lo que nos importa es que una caída de NCBI **no** se le informe al investigador como "identificador inexistente", porque lo llevaría a corregir un dato que estaba bien. <br>**Descartado:** la IA marcó que MA-1 es el único escenario en entorno normal. Lo mantuvimos así: la mantenibilidad se manifiesta en tiempo de desarrollo, no de ejecución, y forzar un "entorno degradado" hubiera sido artificial. Lo dejamos justificado en la nota al comienzo de la §1 del documento. |
| **Error detectado** | En FI-2, la IA puso como medida "reanudar en < 1 min" sin ninguna fuente que la respalde. La conservamos, pero declarada como **meta fijada por el grupo** y no como un dato del SRS. |

---

## [TP2] Verificación de la terminología de la ISO/IEC 25010:2023

| | |
|---|---|
| **Herramienta** | Gemini |
| **Tarea** | Corroborar, en una conversación aparte y sin mostrarle la respuesta de Claude, los nombres de las características y subcaracterísticas de la edición 2023 que usamos (y su equivalente en la edición 2011), para no depender de una sola fuente. |
| **Resultado** | Confirmó los renombres de la edición 2023 (*Usability* → *Interaction capability*, *Portability* → *Flexibility*) y que *extensibility* no es subcaracterística de *Maintainability*. Además mencionó que la edición 2023 agrega la característica *Safety*. |
| **Modificado/descartado** | Adoptamos los nombres confirmados y los tradujimos nosotros al español de forma uniforme ("Protección frente a errores del usuario", "Tolerancia a fallos", "Capacidad de recuperación"), cotejándolos con el Anexo A de la consigna. Evaluamos *Safety* y la descartamos: PrimerCraft Pro no controla equipos ni produce daños físicos; el riesgo de un primer mal diseñado ya está cubierto por Adecuación funcional. |
| **Error detectado** | Tradujo algunas subcaracterísticas con términos distintos en respuestas sucesivas (por ejemplo, "protección contra errores de usuario" y "prevención de errores"). Por eso tomamos como referencia el Anexo A de la consigna y no la traducción de la IA. |

---

## [TP2] Coherencia entre el escenario AF-1 y las maquetas

| | |
|---|---|
| **Herramienta** | Claude Code |
| **Tarea** | Revisar todo el TP2 contra la consigna y las aclaraciones del docente, incluida la coherencia entre la Parte A y la Parte B. |
| **Resultado** | Señaló una contradicción: AF-1 dice que, si el registro no trae la anotación, el sistema localiza el gen por su cuenta y sigue; pero la maqueta UI-2 (estado "Gen no localizado", CU-02 A1) mostraba un error y volvía a UI-1. Propuso que AF-1 cubra también el caso en que la localización interna falla. |
| **Modificado/descartado** | **Aceptado.** Se agregó a la respuesta de AF-1: "Solo si esa localización interna tampoco encuentra el gen, informa que no se pudo localizar (CU-02 E1) y no genera candidatos". En UI-2, el estado "Gen no localizado" ahora aclara que también falló la localización interna. La medida de AF-1 no cambia. |
| **Error detectado** | Ninguno en la propuesta. La contradicción venía del borrador: AF-1 y CU-02 A1 se habían escrito por separado. |

---

## [TP2] Revisión de coherencia entre los escenarios, su registro y el SRS

| | |
|---|---|
| **Herramienta** | Claude Code |
| **Tarea** | Revisar, antes de la entrega, que `quality-scenarios.md` coincida con lo que este registro dice que se hizo y con el SRS. |
| **Resultado** | Encontró que el documento decía "5 de 6 escenarios" pero tenía 5, que el SRS §6.2 nombraba Tolerancia a fallos sin escenario, y que faltaban FI-2, la trazabilidad, los ID y la cláusula de AF-1 descriptos en las entradas anteriores; el SRS §6.4 tenía un texto provisorio sin link. Completó el documento con esos elementos (FI-1 pasa a Tolerancia a fallos; se agrega FI-2), movió la referencia a patrones de MA-1 a la nota opcional de arquitectura, agregó la tabla resumen y renumeró el SRS (§4 a §6). |
| **Modificado/descartado** | Las referencias de trazabilidad se limitaron a escenarios y códigos que existen en el SRS actual (por ejemplo, CU-02 E1 en lugar de A1). El texto de FI-2 queda sujeto a la revisión del grupo. |
| **Error detectado** | Ninguno en la propuesta; las inconsistencias venían de haber subido el documento y su registro en momentos distintos. |
