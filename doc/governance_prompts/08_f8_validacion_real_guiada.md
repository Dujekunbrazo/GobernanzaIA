# F8 Validación Real Guiada

```md
Hemos terminado `F7` y ahora toca `F8` de validación real guiada.

Usa la iniciativa activa de esta conversación.

No arregles código tras el primer fallo material. Primero completa el barrido
real y consolida todos los hallazgos.

No reabras `ask.md`, `plan.md` ni fases anteriores salvo para leer contexto ya
congelado. Tu trabajo aquí es guiar validación real, no replantear la iniciativa.

Haz exactamente esto:

1. prepara el script de pruebas reales ordenado
2. dime las frases o acciones una a una para ejecutarlas en Kiminion
3. tras cada resultado mío, actualiza la matriz de validación
4. registra expected, observed, logs/traces relevantes y resultado
   `PASS` / `FAIL` / `BLOQUEADO`
5. trata como evidencia de primer nivel:
   - chat del producto
   - `trace on`
   - terminal propia de Kiminion
   - cualquier resultado visible en runtime real
6. no propongas fixes generales hasta completar el barrido o declarar bloqueo
   crítico
7. al final genera `real_validation.md` en la carpeta de la iniciativa
8. cierra con una única decisión:
   - `APTA_PARA_F9`
   - `REABRIR_F6`
   - `NO_APLICA`

Antes de seguir, confirma qué iniciativa vas a validar y si `post_audit.md`
ya quedó en `PASS`.
```
