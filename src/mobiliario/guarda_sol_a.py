"""Guarda-sol de bar amarelo (sem marca) com mesa quadrada e duas cadeiras de plástico brancas, de calçada de
boteco."""
import math
import os
import sys

import bmesh
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402


def lona(r, z_aba, z_topo, cores, lados=8, saia=0.03, centro=(0, 0)):
    """Lona do guarda-sol: gomos triangulares (cores alternadas) com saia, e o fundo num polígono só."""
    cx, cy = centro
    pts = [(cx + r * math.cos(2 * math.pi * (k + 0.5) / lados), cy + r * math.sin(2 * math.pi * (k + 0.5) / lados))
           for k in range(lados)]
    for k in range(lados):
        (x0, y0), (x1, y1) = pts[k], pts[(k + 1) % lados]
        bm = bmesh.new()
        a = bm.verts.new((cx, cy, z_topo))
        b, c = bm.verts.new((x0, y0, z_aba)), bm.verts.new((x1, y1, z_aba))
        d, e = bm.verts.new((x1, y1, z_aba - saia)), bm.verts.new((x0, y0, z_aba - saia))
        for vs in ((a, b, c), (b, e, d, c)):
            f = bm.faces.new(vs)
            f.normal_update()
            meio = sum((v.co for v in vs), Vector()) / len(vs)
            if f.normal.dot(meio - Vector((cx, cy, z_aba - 0.05))) < 0:
                f.normal_flip()
        L._objeto(bm, cores[k % len(cores)], nome='gomo')
    bm = bmesh.new()
    f = bm.faces.new([bm.verts.new((x, y, z_aba - saia)) for (x, y) in pts])
    f.normal_update()
    if f.normal.z > 0:
        f.normal_flip()
    L._objeto(bm, cores[0], nome='fundo')


def cadeira(x, y, lado, cor):
    """Cadeira de plástico de bar; `lado` = +1 encosto em +Y, -1 em -Y."""
    L.caixa((0.08, 0.08, 0.012), (x, y, 0.07), cor)
    L.caixa((0.08, 0.012, 0.095), (x, y + lado * 0.034, 0.075), cor, rot=(lado * -8, 0, 0))
    for dx in (-0.034, 0.034):
        L.caixa((0.012, 0.075, 0.07), (x + dx, y, 0), cor)


def construir():
    branco = 'branco'
    # mesa quadrada de plástico
    L.caixa((0.14, 0.14, 0.012), (0, 0, 0.13), branco)
    for dx in (-0.055, 0.055):
        L.caixa((0.012, 0.12, 0.13), (dx, 0, 0), branco)
    cadeira(-0.085, -0.145, -1, branco)
    cadeira(0.085, 0.145, 1, branco)
    # mastro e lona
    L.cano((0, 0, 0.0), (0, 0, 0.44), 0.008, 'metal', lados=4)
    lona(0.17, 0.37, 0.45, ('amarelo',), lados=8, saia=0.03)


L.principal(__file__, construir)
