# Diagrama de contexto — PrimerCraft Pro

Diagrama de contexto DFD, Nivel 0 y Nivel 1.

**Fuente (editable):**
- Nivel 0: https://mermaid.ai/app/projects/560fd739-e2f1-40c9-90d8-4d60dadc6181/diagrams/76e3b407-d329-484d-9f7f-064e26a7c54d/version/v0.1/edit?entryPoint=Share+link
- Nivel 1: https://mermaid.ai/app/projects/560fd739-e2f1-40c9-90d8-4d60dadc6181/diagrams/22a5d970-885a-4ae2-b093-6b9a4a6d46a1/version/v0.1/edit?entryPoint=Share+link

## Nivel 0

```mermaid
---
config:
  theme: base
---
%%{init: {'theme':'base','themeVariables':{'fontSize':'13px','primaryColor':'#EEF2FF','primaryBorderColor':'#6366F1','primaryTextColor':'#1E1B4B','lineColor':'#94A3B8'},'flowchart':{'curve':'basis','nodeSpacing':70,'rankSpacing':150,'useMaxWidth':true}}}%%
flowchart LR
    INV["Investigador/a"]:::externa
    P(("0<br/>PrimerCraft Pro")):::proceso
    NCBI["NCBI Entrez / BLAST"]:::externa
    VAR["Bases de Variantes Poblacionales<br/>dbSNP / Ensembl"]:::externa

    INV -->|"solicitud de diseño:<br/>target o lista + parámetros"| P
    INV -->|"solicitud de validación de<br/>un primer ya existente"| P
    P -->|"primers diseñados y puntuados, desglose de scoring,<br/>alertas de variantes, simulación de amplicón,<br/>reporte trazable"| INV
    P -->|"mensajes de error de<br/>identificación / entrada inválida"| INV

    P -->|"consulta de secuencia de referencia"| NCBI
    P -->|"consulta de especificidad"| NCBI
    NCBI -->|"secuencia FASTA"| P
    NCBI -->|"resultado de BLAST"| P

    P -->|"consulta de variantes en<br/>región de anclaje"| VAR
    VAR -->|"SNPs y frecuencias<br/>poblacionales conocidas"| P

    classDef proceso fill:#4F46E5,stroke:#312E81,stroke-width:2px,color:#FFFFFF;
    classDef externa fill:#FFFFFF,stroke:#475569,stroke-width:2px,color:#0F172A;
```

## Nivel 1

```mermaid
%%{init: {'theme':'base','themeVariables':{'fontSize':'13px','primaryColor':'#EEF2FF','primaryBorderColor':'#6366F1','primaryTextColor':'#1E1B4B','lineColor':'#94A3B8','clusterBkg':'#F8FAFC','clusterBorder':'#CBD5E1'},'flowchart':{'curve':'basis','nodeSpacing':75,'rankSpacing':125,'useMaxWidth':true}}}%%
flowchart LR
    INV["Investigador/a"]:::externa

    subgraph SYS ["Límite del sistema — PrimerCraft Pro"]
      direction LR
      P1(("1<br/>Preparar target y<br/>secuencia de referencia")):::proceso
      P2(("2<br/>Generar y caracterizar<br/>candidatos de primers")):::proceso
      P3(("3<br/>Verificar exposición a variantes")):::proceso
      P4(("4<br/>Puntuar, explicar y<br/>registrar la corrida")):::proceso
      D2[("D2 · Configuración de scoring")]:::almacen
      D1[("D1 · Corridas de diseño")]:::almacen
    end

    subgraph EXT ["Servicios externos"]
      direction TB
      NCBI["NCBI Entrez / BLAST"]:::externa
      VAR["Bases de Variantes Poblacionales<br/>dbSNP / Ensembl"]:::externa
    end

    %% --- entrada del investigador (nombres idénticos al Nivel 0) ---
    INV -->|"solicitud de diseño:<br/>target o lista + parámetros"| P1
    INV -->|"solicitud de validación de<br/>un primer ya existente"| P2

    %% --- pipeline interno ---
    P1 -->|"secuencia de referencia +<br/>parámetros de diseño + <br/> anotacion y versión"| P2
    P2 -->|"candidatos con Tm, %GC, ΔG de<br/>estructuras y amplicón simulado"| P3
    P3 -->|"candidatos con especificidad,<br/> exposición a variantes y marca de variante de alto riesgo en 3'"| P4
    P4 -->|"solicitud de diseño alternativo:<br/>posición a evitar (variante alta<br/>frecuencia en extremo 3')"| P2

    %% --- servicios externos (nombres idénticos al Nivel 0) ---
    P1 -->|"consulta de secuencia de referencia"| NCBI
    NCBI -->|"secuencia FASTA + <br/> Anotacion y versión"| P1
    P2 -->|"consulta de especificidad"| NCBI
    NCBI -->|"resultado de BLAST"| P2
    P3 -->|"consulta de variantes en<br/>región de anclaje"| VAR
    VAR -->|"SNPs y frecuencias<br/>poblacionales conocidas"| P3

    %% --- almacenes y salidas (nombres idénticos al Nivel 0) ---
    D2 -->|"pesos y umbrales de scoring"| P4
    P4 -->|"registro de corrida: parámetros, umbrales,<br/>versión de datos, resultados"| D1
    P1 -->|"mensajes de error de<br/>identificación / entrada inválida"| INV
    P4 -->|"primers diseñados y puntuados, desglose de scoring,<br/>alertas de variantes, simulación de amplicón,<br/>reporte trazable"| INV

    classDef proceso fill:#4F46E5,stroke:#312E81,stroke-width:2px,color:#FFFFFF;
    classDef externa fill:#FFFFFF,stroke:#475569,stroke-width:2px,color:#0F172A;
    classDef almacen fill:#ECFEFF,stroke:#0E7490,stroke-width:2px,color:#083344;
```
