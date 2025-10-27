# Dashboard UI Notes

- Ruta: `/dashboard` (`app/dashboard/page.tsx`).
- Mantiene lenguaje visual del login: bordes redondeados, sombras suaves, tipografía fuerte, fondo claro.
- KPIs base mock (0s) mientras no haya base de datos.
- Banner superior avisa "DATABASE - Prioridad: medium".
- Próximos pasos:
  - Conectar widgets a endpoints reales.
  - Agregar navegación lateral y páginas: Inventario, Guías, Trazabilidad, Gestión, Configuración.
  - Estado en tiempo real (SSE/WebSocket) para escaneos.
