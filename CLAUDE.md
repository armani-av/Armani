# CLAUDE.md

Notas persistentes para las sesiones de Claude Code en este repositorio.

## Entorno

- **PC compartida**: esta computadora es de uso compartido — "tú y Claude compartirán esta PC".
  Asumir que puede haber otra sesión/otro usuario trabajando sobre los mismos archivos.
  - No dar por hecho que el working tree quedó como se dejó en la sesión anterior: revisar
    `git status` y `git log` al empezar.
  - Confirmar antes de operaciones destructivas o difíciles de revertir (borrar archivos,
    `git reset --hard`, force-push, limpiar directorios de trabajo).
  - Preferir ramas propias y commits frecuentes en lugar de dejar cambios sin guardar.

## Proyecto

- Repositorio: `armani-av/armani`. Por ahora solo contiene `README.md`; aún no hay
  stack, build ni tests definidos.
