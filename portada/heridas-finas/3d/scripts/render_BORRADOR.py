"""python render.py <blend> <cam|ALL_TESTS> <res> <samples> <out.png> [alpha]"""
import bpy, sys, os
blend, cam, res, spp, out = sys.argv[1:6]; alpha = len(sys.argv) > 6
bpy.ops.wm.open_mainfile(filepath=blend); S = bpy.context.scene
S.render.resolution_x = S.render.resolution_y = int(res); S.cycles.samples = int(spp)
if alpha:
    S.render.film_transparent = True
    for n in ("Fondo_nebulosa", "Niebla_volumetrica", "Particulas_oro"): bpy.data.objects[n].hide_render = True
cams = [o for o in bpy.data.objects if o.type == 'CAMERA'] if cam == 'ALL_TESTS' else [bpy.data.objects[cam]]
for c in cams:
    S.camera = c; S.render.filepath = out if len(cams) == 1 else os.path.join(out, c.name + ".png")
    bpy.ops.render.render(write_still=True); print("RENDER", c.name)
