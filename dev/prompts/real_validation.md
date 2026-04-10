# Prompt — Real Validation

Actúa como motor activo para ejecutar la validación real guiada.

Sigue estrictamente:

- `AGENTS.md`
- `dev/workflow.md`
- `dev/guarantees/implementation_gate.md`

## Objetivo

Preparar y conducir un barrido real de pruebas antes del cierre
documental, consolidando todos los resultados en `real_validation.md`.

## Entradas obligatorias

1. iniciativa activa
2. `post_audit.md` con resultado `PASS`
3. contexto de comportamiento observable a validar

Si falta una entrada obligatoria:
- detenerse
- declarar `BLOQUEADO`

## Reglas

- No implementar código durante el barrido real.
- No arreglar el primer fallo en caliente, salvo bloqueo crítico que impida
  seguir probando.
- Completar el barrido real antes de proponer correcciones generales.
- Registrar por caso:
  - frase o acción
  - criterio cubierto
  - esperado
  - observado
  - resultado `PASS` / `FAIL` / `BLOQUEADO`
  - evidencia de logs, traces o salida visible
- Si hay fallos materiales, la decisión final debe ser `REABRIR_F3`.
- Si el barrido queda limpio, la decisión final debe ser `APTA_PARA_F6`.
- Si la validación real no aplica, debe declararse `NO_APLICA` con
  justificación explícita.

## Salida obligatoria

Genera un documento listo para guardar en:

`dev/records/initiatives/<initiative_id>/real_validation.md`

Con estas secciones:

1. Objetivo de validación
2. Entorno y alcance probado
3. Script de pruebas
4. Matriz de resultados
5. Hallazgos consolidados
6. Riesgos remanentes
7. Decisión final
