---
title: Perfil de usuario — Investigador/a de biología molecular
---

# Perfil de usuario — Investigador/a de biología molecular

> Actor principal del TP1 . Es el único actor primario definido, por lo que es el único perfil que se elabora.
>
> **Convención de trazabilidad:** cada afirmación lleva entre corchetes su fuente en el TP1 (`[SRS §x]`, `[CU-xx]`, `[HU-xx]`) o la marca **`[Supuesto]`** si es una hipótesis del grupo que el TP1 no establece.

---

## 1. Por qué no hay perfil para el bioinformático/a

El SRS (§2.4) lo define como **stakeholder directo**, no como actor de ningún caso de uso: ninguna HU del TP1 lo tiene como sujeto. Su necesidad ("ingresa secuencia target y sale primers" desde un pipeline) corresponde a RF-02 / API propia, que no tiene HU desarrollada. Como se solicita el maquetado de pantallas que tengan HU que las respalde, **no se elabora su perfil**. Cuando actúa "como investigador" (SRS §2.4) queda cubierto por este perfil.

---

## 2. Perfil

| Aspecto | Descripción | Escenario de uso |
|---|---|---|
| **Quién es** | Biólogo/a molecular que diseña primers para sus propios experimentos de PCR/qPCR. | [SRS §2.4], [SRS §7 Actores] |
| **Dónde trabaja** | Laboratorios chicos o grupos de investigación **sin presupuesto** para suites pagas (Benchling, Geneious). | [SRS §2.2] |
| **Objetivo con el sistema** | Obtener pares de primers robustos (o validar los que ya tiene) **sin saltar entre NCBI, Primer3/Primer-BLAST y una planilla propia**, pasando de horas de trabajo manual a segundos. | [SRS §2.1], [SRS §2.4], [SRS §2.5] |
| **Tareas principales** | (a) Iniciar una corrida de diseño a partir de un identificador NCBI. (b) Validar un par de primers diseñado por otro medio. | [CU-01], [CU-03] |
| **Conocimiento del dominio** | **Alto.** Conoce Tm, %GC, GC clamp, ΔG, horquillas, dímeros y amplicón; hoy hace estos cálculos o los consulta en Primer3. | [SRS §2.1], [SRS §2.2] — el glosario §1.3 usa estos términos sin simplificarlos para el usuario |
| **Conocimiento técnico/informático** | **Medio.** Usa herramientas web (NCBI, Primer3, planillas). **No se asume** que programe ni que use línea de comandos (eso corresponde al bioinformático). | [SRS §2.1] (herramientas que usa hoy) · [Supuesto] (que no programa) |
| **Dispositivo** | Computadora de escritorio o notebook, con navegador web. Las herramientas que reemplaza (NCBI, Primer-BLAST) son web de escritorio. | [Supuesto] derivado de [SRS §2.1] |
| **Lugar** | Oficina o mesada del laboratorio, fuera de la campana/zona de trabajo húmedo. | [Supuesto] |
| **Urgencia** | Media. El diseño es previo a la síntesis de oligos; no es una tarea en tiempo real, pero sí quiere resultados "en segundos" y no esperar sin información. | [SRS §2.5] · [RF-06] (aviso de espera) |
| **Frustraciones actuales** | 1. Copiar y pegar entre pestañas; bajar el FASTA a mano. 2. El scoring de las herramientas es una **caja negra**. 3. No queda registro del criterio usado. 4. Primers que fallan en el laboratorio = reactivos perdidos. | [SRS §2.1], [SRS §2.2], [SRS §2.5], [HU-04 "No requiere intervención manual"] |
| **Limitaciones que condicionan el uso** | - Depende de NCBI: si el identificador no existe o no coincide con el organismo, no puede avanzar. - BLAST público tiene cupo de uso (cola y espera). | [RF-09], [CU-04 E1/E2], [RF-06] |
| **Qué necesita ver para confiar** | Las métricas **desglosadas** (Tm, %GC, GC clamp, ΔG de cada estructura), no solo un número final. | [SRS §1.2] (caja negra), [HU-05] |

### Implicancias de diseño que se desprenden del perfil

Estas implicancias se usan como **criterios** al pedir la generación de las pantallas (ver [`criterios_generacion.md`](criterios_generacion.md)).

1. **Lenguaje técnico sin simplificar**: usar Tm, ΔG, %GC, nt, pb tal cual. Explicarlos sería ruido para este usuario.
2. **Valores por defecto sugeridos** en los parámetros (RF-01), editables.
3. **Mensajes de error concretos** que digan qué campo falló y cómo corregirlo (HU-01.1, HU-04, CU-03 E1).
4. **Estado visible del proceso** mientras el sistema consulta NCBI y caracteriza (la espera no debe ser "a ciegas").
5. **Pantalla de escritorio** como diseño principal, en formato de panel: cada pantalla entra entera en la ventana, sin desplazarse. Como el dispositivo es un supuesto, la maqueta además se adapta a tablet y teléfono sin cambiar funciones (ver `criterios_generacion.md`).

---

## 3. Escenarios de uso

### 3.1 Escenario A — Diseñar primers para un gen (HU-01.1 → HU-04 → HU-02.1/02.2 → HU-05)

> Laura es investigadora en un laboratorio chico que necesita amplificar un fragmento de **BRCA1** en muestras humanas. Antes, buscaba el gen en NCBI, bajaba el FASTA, lo pegaba en Primer3 y anotaba los resultados en una planilla.
>
> Abre PrimerCraft Pro y elige **"Nueva corrida de diseño"**. Escribe el identificador `NM_007294`, selecciona *Homo sapiens* y deja los parámetros sugeridos (Tm 60 °C, %GC 50 %, longitud 20 nt). Al confirmar, el sistema valida el formato y le muestra el avance: obtiene la secuencia de NCBI Entrez, localiza el gen (coordenadas y hebra) y genera y caracteriza candidatos. Laura no tiene que descargar ningún archivo.
>
> Al terminar, ve una tabla de pares candidatos con la Tm, %GC, GC clamp, ΔG de horquillas y dímeros y el tamaño del amplicón de cada uno. Abre el detalle del mejor par para ver el amplicón simulado.

*Nombre y gen de ejemplo: [Supuesto] ilustrativo. El identificador y los parámetros salen del Gherkin de HU-01.1.*

### 3.2 Escenario B — Validar un par diseñado por otro medio (HU-03.1 → HU-03.2 → HU-03.3)

> Laura recibe de un colega un par de primers publicado en un paper y quiere saber si sirve para su target. Elige **"Validar primer existente"**, pega las secuencias forward y reverse, el organismo y el identificador del target. El sistema valida que las secuencias usen solo caracteres IUPAC, obtiene la referencia, localiza el gen y le informa si los primers hibridan en las posiciones y la orientación esperadas, junto con su caracterización completa.

---

## 4. Flujos de navegación

Las pantallas se nombran **UI-1 a UI-5**.

### Flujo de navegación A: Nueva corrida de diseño de primers (Escenario A)

1. El investigador accede al sistema y selecciona la opción de iniciar una nueva corrida, abriendo la pantalla de configuración inicial (UI-1).   
2. Ingresa el identificador NCBI del target y el organismo, y revisa o ajusta los parámetros de diseño sugeridos por defecto, como Tm objetivo, porcentaje de GC y longitud del primer.   
3. Si el identificador tiene un formato inválido o los parámetros están fuera de rango, el sistema retiene al usuario en la pantalla actual (UI-1) y muestra alertas específicas sobre los campos erróneos para su corrección inmediata.   
4. Al enviar el formulario con datos válidos, el usuario avanza a la pantalla de progreso de la corrida (UI-2). En esta interfaz, visualiza el avance secuencial de los procesos internos sin necesidad de recargar la página: obtención de la secuencia FASTA desde NCBI, localización de las coordenadas del gen y generación automática de candidatos.   
5. Si la API de NCBI no encuentra el target ingresado, el flujo se detiene y la pantalla de progreso (UI-2) notifica el error, permitiendo al usuario regresar al inicio para verificar el identificador.   
6. Una vez que el sistema finaliza la caracterización de los candidatos exitosamente, el usuario es redirigido de forma automática a la pantalla de resultados (UI-3).   En la pantalla de resultados (UI-3), el investigador visualiza una tabla con los pares de primers generados y sus métricas termodinámicas desglosadas (Tm real, %GC, GC clamp, ΔG de estructuras secundarias). Puede desplegar el detalle de cualquier par para ver la simulación del amplicón esperado. Si ningún candidato cumplió los parámetros, se informa en esta misma vista.  

### Flujo de navegación B: Validación de un par de primers existente (Escenario B)

1. El investigador selecciona la opción "Validar primer existente", lo que despliega la pantalla de ingreso para validación externa (UI-4).Ingresa manualmente las secuencias de los primers forward y reverse, junto con el organismo y el identificador del target contra el cual desea validarlos.   
2. Si alguna de las secuencias incluye caracteres que no pertenecen al código IUPAC válido, el sistema bloquea el avance y muestra el error en la misma pantalla (UI-4) para que sea subsanado.   
3. Tras validar el formato, el usuario transiciona a la pantalla de progreso (UI-2 compartida). Allí observa cómo el sistema consulta la referencia en NCBI y localiza el gen de interés.   
4. En caso de fallar la obtención de datos externos (por ejemplo, identificador inexistente), el error se muestra en pantalla y el flujo permite volver a la vista de carga (UI-4).   
5. Finalizado el cálculo de hibridación, el sistema dirige al usuario a la pantalla de resultado de validación (UI-5).En esta vista (UI-5), el investigador corrobora si el par ingresado hibrida correctamente en las posiciones y orientaciones esperadas sobre el target. Además, visualiza la caracterización completa de las métricas termodinámicas y estructurales del par; si las secuencias no hibridan, la advertencia se expone en este mismo panel. 

### 4.2 Pantallas resultantes

| Pantalla | Archivo de maqueta | HU que respalda |
|---|---|---|
| UI-1 · Nueva corrida de diseño | `hu-01-1_nueva-corrida-diseno.html` | HU-01.1 |
| UI-2 · Progreso de la corrida | `hu-04_hu-02-1_progreso-corrida.html` | HU-04, HU-02.1 y HU-03.2 (compartida); HU-02.2 como paso |
| UI-3 · Resultados de candidatos | `hu-05_resultados-candidatos.html` | HU-05 |
| UI-4 · Validar primer existente | `hu-03-1_validar-primer.html` | HU-03.1 |
| UI-5 · Resultado de validación | `hu-03-3_resultado-validacion.html` | HU-03.3 |


