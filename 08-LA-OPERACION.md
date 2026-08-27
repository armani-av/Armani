# La operación: qué documentos integran un despacho aduanero

> **Por qué existe este archivo.** Un experto del gremio revisó el pitch y encontró un
> error de fondo: *«te falta conocer la operación, hijo»*. Tenía razón, y el error era mío
> (de Claude), no de Armani — yo escribí el material anterior conflando dos facturas
> distintas. Este archivo corrige eso y se vuelve la base técnica del producto.
>
> **Regla: no se manda un solo correo hasta poder explicar esta cadena de memoria.**

---

## El error que había que corregir

El material anterior decía «cruzo sus pedimentos contra sus CFDI». Eso mezcla dos
documentos que no tienen nada que ver:

| | Qué es | ¿Es CFDI? |
|---|---|---|
| **Factura del agente aduanal al importador** | El cobro de honorarios del agente por el servicio del despacho | **Sí.** Es un CFDI mexicano. |
| **Factura comercial de la mercancía** | La que emite el **proveedor extranjero** por la mercancía que se importa. Es la que ampara el valor y la que se refleja en el pedimento. | **No.** Un proveedor extranjero no emite CFDI. |

En palabras del mentor:

> «Si te refieres a la factura que viene en el pedimento, esa es la factura de la mercancía
> que se va a importar, y NO es la factura del agente aduanal. Es la factura de un proveedor
> extranjero que usará esa factura el importador para meter la mercancía al país.»

**El valor de la operación nace en un documento extranjero.** Ese es el punto de partida
de toda la cadena, y era justo el eslabón que faltaba.

Y el mentor terminó dando la especificación del producto:

> «Y si tu aplicación puede detectar errores justo entre esa factura y el pedimento…»

Eso es lo que hay que construir.

---

## La cadena del valor, en orden

```
  Factura comercial            emitida por el proveedor EXTRANJERO
  (mercancía)                  valor, cantidades, descripción, incoterm, moneda
         │
         ▼
  COVE                         el AGENTE transmite esos datos a VUCEM
  Comprobante de               firmado con sello digital VUCEM
  Valor Electrónico            → devuelve el Acuse de Valor
         │
         ▼
  MVE                          el IMPORTADOR la elabora referenciando ese COVE
  Manifestación de             firmada con su e.firma (el agente NO puede firmarla)
  Valor Electrónica            → devuelve el MNVA
         │
         ▼
  Pedimento                    el agente declara ahí el folio COVE y el MNVA
                               captura, prevalida, paga contribuciones, valida
         │
         ▼
  DODA                         se genera con la info del pedimento validado y pagado
  Documento de Operación       es lo que se presenta físicamente en el módulo
  para Despacho Aduanero
```

### El handoff que rompe las cosas

Nótese la secuencia entre las dos partes:

1. El agente crea y firma el **COVE** → obtiene el Acuse de Valor.
2. El agente **le pasa el número de COVE al importador**.
3. El importador crea la **MVE** referenciando ese COVE y la firma con **su** e.firma.
4. El importador **le regresa el MNVA al agente**.
5. El agente declara COVE y MNVA en el **pedimento**.

**Son cinco pasos y dos empresas distintas por cada operación.** Ahí es donde se cae:
el importador no contesta, firma tarde, referencia un COVE equivocado, o alguien cree
que el agente puede firmar por él —que no puede—. Con responsabilidad solidaria, ese
retraso ya no es un tema administrativo.

> **Esta es la observación operativa que vale más que cualquier dato de mercado.**
> El problema no es un documento mal llenado: es un handoff de cinco pasos entre dos
> empresas, repetido por cada pedimento, sin nadie vigilándolo.

### Dónde sí entran los CFDI

Los CFDI son mexicanos y aparecen en el lado nacional de la operación, no en la factura
de la mercancía:

- **Honorarios del agente aduanal** al importador.
- **Fletes y seguros**, cuando el proveedor del servicio es mexicano.
- **Maniobras, almacenaje, custodia.**
- La **contabilidad del importador** en general, que el SAT sí cruza contra lo declarado.

Así que el cruce contra CFDI existe, pero aplica a los **incrementables y a la
contabilidad**, nunca a la factura de la mercancía. Decirlo mal es exactamente lo que
delata a quien no conoce la operación.

---

## Las tres capas de reconciliación

Este es el producto, ordenado de mayor a menor valor:

### Capa 1 — Factura comercial ↔ COVE ↔ pedimento `← la que señaló el mentor`

La más valiosa y la más difícil técnicamente, porque las facturas comerciales extranjeras
vienen en formatos heterogéneos: PDF, Excel, escaneadas, en inglés, chino o alemán, cada
proveedor con su plantilla.

**Ahí está la ventaja de Armani.** Extraer datos estructurados de documentos no
estandarizados es precisamente un problema de ingeniería, y es la parte que un despacho
de comercio exterior no puede resolver contratando a otro abogado.

Qué se compara: valor total, cantidades, descripción de mercancía, datos del proveedor,
incoterm, moneda y tipo de cambio, condiciones de pago.

### Capa 2 — Incrementables ↔ INCOTERM `← la de mejor relación valor/esfuerzo`

Aquí hay una regla dura, verificable y que produce errores caros. **Es puro motor de
reglas: no necesita IA, y se puede construir en un fin de semana.**

| Grupo INCOTERM | Precio pagado incluye | Flete y seguro |
|---|---|---|
| **E y F** — EXW, FCA, FAS, FOB | Solo la mercancía | **Sí son incrementables.** Deben sumarse. |
| **C y D** — CFR, CIF, CPT, CIP, DAP, DDP | Valor total de la factura, logística incluida | **No son incrementables.** Ya están dentro. |

**Los tres errores clásicos:**

1. **Doble conteo.** El incoterm es del grupo C/D —el flete ya está en el precio pagado—
   y de todas formas se declara el flete como incrementable en el pedimento.
   Resultado: sobrevaluación.
2. **Omisión.** El incoterm es del grupo E/F y no se declaran flete ni seguro.
   Resultado: **subvaluación**, que es la que trae multa de hasta 150 %.
3. **Sin prorrateo.** Los gastos logísticos no se reparten entre las múltiples secuencias
   o partidas del pedimento.

Y el cuarto, que es de criterio y no de aritmética: **el incoterm facturado no corresponde
a la operación real.** Fundamento: artículo 64 de la Ley Aduanera, valor de transacción real.

> Un script que lea el incoterm y compare contra los incrementables declarados detecta
> los primeros tres de forma determinista. **Ese es el primer entregable vendible**, y no
> depende de que el SAT mantenga la fecha del 30 de septiembre.

### Capa 3 — MVE ↔ COVE ↔ contabilidad

- ¿La MVE referencia el COVE correcto?
- ¿El valor comercial del pedimento coincide con el monto del COVE?
- ¿Los incrementables declarados cuadran con los CFDI de fletes y seguros?
- ¿Existe MNVA para cada pedimento del periodo, o hay operaciones sin MVE?

---

## Lo que falta aprender, y cómo

El diagnóstico del mentor fue *«ver qué documentos se integran en el despacho aduanero»*.
No se resuelve leyendo: se resuelve viendo un expediente real.

| Pendiente | Cómo se cierra |
|---|---|
| Ver un expediente completo de una operación real | Pedírselo al mentor, anonimizado: factura comercial, COVE, acuse de valor, MVE, MNVA, pedimento, DODA |
| Entender el layout del pedimento campo por campo | Con el expediente en la mano y el instructivo de llenado |
| Entender el flujo real de quién manda qué a quién | Preguntar en la agencia: ¿quién captura, quién revisa, en qué momento? |
| Ver cómo se ve un error real | «¿Me enseña una rectificación que hayan tenido que hacer y por qué?» |
| Conocer los anexos digitales del pedimento | Documentos que se transmiten como e-document ligados al COVE |

**Ventaja de calendario:** los sábados en IUCAAAREM Armani lleva **Operaciones y Almacenes**
y **Merceología y Clasificación Arancelaria de Metales**. Está literalmente sentado en la
clase que cubre este hueco, con los compañeros que lo viven. La pregunta correcta al
profesor un sábado vale más que una semana de búsquedas.

---

## Qué cambia esto en el pitch

**Antes (mal):**
> «Cruzo sus pedimentos contra sus CFDI.»

**Después (correcto):**
> «Cruzo la factura del proveedor contra el COVE y contra lo declarado en el pedimento,
> y verifico que los incrementables correspondan al incoterm pactado. Ahí es donde se
> generan las diferencias de valor.»

La segunda frase la puede decir frente a un agente con veinte años de oficio sin que lo
desarmen en la primera pregunta. La primera, no.

---

## Fuentes

- [ANAM — Documentos electrónicos o digitales que se transmiten como anexos al pedimento](https://www.anam.gob.mx/documentos-electronicos-o-digitales-que-se-deben-transmitir-como-anexos-al-pedimento-de-importacion/)
- [SAT — Documentos que deben anexarse al pedimento de importación](http://omawww.sat.gob.mx/aduanas/importando_exportando/regimenes/Paginas/documento_que_deben_anexar_al_pedimento_importacion.aspx)
- [VUCEM — Preguntas frecuentes COVE](https://www.ventanillaunica.gob.mx/movil/FAQs/COVE/)
- [VUCEM — Comprobante de Valor Electrónico (PDF)](https://www.ventanillaunica.gob.mx/vucem/preguntasFrecuentes/vucem008360.pdf)
- [ANAM — Preguntas frecuentes DODA](https://www.anam.gob.mx/wp-content/uploads/2021/08/Preguntas_frecuentes_DODA_agosto_2020.pdf)
- [Camtom — COVE vs MVE: diferencias clave](https://www.camtomx.com/en/blog/mve-diferencia-cove-manifestacion-valor)
- [Blog Aduanero — Cómo declarar COVE y pedimento con fletes desglosados](https://blog.cjaduanero.com/como-declarar-cove-y-pedimento-con-fletes/)
- [AJR — COVE en comercio exterior](https://ajrmexico.com/cove-en-comercio-exterior-que-es-y-como-funciona-en-las-operaciones-aduaneras/)
- [Facturama — Uso del DODA en el despacho aduanal](https://facturama.mx/blog/que-significa/doda-documento-de-operacion/)
