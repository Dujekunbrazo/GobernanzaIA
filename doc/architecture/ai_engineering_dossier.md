# Dossier de Gobernanza de Ingenieria IA

Este dossier amplía el marco técnico del repo para desarrollo asistido por IA.
No sustituye a `AGENTS.md` ni a `dev/workflow.md`; funciona como referencia de
profundidad cuando una tarea necesita más contexto.

## 1) Capa macro: MIT Concept-Sync

Objetivo:
- contener complejidad y evitar acoplamiento que rompa funcionalidades
  colaterales.

Principios:
- modelar funcionalidades como unidades coherentes orientadas a valor.
- minimizar dependencias directas entre unidades.
- orquestar interacciones por reglas/eventos trazables.
- priorizar incrementabilidad: cambios locales, impacto predecible.

Señales de sobrediseño:
- proliferación de unidades sin valor funcional claro.
- sincronizaciones demasiado finas que dificultan entender el flujo.
- necesidad de cargar demasiadas capas para explicar una acción simple.

Regla práctica:
- si no puede explicarse un flujo extremo a extremo en pocos pasos claros, la
  arquitectura necesita simplificación.

## 2) Capa micro: Clean Code

Objetivo:
- que el código pueda leerse y evolucionarse con bajo coste cognitivo.

Principios:
- nombres que revelan intención.
- funciones con responsabilidad principal única.
- límites de abstracción claros en cada función/módulo.
- errores tratados de forma explícita sin mezclar caminos.
- mejora incremental del área tocada (Boy Scout acotado al alcance).

Anti-patrón frecuente en IA:
- usar comentarios largos para justificar código opaco en lugar de
  refactorizarlo.

## 3) Capa cognitiva: Krug (Don't Make Me Think)

Objetivo:
- reducir carga cognitiva del usuario final y del integrador de API.

Principios:
- interfaces autoevidentes o al menos autoexplicativas.
- convenciones sobre creatividad arbitraria.
- texto mínimo, directo y accionable.
- mensajes de error diseñados para recuperación inmediata.

Aplicación a errores:
- decir qué falló.
- decir qué puede hacer el usuario ahora.
- evitar verbosidad técnica innecesaria.

## 4) Rendimiento como excepción controlada

Regla:
- en hot paths, se puede priorizar estructura orientada a máquina frente a
  pureza de abstracción.

Condición:
- la excepción solo es válida con evidencia (perfilado, benchmark o métrica).

Ejemplos de tácticas válidas en rutas críticas:
- menos indirectas dinámicas.
- estructuras de control directas.
- diseño de datos alineado con patrón de acceso real.

Riesgo a evitar:
- usar "rendimiento" como excusa sin datos para degradar mantenibilidad global.

## 5) Validación y pruebas (FIRST)

La IA no puede afirmar calidad sin evidencia.

FIRST:
- Fast: feedback rápido.
- Independent: pruebas aisladas.
- Repeatable: mismo resultado en entornos comparables.
- Self-validating: salida binaria clara.
- Timely: cercanas al cambio (idealmente antes o junto al código).

Efecto práctico:
- reduce miedo a cambiar.
- facilita refactor seguro.
- evita degradación silenciosa del sistema.

## 6) Cómo no se pisan las capas

- MIT gobierna forma global del sistema.
- Clean Code gobierna implementación local.
- Krug gobierna experiencia de uso.
- Rendimiento ajusta Clean Code solo en hot paths con evidencia.
- Validación decide si el cambio es aceptable.

Conflictos frecuentes y resolución:
- conflicto macro vs micro: prevalece MIT en límites inter-concepto.
- conflicto micro vs rendimiento: prevalece evidencia técnica en hot path.
- conflicto usabilidad vs implementación: la experiencia de usuario no debe
  depender de complejidad interna evitable.

## 7) Matriz rápida por tipo de tarea

- Cambio de arquitectura/runtime:
  - leer policy de ingeniería + este dossier si la decisión es estructural.
- Cambio local de código:
  - leer policy de ingeniería.
- Cambio UI/CLI/DX/API:
  - leer policy de ingeniería con foco Krug.
- Optimización de hot path:
  - leer policy de ingeniería con foco rendimiento + evidencia.

## 8) Qué NO pretende este dossier

- no define fases del workflow (`F1-F10`).
- no define gates de Ask/Plan/Implementation/Docs.
- no define límites de iteración de auditoría.

Eso vive en:
- `AGENTS.md`
- `dev/workflow.md`
- `dev/guarantees/*.md`
