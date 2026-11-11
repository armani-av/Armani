# HERIDAS FINAS — 3D · Worklog 001: análisis de referencia y plan

Estado: **bloqueado antes del blocking**. La sesión en la nube no tiene conexión con el
MCP de Blender ni las skills `blender-*`. Nada de lo de abajo se ha ejecutado en Blender.

## 1. Lectura de la referencia (`references/portada_referencia_v1.webp`, 1254×1254)

Coordenadas normalizadas (u horizontal, v vertical, origen arriba-izquierda), medidas a ojo, ±0.02.

| Elemento | Posición | Notas |
|---|---|---|
| Título HERIDAS FINAS (2D) | u 0.07–0.94, v 0.03–0.16 | Zona reservada, fuera del render |
| Espada central | pomo v 0.12 · guarda v 0.255 · entra al corazón v ≈ 0.50 · u 0.50 | Vertical; pasa por el centro de la corona; el pomo invade la zona del título |
| Espadas laterales | pomo (0.215, 0.235) / (0.79, 0.235) · guarda ≈ (0.29, 0.33) / (0.72, 0.33) · entran en (0.37, 0.52) / (0.635, 0.525) | ≈ 28° respecto a la vertical, convergen hacia el centro |
| Corona de laurel | u 0.31–0.71, v 0.17–0.36 · aro centrado en v ≈ 0.29 | Elipse: aro inclinado ≈ 15° hacia cámara; flota sobre el corazón, no lo toca |
| Corazón | u 0.29–0.69, v 0.36–0.91 · centro (0.50, 0.63) | 40 % del ancho, 55 % del alto: es el protagonista |
| Triángulo | base v 0.81, esquinas u 0.11 y 0.89 · vértice oculto ≈ v 0.25 | Doble filete. **No es equilátero** en la referencia (alto/ancho ≈ 0.72; equilátero = 0.87) |
| Parental Advisory (2D) | u 0.035–0.17, v 0.89–0.975 | Capa 2D |
| Armani AV (2D) | u 0.81–0.955, v ≈ 0.955 | Capa 2D |

Paleta: negro cálido #0a0405 · borgoña #4a0a0e · rojo brasa #b3261a · oro antiguo #b98a3a · oro luz #e9c97a · acero #8d8f94.

Jerarquía: 1) corazón + 33, 2) corona y espada central (eje vertical), 3) espadas laterales (diagonales que cierran hacia el 33), 4) triángulo, 5) fondo.

## 2. Cámara y cuadrícula

- Cuadrada 1:1, focal larga (85 mm) frontal, casi ortográfica, para conservar la lectura de «carta de tarot».
- Cuadro útil 4×4 unidades en el plano del corazón → 1 u = 25 % del encuadre.
- Eje vertical de simetría en u 0.50; el corazón asimétrico lo rompe ligeramente.
- Franja superior (v < 0.17) e inferior (v > 0.88) reservadas para tipografía y sellos.
- Control de miniatura: reducir cada preview a 256×256 y comprobar que se leen corazón, corona y tres espadas.

## 3. Decisiones estéticas pendientes del artista

1. **Triángulo**: la referencia es isósceles achatado; el concepto original dice «equilátero».
   Propuesta: equilátero real con base u 0.15–0.85 y vértice en v ≈ 0.205 (queda detrás de la corona).
2. **Corazón**: la referencia es anatómico; el brief 3D pide simbólico, asimétrico, cuero lacado o madera tallada. Se sigue el brief.
3. **33**: se trata como parte del corazón (grabado), no como «texto»; va en el render.

## 4. Plan por etapas (cada una: preview 768–1000 px, ≥ 3 problemas, corrección, checkpoint)

1. Blocking + clay render ← **siguiente paso, requiere Blender local**
2. Siluetas · 3. Cámara y composición · 4. Materiales base · 5. Iluminación · 6. Microdetalle · 7. Composición final

## 5. Material disponible en esta carpeta

- `scripts/build_scene_BORRADOR.py`, `scripts/render_BORRADOR.py`: borrador **sin ejecutar** (ver aviso en cabecera).
- Tipografía y sellos 2D editables: `../portada.html` (capas SVG) y `../GrenzeGotisch.ttf` (33).
