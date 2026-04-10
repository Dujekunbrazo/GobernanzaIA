Codex, necesito que audites el siguiente `plan.md` generado por Claude.

Tu objetivo es verificar que el plan es ejecutable, coherente, acotado y seguro
antes de congelarlo.

## Debes revisar
1. coherencia entre problema, evidencia, alcance y estrategia
2. ausencia de alcance extra o huecos materiales
3. calidad del plan por tramos o commits
4. validacion prevista y rollback
5. riesgos tecnicos, operativos y de integracion
6. ausencia de duplicidad con weekly, backlog o narrativa conversacional
7. cumplimiento de la gobernanza del repo

## Reglas obligatorias
- no reescribas el plan
- no implementes fixes
- no uses la categoria `observaciones`
- toda debilidad material debe ir a `Hallazgos`
- si emites `PASS`, justifica explicitamente por que no queda ningun hallazgo pendiente

## Entregable esperado
Devuelve un artefacto listo para guardar en:

`dev/records/initiatives/<initiative_id>/plan_audit.md`

Con estas secciones:
- `## Hallazgos`
- `## Justificacion del veredicto`
- `## Escalado de remediacion`
- `## Condicion para implementacion`

Ademas de escribirlo, replica el artefacto completo al final de tu respuesta en
un bloque ```md``` para recuperacion manual si la escritura falla.

## Plan a auditar
[PEGA AQUI EL PLAN DE CLAUDE]
