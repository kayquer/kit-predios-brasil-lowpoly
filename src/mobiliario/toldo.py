"""Toldo de lona listrado verde e branco de loja, inclinado e com saia na frente, para prender na fachada (a peça
encosta na parede pelo lado +Y)."""
import os
import sys

import bmesh
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402

LARG, N = 0.79, 7
# perfil externo (y, z): preso na parede no alto, desce inclinado e termina na saia
EXT = [(0.07, 0.40), (-0.062, 0.115), (-0.062, 0.0)]
# perfil interno: a mesma lona deslocada para baixo/trás pela espessura
INT = [(0.07, 0.372), (-0.05, 0.112), (-0.05, 0.0)]


def _face(bm, vs, normal):
    f = bm.faces.new(vs)
    f.normal_update()
    if f.normal.dot(Vector(normal)) < 0:
        f.normal_flip()
    return f


def construir():
    inn = INT
    passo = LARG / N
    for i in range(N):
        x0, x1 = -LARG / 2 + i * passo, -LARG / 2 + (i + 1) * passo
        bm = bmesh.new()
        ext0 = [bm.verts.new((x0, y, z)) for (y, z) in EXT]
        ext1 = [bm.verts.new((x1, y, z)) for (y, z) in EXT]
        in0 = [bm.verts.new((x0, y, z)) for (y, z) in inn]
        in1 = [bm.verts.new((x1, y, z)) for (y, z) in inn]
        _face(bm, (ext0[0], ext0[1], ext1[1], ext1[0]), (0, -0.9, 0.4))   # lona inclinada (cima)
        _face(bm, (ext0[1], ext0[2], ext1[2], ext1[1]), (0, -1, 0))       # saia (frente)
        _face(bm, (in0[0], in0[1], in1[1], in1[0]), (0, 0.9, -0.4))       # lona por baixo
        _face(bm, (in0[1], in0[2], in1[2], in1[1]), (0, 1, 0))            # saia por dentro
        _face(bm, (ext0[2], in0[2], in1[2], ext1[2]), (0, 0, -1))         # barra da saia
        if i in (0, N - 1):
            x, vs, nx = (x0, ext0 + in0[::-1], -1) if i == 0 else (x1, ext1 + in1[::-1], 1)
            _face(bm, vs, (nx, 0, 0))                                      # lateral fechada
        L._objeto(bm, 'toldo_verde' if i % 2 == 0 else 'branco', nome='listra')


L.principal(__file__, construir)
