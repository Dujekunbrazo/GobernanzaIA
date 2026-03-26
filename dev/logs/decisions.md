# Decision Log

Este archivo registra decisiones de baseline que siguen siendo relevantes para
la gobernanza reusable. No debe contener historiales de producto, runtime de
una app concreta ni referencias a repos consumidores específicos.

Cada entrada debe ser breve, clara y justificada.

---

## Formato de entrada

### YYYY-MM-DD — Título corto de la decisión

**Contexto**
Qué problema o situación llevó a tomar esta decisión.

**Decisión**
Qué se decidió exactamente.

**Motivo**
Por qué se eligió esta solución frente a otras.

**Impacto**
Qué partes del baseline afecta.

**Riesgos asumidos**
Qué trade-offs aceptamos.

**Revisión futura**
Cuándo tendría sentido reconsiderar esta decisión (si aplica).

---

# Registro

---

### 2026-03-11 — Separación formal entre gobernanza recuperable y código vivo

**Contexto**
La gobernanza activa consumía demasiado contexto y mezclaba en la misma capa
reglas de procedimiento, histórico documental y navegación de código.

**Decisión**
Adoptar una arquitectura de contexto con tres piezas:
- capa estática mínima siempre presente
- gobernanza textual recuperable bajo demanda mediante recuperación híbrida
- `SymDex` reservado exclusivamente para código vivo del repo consumidor

Además:
- el modo por defecto pasa de `M1` a `M0`
- no existen motores por defecto
- `Codex`, `Claude`, `Gemini` y `Roo` pueden actuar como `motor_activo` o
  `motor_auditor` si el usuario los designa
- las auditorías formales separan `hallazgos` bloqueantes de `observaciones`
  no bloqueantes

**Motivo**
Reducir tokens, separar proceso de sustancia técnica, mantener auditabilidad
real y evitar que detalles editoriales bloqueen fases formales.

**Impacto**
`AGENTS.md`, `dev/workflow.md`, adaptadores de motor, compatibilidad `.roo/`,
prompts/templates de auditoría y documentación de arquitectura del baseline.

**Riesgos asumidos**
Necesidad de mantener consistencia estricta entre fuentes canónicas y capas de
compatibilidad.

**Revisión futura**
Si la recuperación de gobernanza sigue trayendo ruido o ambigüedad, evaluar
endurecer más el filtro determinista o incorporar configuración técnica
dedicada del retrieval.

---

### 2026-03-26 — Baseline reusable con packs opcionales y perfil multi-IA

**Contexto**
La gobernanza ya estaba madura, pero seguía viviendo mezclada con un repo de
producto y no existía un mecanismo único para instalarla de forma limpia en
otros proyectos.

**Decisión**
Consolidar `GobernanzaIA` como baseline reusable con:
- `core` obligatorio
- packs opcionales `claude`, `codex`, `gemini`, `roo`
- packs operativos opcionales `governance_search` y `symdex`
- perfil multi-IA obligatorio con mínimo dos IAs y preferencia separada de
  trabajo y auditoría como metadata de instalación

**Motivo**
Permitir instalaciones repetibles, versionables y neutrales respecto al repo
consumidor sin arrastrar runtime ni históricos.

**Impacto**
`scripts/migration/bootstrap_governance.py`, `scripts/README.md`, `README.md`,
políticas de distribución y tooling MCP opcional del baseline.

**Riesgos asumidos**
Mayor superficie de mantenimiento en el bootstrap y necesidad de conservar
alineadas las superficies opcionales con la fuente canónica.

**Revisión futura**
Si aparecen nuevas superficies de editor o nuevas IAs soportadas, incorporarlas
como packs opcionales sin convertirlas en fuente normativa primaria.
