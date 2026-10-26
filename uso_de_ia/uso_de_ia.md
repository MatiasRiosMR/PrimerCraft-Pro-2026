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

---

## [TP2] Datos de ejemplo reales de BRCA1 en las maquetas (ciclo 3)

| | |
|---|---|
| **Herramienta** | Claude Code |
| **Tarea** | Revisar la coherencia biológica de las maquetas y reemplazar los pares de ejemplo por pares reales de BRCA1, obtenidos de NCBI, sin cambiar la interfaz. |
| **Resultado** | El par de ejemplo anterior y los 24 pares de UI-3 no existían en BRCA1. Se reemplazaron por pares tomados de NC_000017.11 (GRCh38), con Tm por Nearest-Neighbor (SantaLucia 1998) en las condiciones por defecto de Primer3, y se verificó cada amplicón contra la secuencia de NCBI. El par principal (208 pb) queda en el exón 10 de NM_007294.4. Detalle en el ciclo 3 de `docs/ui/heuristic-review/hu-05_resultados-candidatos.md`. |
| **Modificado/descartado** | Se descartaron los primers derivados de elementos Alu. La especificidad se mantiene como simulada (SRS §2.6) y se aclaró en la maqueta que se cuenta en la región del gen, no en el genoma. |
| **Error detectado** | La primera selección dejó como "sin advertencias" pares con homodímeros < −6 kcal/mol; se rehízo la selección. La IA había marcado antes como "GC clamp" pares cuyo forward terminaba en A. |

---

## [TP2] Aplicación de los hallazgos aceptados en las maquetas (ciclo 4)

| | |
|---|---|
| **Herramienta** | Claude Code |
| **Tarea** | Aplicar a las maquetas los hallazgos aceptados en la revisión crítica (UI-3 H4, UI-2 H8 y UI-5 H5) y regenerar las capturas. En la misma sesión, mover el material de interfaz a las rutas de la consigna (§5): `docs/ui/user-profiles/`, `docs/ui/mockups/` y `docs/ui/heuristic-review/`. |
| **Resultado** | UI-3 tiene un botón "← Ajustar parámetros" en el estado con candidatos; UI-2 avisa cuando una etapa tarda más de lo habitual; UI-3 y UI-5 muestran las condiciones con las que se calculan la Tm y el ΔG. Se actualizaron los enlaces del sitio y de los README a las rutas nuevas. Detalle en el ciclo 4 de cada evaluación en `docs/ui/heuristic-review/`. |
| **Modificado/descartado** | No se repitió la evaluación heurística completa, porque los cambios se limitan a los hallazgos aceptados. |
| **Error detectado** | Ninguno. |

---

## [TP2] Reintento ante una caída de NCBI en UI-2 (ciclo 5)

| | |
|---|---|
| **Herramienta** | Claude Code |
| **Tarea** | Revisar si las maquetas cumplen las heurísticas de Nielsen después del ciclo 4 y, a pedido del grupo, agregar a UI-2 el estado de caída de NCBI con reintento que pide el escenario de calidad FI-2. |
| **Resultado** | La IA señaló que el rechazo de H4 de UI-2 contradecía FI-2. Se agregó a UI-2 el estado "NCBI no disponible", con reintento automático, botón "Reintentar ahora" y los datos conservados. Detalle en el ciclo 5 de `docs/ui/heuristic-review/hu-04_hu-02-1_progreso-corrida.md`. |
| **Modificado/descartado** | El grupo cambió la decisión sobre H4 de "Rechaza" a "Acepta", solo para la caída de NCBI. Los demás errores de UI-2 siguen sin "Reintentar", porque reintentar no los resuelve. |
| **Error detectado** | Ninguno. |


## [TP3] Drivers, estilo, patrones y tecnologías de la arquitectura

| | |
|---|---|
| **Herramienta** | Claude Code, Gemini Pro, Kimi k3 |
| **Tarea** | Elegir los drivers de arquitectura entre los escenarios del TP2, proponer tácticas, estilo base, patrones y tecnologías, y contrastarlos con las Tablas 2 a 6 de la consigna. |
| **Resultado** | Selección de cuatro drivers (`EC-03`, `EC-04`, `EC-05`, `EC-06`). Estilo base: tuberías y filtros (pipeline) para el procesamiento core, combinado con cliente-servidor para la interfaz. Patrones por contenedor: Broker, Arquitectura Hexagonal, Capas y MVVM. Stack tecnológico: NATS JetStream para la mensajería, PostgreSQL para la persistencia, Node.js/TypeScript para la API y Python para las etapas del pipeline. |
| **Modificado/descartado** | **1.** La propuesta inicial de Claude Code utilizaba Cliente-Servidor puro con Orientada a Eventos y descartaba Tuberías y Filtros; se rehízo completamente tras la indicación de la cátedra.<br>**2.** Se evaluó y descartó el estilo Repositorio (sugerido por Gemini Pro como alternativa de acoplamiento centralizado), ya que forzaba a hacer toda la comunicación interproceso mediante consultas recurrentes a la base de datos.<br>**3.** Kimi k3 propuso un enfoque 100% reactivo/event-driven para todas las capas, pero se descartó en la API y cliente por agregar complejidad innecesaria respecto a un modelo REST/MVVM estándar.<br>**4.** *Pendiente:* Validación final del stack tecnológico según las capacidades y dominio técnico del equipo. |
| **Error detectado** | Dos tácticas planteadas ("persistir el estado antes de actuar" y "validar la entrada antes de actuar") no figuraban explícitamente en la Tabla 2 de la consigna. Una versión previa clasificó la primera erróneamente como "transacciones"; se corrigió declarándolas como tácticas propias. Asimismo, se detectó que la objeción original contra Tuberías y Filtros solo aplicaba a esquemas con estado compartido centralizado en la base de datos. |

---

## [TP3] Diagramas C4 en Mermaid y reducción del documento

| | |
|---|---|
| **Herramienta** | Claude Code, Gemini Pro, Kimi k3 |
| **Tarea** | Diseñar los 7 diagramas C4 (Contexto, Contenedores y 5 Vistas de Componentes) en sintaxis Mermaid, validar su legibilidad visual renderizándolos con `mermaid-cli`, y sintetizar el documento para cumplir con las restricciones de extensión. |
| **Resultado** | Diagramas reestructurados y optimizados visualmente: se ajustó la declaración de elementos para evitar el cruzamiento de flechas sobre cajas (aprovechando las reglas de layout de Mermaid por orden de declaración). Se eliminaron las tablas explícitas de relaciones entre componentes, al estar sus tecnologías y protocolos documentados en el propio gráfico (§4.1 de la consigna), y se fusionaron decisiones redundantes. |
| **Modificado/descartado** | **1.** Se eliminó "Instrumentación" como componente independiente (Gemini Pro y Kimi k3 coincidieron en que el registro de logs/métricas estándar de la plataforma era suficiente sin saturar la vista C4).<br>**2.** Se dividió el motor de procesamiento en 3 etapas desacopladas para garantizar que ninguna vista de componentes superara el límite recomendado de 8 elementos por diagrama.<br>**3.** Se rechazó una propuesta de Kimi k3 de usar sintaxis de diagramas de secuencia para detallar los componentes, manteniendo la notación estricta de C4 en Mermaid. |
| **Error detectado** | En la primera iteración, el motor de procesamiento agrupaba 17 componentes en una única vista C4, volviéndola completamente ilegible. Además, la disposición inicial provocaba superposición de etiquetas y solapamiento de líneas de conexión sobre los bloques de arquitectura. |

---

## [TP3] Redacción del informe y justificación de decisiones arquitectónicas

| | |
|---|---|
| **Herramienta** | Gemini Pro, Claude Code, Kimi k3 |
| **Tarea** | Redactar las secciones de justificación técnica del informe del TP3, argumentando la selección de estilos, patrones y compensaciones (*trade-offs*) de calidad. |
| **Resultado** | Un documento consolidado con la fundamentación del modelo Híbrido Pipeline/Cliente-Servidor, detallando los atributos de calidad priorizados (rendimiento, modificabilidad y disponibilidad) y la matriz de trazabilidad respecto a los escenarios de calidad del TP2. |
| **Modificado/descartado** | **1.** Claude Code propuso una justificación extensa orientada a microservicios que fue descartada por no coincidir con el diseño en contenedores acoplados por NATS.<br>**2.** Kimi k3 sugirió estructurar la justificación bajo la norma ISO/IEC 25010; se simplificó usando directamente los términos de las tablas fijadas en la consigna del TP.<br>**3.** Gemini Pro ayudó a sintetizar las secciones argumentativas para cumplir con la restricción estricta de páginas. |
| **Error detectado** | En la redacción borrador se mencionaba la baja latencia como driver principal, cuando en realidad el escenario `EC-04` ponía énfasis en la tolerancia a fallos y resiliencia en el procesamiento asincrónico. |

---

## [TP3] Análisis de alternativas de almacenamiento y persistencia

| | |
|---|---|
| **Herramienta** | Kimi k3, Gemini Pro |
| **Tarea** | Evaluar distintas opciones de bases de datos y estrategias de persistencia para los estados intermedios del procesamiento y los datos de usuario. |
| **Resultado** | Selección de PostgreSQL como base de datos relacional principal para la API y estado global, aprovechando la capacidad de soporte de documentos JSONB para cargas dinámicas y evitando la necesidad de un motor NoSQL secundario. |
| **Modificado/descartado** | **1.** Kimi k3 propuso una arquitectura políglota utilizando MongoDB para eventos y Redis para caché de sesión.<br>**2.** Gemini Pro fundamentó la simplificación del stack hacia PostgreSQL unificado para no incrementar los costos operativos ni la complejidad de mantenimiento en el prototipo.<br>**3.** Se descartó el almacenamiento de imágenes directamente en la base de datos (BLOB), optando por URLs con almacenamiento en volúmenes/S3. |
| **Error detectado** | Se detectó un cuello de botella en el diseño inicial propuesto por Kimi k3 donde la API realizaba escrituras sincrónicas en base de datos por cada mensaje procesado en el pipeline, lo cual violaba el atributo de rendimiento esperado en `EC-03`. |

---

## [TP3] Estrategia de seguridad, autenticación y autorización

| | |
|---|---|
| **Herramienta** | Gemini Pro, Claude Code |
| **Tarea** | Definir el esquema de seguridad, mecanismos de autenticación y control de acceso para los contenedores de la API y los clientes web/móviles. |
| **Resultado** | Definición de esquema basado en Tokens JWT con claves asimétricas (RS256) y un Middleware de Autorización basado en Roles (RBAC) en el contenedor de API Gateway/Servidor. |
| **Modificado/descartado** | **1.** Claude Code sugirió delegar la autenticación a un proveedor externo (Keycloak) mediante un contenedor dedicado.<br>**2.** Se descartó la integración de Keycloak por agregar un contenedor extra no contemplado en los escenarios del TP2 y se optó por autenticación nativa simplificada por JWT.<br>**3.** Gemini Pro revisó el flujo de refresh tokens para asegurar la persistencia en sesión sin almacenar credenciales en el cliente. |
| **Error detectado** | La propuesta inicial situaba la validación de permisos dentro de las etapas del pipeline de procesamiento, lo cual mezclaba lógica de negocio con seguridad de infraestructura; se movió la responsabilidad exclusivamente a la capa de API. |

---

## [TP3] Matriz de trazabilidad y mapeo Escenarios vs. Tácticas

| | |
|---|---|
| **Herramienta** | Kimi k3, Gemini Pro, Claude Code |
| **Tarea** | Construir la matriz de trazabilidad entre los escenarios de calidad del TP2 (`EC-01` a `EC-06`) y las tácticas/patrones seleccionados en el TP3. |
| **Resultado** | Matriz tabular completa que correlaciona cada escenario con su respuesta táctica, indicando en qué contenedor o componente C4 se implementa concretamente. |
| **Modificado/descartado** | **1.** Kimi k3 propuso mapear escenarios no seleccionados como primarios para "demostrar cobertura total"; Gemini Pro sugirió enfocarse únicamente en los 4 drivers elegidos para no generar contradicciones en el informe.<br>**2.** Se descartaron tácticas genéricas ("usar buenas prácticas de código") reemplazándolas por tácticas específicas de las Tablas 2 y 3 de la consigna. |
| **Error detectado** | Inconsistencia en la identificación de códigos: en el primer borrador generado por Claude Code se intercambiaron las respuestas de los escenarios `EC-03` (Rendimiento) y `EC-05` (Modificabilidad). |

---

## [TP3] Revisión cruzada de consistencia del documento y checklist de entrega

| | |
|---|---|
| **Herramienta** | Gemini Pro, Kimi k3, Claude Code |
| **Tarea** | Auditar de manera cruzada la totalidad del documento `.md` antes de la entrega final para verificar cumplimiento estricto de consignas y nomenclaturas. |
| **Resultado** | Informe final verificado sin discrepancias en nombres de componentes entre texto y diagramas C4, con formato estandarizado para tablas y referencias. |
| **Modificado/descartado** | **1.** Gemini Pro identificó discordancias en la nomenclatura de un componente (mencionado como `NotificationService` en el texto y como `Notifier` en el C4); se unificó a `Notification Engine`.<br>**2.** Kimi k3 revisó que no quedaran referencias a infraestructura no solicitada en las consignas de arquitectura conceptual.<br>**3.** Claude Code automatizó el conteo de palabras y secciones para garantizar el cumplimiento del límite de páginas. |
| **Error detectado** | Se encontraron dos enlaces rotos a las secciones de anexos del TP2 y figuras en Mermaid que no renderizaban correctamente por caracteres especiales en las etiquetas. |

---

## [TP3] Vista de despliegue, decisión DA-08 y trazabilidad de nodos

| | |
|---|---|
| **Herramienta** | Claude Code |
| **Tarea** | Armar el diagrama de despliegue C4 del entorno de producción (sección 8) con su catálogo de nodos, a partir de la vista de contenedores ya definida por el grupo y de las reglas de las secciones 4.6, 4.7 y 4.8 de la consigna. Registrar la decisión de despliegue, sumar los nodos a la trazabilidad y agregar el riesgo correspondiente. |
| **Resultado** | Diagrama `C4Deployment` en Mermaid con la computadora del usuario y una VPS con Docker que ejecuta los siete contenedores del sistema; catálogo de nodos con su justificación; decisión `DA-08`; nodos en la tabla de trazabilidad de `EC-05`; riesgo 9 (VPS como punto único de falla); renumeración de las secciones 9 a 12 y del índice. |
| **Modificado/descartado** | **1.** El grupo indicó que el despliegue sería en una VPS privada, y el nodo "Servidor de producción" se renombró a "VPS privada".<br>**2.** Se descartó dibujar NCBI y las bases de variantes, porque la regla 4.8 excluye los sistemas externos de esta vista.<br>**3.** Se descartó separar la base de datos en un nodo propio, como en el ejemplo del Anexo C, porque ningún escenario lo exige y la restricción es una sola máquina.<br>**4.** Se agregaron al `DA-08` el reinicio automático de contenedores y el backup de PostgreSQL fuera de la VPS, a partir de revisar qué ocurre si se cae un nodo. |
| **Error detectado** | El primer render de Mermaid tenía flechas que cruzaban cajas y etiquetas superpuestas; se reordenaron los contenedores y se ajustaron las posiciones de las etiquetas. Los nombres de contenedores se tomaron de un borrador y se verificaron contra la sección 6 publicada en `main`. |
