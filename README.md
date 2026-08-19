<div align="center">

# PrimerCraft Pro

**Diseño y puntuación automática de primers para PCR/qPCR**

**Trabajo Final — Ingeniería de Software (2026)**

</div>

---

## Integrantes

- Barbara Sara
- Vergara Emilia
- Rios Matias

**Carrera:** Licenciatura en Bioinformática
**Institución:** Facultad de Ingeniería, Universidad Nacional de Entre Ríos (FIUNER)

---

## Índice

aun no realizado 
---

## Sobre el proyecto

**PrimerCraft Pro** es una herramienta que diseña y puntúa automáticamente pares de primers para PCR/qPCR a partir de una secuencia blanco, integrando en un solo flujo:

- **Cálculo termodinámico** mediante el modelo Nearest-Neighbor
- **Detección de estructuras secundarias** (hairpins, dímeros)
- **Simulación del amplicón**
- **Verificación de especificidad**

Está pensada para investigadores/as de biología molecular que hoy alternan entre múltiples herramientas dispersas (NCBI, Primer3/Primer-BLAST, verificadores de estructura) para llegar al mismo resultado, y para quienes necesitan diseñar primers en lote sin repetir el proceso manual target por target.

---

## Modelo de ciclo de vida

El proyecto adopta un modelo **incremental, con iteraciones cortas alineadas al cronograma de la materia** (una iteración por TP: requerimientos, UX, arquitectura, diseño, pruebas).

Esta elección responde a atributos propios del proyecto:

1. **Disponibilidad del equipo** — el equipo (2-3 personas) está condicionado al calendario semanal de la cursada, lo que hace inviable un modelo secuencial de una sola entrega final.
2. **Valor evaluable temprano** — cada instancia de presentación exige mostrar avances funcionales de forma temprana.
3. **Gestión de riesgo externo** — el riesgo más relevante del proyecto, la integración con APIs de terceros (NCBI), se gestiona mejor incorporándola de a poco y con mocks documentados antes de depender de un servicio real con límites de uso estrictos.

---

## Documentación

| Documento | Descripción |
|---|---|
| [`docs/requirements/srs.md`](docs/requirements/srs.md) | Especificación de Requerimientos de Software (visión y alcance) |

---

## Licencia

Proyecto académico desarrollado en el marco de la materia **Ingeniería de Software** (FIUNER, 2026). Uso educativo.
