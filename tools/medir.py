"""
Mede os .glb exportados e compara com tools/alvos.json (rodar no Blender, sem interface):

    blender -b --factory-startup --python tools/medir.py -- residencial/casa_terrea comercial/padaria_toldo
    blender -b --factory-startup --python tools/medir.py -- residencial      # um grupo inteiro

Imprime w (X), d (Y), h (Z), triângulos e se cabe no alvo (w e d são teto; h ±15%).
"""
import json
import os
import sys

import bpy
from mathutils import Vector

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALVOS = json.load(open(os.path.join(RAIZ, 'tools', 'alvos.json'), encoding='utf-8'))
args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
chaves = []
for a in args or [k for k in ALVOS if not k.startswith('_')]:
    chaves += [k for k in ALVOS if k == a or k.startswith(a + '/')]

for chave in chaves:
    caminho = os.path.join(RAIZ, 'models', chave + '.glb')
    if not os.path.exists(caminho):
        print(f'MEDIDA {chave}: sem arquivo')
        continue
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=caminho)
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    tris = 0
    for o in bpy.context.scene.objects:
        if o.type != 'MESH':
            continue
        for v in o.bound_box:
            p = o.matrix_world @ Vector(v)
            mn = Vector(map(min, mn, p))
            mx = Vector(map(max, mx, p))
        o.data.calc_loop_triangles()
        tris += len(o.data.loop_triangles)
    w, d, h = mx.x - mn.x, mx.y - mn.y, mx.z - mn.z
    alvo = ALVOS[chave]
    ok = w <= alvo['w'] + 0.005 and d <= alvo['d'] + 0.005 and abs(h - alvo['h']) <= 0.15 * alvo['h'] and tris <= 1500
    kb = os.path.getsize(caminho) / 1024
    print(f"MEDIDA {chave}: w {w:.3f}/{alvo['w']} d {d:.3f}/{alvo['d']} h {h:.3f}/{alvo['h']} tris {tris} kb {kb:.1f} -> {'OK' if ok else 'FORA DO ALVO'}")
