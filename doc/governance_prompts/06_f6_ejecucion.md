# F6 Ejecución

El Plan ya está congelado. Quiero ejecutar esta iniciativa.

Usa la iniciativa activa de esta conversación.

Trabaja siguiendo solo el `plan.md` congelado de esa iniciativa y documenta la
ejecución en `execution.md` dentro de la misma carpeta.

`execution.md` debe respetar exactamente la estructura canónica de la plantilla:

- metadata completa al inicio
- `## Referencia al plan congelado`
- `## Estado operativo de F6`
- `## Commits ejecutados`
- `## Validaciones`
- `## Riesgos detectados`
- `## Desvios respecto al plan`

No sustituyas esa estructura por un resumen libre. Si necesitas añadir contexto,
hazlo dentro de esas secciones.

Reglas operativas:

- `execution.md` lo escribes tú como `motor_activo`; no lo reconstruye el orquestador
- si el `phase_ticket` limita esta ejecución a un commit o tramo concreto, trabaja solo ese tramo
- deja explícito cuál fue el último tramo completado y cuál sería el siguiente
- no dependas de memoria conversacional previa; usa `phase_ticket` y `resume_packet` como contexto operativo vigente

Antes de empezar, confirma qué iniciativa vas a ejecutar y luego continua
