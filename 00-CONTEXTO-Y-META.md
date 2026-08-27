# Contexto permanente del proyecto

> Este archivo existe para que cualquier sesión futura de Claude (u otra persona)
> retome el proyecto sin volver a preguntar lo básico. Las sesiones **no** comparten
> memoria: lo que no esté escrito aquí, se pierde.

Última actualización: 25 de agosto de 2026 (rev. 2 — horario real y corrección del mentor)

---

## Quién

**Leonardo Armani Aguirre Vera** — av.esc.armani@gmail.com

Tres formaciones en curso simultáneo:

| Institución | Programa | Estado |
|---|---|---|
| CAAAREM | Comercio exterior / formación del gremio de agentes aduanales | 7º cuatrimestre |
| UNAM (FCA) | Negocios Internacionales | En curso |
| Ibero | Ingeniería en Inteligencia Artificial | En curso |

**Carga académica: 55 h/semana de clase, 17 materias, sin empalmes.** Horario recibido y
verificado (`Horario semanal 2027-1`).

Bloques libres reales:

| Día | Hueco | Nota |
|---|---|---|
| Lunes | 11:00–16:00 (5 h) | Horario hábil |
| Martes | 13:00–16:00 (3 h) | Horario hábil |
| Miércoles | 11:00–16:00 (5 h) | Horario hábil |
| Jueves | **cero** | 12 h de clase + traslado crítico 15–16 |
| Viernes | 13:00–16:00 (3 h) | Horario hábil |
| Sábado | 17:00–21:00 (4 h) | Tras IUCAAAREM + 1 h 20 de traslado |
| Domingo | Día Capital | Menos comida y ejercicio |

**16 h/semana caen en horario hábil** — el recurso escaso para vender, porque las agencias
solo contestan de lunes a viernes en horario de oficina.

Presupuesto propio del proyecto: **~12 h/semana**, de los buckets *IA/Proyectos* (10 h) y
*Reserva* (20 h) del Plan Ejecutivo Agosto 14-31. **Sin tocar música ni académico.**

Duda pendiente: la guía marca IUCAAAREM como «en línea», pero Armani menciona traslado
presencial. Si alguna sesión es en línea, libera hasta 2 h 40 el sábado.

## Meta económica

| Horizonte | Cifra | Equivalente en MXN (@ 17.00) |
|---|---|---|
| Semanal | 2 500 USD | ~42 500 MXN |
| Mensual | 10 000 USD | ~170 000 MXN |

Formulaciones equivalentes que Armani planteó: 4 clientes × 2 500 USD, o 2 × 5 000, o
1 × 10 000.

**Plazo que Armani pidió: 2 semanas para llegar a la meta mensual.**
Ver `02-ESTRATEGIA.md` → "Reencuadre del plazo" para el análisis honesto de qué parte
de eso es alcanzable en 14 días y qué parte no.

**Motivo declarado (importante para las decisiones de diseño):** no es urgencia de
liquidez. Es querer empezar a generar ingreso propio. Eso permite optimizar por
*construir un activo* en lugar de por *cobrar rápido a cualquier costo* — pero Armani
también pidió explícitamente velocidad de ejecución, así que el plan busca ambas.

## Tesis del negocio

Vender **servicios** de auditoría y remediación de cumplimiento aduanero mexicano,
**no software**.

Razones:
1. No requiere capital inicial.
2. No compite de frente contra startups financiadas (ver Camtom en la investigación).
3. Se cobra desde el primer cliente, no dentro de un año.
4. Los primeros clientes se convierten en la especificación del producto, si algún día
   hay producto.

**Decisión tomada y cerrada: NO construir un clasificador arancelario con IA.**
Ese hueco ya está ocupado por Camtom/TariffPro, con capital, ventaja temporal y datos
propietarios. Armani ya intentó dos veces (un clasificador con IA y un analizador de
documentos de comercio); ambos fallaron por infraestructura y ejecución. El diagnóstico
de esos fracasos es que el problema estaba bien elegido y el vehículo mal.

Armani también señaló el riesgo estratégico de hacer software: cualquier tercero con
más maquinaria y equipo puede copiar la idea y ejecutarla mejor. El servicio, en cambio,
se apoya en algo que no se copia: su acceso al gremio vía CAAAREM.

## La ventaja que no se compra

- **Acceso al gremio golpeado.** CAAAREM es la confederación de los agentes aduanales
  (~800–875 agentes, 38 asociaciones, ~99 % de cobertura nacional). Los maestros y
  compañeros de Armani *son* las personas que recibieron el golpe regulatorio.
- **Intersección técnica rara.** Quien sabe de aduanas no programa; quien programa no
  distingue una fracción arancelaria de un pedimento.
- **Fracasos previos con la tesis correcta.** Sabe dónde está el problema real.

## Activos disponibles

- Conocimiento técnico (IA, análisis de datos, automatización) ya adquirido.
- **Un mentor experto del gremio, activo y dispuesto a corregir.** El activo más valioso
  del proyecto. Ver abajo.
- Acceso a maestros de renombre en CAAAREM para asesoría y posible aval/referencia.
- Sábados en IUCAAAREM cursando *Operaciones y Almacenes* y *Merceología y Clasificación
  Arancelaria de Metales* — justo las materias del hueco técnico.
- Un proyecto de IA en ejecución en paralelo — **no** es el vehículo comercial de este plan.
- **Armani AV** (música, 24 h/quincena). Proyecto de identidad, **no recortable**.

## El mentor y la corrección del 25 de agosto

Un experto del gremio revisó el pitch y encontró un error de fondo: el material confundía
**la factura de honorarios del agente aduanal** (que sí es CFDI) con **la factura comercial
de la mercancía** (que emite un proveedor extranjero y no es CFDI). Su diagnóstico:
*«te falta conocer la operación»*.

Y después dio la especificación del producto: *«si tu aplicación puede detectar errores
justo entre esa factura y el pedimento…»*.

**Consecuencias, ya incorporadas:**
- `08-LA-OPERACION.md` documenta la cadena correcta y las tres capas de reconciliación.
- Todo el material comercial fue corregido.
- La secuencia cambió: **aprender la operación antes de vender**, no en paralelo.
- Regla dura: **no se manda un correo comercial hasta poder explicar la cadena de memoria.**

## Preguntas abiertas (bloquean afinar el plan)

1. ~~Horario semanal.~~ **Recibido y verificado.**
2. ¿Tiene RFC activo y puede facturar? Determina si puede cobrar a empresas formales
   (casi todas las IMMEX exigen factura) o si necesita un intermediario mientras tanto.
3. ¿Hay algún maestro de CAAAREM con quien ya tenga confianza suficiente para pedirle
   introducciones, no solo asesoría?
4. ¿Presupuesto disponible para gastos mínimos (dominio, correo profesional, viáticos
   a una reunión)? El plan asume ~0 y funciona, pero cambia la velocidad.

## Archivos del proyecto

| Archivo | Contenido |
|---|---|
| `00-CONTEXTO-Y-META.md` | Este archivo. Contexto permanente. |
| `01-INVESTIGACION-DE-MERCADO.md` | Hallazgos verificados con fuentes y fechas. |
| `02-ESTRATEGIA.md` | La tesis, el wedge, el canal, la ruta a 10k USD/mes. |
| `03-SERVICIOS-Y-PRECIOS.md` | Paquetes, precios y la aritmética real. |
| `04-PLANTILLAS-CONTACTO.md` | Copy listo para enviar hoy. |
| `05-PLAN-EJECUCION.md` | Calendario sobre los bloques reales del horario. |
| `06-CUESTIONARIO-DIAGNOSTICO.md` | Qué preguntar en la llamada de descubrimiento. |
| `07-PROPUESTA-PLANTILLA.md` | Plantilla de propuesta comercial. |
| `08-LA-OPERACION.md` | **Los documentos del despacho y las tres capas de reconciliación.** Base técnica. |
| `09-RESPUESTA-AL-MENTOR.md` | Cómo contestarle y qué pedirle. |
| `pipeline.csv` | CRM mínimo. Actualizar a mano. |
