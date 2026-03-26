# Debug Mode Behavior (Diagnóstico)

Objetivo: diagnosticar problemas específicos en `M2 DEBUG` sin introducir fixes
ni cambios de arquitectura no solicitados.

## Fuente de verdad

1) `AGENTS.md`
2) `dev/workflow.md`
3) `.roo/rules/*` como capa de compatibilidad

Este modo no redefine `M0-M4` ni `F1-F9`.
El rol oficial de gobernanza sigue siendo `motor_activo`.

## Principios básicos

1) No asumir causa sin evidencia.
2) Trabajar solo con:
   - logs proporcionados
   - código existente en el repo
   - comportamiento descrito por el usuario
3) No introducir mejoras arquitectónicas durante debugging.
4) No mezclar fix con refactor.
5) Si la consulta es de gobernanza, usar `governance_search` antes de cualquier
   lectura directa.
6) Si la consulta es de código vivo, usar `symdex_search_code` y luego
   `symdex_read_code`.
7) Declarar herramienta usada y fuente canónica usada en cada respuesta
   técnica.
8) Si faltan MCPs activos, declarar limitación operativa.

---

## Proceso obligatorio

### 1. Confirmación del problema
- Declarar el modo operativo si no está claro.
- Resumir el problema en 1–3 frases.
- Si la sesión acaba de arrancar o se ha recargado, confirma si están activos
  `governance_search`, `symdex_search_code` y `symdex_read_code`.
- Si Roo va a intervenir como canal de auditoría en `F7`, pregunta antes si el
  usuario desea mantener o cambiar la API/modelo para esa auditoría.
- Identificar qué información falta, si aplica.

### 2. Hipótesis (máximo 3)
- Listar hipótesis ordenadas por probabilidad.
- Para cada hipótesis:
  - evidencia que la soporta
  - cómo validarla

### 3. Aislamiento
- Identificar el archivo, símbolo o flujo exacto implicado.
- Cargar solo el contexto mínimo necesario.
- Si falta evidencia, declarar `BLOQUEADO`.

### 4. Propuesta de fix mínimo
- Cambio más pequeño posible.
- Sin modificar arquitectura.
- Sin introducir mejoras colaterales.
- Si el problema exige rediseño o aumenta alcance/riesgo, proponer escalar a
  `M3` o reabrir ask.

### 5. Validación
- Indicar cómo comprobar que el bug desaparece.
- Indicar qué resultado esperado confirma el fix.

---

## Restricciones

- En `M2` no implementar cambios.
- No ejecutar cambios masivos.
- No reestructurar archivos.
- No usar iniciativas previas como fuente principal de proceso si existe fuente
  canónica.
- Usar solo terminología activa: `motor_activo` y `motor_auditor`.
- Los modos nativos de Roo no redefinen `M0-M4` ni `F1-F9`.

---

## Salida esperada

- Resumen del problema
- Hipótesis numeradas
- Evidencia utilizada
- Fix mínimo propuesto
- Pasos de validación
