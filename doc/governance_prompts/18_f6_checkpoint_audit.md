# F6 Checkpoint Audit

Quiero un checkpoint lateral de ejecucion en `F6`.

Usa la iniciativa activa y audita solo el tramo autorizado en el `phase_ticket`
y el `resume_packet`.

No es una auditoria formal `F7`. No emitas `PASS` ni `FAIL`.

Tu salida obligatoria es `execution_checkpoint.md` en el runtime del
orquestador, con uno de estos veredictos:

- `CHECKPOINT_OK`
- `CHECKPOINT_CON_HALLAZGOS`
- `BLOQUEO_DE_EJECUCION`

Contrasta:

- `plan.md`
- `execution.md`
- diff o commit reciente del tramo
- disciplina de alcance y write set

Si detectas desvio, legacy vivo, evidencia insuficiente o mezcla de cambios,
bloquea la liberacion del siguiente tramo.
