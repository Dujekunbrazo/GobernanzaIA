# Audit Finding Contract Policy

## Proposito

Reducir iteraciones entre `F1 -> F2 -> F3 -> F4` haciendo que toda auditoria
formal produzca hallazgos pequenos, tipados, accionables y verificables.

La auditoria formal no debe limitarse a diagnosticar. Debe indicar el cambio
minimo necesario para cerrar el hallazgo y el criterio binario que confirma el
cierre.

## Ambito

Aplica a:

- `F2` (`plan_audit.md`)
- `F4` (`post_audit.md`)

No redefine `F5`. Tampoco autoriza implementar fixes durante la auditoria.

## Principios

1. Un `FAIL` incompleto es peor que un `FAIL` duro: si el auditor no puede
   decir exactamente que cerrar, la salida no es apta para remediacion.
2. La auditoria debe identificar deficiencias, no mezclar revision e
   implementacion.
3. Cada hallazgo debe ser minimamente suficiente para una remediacion atomica.
4. El cierre de un hallazgo debe ser verificable con un criterio binario.
5. El alcance de reejecucion debe quedar acotado para evitar loops ciegos.
6. Si el plan define invariantes congeladas, `F4` debe auditar primero contra
   esas invariantes; si no existen, audita contra `plan.md` congelado,
   `execution.md` y la evidencia de validacion registrada.

## Tipos canonicos de hallazgo

Todo hallazgo formal debe declarar un `Tipo:` tomado de esta taxonomia minima:

- `PLAN_MISMATCH`
- `EXECUTION_MISMATCH`
- `EVIDENCE_MISSING`
- `SCOPE_DRIFT`
- `LEGACY_LEFT_BEHIND`
- `INVARIANT_VIOLATION`
- `ARTIFACT_CONTRACT_BROKEN`

Si ningun tipo aplica claramente, el estado correcto es `BLOQUEADO` hasta poder
clasificar el hallazgo con precision.

## Contrato minimo por hallazgo

Todo hallazgo numerado en `F2` o `F4` debe incluir, en este orden logico:

- `Tipo:`
- `Artefacto afectado:`
- `Seccion exacta:`
- `Archivos permitidos:`
- `Archivos prohibidos:`
- `Cambio minimo requerido:`
- `Criterio de cierre:`
- `Rerun scope:`
- `Reapertura requerida:`
- `Evidencia:`

### Reglas por campo

- `Tipo:` clasifica el fallo y no puede quedar vacio.
- `Artefacto afectado:` identifica el artefacto primario a corregir.
- `Seccion exacta:` acota la seccion, bloque o contrato concreto a tocar.
- `Archivos permitidos:` lista el write set minimo necesario para la
  remediacion.
- `Archivos prohibidos:` evita ampliaciones encubiertas de alcance.
- `Cambio minimo requerido:` manda el cierre minimo; no debe pedir mejoras
  vagas como "mejorar", "revisar" o "pulir".
- `Criterio de cierre:` debe ser binario y verificable.
- `Rerun scope:` indica la reejecucion minima necesaria:
  `F2`, `F4`, `F4_FINAL`, `F4 + F5`, `F4_FINAL + F5` o `n/a`.
- `Reapertura requerida:` indica la fase que debe reabrirse:
  `F1`, `F3`, `ninguna` o la fase previa estrictamente necesaria.
- `Evidencia:` ancla el hallazgo en artefactos, rutas, comandos, logs o
  resultados reales.

## Regla de veredicto

- `PASS`: sin hallazgos materiales ni pendientes.
- `FAIL`: existe al menos un hallazgo material pendiente.

No se permite `PASS` con hallazgos abiertos, ni `FAIL` con hallazgos sin
contrato de remediacion.

## Regla anti-iteracion vaga

Si una auditoria emite `FAIL` sin `Cambio minimo requerido` o sin `Criterio de
cierre`, el artefacto es invalido y debe tratarse como conflicto mecanico del
artefacto de auditoria, no como una auditoria reutilizable.

## Regla de escalado

Una observacion no bloqueante solo es admisible cuando no deja:

- legacy conviviendo con canon
- dualidad de contrato
- cleanup estructural dentro del scope
- evidencia material pendiente para verificar el cierre

Si alguno de esos casos aparece, el punto debe escalar a hallazgo bloqueante.

## SAFE_AUDITOR_AUTOFIX

Para reducir iteraciones mecanicas de gobernanza, `motor auditor` puede corregir
directamente ciertos fallos del propio expediente y reauditar en el mismo loop,
sin devolver el control al motor activo.

Condiciones minimas:

- la auditoria ya emitio un `FAIL` valido
- todos los hallazgos elegibles afectan solo a artefactos del expediente o a
  reconciliaciones mecanicas ya decididas entre `plan.md`, DoD, write set,
  sidecars, `execution.md`, `plan_audit.md` o `post_audit.md`
- `Archivos permitidos:` queda acotado a esos artefactos de iniciativa y, si
  aplica, al archivo de gobernanza/tooling ya implicado por el DoD o el write
  set congelado
- no se toca codigo de producto, tests, runtime, prompts canonicos, policies ni
  alcance sustantivo
- `Rerun scope:` coincide exactamente con la fase auditada en curso
- `Reapertura requerida:` es `ninguna` o la fase previa canonica (`F1` en
  `F2`, `F3` en `F4`) cuando el fix sigue siendo puramente mecanico y local al
  expediente

Casos tipicos elegibles:

- `ARTIFACT_CONTRACT_BROKEN`
- `EVIDENCE_MISSING`
- en `F2`, `PLAN_MISMATCH` cuando la remediacion se limita a `plan.md`
- en `F4`, `EXECUTION_MISMATCH` cuando la remediacion se limita a
  `execution.md`
- `SCOPE_DRIFT` o `PLAN_MISMATCH` cuando el plan ya exigia el resultado y el
  fix solo reconcilia trazabilidad/write set/DoD sin decision material nueva
- `INVARIANT_VIOLATION` cuando el cambio requerido sigue siendo mecanico y
  local al expediente
- `LEGACY_LEFT_BEHIND` cuando el cleanup se limita al expediente

Casos no elegibles:

- cambios de producto o de comportamiento observable
- reinterpretacion del alcance o del objetivo de la iniciativa
- fixes de codigo o de validacion runtime
- relajar criterios PASS/FAIL, eliminar restricciones o cambiar decisiones
  materiales

Reglas:

- el autofix del auditor debe ser minimo, mecanico y trazable
- si el fallo es de artefactos de iniciativa y cumple estas condiciones, motor auditor
  debe corregirlo en el acto; no se devuelve a motor activo por ceremonia
- tras el autofix, la fase debe reauditarse inmediatamente
- si el autofix no cierra el hallazgo, el flujo vuelve al comportamiento
  normal de `FAIL`
- esta via no autoriza a `motor auditor` a cambiar producto; solo expediente y
  reconciliaciones mecanicas de gobernanza ya cerradas
