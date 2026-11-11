# ⚠ BORRADOR SIN EJECUTAR NI PROBAR. Escrito a ciegas, sin Blender delante.
# ⚠ Llama a read_factory_settings(use_empty=True): VACÍA la escena abierta.
#   Ejecutar solo en un Blender nuevo, nunca sobre un .blend con trabajo.
#   Sirve como punto de partida para el blocking, no como escena final.
"""HERIDAS FINAS — escena 3D (Blender / Cycles). Uso: python build_scene.py
Construye todo por código: corazón-reliquia, 3 espadas, corona (Geometry Nodes),
triángulo, materiales PBR procedurales, luces, niebla, partículas y compositor."""
import bpy, bmesh, math, random, os
import numpy as np
from mathutils import Vector, Matrix, Euler

HERE = os.path.dirname(os.path.abspath(__file__))
CK = os.path.join(HERE, "checkpoints"); os.makedirs(CK, exist_ok=True)
random.seed(33)
bpy.ops.wm.read_factory_settings(use_empty=True)
S = bpy.context.scene

def coll(name):
    c = bpy.data.collections.new(name); S.collection.children.link(c); return c
C_HEART, C_SW, C_CROWN, C_TRI, C_FX, C_LIGHT = [coll(n) for n in
    ("Corazon", "Espadas", "Corona", "Triangulo", "FX_fondo", "Luces")]

def link(o, c):
    for k in list(o.users_collection): k.objects.unlink(o)
    c.objects.link(o); return o

def mesh_obj(name, bm, c, smooth=True):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); c.objects.link(o)
    for p in me.polygons: p.use_smooth = smooth
    return o

def prim(op, c, name, **kw):
    getattr(bpy.ops.mesh, op)(**kw); o = bpy.context.active_object; o.name = name
    link(o, c); return o

def smooth(o):
    for p in o.data.polygons: p.use_smooth = True

# ───────────────────────── MATERIALES PBR ─────────────────────────
def pbr(name, colA, colB, metallic, r0, r1, *, grain=60, grain_str=.15, scratch=.0,
        scratch_dir=(300, 300, 6), coat=0, coat_rough=.15, ao=None, edge=None,
        cracks=0, emission=None, var_scale=3.0, seam=False, aniso=0):
    m = bpy.data.materials.new(name)
    try: m.use_nodes = True
    except Exception: pass
    nt = m.node_tree; N = nt.nodes; L = nt.links
    b = next(n for n in N if n.type == 'BSDF_PRINCIPLED')
    def node(t, **kw):
        n = N.new(t)
        for k, v in kw.items(): setattr(n, k, v)
        return n
    tc = node('ShaderNodeTexCoord'); co = tc.outputs['Object']
    # variación amplia (color + roughness)
    n1 = node('ShaderNodeTexNoise'); n1.inputs['Scale'].default_value = var_scale
    n1.inputs['Detail'].default_value = 8; n1.inputs['Roughness'].default_value = .62
    L.new(co, n1.inputs['Vector'])
    mix = node('ShaderNodeMix', data_type='RGBA')
    mix.inputs['A'].default_value = (*colA, 1); mix.inputs['B'].default_value = (*colB, 1)
    cr = node('ShaderNodeValToRGB'); cr.color_ramp.elements[0].position = .35; cr.color_ramp.elements[1].position = .68
    L.new(n1.outputs['Fac'], cr.inputs['Fac']); L.new(cr.outputs['Color'], mix.inputs['Factor'])
    color = mix.outputs['Result']
    rough = node('ShaderNodeMapRange'); rough.inputs['To Min'].default_value = r0; rough.inputs['To Max'].default_value = r1
    n1b = node('ShaderNodeTexNoise'); n1b.inputs['Scale'].default_value = var_scale * 4.3; n1b.inputs['Detail'].default_value = 6
    L.new(co, n1b.inputs['Vector']); L.new(n1b.outputs['Fac'], rough.inputs['Value'])
    rough_out = rough.outputs['Result']
    # grano fino → bump
    g = node('ShaderNodeTexNoise'); g.inputs['Scale'].default_value = grain; g.inputs['Detail'].default_value = 4
    L.new(co, g.inputs['Vector'])
    bump = node('ShaderNodeBump'); bump.inputs['Strength'].default_value = grain_str; bump.inputs['Distance'].default_value = .01
    L.new(g.outputs['Fac'], bump.inputs['Height'])
    normal = bump.outputs['Normal']
    def add_math(a, bsock, op='ADD', clamp=False):
        mm = node('ShaderNodeMath', operation=op, use_clamp=clamp); L.new(a, mm.inputs[0])
        if isinstance(bsock, (int, float)): mm.inputs[1].default_value = bsock
        else: L.new(bsock, mm.inputs[1])
        return mm.outputs[0]
    def darken(col, fac_sock, to=(0, 0, 0)):
        mx = node('ShaderNodeMix', data_type='RGBA'); L.new(col, mx.inputs['A'])
        mx.inputs['B'].default_value = (*to, 1); L.new(fac_sock, mx.inputs['Factor']); return mx.outputs['Result']
    # microarañazos (ruido estirado en 2 direcciones)
    if scratch:
        acc = None
        for i, rot in enumerate(((0, 0, 0), (.3, 1.1, .7), (1.2, .2, 2.1))[: (1 if aniso else 3)]):
            mp = node('ShaderNodeMapping'); mp.inputs['Scale'].default_value = scratch_dir; mp.inputs['Rotation'].default_value = rot
            L.new(co, mp.inputs['Vector'])
            sn = node('ShaderNodeTexNoise'); sn.inputs['Scale'].default_value = 1.0 + i * .37; sn.inputs['Detail'].default_value = 3
            L.new(mp.outputs['Vector'], sn.inputs['Vector'])
            r = node('ShaderNodeValToRGB'); r.color_ramp.elements[0].position = .60 if not aniso else .3
            r.color_ramp.elements[1].position = .66 if not aniso else .7
            L.new(sn.outputs['Fac'], r.inputs['Fac'])
            acc = r.outputs['Color'] if acc is None else add_math(acc, r.outputs['Color'], 'MAXIMUM')
        sc = add_math(acc, scratch, 'MULTIPLY')
        rough_out = add_math(rough_out, sc, 'ADD', True)
        b2 = node('ShaderNodeBump'); b2.inputs['Strength'].default_value = .25 if not aniso else .12; b2.inputs['Distance'].default_value = .002; b2.invert = True
        L.new(acc, b2.inputs['Height']); L.new(normal, b2.inputs['Normal']); normal = b2.outputs['Normal']
    # grietas (voronoi distancia-al-borde)
    if cracks:
        wn = node('ShaderNodeTexNoise'); wn.inputs['Scale'].default_value = 2.5; L.new(co, wn.inputs['Vector'])
        wm = node('ShaderNodeMix', data_type='RGBA'); wm.inputs['Factor'].default_value = .12
        L.new(co, wm.inputs['A']); L.new(wn.outputs['Color'], wm.inputs['B'])
        v = node('ShaderNodeTexVoronoi', feature='DISTANCE_TO_EDGE'); v.inputs['Scale'].default_value = 5.5
        L.new(wm.outputs['Result'], v.inputs['Vector'])
        r = node('ShaderNodeValToRGB'); r.color_ramp.elements[0].position = 0.0; r.color_ramp.elements[0].color = (1, 1, 1, 1)
        r.color_ramp.elements[1].position = .035; r.color_ramp.elements[1].color = (0, 0, 0, 1)
        L.new(v.outputs['Distance'], r.inputs['Fac'])
        # máscara: sólo en algunas zonas
        mk = node('ShaderNodeTexNoise'); mk.inputs['Scale'].default_value = 1.4; L.new(co, mk.inputs['Vector'])
        mr = node('ShaderNodeValToRGB'); mr.color_ramp.elements[0].position = .48; mr.color_ramp.elements[1].position = .62
        L.new(mk.outputs['Fac'], mr.inputs['Fac'])
        ck = add_math(add_math(r.outputs['Color'], mr.outputs['Color'], 'MULTIPLY'), cracks, 'MULTIPLY')
        color = darken(color, ck, (.02, .004, .004)); rough_out = add_math(rough_out, ck, 'ADD', True)
        b3 = node('ShaderNodeBump'); b3.inputs['Strength'].default_value = .6; b3.inputs['Distance'].default_value = .01; b3.invert = True
        L.new(ck, b3.inputs['Height']); L.new(normal, b3.inputs['Normal']); normal = b3.outputs['Normal']
    if seam:  # costura central: surco en x=0
        sx = node('ShaderNodeSeparateXYZ'); L.new(co, sx.inputs[0])
        ab = add_math(sx.outputs['X'], 0, 'ABSOLUTE')
        r = node('ShaderNodeMapRange'); r.inputs['From Min'].default_value = 0.0; r.inputs['From Max'].default_value = .022
        r.inputs['To Min'].default_value = 1; r.inputs['To Max'].default_value = 0
        L.new(ab, r.inputs['Value'])
        color = darken(color, add_math(r.outputs['Result'], .7, 'MULTIPLY'), (.03, .005, .005))
        b4 = node('ShaderNodeBump'); b4.inputs['Strength'].default_value = .9; b4.inputs['Distance'].default_value = .02; b4.invert = True
        L.new(r.outputs['Result'], b4.inputs['Height']); L.new(normal, b4.inputs['Normal']); normal = b4.outputs['Normal']
    # pátina en cavidades (AO)
    if ao:
        a = node('ShaderNodeAmbientOcclusion'); a.inputs['Distance'].default_value = .06; a.samples = 8
        L.new(normal, a.inputs['Normal'])
        inv = node('ShaderNodeMapRange'); inv.inputs['From Min'].default_value = .35; inv.inputs['From Max'].default_value = .9
        inv.inputs['To Min'].default_value = .85; inv.inputs['To Max'].default_value = 0
        L.new(a.outputs['AO'], inv.inputs['Value'])
        color = darken(color, inv.outputs['Result'], ao)
        rough_out = add_math(rough_out, add_math(inv.outputs['Result'], .35, 'MULTIPLY'), 'ADD', True)
    # desgaste de bordes (pointiness)
    if edge:
        ge = node('ShaderNodeNewGeometry')
        r = node('ShaderNodeValToRGB'); r.color_ramp.elements[0].position = .53; r.color_ramp.elements[1].position = .62
        L.new(ge.outputs['Pointiness'], r.inputs['Fac'])
        en = node('ShaderNodeTexNoise'); en.inputs['Scale'].default_value = 25; L.new(co, en.inputs['Vector'])
        ef = add_math(r.outputs['Color'], en.outputs['Fac'], 'MULTIPLY')
        color = darken(color, ef, edge[0]); rough_out = add_math(rough_out, add_math(ef, edge[1], 'MULTIPLY'), 'ADD', True)
    L.new(color, b.inputs['Base Color']); L.new(rough_out, b.inputs['Roughness']); L.new(normal, b.inputs['Normal'])
    b.inputs['Metallic'].default_value = metallic
    if aniso: b.inputs['Anisotropic'].default_value = aniso
    if coat:
        b.inputs['Coat Weight'].default_value = coat; b.inputs['Coat Roughness'].default_value = coat_rough
        b.inputs['Coat Tint'].default_value = (.9, .55, .45, 1)
    if emission:
        b.inputs['Emission Color'].default_value = (*emission[0], 1); b.inputs['Emission Strength'].default_value = emission[1]
    return m

M_HEART = pbr("Cuero_lacado_rojo", (.115, .008, .010), (.035, .004, .006), 0, .30, .62, grain=140, grain_str=.22,
              scratch=.22, scratch_dir=(160, 160, 5), coat=.45, coat_rough=.22, cracks=.9,
              edge=((.30, .13, .07), .35), ao=(.012, .002, .003), var_scale=2.2, seam=True)
M_STEEL = pbr("Acero_cepillado", (.62, .62, .64), (.42, .43, .46), 1, .16, .34, grain=220, grain_str=.04,
              scratch=.30, scratch_dir=(900, 900, 3), aniso=.6, var_scale=6, edge=((.9, .9, .9), -.25))
M_BRASS = pbr("Laton_envejecido", (.52, .33, .10), (.30, .17, .05), 1, .30, .58, grain=180, grain_str=.10,
              scratch=.25, ao=(.035, .03, .012), edge=((.85, .62, .28), -.2), var_scale=9)
M_GRIP = pbr("Cuero_borgona", (.085, .010, .016), (.03, .004, .008), 0, .50, .78, grain=260, grain_str=.35,
             scratch=.15, ao=(.008, .001, .002), edge=((.25, .08, .06), .2), var_scale=14)
M_GOLD = pbr("Oro_envejecido", (.80, .52, .16), (.50, .29, .07), 1, .22, .46, grain=200, grain_str=.08,
             scratch=.30, ao=(.05, .028, .008), edge=((1, .82, .45), -.15), var_scale=7)
M_TRI = pbr("Oro_triangulo_emisivo", (.80, .52, .16), (.55, .32, .08), 1, .25, .45, grain=160, grain_str=.08,
            scratch=.25, ao=(.06, .03, .01), emission=((1, .55, .16), .35), var_scale=5)
M_THREAD = pbr("Hilo_encerado", (.42, .26, .10), (.25, .14, .05), 0, .55, .8, grain=500, grain_str=.4, var_scale=30)
M_33 = pbr("Oro_quemado_33", (.20, .12, .035), (.07, .04, .012), 1, .35, .6, grain=200, grain_str=.1, scratch=.2, var_scale=12)

# ───────────────────────── 1. CORAZÓN SIMBÓLICO ─────────────────────────
HS = Vector((.66, .80, .80)); HO = Vector((0, 0, -.63))   # escala / posición
def heart_f(p):
    x, y, z = p[..., 0], p[..., 1], p[..., 2]
    return (x*x + 2.25*y*y + z*z - 1)**3 - x*x*z**3 - (9/80)*y*y*z**3
def heart_r(d):
    lo = np.zeros(len(d)); hi = np.full(len(d), 3.0)
    for _ in range(40):
        mid = (lo + hi) / 2; inside = heart_f(d * mid[:, None]) < 0
        lo = np.where(inside, mid, lo); hi = np.where(inside, hi, mid)
    return (lo + hi) / 2
bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=6, radius=1)
d = np.array([v.co[:] for v in bm.verts]); d /= np.linalg.norm(d, axis=1)[:, None]
r = heart_r(d)
for v, dd, rr in zip(bm.verts, d, r): v.co = Vector(dd * rr) * HS
heart = mesh_obj("Corazon_reliquia", bm, C_HEART); heart.location = HO; heart.data.materials.append(M_HEART)
sm = heart.modifiers.new("Suavizado", 'CORRECTIVE_SMOOTH'); sm.iterations = 6; sm.factor = .5

def heart_pt(dirv):  # punto de superficie en espacio mundo
    dd = np.array([dirv]); dd = dd / np.linalg.norm(dd)
    return Vector(dd[0] * heart_r(dd)[0]) * HS + HO
# costura: puntadas cruzadas sobre la línea central frontal
for i in range(26):
    phi = math.radians(-62 + i * 5.2)
    p = heart_pt((0, -math.cos(phi), math.sin(phi)))
    st = prim("primitive_cylinder_add", C_HEART, f"Puntada_{i:02d}", radius=.0055, depth=.085, vertices=10)
    st.rotation_euler = (phi + math.pi/2, math.radians(90), 0); st.rotation_euler = Euler((0, math.radians(90), 0))
    st.rotation_euler.rotate_axis('X', random.uniform(-.25, .25) + (.35 if i % 2 else -.35))
    st.location = p + Vector((0, -.001, 0)); smooth(st); st.data.materials.append(M_THREAD)
# 33 gótico, incrustado en el cuero
font = os.path.join(HERE, "..", "GrenzeGotisch.ttf")
cu = bpy.data.curves.new("txt33", 'FONT'); cu.body = "33"; cu.size = .34; cu.align_x = 'CENTER'; cu.align_y = 'CENTER'
cu.resolution_u = 8
if os.path.exists(font): cu.font = bpy.data.fonts.load(font)
t = bpy.data.objects.new("Marca_33", cu); C_HEART.objects.link(t)
t.rotation_euler = (math.radians(90), 0, 0); t.location = (0.0, -1.2, -.66)
bpy.context.view_layer.objects.active = t; t.select_set(True)
bpy.ops.object.convert(target='MESH'); bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.quads_convert_to_tris(); bpy.ops.mesh.subdivide(number_cuts=2); bpy.ops.object.mode_set(mode='OBJECT')
sw = t.modifiers.new("Proyectar", 'SHRINKWRAP'); sw.target = heart; sw.wrap_method = 'PROJECT'
sw.use_project_x = False; sw.use_project_y = True; sw.use_project_z = False; sw.use_positive_direction = True
sw.use_negative_direction = False; sw.offset = .002
so = t.modifiers.new("Grosor", 'SOLIDIFY'); so.thickness = .012; so.offset = 1
t.data.materials.append(M_33); t.select_set(False)

# ───────────────────────── 2. ESPADAS ─────────────────────────
def make_sword(name, guard_pos, direction):
    root = bpy.data.objects.new(name, None); C_SW.objects.link(root); root.empty_display_size = .1
    parts = []
    BL = 1.55
    # hoja: sección hexagonal aplanada con vaciado central, estrechada hacia la punta
    bm = bmesh.new(); rings = []; n = 28
    for i in range(n):
        tt = i / (n - 1) * .93
        w = .058 * (1 - .42 * tt); th = .0115 * (1 - .45 * tt); z = -tt * BL
        sec = [(w, 0), (.34*w, th), (.10*w, th*.55), (-.10*w, th*.55), (-.34*w, th), (-w, 0),
               (-.34*w, -th), (-.10*w, -th*.55), (.10*w, -th*.55), (.34*w, -th)]
        if tt > .72:  # el vaciado muere antes de la punta
            sec = [(a, (bb if abs(a) > .2*w else math.copysign(th, bb))) for a, bb in sec]
        rings.append([bm.verts.new((a, bb, z)) for a, bb in sec])
    for a, bb in zip(rings, rings[1:]):
        for j in range(10): bm.faces.new((a[j], a[(j+1) % 10], bb[(j+1) % 10], bb[j]))
    tip = bm.verts.new((0, 0, -BL))
    for j in range(10): bm.faces.new((rings[-1][j], rings[-1][(j+1) % 10], tip))
    bm.faces.new(rings[0][::-1])
    blade = mesh_obj(name + "_hoja", bm, C_SW, smooth=False); blade.data.materials.append(M_STEEL); parts.append(blade)
    # guarda: perfil rectangular que se ensancha en los extremos + biseles
    bm = bmesh.new(); rings = []; n = 21
    for i in range(n):
        x = (i / (n - 1) - .5) * .56; u = abs(x) / .28
        h = .020 + .020 * u**2.2 + .018 * math.exp(-(u / .16)**2); dpt = .020 + .006 * u**2 + .012 * math.exp(-(u / .16)**2)
        zc = .012 - .030 * u**2   # ligera curva hacia la hoja
        rings.append([bm.verts.new((x, sy * dpt, zc + sz * h)) for sy, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1))])
    for a, bb in zip(rings, rings[1:]):
        for j in range(4): bm.faces.new((a[j], bb[j], bb[(j+1) % 4], a[(j+1) % 4]))
    bm.faces.new(rings[0]); bm.faces.new(rings[-1][::-1])
    guard = mesh_obj(name + "_guarda", bm, C_SW, smooth=False); guard.data.materials.append(M_BRASS)
    bv = guard.modifiers.new("Bisel", 'BEVEL'); bv.width = .007; bv.segments = 3
    ss = guard.modifiers.new("Subd", 'SUBSURF'); ss.levels = ss.render_levels = 1; smooth(guard); parts.append(guard)
    for sx in (-1, 1):
        fin = prim("primitive_uv_sphere_add", C_SW, name + "_remate", radius=.036, segments=24, ring_count=12,
                   location=(sx * .285, 0, -.018)); fin.scale = (1, .9, 1.15); smooth(fin); fin.data.materials.append(M_BRASS); parts.append(fin)
    # empuñadura abarrilada + cordón de cuero en espiral + virolas
    bm = bmesh.new(); rings = []; n = 14; G0, G1 = .035, .40
    for i in range(n):
        tt = i / (n - 1); rr = .024 + .009 * math.sin(math.pi * tt) ** .8
        rings.append([bm.verts.new((rr * math.cos(a), rr * .88 * math.sin(a), G0 + tt * (G1 - G0)))
                      for a in [k * math.tau / 20 for k in range(20)]])
    for a, bb in zip(rings, rings[1:]):
        for j in range(20): bm.faces.new((a[j], a[(j+1) % 20], bb[(j+1) % 20], bb[j]))
    grip = mesh_obj(name + "_empunadura", bm, C_SW); grip.data.materials.append(M_GRIP); parts.append(grip)
    cu = bpy.data.curves.new(name + "_cordon", 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = .0062; cu.bevel_resolution = 3
    sp = cu.splines.new('POLY'); turns = 11; npt = turns * 24; sp.points.add(npt - 1)
    for i in range(npt):
        tt = i / (npt - 1); a = tt * turns * math.tau; rr = .026 + .009 * math.sin(math.pi * tt) ** .8
        sp.points[i].co = (rr * math.cos(a), rr * .88 * math.sin(a), G0 + .01 + tt * (G1 - G0 - .02), 1)
    cord = bpy.data.objects.new(name + "_cordon", cu); C_SW.objects.link(cord); cord.data.materials.append(M_GRIP); parts.append(cord)
    for z, rr in ((G0 + .004, .034), (G1 - .002, .031)):
        fe = prim("primitive_torus_add", C_SW, name + "_virola", major_radius=rr - .006, minor_radius=.0085,
                  major_segments=32, minor_segments=10, location=(0, 0, z)); smooth(fe); fe.data.materials.append(M_BRASS); parts.append(fe)
    pm = prim("primitive_uv_sphere_add", C_SW, name + "_pomo", radius=1, segments=32, ring_count=16, location=(0, 0, G1 + .058))
    pm.scale = (.062, .048, .066); smooth(pm); pm.data.materials.append(M_BRASS); parts.append(pm)
    nb = prim("primitive_uv_sphere_add", C_SW, name + "_boton", radius=.02, segments=16, ring_count=8, location=(0, 0, G1 + .13))
    smooth(nb); nb.data.materials.append(M_BRASS); parts.append(nb)
    for p in parts: p.parent = root
    root.location = guard_pos
    dv = Vector(direction).normalized(); q = Vector((0, 0, -1)).rotation_difference(dv)
    root.rotation_euler = q.to_euler()
    return root

make_sword("Espada_centro", (0, -.06, 1.00), (0, .03, -1))
make_sword("Espada_izq", (-.93, -.42, .72), (.50, .22, -1))
make_sword("Espada_der", (.93, -.42, .72), (-.50, .22, -1))

# ───────────────────────── 3. CORONA DE LAUREL (Geometry Nodes) ─────────────────────────
bm = bmesh.new(); Lf, Wf = .30, .095; grid = []
for i in range(15):
    s = i / 14; w = Wf * (s ** .55) * ((1 - s) ** .85) * 1.75; row = []
    for j in range(7):
        u = j / 3 - 1
        z = .9 * w * u * u + .10 * Lf * s * s - .012 * (1 - abs(u)) * math.sin(math.pi * s)
        row.append(bm.verts.new((s * Lf, u * w, z)))
    grid.append(row)
for a, bb in zip(grid, grid[1:]):
    for j in range(6): bm.faces.new((a[j], a[j+1], bb[j+1], bb[j]))
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
leaf = mesh_obj("Hoja_laurel", bm, C_CROWN); leaf.data.materials.append(M_GOLD)
so = leaf.modifiers.new("Grosor", 'SOLIDIFY'); so.thickness = .007; so.offset = 0
ss = leaf.modifiers.new("Subd", 'SUBSURF'); ss.levels = ss.render_levels = 1
leaf.hide_render = True; leaf.hide_viewport = True

ng = bpy.data.node_groups.new("GN_Corona_Laurel", 'GeometryNodeTree')
ng.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
N, L = ng.nodes, ng.links
def gn(t, **kw):
    n = N.new(t)
    for k, v in kw.items(): setattr(n, k, v)
    return n
def setin(n, **kw):
    for k, v in kw.items():
        n.inputs[k.replace('_', ' ')].default_value = v
R = .70
arc = gn('GeometryNodeCurveArc'); setin(arc, Resolution=64, Radius=R, Start_Angle=math.radians(97), Sweep_Angle=math.radians(166))
res = gn('GeometryNodeResampleCurve'); L.new(arc.outputs['Curve'], res.inputs['Curve']); res.inputs['Count'].default_value = 46
oi = gn('GeometryNodeObjectInfo'); oi.inputs['Object'].default_value = leaf; oi.inputs['As Instance'].default_value = True
tan = gn('GeometryNodeInputTangent')
al = gn('FunctionNodeAlignRotationToVector', axis='X'); L.new(tan.outputs['Tangent'], al.inputs['Vector'])
def rnd(lo, hi, seed):
    n = gn('FunctionNodeRandomValue', data_type='FLOAT'); n.inputs[2].default_value = lo; n.inputs[3].default_value = hi
    n.inputs['Seed'].default_value = seed; return n.outputs[1]
cx = gn('ShaderNodeCombineXYZ'); L.new(rnd(-1.5, 1.5, 1), cx.inputs['X']); L.new(rnd(-.75, -.2, 2), cx.inputs['Y']); L.new(rnd(-.85, .85, 3), cx.inputs['Z'])
e2r = gn('FunctionNodeEulerToRotation'); L.new(cx.outputs[0], e2r.inputs[0])
rr = gn('FunctionNodeRotateRotation', rotation_space='LOCAL'); L.new(al.outputs['Rotation'], rr.inputs['Rotation']); L.new(e2r.outputs[0], rr.inputs['Rotate By'])
iop = gn('GeometryNodeInstanceOnPoints')
L.new(res.outputs['Curve'], iop.inputs['Points']); L.new(oi.outputs['Geometry'], iop.inputs['Instance'])
L.new(rr.outputs['Rotation'], iop.inputs['Rotation'])
scl = gn('ShaderNodeCombineXYZ'); sv = rnd(.62, 1.12, 4)
for k in 'XYZ': L.new(sv, scl.inputs[k])
L.new(scl.outputs[0], iop.inputs['Scale'])
rz = gn('GeometryNodeRealizeInstances'); L.new(iop.outputs['Instances'], rz.inputs['Geometry'])
tr = gn('GeometryNodeTransform'); tr.inputs['Scale'].default_value = (-1, 1, 1); L.new(rz.outputs['Geometry'], tr.inputs['Geometry'])
ff = gn('GeometryNodeFlipFaces'); L.new(tr.outputs['Geometry'], ff.inputs['Mesh'])
circ = gn('GeometryNodeCurvePrimitiveCircle'); setin(circ, Resolution=96, Radius=R)
prof = gn('GeometryNodeCurvePrimitiveCircle'); setin(prof, Resolution=12, Radius=.021)
c2m = gn('GeometryNodeCurveToMesh'); L.new(circ.outputs['Curve'], c2m.inputs['Curve']); L.new(prof.outputs['Curve'], c2m.inputs['Profile Curve'])
shs = gn('GeometryNodeSetShadeSmooth'); L.new(c2m.outputs['Mesh'], shs.inputs[0])
jn = gn('GeometryNodeJoinGeometry')
for src in (rz.outputs['Geometry'], ff.outputs['Mesh'], shs.outputs[0]): L.new(src, jn.inputs[0])
sm_ = gn('GeometryNodeSetMaterial'); sm_.inputs['Material'].default_value = M_GOLD; L.new(jn.outputs[0], sm_.inputs['Geometry'])
out = gn('NodeGroupOutput'); L.new(sm_.outputs[0], out.inputs[0])
crown = bpy.data.objects.new("Corona_laurel", bpy.data.meshes.new("Corona_laurel")); C_CROWN.objects.link(crown)
md = crown.modifiers.new("GeometryNodes", 'NODES'); md.node_group = ng
crown.location = (0, -.02, .86); crown.rotation_euler = (math.radians(16), 0, 0)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(CK, "v01_modelos.blend"))

# ───────────────────────── 4. TRIÁNGULO ─────────────────────────
def tri_pts(half, zb): return [(-half, zb), (half, zb), (0, zb + half * math.sqrt(3))]
bm = bmesh.new(); T = .028
o_ = tri_pts(1.42, -1.33); i_ = tri_pts(1.42 - .095 * math.sqrt(3), -1.33 + .095)
vs = {(k, s, j): bm.verts.new((p[0], s * T, p[1])) for k, pts in (('o', o_), ('i', i_)) for s in (-1, 1) for j, p in enumerate(pts)}
for j in range(3):
    k = (j + 1) % 3
    bm.faces.new((vs['o', -1, j], vs['o', -1, k], vs['i', -1, k], vs['i', -1, j]))
    bm.faces.new((vs['o', 1, k], vs['o', 1, j], vs['i', 1, j], vs['i', 1, k]))
    bm.faces.new((vs['o', -1, k], vs['o', -1, j], vs['o', 1, j], vs['o', 1, k]))
    bm.faces.new((vs['i', -1, j], vs['i', -1, k], vs['i', 1, k], vs['i', 1, j]))
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
tri = mesh_obj("Triangulo_oro", bm, C_TRI, smooth=False); tri.location = (0, .95, 0); tri.data.materials.append(M_TRI)
bv = tri.modifiers.new("Bisel", 'BEVEL'); bv.width = .012; bv.segments = 3
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(CK, "v02_materiales.blend"))

# ───────────────────────── 5. FONDO, NIEBLA, PARTÍCULAS ─────────────────────────
bg = prim("primitive_plane_add", C_FX, "Fondo_nebulosa", size=16, location=(0, 4.5, 0)); bg.rotation_euler = (math.radians(90), 0, 0)
m = bpy.data.materials.new("Nebulosa_borgona")
try: m.use_nodes = True
except Exception: pass
nt = m.node_tree; N = nt.nodes; L = nt.links; N.clear()
tc = N.new('ShaderNodeTexCoord')
n1 = N.new('ShaderNodeTexNoise'); n1.inputs['Scale'].default_value = .55; n1.inputs['Detail'].default_value = 10; n1.inputs['Roughness'].default_value = .68; n1.inputs['Distortion'].default_value = 1.6
L.new(tc.outputs['Object'], n1.inputs['Vector'])
cr = N.new('ShaderNodeValToRGB'); e = cr.color_ramp.elements
e[0].position = .40; e[0].color = (.0015, .0003, .0005, 1); e[1].position = .78; e[1].color = (.9, .22, .04, 1)
for pos, col in ((.52, (.03, .002, .004, 1)), (.63, (.16, .008, .008, 1)), (.70, (.38, .04, .012, 1))):
    x = e.new(pos); x.color = col
L.new(n1.outputs['Fac'], cr.inputs['Fac'])
# viñeta radial para que el centro respire detrás del corazón y los bordes caigan a negro
sx = N.new('ShaderNodeVectorMath'); sx.operation = 'LENGTH'; L.new(tc.outputs['Object'], sx.inputs[0])
vr = N.new('ShaderNodeMapRange'); vr.inputs['From Min'].default_value = 1.2; vr.inputs['From Max'].default_value = 4.2
vr.inputs['To Min'].default_value = 1; vr.inputs['To Max'].default_value = .08; L.new(sx.outputs['Value'], vr.inputs['Value'])
em = N.new('ShaderNodeEmission'); L.new(cr.outputs['Color'], em.inputs['Color']); L.new(vr.outputs['Result'], em.inputs['Strength'])
o = N.new('ShaderNodeOutputMaterial'); L.new(em.outputs[0], o.inputs['Surface']); bg.data.materials.append(m)

fog = prim("primitive_cube_add", C_FX, "Niebla_volumetrica", size=1, location=(0, .5, 0)); fog.scale = (9, 8, 8)
m = bpy.data.materials.new("Niebla")
try: m.use_nodes = True
except Exception: pass
nt = m.node_tree; nt.nodes.clear()
pv = nt.nodes.new('ShaderNodeVolumePrincipled'); pv.inputs['Density'].default_value = .012; pv.inputs['Anisotropy'].default_value = .35
pv.inputs['Color'].default_value = (.9, .6, .5, 1)
o = nt.nodes.new('ShaderNodeOutputMaterial'); nt.links.new(pv.outputs[0], o.inputs['Volume']); fog.data.materials.append(m)
fog.display_type = 'WIRE'

bm = bmesh.new()
for i in range(420):
    p = Vector((random.uniform(-2.8, 2.8), random.uniform(-6.5, 3.5), random.uniform(-2.8, 2.8)))
    if abs(p.x) < 1.0 and abs(p.z) < 1.4 and -2 < p.y < 1: continue
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=random.uniform(.003, .011) * (1 + (p.y + 6.5) * .12),
                               matrix=Matrix.Translation(p))
dust = mesh_obj("Particulas_oro", bm, C_FX)
m = bpy.data.materials.new("Brasa")
try: m.use_nodes = True
except Exception: pass
nt = m.node_tree; nt.nodes.clear()
oi_ = nt.nodes.new('ShaderNodeNewGeometry')
cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = (1, .22, .05, 1); cr.color_ramp.elements[1].color = (1, .72, .28, 1)
nt.links.new(oi_.outputs['Random Per Island'], cr.inputs['Fac'])
em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Strength'].default_value = 14; nt.links.new(cr.outputs['Color'], em.inputs['Color'])
o = nt.nodes.new('ShaderNodeOutputMaterial'); nt.links.new(em.outputs[0], o.inputs['Surface']); dust.data.materials.append(m)

# ───────────────────────── 6. LUCES Y CÁMARA ─────────────────────────
def area(name, loc, target, size, power, color, spread=None):
    d = bpy.data.lights.new(name, 'AREA'); d.size = size; d.energy = power; d.color = color
    if spread: d.spread = spread
    o = bpy.data.objects.new(name, d); C_LIGHT.objects.link(o); o.location = loc
    o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler(); return o
area("Key_calida_45", (-4.2, -5.2, 4.6), (0, 0, -.2), 4.5, 1500, (1, .80, .58))
area("Fill_fria", (4.5, -4.5, -.5), (0, 0, -.3), 5, 110, (.55, .72, 1))
area("Rim_dorada_sup", (0, 3.2, 4.2), (0, 0, .1), 2.5, 1300, (1, .66, .26))
area("Rim_dorada_izq", (-3.6, 2.4, .3), (0, 0, -.4), 2.0, 700, (1, .60, .22))
area("Rim_dorada_der", (3.6, 2.4, .3), (0, 0, -.4), 2.0, 700, (1, .52, .20))
area("Brasa_inferior", (0, -1.5, -3.6), (0, 0, -.8), 3.0, 160, (1, .25, .08))

w = bpy.data.worlds.new("Mundo_borgona"); S.world = w
try: w.use_nodes = True
except Exception: pass
bgn = next(n for n in w.node_tree.nodes if n.type == 'BACKGROUND')
bgn.inputs['Color'].default_value = (.012, .0015, .003, 1); bgn.inputs['Strength'].default_value = 1

def camera(name, loc, target, lens=85, fstop=2.0):
    cd = bpy.data.cameras.new(name); cd.lens = lens; cd.sensor_width = 36
    cd.dof.use_dof = True; cd.dof.aperture_fstop = fstop
    o = bpy.data.objects.new(name, cd); S.collection.objects.link(o); o.location = loc
    o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    cd.dof.focus_distance = (Vector(target) - Vector(loc)).length - .45; return o
CAM = camera("Cam_PORTADA", (0, -9.6, 0), (0, 0, 0))
camera("Cam_test_34_izq", (-5.2, -7.4, 1.6), (0, 0, -.1))
camera("Cam_test_34_der", (5.4, -7.0, -.6), (0, 0, -.1))
camera("Cam_test_contacto", (-1.3, -3.6, 1.1), (-.1, -.2, .25), lens=70, fstop=4)
camera("Cam_test_corona", (1.2, -3.4, 2.2), (0, -.1, .85), lens=70, fstop=4)
S.camera = CAM

# ───────────────────────── 7. RENDER + COMPOSICIÓN ─────────────────────────
S.render.engine = 'CYCLES'; S.cycles.device = 'CPU'
S.cycles.samples = 128; S.cycles.use_adaptive_sampling = True; S.cycles.adaptive_threshold = .02
S.cycles.use_denoising = True; S.cycles.volume_bounces = 0; S.cycles.max_bounces = 6
S.cycles.sample_clamp_indirect = 6
S.render.resolution_x = S.render.resolution_y = 3000
S.view_settings.view_transform = 'AgX'
try: S.view_settings.look = 'AgX - Medium High Contrast'
except Exception as ex: print("look:", ex)
S.render.image_settings.file_format = 'PNG'; S.render.image_settings.color_mode = 'RGBA'

try:   # bloom en el compositor (Blender 5.x)
    ct = bpy.data.node_groups.new("Comp_Bloom", 'CompositorNodeTree'); S.compositing_node_group = ct
    ct.interface.new_socket(name="Image", in_out='OUTPUT', socket_type='NodeSocketColor')
    rl = ct.nodes.new('CompositorNodeRLayers'); gl = ct.nodes.new('CompositorNodeGlare'); go = ct.nodes.new('NodeGroupOutput')
    gl.inputs['Type'].default_value = 'Bloom'; gl.inputs['Threshold'].default_value = 1.4
    gl.inputs['Strength'].default_value = .55; gl.inputs['Size'].default_value = .55
    ct.links.new(rl.outputs['Image'], gl.inputs['Image']); ct.links.new(gl.outputs['Image'], go.inputs[0])
    print("COMPOSITOR OK", [i.name for i in gl.inputs])
except Exception as ex:
    print("COMPOSITOR FALLO:", repr(ex))
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(CK, "v03_luces.blend"))
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, "heridas_finas.blend"))
print("ESCENA GUARDADA")
