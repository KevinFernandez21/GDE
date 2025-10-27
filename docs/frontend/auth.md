# Frontend Auth Flow (Temporal)

Estado actual orientado a demo:

- Login en `/` con el componente `LoginForm`.
- Se valida conectividad contra `http://localhost:8000/health`.
- Si responde OK, el cliente setea cookie `gde_auth=demo` por 1 hora y redirige a `/dashboard` o al valor de `?redirect=`.
- `middleware.ts` protege `/dashboard/*` (si no hay cookie -> redirige a `/`). Si hay cookie y se visita `/`, redirige a `/dashboard`.

Pendientes a futuro (real):

- Cambiar cookie dummy por sesión/JWT firmado desde backend.
- Validar token en middleware/edge y refrescar expiración.
- Agregar logout que borre cookie y lleve a `/`.
- Conectar métricas a datos reales.


