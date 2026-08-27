# Investigación de mercado — cumplimiento aduanero México

Fecha de investigación: **25 de agosto de 2026**
Tipo de cambio de referencia: **16.9018 MXN/USD** (DOF, 24 ago 2026). Para planeación uso **17.00**.

> **Nota sobre confiabilidad.** Todo lo de abajo viene de fuentes públicas secundarias
> (despachos, medios especializados, blogs de agencias). Antes de usar cualquier cifra
> **frente a un cliente**, verificar contra el DOF y las RGCE vigentes. Marco con
> ⚠️ los datos donde encontré contradicción entre fuentes.

---

## 1. El hallazgo que cambia el timing del plan

**La Manifestación de Valor Electrónica (MVE) es obligatoria desde el 1 de agosto de 2026,
con facilidades transitorias que vencen el 30 de septiembre de 2026.**

- Fundamento: *Tercera Versión Anticipada de la Segunda Resolución de Modificaciones a
  las RGCE para 2026*, publicada en el Portal del SAT el **31 de julio de 2026**,
  que actualiza el **transitorio Décimo Primero** de las reglas publicadas en el
  DOF del **27 de diciembre de 2025**.
- Historial de prórrogas: disponible desde ago-2025 → obligatoria dic-2025 → 1 abr 2026
  → 1 jun 2026 → 31 jul 2026 → operaciones ordinarias desde **1 ago 2026** → facilidades
  hasta **30 sep 2026**.

### Por qué esto importa más que todo lo demás

**Hoy quedan ~36 días** para el 30 de septiembre. Esto es un dolor con **fecha**, no un
dolor difuso. Un problema con fecha se vende; uno sin fecha se pospone indefinidamente.

Además, el historial de cinco prórrogas produce un efecto psicológico explotable: **medio
mercado asumió que habría una sexta y no se preparó.** Ese es exactamente el cliente que
compra en septiembre.

### Qué exige la MVE

- Documento digital transmitido por **VUCEM**, firmado con la **e.firma del importador**
  (o de su representante legal). La autoría es explícita y trazable a un único responsable.
- Se transmite **antes del pago del pedimento**; se declara un **folio de 13 caracteres**.
- Contenido: valor en aduana y precio pagado o por pagar; incrementables (fletes, seguros,
  embalajes, regalías); datos del proveedor; incoterm; medios de pago; documentos
  contractuales y relación comercial; descuentos; evidencia de vinculación corporativa.
- **Formato E15** ("Información de contratos asociados a la Manifestación de Valor"):
  hasta el **31 de diciembre de 2026** se puede transmitir el E15 con los datos generales
  de los contratos, en lugar de subir los contratos completos a VUCEM.

### El mecanismo de detección

El SAT cruza algorítmicamente lo declarado contra la contabilidad del importador, incluidos
los **CFDI** de fletes y seguros. Si el valor o los incrementables declarados no coinciden,
se detonan inconsistencias.

> ⚠️ **Precisión necesaria.** Ese cruce aplica a los **incrementables y a la contabilidad
> mexicana**, nunca a la factura de la mercancía: esa la emite un **proveedor extranjero**
> y no es un CFDI. Confundirlas es el error que un agente aduanal detecta en la primera
> frase. Ver `08-LA-OPERACION.md`.

**Esto es lo importante comercialmente:** el problema no es *llenar un formato*. Es
**reconciliar documentos que en la mayoría de las empresas nunca se cotejaron entre sí** —
la factura del proveedor extranjero, el COVE, la MVE, el pedimento y, del lado mexicano,
los CFDI de los servicios. Eso es trabajo de datos, no de abogados, y es exactamente lo
que Armani sabe hacer.

Añade a eso un handoff de cinco pasos entre dos empresas por cada operación (el agente
hace el COVE, el importador hace la MVE con su e.firma, y los folios regresan al
pedimento). Nadie vigila esa cadena. Ver `08-LA-OPERACION.md`.

### Consecuencias del incumplimiento

- ⚠️ **Multa por pedimento despachado sin MVE:** una fuente indica hasta **7 190 MXN**;
  otra indica hasta **22 000 MXN**. *Contradicción sin resolver — verificar en el DOF antes
  de citar la cifra a un cliente.*
- Multas por **subvaluación de hasta 150 %**.
- Rechazo de la **deducibilidad** de la mercancía importada.
- Retención de mercancía; revisión exhaustiva de embarques futuros.
- **Cancelación / suspensión temporal del Padrón de Importadores.**

---

## 2. La reforma de fondo (contexto que sostiene todo lo demás)

Decreto publicado en el **DOF el 19 de noviembre de 2025**, en vigor el **1 de enero de 2026**,
con más de sesenta artículos modificados.

### Responsabilidad: el cambio estructural

- **Se eliminan las excluyentes de responsabilidad directa del agente aduanal.** Ya no puede
  excluirse su responsabilidad por la inexactitud o falsedad de los datos que le proporcione
  el importador o exportador.
- Los agentes aduanales pasan de **subsidiariamente** a **solidariamente** responsables del
  pago de impuestos al comercio exterior, contribuciones y cuotas compensatorias.
- Son responsables solidarios por las contribuciones no pagadas en operaciones promovidas
  por las **agencias aduanales de las que sean socios**.
- Responsabilidad solidaria sobre la **veracidad de la información** y la **correcta
  clasificación arancelaria**.

> **Traducción comercial:** antes, un error del importador era problema del importador.
> Hoy es problema del agente aduanal, con su patrimonio. Eso convierte a la agencia aduanal
> en un **comprador motivado de control de calidad sobre los datos de sus propios clientes**.
> Es el hecho central de toda la estrategia de canal.

### Otras obligaciones nuevas

| Obligación | Detalle |
|---|---|
| Certificación periódica | Los agentes aduanales se certifican **cada 3 años** para mantener la patente activa. |
| Vigencia | Patente de agente aduanal y autorización de agencia aduanal: **20 años**, prorrogables por igual plazo. |
| Verificación de domicilio | Obligación de constatar que el importador tiene **domicilio fiscal activo** ante el SAT antes de operar. |
| Restricción de vinculación | El agente no debe ser socio, accionista, representante legal, ni tener relación laboral o vinculación con quien le tramite operaciones. |
| Conservación documental | **10 años** para regímenes especiales (IMMEX, depósito fiscal, tránsito interno). |
| Sistemas electrónicos | Obligación de sistemas de registro y control con trazabilidad en tiempo real. |

### Plazos diferidos relevantes de 2026

- **1 de febrero de 2026** — cancelación de la Cuenta Aduanera de Garantía a los 12 meses.
- **1 de abril de 2026** — obligación de Cuenta Aduanera de Garantía en Recinto Fiscalizado Estratégico (RFE).
- **19 – 31 de mayo de 2026** — pruebas piloto de la figura de agencia aduanal.
- **1 de junio de 2026** — inicio de operaciones formales bajo la figura de **agencia aduanal**.
- **1 de agosto de 2026** — MVE obligatoria para operaciones ordinarias.
- **30 de septiembre de 2026** — vencen las facilidades transitorias de la MVE. ← *ventana actual*
- **31 de diciembre de 2026** — vence la opción de transmitir el formato E15 en lugar de contratos.

### Sanciones de rango patrimonial

- **70 – 100 %** de las contribuciones omitidas por mala clasificación.
- Hasta **300 %** del valor comercial si el error toca regulaciones no arancelarias.
- **250 – 300 %** del valor comercial en presunción de contribuciones omitidas (IMMEX).
- **30 – 50 %** del valor comercial por exceder el plazo de retorno de importación temporal.
- Suspensión del **Padrón de Importadores** por datos inexactos.
- Suspensión o cancelación del **Programa IMMEX** y retiro de la **Certificación IVA-IEPS**.

---

## 3. Que el riesgo ya se está materializando (la prueba, no la amenaza)

Esto es lo que convierte el discurso de "podría pasarte" en "ya le está pasando a miles":

- El SAT dio de baja a **18 924** contribuyentes del Padrón de Importadores en 2026
  (La Jornada, 23 de junio de 2026).
- A la segunda semana de junio de 2026, las suspensiones del padrón acumulaban un
  **aumento de 22.4 %**.
- Desde 2021 se acumulan **65 419** suspensiones, y **9 de cada 10 ocurrieron entre 2025
  y lo que va de 2026**.
- Desglose 2026: **17 855** bajas por simplemente dejar de importar; al menos **94** por
  causas ligadas a contrabando, piratería y evasión.
- Se añadieron dos nuevas causales de suspensión (**fracciones XLIX y L**), ligadas
  directamente a la reforma de la Ley Aduanera y el CFF: **omisión de garantías** y
  **emisión de comprobantes fiscales falsos**.

> **Matiz honesto que hay que respetar al vender:** la mayoría de las 18 924 bajas
> (17 855) fueron por inactividad, no por sanción. Presentar la cifra completa como
> "castigos" sería deshonesto y, peor, un agente aduanal experimentado lo detectaría al
> instante y Armani perdería toda credibilidad. **La cifra correcta que sí sostiene el
> argumento es el aumento de 22.4 % en suspensiones y la concentración de 9 de cada 10
> en los últimos 18 meses.**

Consecuencia de segundo orden: con responsabilidad solidaria plena, **tramitar para un
importador suspendido es ahora un riesgo patrimonial para la agencia**. Verificar el
estatus del padrón de la cartera de clientes pasó de trámite a control de riesgo.

---

## 4. Tamaño del mercado

### Empresas IMMEX (el segmento de mayor dolor)

- **6 490 establecimientos** con Programa IMMEX: **5 195** manufactureros, **1 295** no manufactureros (INEGI).
- Otras fuentes: **más de 6 300 empresas**.
- Generan **3.2 millones de empleos**.
- Representan ~**85 %** de las exportaciones manufactureras.
- Facturaron **225 mil millones USD** al cierre de 2024 = **68 %** de las exportaciones nacionales.

**Concentración geográfica:** Baja California, Nuevo León y Chihuahua concentran **40 %**.
El Bajío tiene **más de 700**.

### Agentes y agencias aduanales (el canal)

- CAAAREM agrupa **más de 800** agentes aduanales (una fuente precisa **875**).
- **38 asociaciones** afiliadas.
- Cobertura de ~**99 %** de los agentes en puntos fronterizos, marítimos, aéreos e interiores.
- Más de **800** agentes asistieron al Congreso Nacional 2026.

### Padrón de Importadores

Decenas de miles de contribuyentes activos (65 419 suspensiones acumuladas desde 2021 dan
una idea de la escala del universo).

**Mercado direccionable realista para Armani:** no son 6 490 empresas. Son las
**decenas de agencias aduanales alcanzables vía CAAAREM**, cada una con carteras de
**20 a 100+ importadores**. Ese es el número que importa.

---

## 5. Competencia

### Software / producto — **zona prohibida**

| Actor | Qué hace | Lectura |
|---|---|---|
| **Camtom** (Mérida, 2023; Shark Tank México) | Agencia aduanal digital, +100 clientes. **TariffPro**: clasificación entrenada con TIGIE y miles de resoluciones. **95 %** de precisión vs **82 %** manual; de 15 min a <2 min por clasificación. | **No competir.** Capital, ventaja temporal, datos propietarios. |
| **Grupo Gamas** | **MAVE TradeLinkx**, solución específica para MVE. | Ya hay producto para MVE. Confirma la demanda **y** cierra la puerta al producto. |
| **OP-CBS** | Contenido y automatización de cumplimiento MVE / Anexo 24. | Compite por el mismo lector. |
| SIMPLEX, AduanaSoft, Siimmex, SAP GTS, Thomson Reuters | Control de inventarios IMMEX, trazabilidad, conciliación con pedimentos. | Categoría madura. |

### Consultoría — el terreno real

Despachos activos localizados: **TLC Asociados, MZA, GTC México, Grupo SH, Aduax, BMR
Consultores, Grupo Consultor Internacional, Lawtrade, Cuesta Campos, Stratego, Grupo EI,
ACEI, Lacam, RML, Trafilog**. Big Four presentes: **BDO, KPMG, EY**.

Servicios que ya ofrecen: diagnóstico de cumplimiento IMMEX, auditoría de comercio exterior,
Anexo 24/30/31, alta de IMMEX, padrón de importadores, auto-auditorías preventivas,
evaluación operativa mensual, mapeo de procesos y manuales de operación.

**Ninguno publica honorarios.** Confirmado tras búsqueda dirigida. Esto es normal en el
sector y significa que **el precio se descubre preguntando, no buscando**.

### Capacitación — el termómetro de precio

| Proveedor | Producto | Precio |
|---|---|---|
| Antón Rioja | Taller de llenado de MVE, en línea y en vivo | **812 MXN/persona** (IVA incl.). 50 % de descuento con iguala activa; 15 % para grupos de 5+. |
| CEFA | "Reformas Aduaneras 2026 y la MVE"; "MVE e INCOTERMS" | Empresas con 12+ participantes. |
| TradeMasters | "Llenado de la MVE en VUCEM" | — |
| Kansei Capacitación | Curso MVE | — |

> **El hueco, en una frase:** el mercado está lleno de gente que te **enseña** a llenar
> la MVE (812 MXN) y de software que te la **transmite**. Está vacío de gente que
> **entre a tus datos, encuentre las inconsistencias que ya tienes, y te las arregle
> antes del 30 de septiembre.** Ni el curso ni el software hacen eso: el curso te deja
> con el conocimiento y el problema intacto; el software transmite basura igual de rápido
> si los datos de origen están mal.

Nota táctica: que Antón Rioja ofrezca **50 % de descuento a clientes con iguala activa**
confirma que **la iguala mensual es el modelo comercial estándar del sector**. Armani debe
vender igualas, no horas.

---

## 6. Precios de referencia (triangulación)

Nadie publica honorarios de consultoría de cumplimiento. Estas son las anclas indirectas:

| Concepto | Rango | Fuente |
|---|---|---|
| Honorarios de agente aduanal, operación estándar | 3 500 – 8 000 MXN | Camtom / Aduaeasy |
| Operación compleja (regulados, permisos múltiples) | hasta 15 000 MXN | Camtom |
| Clasificación arancelaria contratada por separado | 1 000 – 3 000 MXN **por fracción** | Camtom |
| Esquema ad valorem | 0.35 % – 0.65 % del valor de la mercancía, con mínimo garantizado | Camtom |
| Auditoría financiera o fiscal (dictamen) | 25 000 – 150 000+ MXN | Praxium |
| Consultor independiente, tarifa horaria general | 1 111 – 1 333 MXN/h (multiplicador 2.5× – 3×) | MercadoPago / deGerencia |
| Curso MVE | 812 MXN/persona | Antón Rioja |
| Ingeniero de IA asalariado en México | 3 000 – 5 500 USD/mes; como contratista, +15–25 % | ProLatam / Remotely Talents |

**Lecturas para fijar precio:**

1. La ancla de **1 000 – 3 000 MXN por fracción arancelaria** es la más útil: establece que
   el gremio ya paga por trabajo unitario de precisión documental. Una revisión de MVE por
   pedimento se puede anclar ahí.
2. La ancla de **25 000 – 150 000 MXN por auditoría** establece el techo de un proyecto
   de diagnóstico. Un diagnóstico de MVE bien vendido cabe cómodamente en la parte baja
   de ese rango sin parecer caro.
3. La meta de **10 000 USD/mes = ~170 000 MXN/mes** equivale a **una auditoría grande
   al mes**, o a **7–11 igualas** en el rango de 15 000 – 25 000 MXN. Lo segundo es más
   estable y más alcanzable que lo primero.
4. El peso se apreció ~4.8 % en 2026 (abrió el año en 18.01, hoy 16.90). **Una meta fijada
   en USD sube en dificultad medida en pesos conforme el peso se fortalece.** Vale la pena
   decidir si la meta real es en dólares o en pesos.

---

## Fuentes

**Reforma y marco legal**
- [EY México — Reformas a la Ley Aduanera para 2026](https://www.ey.com/es_mx/technical/tax/boletines-fiscales/reformas-ley-aduanera-para-2026)
- [Estrategia Aduanera — DOF publica el decreto de reformas a la Ley Aduanera](https://estrategiaaduanera.mx/ultima-hora-dof-publica-el-decreto-por-el-que-se-reforman-adicionan-y-derogan-diversas-disposiciones-de-la-ley-aduanera/)
- [KPMG — Flash: Reglas Generales de Comercio Exterior para 2026](https://kpmg.com/mx/es/tendencias/2026/01/flash-reglas-generales-de-comercio-exterior-para-2026.html)
- [LexLatin — México reforma la Ley Aduanera](https://lexlatin.com/reportajes/reforma-ley-aduanera-cambia-dinamica-comercio-exterior-mexico)
- [Stratego — Ley Aduanera 2026: impacto de la reforma](https://www.stratego-st.com/articulos-especializados/ley-aduanera-2026/)
- [Grupo EI — Agencia aduanal vs. agente aduanal: guía 2026](https://blog.grupoei.com.mx/comparativa-agencia-aduanal-vs-agente-aduanal)
- [MZA — Aduanas en México 2026](https://www.mza.mx/aduanas-en-mexico-2026-nuevas-reglas-obligaciones-y-como-prepararte-para-evitar-contingencias-fiscales-y-logisticas/)
- [Trade Law College — Obligaciones del agente aduanal respecto de la verificación de socios comerciales](https://www.tradelawcollege.edu.mx/single-post/obligaciones-del-agente-aduanal-con-respecto-de-la-verificaci%C3%B3n-de-los-socios-comerciales)

**MVE**
- [Mundo Fiscal — SAT y ANAM amplían plazo para la MVE hasta el 30 de septiembre](https://www.mundofiscalmx.com/contribuyentes/sat-y-anam-amplian-plazo-para-la-manifestacion-de-valor-electronica-hasta-el-30-de-septiembre/)
- [ANAM — Comunicado de prensa conjunto 16/2026](https://www.anam.gob.mx/comunicado-prensa-conjunto-16-2026/)
- [Zamcomer — MVE obligatoria desde el 1 de agosto](https://zamcomer.com/mve-obligatoria-1-agosto-2026-importaciones-excepciones/)
- [Trade Law College — Prontuario sobre la MVE 2026](https://www.tradelawcollege.edu.mx/single-post/prontuario-sobre-la-manifestaci%C3%B3n-de-valor-electr%C3%B3nica-mve-2026)
- [Simetría Legal — MVE 2026 y formato E15](https://www.simetrialegal.mx/negocio-sin-riesgo/manifestacion-valor-electronica-vucem-2026)
- [Contadores XXI — Nueva MVE 2026](https://www.contadoresxxi.com/post/nueva-manifestaci%C3%B3n-de-valor-electr%C3%B3nica-mve-2026-qu%C3%A9-cambia-a-qui%C3%A9n-aplica-y-c%C3%B3mo-deben-prepara)
- [Cuesta Campos — ¿Está tu empresa preparada para la transmisión de la MVE?](https://cuestacampos.com/esta-tu-empresa-preparada-para-la-transmision-de-la-manifestacion-de-valor-electronica-mve)
- [ContadorMx — MVE 2026: nueva prórroga del SAT](https://contadormx.com/manifestacion-de-valor-electronica-importacion/)
- [El Cronista — Manifestación de valor electrónica: cómo tramitarla](https://www.cronista.com/mexico/finanzas-economia/manifestacion-de-valor-electronica-como-tramitar-el-nuevo-documento-obligatorio-del-sat/)
- [Grupo Gamas — MVE 2026: de obligación normativa a ventaja operativa](https://gamas.com.mx/importadores-en-mexico-manifestacion-valor-electronica-2026-mve)

**Padrón de Importadores**
- [La Jornada — El SAT da de baja a 19 mil contribuyentes del padrón de importadores](https://www.jornada.com.mx/2026/06/23/economia/017n1eco)
- [Lamassu — Nuevas causales de suspensión del Padrón de Importadores](https://lamassu.mx/nuevas-causales-de-suspension-del-padron-de-importadores/)
- [Trade Law College — Principales motivos de suspensión de los padrones](https://www.tradelawcollege.edu.mx/single-post/principales-motivos-de-suspensi%C3%B3n-de-los-padrones-de-importadores-y-sectoriales)

**IMMEX y Anexo 24/30**
- [OP-CBS — Anexo 24 IMMEX 2026: qué cambia y cómo cumplirlo](https://op-cbs.com/blog/que-es-anexo-24-empresas-immex-24myev/)
- [ACEI — Reformas al Anexo 24 para IMMEX y control de inventarios](https://blog.acei.com.mx/reformas-al-anexo-24-immex/)
- [CPCON — IMMEX y Anexo 24: control de inventarios aduaneros, guía 2026](https://cpcongroup.mx/insights/immex-anexo-24-control-de-inventarios-aduaneros-mexico)
- [APCE — Anexo 24: guía completa para cumplirlo y evitar multas](https://www.apce.com.mx/anexo-24/)
- [México Industry — Radiografía de las empresas con Programa IMMEX](https://mexicoindustry.com/noticia/radiografia-de-las-empresas-con-programa-immex-en-mexico)
- [INEGI — Estadística del Programa IMMEX](https://www.inegi.org.mx/rnm/index.php/catalog/1092)

**Gremio y competencia**
- [CAAAREM — ¿Qué es CAAAREM?](https://www.caaarem.mx/nosotros.html)
- [Eje Central — CAAAREM reúne a más de 800 agentes aduanales en el Congreso Nacional 2026](https://www.ejecentral.com.mx/nuestro-eje/caaarem-reune-a-mas-de-800-agentes-aduanales-que-temas-se-analizan-en-el-congreso-nacional-2026)
- [Opportimes — Agentes aduanales en agencias aduanales inician pruebas](https://www.opportimes.com/logistica/agentes-aduanales-en-agencias-aduanales-inician-pruebas/)
- [Camtom — Guía completa del programa IMMEX](https://www.camtomx.com/en/blog/immex-guia-completa-programa-maquiladora)
- [Camtom — Reforma aduanera 2026: qué cambia para tu agencia](https://www.camtomx.com/en/blog/reforma-aduanera-2026-cambios-agencias)

**Precios**
- [Camtom — ¿Cuánto cobra un agente aduanal en México? Costos 2026](https://www.camtomx.com/en/blog/cuanto-cobra-agente-aduanal-mexico)
- [Praxium — ¿Cuánto cobra un contador en México? Honorarios 2026](https://praxiumconsultores.com/blog/cuanto-cobra-un-contador-en-mexico-honorarios-2026)
- [MercadoPago — Cómo calcular tus honorarios como consultor](https://www.mercadopago.com.mx/blog/calcular-honorarios-consultoria-mexico)
- [Antón Rioja — Taller de llenado de la nueva MVE 2026](https://antonrioja.com/taller-de-llenado-de-la-nueva-manifestacion-de-valor-electronica-2026-feb-26-1600/)
- [TradeMasters — Curso MVE](https://www.trademasters.com.mx/courses/taller-llenado-de-la-manifestacion-de-valor-electronica)
- [DOF — Tipo de cambio, 24 de agosto de 2026](https://dolardof.com/)
