# Respuesta al mentor

## Por qué esta conversación vale más que todo lo demás

Lo que pasó en ese chat, leído con calma:

1. **Detectó un error de fondo en segundos.** «Una cosa es la factura que hace el agente
   aduanal al cliente… y NO es la factura del agente aduanal. Es la factura de un proveedor
   extranjero.» Eso es exactamente el filtro que iba a aplicar cualquier agente aduanal en
   la primera junta — solo que este te lo dijo gratis y sin costarte un prospecto.

2. **Nombró el hueco con precisión:** *«te falta conocer la operación»* y *«ver qué
   documentos se integran en el despacho aduanero»*. No es una crítica vaga: es una
   instrucción con pasos.

3. **Y después te dio la especificación del producto:**
   > «Y si tu aplicación puede detectar errores justo entre esa factura y el pedimento…»

   Un experto del gremio te acaba de decir qué construir. Eso no se compra ni se
   investiga: normalmente cuesta seis meses de conversaciones equivocadas.

**No se quedó en corregir. Se quedó pensando en cómo hacerlo funcionar.** Eso no es alguien
desestimando la idea; es alguien entrándole.

## Cómo contestar

Tres cosas, en este orden:

1. **Aceptar la corrección sin defenderla.** Nada de «sí, sí sabía». La respuesta correcta
   a un experto que te corrige es agradecer y demostrar que entendiste.
2. **Demostrar que ya trabajaste con lo que dijo.** Devolverle la cadena correcta es la
   prueba de que lo escuchaste.
3. **Pedir una sola cosa concreta.** El expediente real. Una petición, no tres.

---

## Mensaje sugerido

> Ajústalo a como se hablan ustedes. Si es tu papá, esto probablemente suena demasiado
> formal — báJale. Lo que no debe cambiar es la estructura: acepto, demuestro, pido una cosa.

```
Tienes razón y me sirvió mucho que me lo dijeras así.

Estaba mezclando dos facturas distintas: la de honorarios que la agencia le
cobra al importador, con la factura de la mercancía, que la emite el
proveedor extranjero y es la que ampara el valor. No son lo mismo y yo las
estaba tratando igual.

Me puse a estudiarlo y lo que entiendo ahora es esto, corrígeme donde me
equivoque:

La factura del proveedor extranjero se transmite como COVE, que lo hace la
agencia y firma con el sello de VUCEM, y de ahí sale el acuse de valor. Con
ese número el importador elabora la MVE y la firma con su e.firma, porque la
agencia no puede firmarla por él, y de ahí sale el MNVA. Los dos folios se
declaran en el pedimento, y ya validado y pagado se genera el DODA.

Lo que más me llamó la atención estudiándolo es el tema de los incrementables
según el incoterm. Si la operación es CIF o CFR el flete ya viene dentro del
precio pagado y volver a declararlo sobrevalúa; si es FOB y no se declara,
subvalúa. Eso último es lo que trae multa fuerte.

Eso sí lo puedo detectar de forma automática. No necesito ni IA: es comparar
el incoterm contra los incrementables declarados y marcar cuando no cuadran.

Lo que me falta es justo lo que dijiste: no he visto un expediente completo de
una operación real.

¿Me puedes conseguir uno, aunque venga tachado o con datos falsos? Lo que
necesito ver es la factura del proveedor, el COVE con su acuse, la MVE y el
MNVA, el pedimento y el DODA de una sola operación, para poder seguirla de
principio a fin.

Con eso armo el comparador y te lo enseño antes de enseñárselo a nadie más.
```

## Después de que conteste

**Si manda el expediente** — es la señal más fuerte que puedes recibir. Bloquea el sábado
completo. Traza la operación a mano antes de escribir una línea de código: cada campo,
de dónde sale, a dónde llega.

**Si contesta pero no manda nada** — pídele algo más chico y más fácil de dar:
> «¿Me dejas ver cómo se hace un COVE alguna vez que tengas uno abierto? Con verlo una vez
> me destrabo.»

**Si te corrige otra vez** — mejor todavía. Cada corrección de este tipo vale más que una
semana de investigación. Escríbelas todas en `08-LA-OPERACION.md`.

**Cuando el validador funcione, se lo enseñas a él primero.** Si un agente con años de
oficio dice «esto sí sirve», ya tienes el producto validado. Y si dice «no sirve», te
ahorró meses.

## Las preguntas siguientes, cuando haya oportunidad

Una por conversación, nunca en lista:

1. ¿Qué tan seguido se atora el ida y vuelta del COVE y el MNVA con los importadores?
2. Cuando hay que rectificar un pedimento, ¿cuánto cuesta en dinero y en tiempo?
3. ¿Quién captura los datos del COVE en una agencia? ¿Alguien los revisa después?
4. De los errores que has visto, ¿cuál es el que más caro sale?
5. Con la responsabilidad solidaria nueva, ¿cambió algo de cómo revisan a sus importadores?

> La 2 y la 4 son las que producen la cifra de dolor. Sin una cifra no hay precio
> defendible. Pero se preguntan sueltas, en su momento — no como cuestionario.

## Una nota

Escribió «¡Eres exitoso hijo!» en tu pizarrón. Quien te corrige con ese detalle y además
te escribe eso no está dudando de ti: te está exigiendo el estándar del gremio en el que
te va a tener que presentar. **Ese es el mejor activo que tiene este proyecto**, y vale
más que la investigación de mercado, la ventana del 30 de septiembre y el catálogo de
precios juntos.
