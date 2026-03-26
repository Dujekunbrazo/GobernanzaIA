# Exception Rules (Hard)

Estas reglas gobiernan excepciones formales a la gobernanza canónica.

## 1) Cuándo existe una excepción

- Una excepción solo existe si quedó registrada en `exception_record.md`.
- Una excepción no puede vivir solo en chat, commit o comentario disperso.

## 2) Cuándo se permite

- Solo se permite cuando una restricción real bloquea temporalmente el camino
  canónico.
- No se permite abrir excepción para justificar conveniencia, prisa o diseño
  oportunista.

## 3) Contenido mínimo obligatorio

Toda excepción debe declarar:
- `Exception ID`
- owner responsable
- regla canónica afectada
- motivo verificable
- riesgo aceptado
- alcance exacto
- fecha de alta
- trigger o fecha de retiro
- validación compensatoria mientras exista

## 4) Límites duros

- Una excepción no redefine la fuente de verdad.
- Una excepción no autoriza branching oportunista permanente.
- Una excepción no puede quedar abierta sin criterio de retiro.
- Una excepción no puede cerrar una iniciativa como `PASS` si deja
  inconsistencia material sin declarar.

## 5) Cierre y retiro

- Toda excepción debe terminar en uno de estos estados:
  - `APROBADA` mientras siga activa
  - `RETIRADA` cuando el camino canónico ya está restituido
  - `RECHAZADA` si no procede
- `closeout.md` debe declarar el estado final de cualquier excepción abierta.
