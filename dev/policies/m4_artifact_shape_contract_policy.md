# M4 Artifact Shape Contract Policy

## Proposito

Evitar iteraciones mecanicas entre `F1 -> F2` y `F3 -> F4` endureciendo el
contrato estructural de los artefactos base de `M4`.

Los artefactos de iniciativa no se tratan como texto libre. Se tratan como
documentos canónicos con shape, metadata y headings obligatorios.

## Ambito

Aplica como minimo a:

- `plan.md`
- `execution.md`
- `plan_audit.md`
- `post_audit.md`

Esta policy se centra en `plan.md` y `execution.md`, porque son los artefactos
producidos por el motor activo antes de pasar a auditoria formal.

## Reglas generales

1. La plantilla canónica es contrato de salida, no referencia orientativa.
2. Un artefacto con headings omitidos o metadata obligatoria ausente no es
   "semánticamente casi válido"; es estructuralmente inválido.
3. Un error de shape debe detectarse intra-fase antes de consumir la auditoría
   formal siguiente, siempre que el script pueda comprobarlo de forma
   determinista.
4. Si una sección existe en la plantilla, no puede borrarse. Si aplica poco,
   se rellena explícitamente con contenido mínimo.
5. Los prompts base de `F1` y `F3` deben enumerar headings y metadata exactos.

## Contrato de `plan.md`

Metadata obligatoria:

- `Initiative ID`
- `Modo: M4`
- `Estado`
- `Fecha`
- `Motor activo`
- `Motor auditor`
- `Rama`
- `Origen`
- `Etiqueta`

Headings obligatorios:

- `## Objetivo`
- `## Problema real`
- `## Resultado esperado`
- `## Evidencia base`
- `## Contexto tecnico relevante`
- `## Alcance`
- `## No-alcance`
- `## Restricciones`
- `## Supuestos`
- `## Riesgos principales`
- `## Superficies y modulos afectados`
- `## Decisiones ya tomadas`
- `## Dudas abiertas`
- `## Estrategia de implementacion`
- `## Plan por tramos`
- `## Validacion global prevista`
- `## Rollback`
- `## Definition of Done`
- `## Referencias`

## Contrato de `execution.md`

Metadata obligatoria:

- `Initiative ID`
- `Modo`
- `Fecha`
- `Motor activo`
- `Rama`

Headings obligatorios:

- `## Referencia al plan congelado`
- `## Estado operativo`
- `## Tramos o commits ejecutados`
- `## Evidencia de validacion`
- `## Riesgos detectados`
- `## Desvios respecto al plan`

## Vacios explicitos validos

Se considera valido que una sección quede minimamente poblada con una de estas
formas equivalentes:

- `N/A`
- `No aplica`
- `Sin desvios materiales`
- `Sin riesgos adicionales`
- texto mínimo equivalente, siempre que mantenga el heading

Lo que no es válido:

- omitir el heading
- fusionar dos headings bajo un titulo inventado
- sustituir metadata por narrativa libre

## Regla de ejecucion

El script `ping_pong` debe validar este contrato:

- inmediatamente tras `F1`, antes de abrir `F2`
- inmediatamente tras `F3`, antes de abrir `F4`

Si el artefacto falla por shape:

- no debe consumirse una auditoría formal de la fase siguiente
- el estado correcto es bloqueo o corrección intra-fase, según capacidad del
  script

## Relacion con otras policies

- `dev/policies/audit_finding_contract_policy.md` define el contrato de los
  hallazgos de auditoría formal
- esta policy define el contrato estructural previo para que el artefacto sea
  apto para entrar en auditoría
