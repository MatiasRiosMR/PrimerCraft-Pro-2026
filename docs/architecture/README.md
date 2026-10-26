---
title: Arquitectura
nav_order: 2
has_children: true
permalink: /architecture/
---

# Arquitectura

Modelos y especificación del sistema: diagrama de contexto, modelo de dominio y documento de especificación de arquitectura (vistas C4 de contenedores, componentes y despliegue). Los diagramas están en bloques Mermaid dentro de cada `.md`, y cada documento enlaza también a su fuente editable.

## Documentos

| Documento | Contenido |
|---|---|
| [`contexto_inicial.md`](contexto_inicial.md) | Diagrama de contexto DFD: [Nivel 0](contexto_inicial.md#nivel-0) (sistema y entidades externas) y [Nivel 1](contexto_inicial.md#nivel-1) (procesos y almacenes, incluido el almacén de corridas de diseño) |
| [`modelo-dominio-inicial.md`](modelo-dominio-inicial.md) | Modelo de dominio: conceptos, relaciones y cardinalidades con el vocabulario del dominio |
| [`arquitectura.md`](arquitectura.md) | Documento de especificación de arquitectura: drivers, estrategia de solución, vistas C4 (contenedores, componentes y [despliegue](arquitectura.md#8-vista-de-despliegue)), decisiones `DA-xx` y trazabilidad |

## Relacionado

- Requerimientos que modelan estos diagramas: [`../requirements/srs.md`](../requirements/srs.md)
