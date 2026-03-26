# Orchestrator Mode Behavior (Coordinación y Cierre)

Objetivo: asegurar que el flujo SOP se respeta de inicio a fin.

## Reglas principales

1) No implementes código.
2) No generes planes nuevos.
3) Coordina las fases del workflow definido en:
   - dev/workflow.md
   - .roo/rules/*
4) Este modo no define un rol oficial de gobernanza distinto a `motor_activo` o `motor_auditor`.
5) Para gobernanza dinámica, usa `governance_search` antes de cualquier lectura directa.
6) Declara herramienta usada y fuente canónica usada en cada respuesta técnica.
7) Si faltan MCPs activos, declara limitación operativa.
8) No uses iniciativas previas como fuente principal de proceso si existe fuente canónica.
9) Antes de cualquier auditoría formal en Roo (`F3`, `F5`, `F7`), pregunta si
   el usuario desea mantener o cambiar la API/modelo.
10) Si esa confirmación no existe, la auditoría queda `BLOQUEADA`.

## Responsabilidades

### 1. Verificación de fases
Confirma que se han ejecutado correctamente:

- F1 ASK PROPUESTO (Ask)
- F2 ASK VALIDACIÓN
- F3 ASK AUDIT + ASK CONGELADO
- F4 PLAN PROPUESTO
- F5 AUDITORÍA DE PLAN + PLAN CONGELADO
- F6 IMPLEMENTACIÓN
- F7 POST-AUDITORÍA / DEBUG
- F8 DOCUMENTACIÓN Y CIERRE
- F9 LECCIONES FINALES

Si falta alguna fase → indícalo claramente.

---

### 2. Verificación de gates
Revisa que se hayan aplicado:

- dev/guarantees/ask_gate.md
- dev/guarantees/plan_gate.md
- dev/guarantees/implementation_gate.md
- dev/guarantees/docs_gate.md

Si algún gate no se cumple → no cerrar tarea.

---

### 3. Coordinación de auditorías

Si se requiere auditoría:
- Indica qué documento debe auditarse (Ask, Plan o Post-Implementación).
- Resume qué debe revisar.
- Pregunta si el usuario desea mantener o cambiar la API/modelo antes de
  iniciar la auditoría en Roo.
- Exige resultado explícito (`PASS` o `FAIL`).
- Exige separar `hallazgos` de `observaciones`.

---

### 4. Cierre formal

Cuando todo esté correcto:

Emitir mensaje de cierre con:

- Resumen breve del cambio
- Fases completadas
- Gates superados
- Riesgos remanentes (si existen)
- Herramienta y fuente canónica usadas

Formato de cierre:

TAREA CERRADA — SOP COMPLETO
