<div align="center">

<img src="docs/marca/logotipo-original.png" alt="PrimerCraft Pro" width="480">

# PrimerCraft Pro

**Diseño y puntuación automática de primers para PCR/qPCR**

**Trabajo Final — Ingeniería de Software (2026)**

**[Ver la documentación publicada](https://matiasriosmr.github.io/PrimerCraft-Pro-2026/)**

</div>

---

## Integrantes

- Barbara Sara
- Vergara Emilia
- Rios Matias

**Carrera:** Licenciatura en Bioinformática

**Institución:** Facultad de Ingeniería, Universidad Nacional de Entre Ríos (FIUNER)

---
## Sobre el proyecto

**PrimerCraft Pro** es una herramienta que diseña y puntúa automáticamente pares de primers para PCR/qPCR a partir de una secuencia blanco, garantizando la trazabilidad e integrando en un solo flujo:

- **Cálculo termodinámico** (Tm, %GC)
- **Detección de estructuras secundarias** (hairpins, dímeros) y **variantes**
- **Simulación del amplicón**
- **Verificación de especificidad**

Está pensada para investigadores/as de biología molecular que hoy alternan entre múltiples herramientas dispersas (NCBI, Primer3/Primer-BLAST, verificadores de estructura) para llegar al mismo resultado.

Para profundizar más sobre esto, ir a: [`docs/requirements/srs.md`](docs/requirements/srs.md)


---

## Arquitectura en breve

La arquitectura se deriva de un problema: NCBI BLAST limita las consultas (100 corridas cada 24 h) y puede rechazar pedidos durante horas, y el sistema no puede perder los candidatos ya calculados (escenario de calidad `EC-05`, driver principal).

- **Estilo base: tuberías y filtros.** Una cadena de etapas independientes (Preparación de datos, Diseño de candidatos y Verificación de especificidad) conectadas por tuberías de mensajes que guardan el trabajo en disco, de modo que la espera de BLAST no frena al resto.
- **Interfaz: cliente-servidor.** Una aplicación web que conversa con un Servidor de corridas, que es el único que accede a la base de datos.
- **Patrones por contenedor:** broker en las tuberías, hexagonal en las etapas con servicios externos (`EC-03`, `EC-04`), capas en el Servidor de corridas y MVVM en la web.
- **Despliegue:** una sola VPS con Docker, con reinicio automático de los contenedores, volúmenes en disco y backup de la base fuera de la VPS.
- **Tecnologías propuestas:** TypeScript y React (web), Node.js y Fastify (Servidor de corridas), Python (etapas de cálculo), NATS JetStream (tuberías) y PostgreSQL (base de datos).

El detalle está en [`docs/architecture/arquitectura.md`](docs/architecture/arquitectura.md).

---

## Modelo de ciclo de vida

Se elige el ciclo de vida **Iterativo e Incremental** porque permite construir la herramienta por etapas, entregando primero el núcleo útil del sistema y agregando valor funcional en cada entrega. De forma **incremental**, se puede poner a punto el cálculo básico de primers antes de sumar capacidades más avanzadas como la alerta por variantes poblacionales (SNPs) o el procesamiento automático de listas en lote. De forma **iterativa**, permite ajustar progresivamente aspectos complejos como la conexión con servicios externos (NCBI BLAST), probando primero con una versión simulada antes de implementar la integración definitiva.


---

## Documentación

| Área | Documento | Contenido |
|---|---|---|
| Requerimientos | [`docs/requirements/srs.md`](docs/requirements/srs.md) | SRS: visión y alcance, requerimientos funcionales y no funcionales, casos de uso e historias de usuario |
| | [`docs/requirements/quality-scenarios/quality-scenarios.md`](docs/requirements/quality-scenarios/quality-scenarios.md) | Escenarios de calidad (ISO/IEC 25010) |
| | [`docs/requirements/quality-scenarios/registro-uso-ia.md`](docs/requirements/quality-scenarios/registro-uso-ia.md) | Registro de uso de IA de los escenarios de calidad |
| Arquitectura | [`docs/architecture/contexto_inicial.md`](docs/architecture/contexto_inicial.md) | Diagrama de contexto (DFD nivel 0 y nivel 1) |
| | [`docs/architecture/modelo-dominio-inicial.md`](docs/architecture/modelo-dominio-inicial.md) | Modelo de dominio |
| | [`docs/architecture/arquitectura.md`](docs/architecture/arquitectura.md) | Documento de especificación de arquitectura: drivers, estrategia de solución (tácticas, estilos y patrones), vistas C4 de contenedores, componentes y despliegue, historias de usuario sobre las vistas, decisiones `DA-xx`, trazabilidad y riesgos |
| Diseño detallado | [`docs/design/diseno-detallado.md`](docs/design/diseno-detallado.md) | TP4, Parte A: diseño detallado de `HU-04` (ficha, análisis tridimensional, robustez, secuencias, modelo de clases obtenido del código, pruebas y trazabilidad) |
| UX | [`docs/ui/README.md`](docs/ui/README.md) | Índice del diseño de experiencia de usuario |
| | [`docs/ui/user-profiles/perfil-investigador.md`](docs/ui/user-profiles/perfil-investigador.md) | Perfil de usuario, escenarios de uso y flujos de navegación |
| | [`docs/ui/criterios_generacion.md`](docs/ui/criterios_generacion.md) | Criterios de generación de las maquetas |
| | [`docs/ui/heuristic-review/`](docs/ui/README.md#pantallas) | Evaluación heurística de cada pantalla (UI-1 a UI-5) |
| Maquetas | `docs/ui/mockups/` | Maquetas HTML de las 5 pantallas y sus capturas de escritorio y móvil. Para usarlas en el navegador: [UI-1](https://matiasriosmr.github.io/PrimerCraft-Pro-2026/ui/mockups/hu-01-1_nueva-corrida-diseno.html), [UI-2](https://matiasriosmr.github.io/PrimerCraft-Pro-2026/ui/mockups/hu-04_hu-02-1_progreso-corrida.html), [UI-3](https://matiasriosmr.github.io/PrimerCraft-Pro-2026/ui/mockups/hu-05_resultados-candidatos.html), [UI-4](https://matiasriosmr.github.io/PrimerCraft-Pro-2026/ui/mockups/hu-03-1_validar-primer.html), [UI-5](https://matiasriosmr.github.io/PrimerCraft-Pro-2026/ui/mockups/hu-03-3_resultado-validacion.html) |
| Marca | `docs/marca/` | Isotipo y logotipo del grupo |
| Uso de IA | [`uso_de_ia/uso_de_ia.md`](uso_de_ia/uso_de_ia.md) | Registro general de uso de IA generativa, actualizado TP a TP |

## Estructura del repositorio

```
PrimerCraft-Pro-2026/
├── README.md
├── docs/                         # documentación; se publica como sitio web (GitHub Pages)
│   ├── index.md                  # portada del sitio
│   ├── _config.yml               # configuración del sitio (tema, menú, Mermaid)
│   ├── _includes/, _sass/        # personalización del tema (estilos, scripts, diagramas)
│   ├── requirements/             # TP1 y TP2: requerimientos y calidad
│   │   ├── srs.md                # SRS
│   │   └── quality-scenarios/    # escenarios de calidad y su registro de uso de IA
│   ├── architecture/             # TP1 y TP3: modelos y arquitectura
│   │   ├── contexto_inicial.md          # diagrama de contexto (DFD nivel 0 y 1)
│   │   ├── modelo-dominio-inicial.md    # modelo de dominio
│   │   └── arquitectura.md              # especificación de arquitectura (vistas C4, decisiones)
│   ├── ui/                       # TP2: experiencia de usuario
│   │   ├── user-profiles/        # perfil de usuario, escenarios y flujos
│   │   ├── mockups/              # maquetas HTML y capturas (capturas/, capturas/movil/)
│   │   └── heuristic-review/     # evaluación heurística por pantalla
│   └── marca/                    # isotipo y logotipo
├── src/                          # código fuente (todavía vacío)
├── tests/                        # pruebas (todavía vacío)
└── uso_de_ia/                    # registro general de uso de IA, actualizado TP a TP
```

---

## Licencia

Proyecto académico desarrollado en el marco de la materia **Ingeniería de Software** (FIUNER, 2026). Uso educativo.

## TP4 · Implementación y pruebas de HU-04

Implementación de la historia de usuario **HU-04 · Obtener la secuencia de referencia del target**, siguiendo el
[diseño detallado](docs/design/diseno-detallado.md) (Parte A): robustez y secuencias, con el modelo de clases obtenido del código y validado contra ellas.

Dado un identificador NCBI y un organismo, el sistema consulta NCBI Entrez y obtiene la secuencia FASTA y la
anotación. Si NCBI no devuelve resultados, rechaza e informa que se verifique el identificador.

> **Documentos:** [diseño detallado](docs/design/diseno-detallado.md), [tabla de casos de prueba](docs/design/diseno-detallado.md#7-pruebas) y [cobertura](docs/design/cobertura.md).

### Requisitos

- Python 3.11 o superior
- Conexión a internet para consultar NCBI real (opcional: hay un modo simulado)

### Instalación

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

### Ejecutar la interfaz

```bash
uvicorn src.interfaz.app:app
```

Abrir <http://127.0.0.1:8000>. La pantalla es un panel de una sola vista con la identidad de PrimerCraft Pro. Trae dos ejemplos para recorrer los dos caminos del criterio de aceptación:

| Ejemplo | Resultado |
|---|---|
| `NM_000518` · *Homo sapiens* | Referencia obtenida: secuencia de 628 nt y su anotación |
| `NM_999999` · *Homo sapiens* | Rechazo: «No se encontró el target … Verifique el identificador ingresado.» |

#### Modo simulado (sin internet)

Usa respuestas de NCBI grabadas en `src/infraestructura/grabaciones/`. Solo conoce `NM_000518` (*Homo sapiens*) y
`NM_SIN_SECUENCIA` (un registro que existe pero viene vacío); cualquier otro identificador se rechaza.

```bash
# Windows (PowerShell)
$env:PRIMERCRAFT_NCBI = "simulado"; uvicorn src.interfaz.app:app
# Windows (cmd)
set PRIMERCRAFT_NCBI=simulado && uvicorn src.interfaz.app:app
# Linux / macOS
PRIMERCRAFT_NCBI=simulado uvicorn src.interfaz.app:app
```

La pantalla indica arriba a la derecha si está en modo `real` o `simulado`.

#### Qué muestra la pantalla

- **Target** (formulario con dos ejemplos para recorrer los dos caminos).
- **Resultado:** longitud, secuencia FASTA en bloques de 10 nt con posiciones (con la leyenda de las bases A, C, G y T) y el texto de la anotación GenBank con colores por tipo de texto.
- **Animaciones decorativas:** una doble hélice mientras se consulta a NCBI, la secuencia que aparece «leída» en cascada, y la hebra que se corta en el rechazo. No representan datos y se apagan si el sistema pide «reducir movimiento».
- **Acciones:** copiar la secuencia en FASTA y descargarla como `.fasta`.
- **Rechazo:** panel con el motivo y el paso «Referencia» del flujo marcado en rojo.

La pantalla no calcula nada: `src/interfaz/presentacion.py` solo ordena en líneas y bloques lo que devuelve el controlador.

### Ejecutar las pruebas

```bash
pytest --cov
```

Las pruebas no usan internet ni la interfaz: prueban el dominio, el controlador, el adaptador y el consumidor
con dobles. El reporte de cobertura excluye la interfaz y el arranque (`.coveragerc`). Para ver también las ramas:
`pytest --cov --cov-branch`.

- Tabla de casos de prueba (técnica, origen, datos y resultado esperado): [`docs/design/diseno-detallado.md`, sección 7](docs/design/diseno-detallado.md#7-pruebas)
- Complejidad ciclomática de las operaciones de la HU, con una prueba por camino: [sección 7.3](docs/design/diseno-detallado.md#73-complejidad-ciclomática)
- Reporte de cobertura y su análisis: [`docs/design/cobertura.md`](docs/design/cobertura.md)

### Estructura

```
src/
├── dominio/            InformacionGenoma, ReferenciaSinSecuencia
├── aplicacion/         ControladorObtencionReferencia, GestionDeExcepciones,
│                       puertos (PuertoReferenciaGenomica, PuertoMensajes, RepositorioReferencias), DatosDeReferencia, Aviso, Resultado
├── infraestructura/    AdaptadorNcbiEntrez, PublicadorDeEtapa, ConsumidorDeEtapa,
│                       RepositorioReferenciasSqlite / EnMemoria, grabaciones/
├── interfaz/           pantalla (FastAPI + plantilla HTML), presentacion.py, static/ (isotipo)
└── arranque.py         único lugar donde se arman los objetos concretos
tests/
docs/design/            diseño detallado, tabla de casos de prueba y cobertura
```

Las dependencias van en un solo sentido: `interfaz → aplicacion → dominio`, e `infraestructura` implementa los
puertos de `aplicacion`. El dominio no importa nada de las demás capas.

### Dónde está la arquitectura del TP3

El código implementa **un contenedor** del TP3, **Preparación de datos (etapa 1)**, con el patrón hexagonal de su vista de componentes (sección 7.3 de la arquitectura). Las carpetas siguen las capas que sugiere la consigna; cada archivo dice en su primera línea qué componente del TP3 es.

| Componente del TP3 | Capa hexagonal | Carpeta y archivo |
|---|---|---|
| Consumidor de etapa | Adaptador de entrada | `infraestructura/consumidor_de_etapa.py` |
| Obtención de referencia | Núcleo | `aplicacion/controlador_obtencion_referencia.py` y `dominio/informacion_genoma.py` (la entidad) |
| Gestión de excepciones | Núcleo | `aplicacion/gestion_de_excepciones.py` |
| Puerto de referencia genómica, Puerto de mensajes | Núcleo (interfaces) | `aplicacion/puertos.py` |
| Adaptador NCBI Entrez | Adaptador de salida | `infraestructura/adaptador_ncbi_entrez.py` |
| Publicador de etapa | Adaptador de salida | `infraestructura/publicador_de_etapa.py` |
| *(sin componente en el TP3)* Repositorio de referencias | Adaptador de salida | `infraestructura/repositorio_referencias.py` (excepción a `DA-04`) |
| Aplicación web *(simulada por una pantalla mínima)* | Frontera con la persona | `interfaz/` |

Lo demás del TP3 (Servidor de corridas, tuberías NATS, Localización de gen, otras etapas, PostgreSQL) queda fuera de `HU-04`: las tuberías y la base se simulan detrás de interfaces (publicador y repositorio).

### Qué se reemplaza y cómo

| Qué | Cómo |
|---|---|
| Proveedor genómico (NCBI → otro) | Escribir una clase que cumpla `PuertoReferenciaGenomica` y pasarla en `arranque.py`. El controlador no cambia (ver `ReferenciasFalsas` en `tests/test_hu04.py`) |
| NCBI real ↔ respuestas grabadas | `PRIMERCRAFT_NCBI=simulado` o la función de transporte que recibe `AdaptadorNcbiEntrez` |
| Base de datos | Otra clase que cumpla `RepositorioReferencias` y cambiar `arranque.py` |
| Broker de mensajes | `PublicadorDeEtapa` guarda los avisos en memoria; NATS iría detrás de `PuertoMensajes`. El `ConsumidorDeEtapa` recibe el mismo JSON que definió el TP3 (`idCorrida`, `carga.identificadorNcbi`, `carga.organismo`) |

### Persistencia

Las referencias obtenidas se guardan en una base **SQLite** (`primercraft.db`, se crea sola al primer uso) detrás de la
interfaz `RepositorioReferencias`. El controlador solo conoce la interfaz; hay dos implementaciones:

| Implementación | Uso |
|---|---|
| `RepositorioReferenciasSqlite` | Por defecto, en `arranque.py`. Archivo configurable con `PRIMERCRAFT_DB` |
| `RepositorioReferenciasEnMemoria` | Pruebas: no toca el disco |

Solo se guarda cuando la referencia se obtuvo; ante un rechazo no se guarda nada. Para inspeccionar la base:
`sqlite3 primercraft.db "select corrida_id, identificador, organismo, length(secuencia) from referencias"`.

> **Ojo con el diseño:** `DA-04` dice que ninguna etapa usa la base y que solo el Servidor de corridas guarda el estado de
> la corrida. Esta persistencia es de la etapa, así que es una **excepción acotada a `DA-04`**, documentada en la Parte A
> (sección 5.2, decisión 7): es persistencia local de demostración, que en el sistema real guardaría el Servidor de corridas.

### Alcance y límites

- Cubre los dos criterios de aceptación de HU-04. Quedan fuera, como se documenta en el diseño: el rechazo por
  organismo que no coincide y el reintento por «NCBI no disponible» (`DA-03`). Ante cualquier falla inesperada (por
  ejemplo, sin conexión a NCBI), la pantalla muestra un aviso genérico.
- Los servicios externos (NCBI, broker) están detrás de interfaces y tienen implementación simulada.
