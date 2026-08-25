# Contexto permanente del proyecto

> Este archivo existe para que cualquier sesión futura de Claude (u otra persona)
> retome el proyecto sin volver a preguntar lo básico. Las sesiones **no** comparten
> memoria: lo que no esté escrito aquí, se pierde.

Última actualización: 25 de agosto de 2026

---

## Quién

**Leonardo Armani Aguirre Vera** — av.esc.armani@gmail.com

Tres formaciones en curso simultáneo:

| Institución | Programa | Estado |
|---|---|---|
| CAAAREM | Comercio exterior / formación del gremio de agentes aduanales | 7º cuatrimestre |
| UNAM (FCA) | Negocios Internacionales | En curso |
| Ibero | Ingeniería en Inteligencia Artificial | En curso |

**Carga académica declarada: 55 horas/semana ocupadas.** Equivalente a un empleo de
tiempo completo, y un poco más. Cualquier plan que ignore esto no es ejecutable.
(Horario semanal detallado: **pendiente de entregar**. Ver "Preguntas abiertas".)

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
- Acceso a maestros de renombre en CAAAREM para asesoría y posible aval/referencia.
- Un proyecto de IA en ejecución en paralelo — **no** es el vehículo comercial de este plan.

## Preguntas abiertas (bloquean afinar el plan)

1. **Horario semanal detallado.** Armani ofreció mandarlo. Sin él, el calendario de
   `05-PLAN-14-DIAS.md` usa supuestos declarados que hay que corregir.
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
| `05-PLAN-14-DIAS.md` | Calendario día por día. |
| `06-CUESTIONARIO-DIAGNOSTICO.md` | Qué preguntar en la llamada de descubrimiento. |
| `07-PROPUESTA-PLANTILLA.md` | Plantilla de propuesta comercial. |
| `pipeline.csv` | CRM mínimo. Actualizar a mano. |
