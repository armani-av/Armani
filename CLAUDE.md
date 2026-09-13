# CLAUDE.md

Notas persistentes para las sesiones de Claude Code en este repositorio.

## Entorno

- **PC compartida con Codex**: esta computadora la comparten Claude Code y Codex (el agente
  de consola de OpenAI). Asumir siempre que Codex —u otra sesión— puede estar trabajando
  sobre los mismos archivos al mismo tiempo.
  - No dar por hecho que el working tree quedó como se dejó en la sesión anterior: revisar
    `git status` y `git log` al empezar, porque los cambios pueden ser de Codex.
  - Confirmar antes de operaciones destructivas o difíciles de revertir (borrar archivos,
    `git reset --hard`, force-push, limpiar directorios de trabajo): podrían pisar trabajo
    de la otra sesión.
  - Preferir ramas propias y commits frecuentes en lugar de dejar cambios sin guardar.
  - No atribuirse cambios ajenos: si aparece trabajo que no se hizo en esta sesión,
    mencionarlo en lugar de asumirlo como propio.

## Proyecto

- Repositorio: `armani-av/armani`. Por ahora solo contiene `README.md`; aún no hay
  stack, build ni tests definidos.
