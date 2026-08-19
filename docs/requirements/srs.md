# SRS — PrimerCraft Pro

## 1. Visión y alcance

**Dominio y problema.** PrimerCraft Pro opera en biología molecular, en el diseño y evaluación de primers (cebadores) para PCR/qPCR. El problema no es la ausencia de herramientas de cálculo: Primer3 y NCBI Primer-BLAST son estándares de facto, validados desde hace más de 25 años. El problema real, verificable en la documentación pública de NCBI, es doble: (1) **fragmentación del flujo de trabajo** — el/la investigador/a debe alternar entre múltiples sitios web (buscar y descargar la secuencia de referencia en NCBI, subirla a Primer3/Primer-BLAST para el diseño, verificar estructuras secundarias en una herramienta distinta) sin que exista una plataforma que integre estos pasos; y (2) **falta de soporte para automatización a escala** — la documentación de NCBI BLAST (Common URL API) advierte que su servicio público está pensado para uso interactivo, limita a quienes superan 100 búsquedas en 24 horas y recomienda a proyectos de alto volumen usar una interfaz RESTful propia o BLAST en un proveedor cloud, lo que impide hoy diseñar primers en lote para paneles (diagnóstico multiplex, vigilancia epidemiológica, genotipado) sin repetir el proceso manual target por target.

**Datos.** El sistema trabaja sobre secuencias de ácidos nucleicos en formato FASTA, con validación de caracteres IUPAC, cargadas manualmente por el/la investigador/a.

**Usuarios y stakeholders.** Detallados en la sección 2; el usuario principal es el/la investigador/a de biología molecular.

**Valor.** Si el sistema funciona, el/la investigador/a diseña y prioriza primers confiables en un único flujo, con menos iteraciones fallidas en el banco húmedo y sin alternar manualmente entre herramientas dispersas.

**Alcance realista (MVP de este cuatrimestre).** Carga y validación de secuencia FASTA (IUPAC), cálculo de propiedades termodinámicas (Tm Nearest-Neighbor, %GC, GC clamp, penalización por repeticiones), chequeo de estructuras secundarias (hairpins, self-dimers) por ΔG, puntuación y sugerencia de los 3 mejores pares Forward/Reverse, y simulación de PCR in silico (amplicón teórico y tamaño esperado). Detalle completo de lo excluido en la sección 8.

## 2. Stakeholders y usuarios

| Rol | Tipo | Interés principal |
|---|---|---|
| Investigador/a de biología molecular | Usuario principal | Diseñar primers confiables en menos tiempo, con menos iteraciones fallidas en el banco húmedo |
| Docente / director/a de laboratorio | Stakeholder indirecto | Confiar en que el criterio de diseño usado por el equipo es riguroso y auditable |
| Bioinformático/a de soporte | Stakeholder indirecto | Poder exportar o integrar el resultado en un pipeline propio |
| Laboratorio de síntesis de oligonucleótidos | Stakeholder indirecto | Recibir una secuencia final sin ambigüedades (caracteres IUPAC válidos) |


