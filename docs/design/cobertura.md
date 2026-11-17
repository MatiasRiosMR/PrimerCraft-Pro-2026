---
title: Cobertura de las pruebas
parent: Diseño detallado
nav_order: 2
---

# Parte C — Reporte de cobertura y análisis

## Cómo se mide

```bash
pytest --cov --cov-branch
```

Se mide el paquete `src/` **sin** la interfaz gráfica ni el arranque (`.coveragerc`): la consigna pide que las pruebas unitarias no pasen por la interfaz, y `arranque.py` solo arma los objetos concretos.

## Resultado

| Momento | Pruebas | Sentencias | Cobertura de sentencias | Ramas |
|---|---|---|---|---|
| Primera corrida (Parte B) | 15 | 164 | 90 % | — |
| Después de revisar el reporte y alinear con el diseño | 22 | 156 | 100 % | 32 de 32 |
| Después de calcular la complejidad ciclomática | 24 | 156 | 100 % | 32 de 32 |
| Después de romper el código a propósito | 29 | 156 | 100 % | 32 de 32 |

Por archivo, en la ejecución final:

| Archivo | Sentencias | Sin cubrir | Ramas | Cobertura |
|---|---|---|---|---|
| `aplicacion/controlador_obtencion_referencia.py` | 25 | 0 | 0 | 100 % |
| `aplicacion/gestion_de_excepciones.py` | 7 | 0 | 2 | 100 % |
| `aplicacion/puertos.py` | 18 | 0 | 0 | 100 % |
| `dominio/informacion_genoma.py` | 13 | 0 | 4 | 100 % |
| `infraestructura/adaptador_ncbi_entrez.py` | 55 | 0 | 24 | 100 % |
| `infraestructura/consumidor_de_etapa.py` | 13 | 0 | 2 | 100 % |
| `infraestructura/publicador_de_etapa.py` | 6 | 0 | 0 | 100 % |
| `infraestructura/repositorio_referencias.py` | 19 | 0 | 0 | 100 % |
| **Total** | **156** | **0** | **32** | **100 %** |

## Qué no estaba cubierto y qué se hizo

La primera corrida dejó dos zonas sin cubrir en `adaptador_ncbi_entrez.py` (69 %):

- **Líneas 17 a 40, `consultar_entrez`:** es el transporte real, que pide los datos a NCBI por internet. Ninguna prueba lo ejecutaba porque las pruebas no usan la red. Se agregaron `CP-16` y `CP-17`, que reemplazan `requests.get` por respuestas armadas a mano (y la espera de 0,4 s entre pedidos) y recorren el camino de éxito y el de «sin resultados».
- **Línea 69, el corte ante un segundo registro FASTA:** nadie probaba que el adaptador ignore los registros que siguen al primero. Se agregó `CP-15`.

Al revisar el código también se encontró que un identificador como `BRCA1 OR TP53` cambiaba la búsqueda en NCBI. El adaptador, que es el único que conoce la sintaxis de NCBI, ahora lo trata como target no encontrado sin consultar (`CP-20`, `CP-21`) y descarta espacios sobrantes (`CP-22`).

También se agregaron `CP-09` a `CP-14` para las ramas de la entidad, de la gestión de excepciones y del consumidor que las pruebas de los criterios no ejercitaban por sí solas (por ejemplo, el alfabeto IUPAC o el error desconocido).

Al calcular la complejidad ciclomática (ver abajo) apareció algo que el 100 % de ramas no muestra: dos caminos de condición sin una prueba propia. `CP-23` cubre el caso del FASTA ausente en `_leer_campos_conocidos` y `CP-24`, el de `NM_000518` con otro organismo en `consultar_grabacion`. No cambian el porcentaje, porque las ramas ya estaban recorridas por otras pruebas; sí hacen que cada camino tenga su caso.

## Si las pruebas detectan errores: cambios deliberados en el código

El 100 % de cobertura dice qué se ejecutó, no qué se verificó. Para comprobar que las pruebas detectan errores se rompió el código a propósito de 15 maneras, una por vez, en una copia temporal, y se corrió `pytest` después de cada cambio (por ejemplo: no publicar el aviso, marcar el aviso como reintentable, aceptar caracteres fuera de IUPAC, no cortar en el segundo registro, confirmar el mensaje también en el éxito, buscar por otro campo en NCBI, mezclar las columnas de SQLite). Con las 24 pruebas anteriores, **5 cambios pasaron sin que ninguna prueba fallara**, todos en un código que ya estaba cubierto al 100 %:

| Cambio que no se detectaba | Por qué | Qué se hizo |
|---|---|---|
| Buscar por `[Title]` y no por `[Accession]`, o por otro organismo | El `requests.get` falso ignoraba los parámetros | `CP-25` comprueba la búsqueda que se arma |
| Pedir el último resultado de la búsqueda y no el primero | Las pruebas tenían un solo resultado | `CP-25` usa dos resultados y exige el primero |
| Quitar la espera entre pedidos (NCBI admite 3 por segundo) | La espera se anulaba en las pruebas y no se registraba | `CP-27` registra las esperas |
| Guardar la anotación en la columna del organismo en SQLite | `CP-08` solo miraba tres columnas | `CP-08` compara las cinco |

También se reforzaron `CP-13` (ahora verifica que el aviso se publique **antes** de confirmar el mensaje, como pide `DA-02`) y la medida de `EC-04`, que se probaba con un solo ejemplo: `CP-26` agrega tres variantes del formato del FASTA. Con las pruebas actuales los 15 cambios se detectan. Esto no demuestra que no haya otros errores no detectados, pero sí que lo que cubre el reporte también se verifica.

## Pruebas que pasan pero verifican poco

Que una línea esté cubierta no prueba que su resultado sea correcto. Estas pruebas son las más débiles:

- `CP-05` y `CP-12` solo comprueban que `obtenida` sea verdadera: no miran el contenido de la referencia.
- `CP-16` comprueba solo el comienzo de las dos respuestas: no verifica que la secuencia completa se conserve.
- `CP-18` depende del archivo grabado de `NM_000518`: si cambia la grabación, cambia el 628.

Se dejaron así porque cada una apunta a un único comportamiento (que el controlador no cambie, que el consumidor traduzca el JSON, que el camino real devuelva ambas respuestas) y el contenido ya lo verifican `CP-01` y `CP-04`.

## Lo que la cobertura no dice

- **El 100 % se calcula sin la interfaz ni el arranque.** Esas partes no tienen reglas de negocio y se probaron a mano en el navegador: la pantalla carga, obtiene `NM_000518` (628 nt), rechaza `NM_999999` y `BRCA1 OR TP53`, muestra el estado «consultando» y la falla inesperada. Además se pasó una auditoría automática de accesibilidad (axe-core, WCAG 2.2 AA) en los estados inicial, éxito y rechazo, sin violaciones.
- **No hay pruebas automáticas contra el servicio real de NCBI.** Se probó a mano en modo real con `NM_007294`. Automatizarlo depende de internet y de la cuota de NCBI.
- **Fuera del alcance de `HU-04`**, y por lo tanto sin pruebas: el reintento por «NCBI no disponible» (`DA-03`), el rechazo cuando el organismo no coincide con el identificador, el descarte de mensajes repetidos por `idMensaje` (`DA-02`) y la publicación de `referencia.localizada` (`HU-02.1`).

## Complejidad ciclomática

La tabla completa (cada operación de `HU-04` con sus decisiones, su complejidad y la prueba de cada camino) está en [`diseno-detallado.md`, sección 7.3](diseno-detallado.md#73-complejidad-ciclomática). Resumen:

| Operación | Complejidad |
|---|---|
| `AdaptadorNcbiEntrez._leer_campos_conocidos` | 8 |
| `consultar_grabacion` | 4 |
| `consultar_entrez`, `AdaptadorNcbiEntrez.obtener_referencia`, `InformacionGenoma.__init__` | 3 |
| `ControladorObtencionReferencia.obtener`, `GestionDeExcepciones.clasificar`, `ConsumidorDeEtapa.procesar` | 2 |

Ninguna llega a 10, el umbral a partir del cual conviene dividir una operación. La cobertura de ramas del reporte de arriba (32 de 32) confirma que no queda ninguna decisión sin recorrer. `consultar_entrez` tiene un camino que no existe: su ciclo recorre una tupla fija de dos pedidos y nunca queda sin vueltas.
