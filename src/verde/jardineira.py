"""Jardineira de calçada de concreto com terra, folhas grandes de comigo-ninguém-pode no meio e touceiras floridas
de maria-sem-vergonha rosa e vermelha nas pontas."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402

L.PALETA['folha_rajada'] = '#c9e39a'     # miolo claro da folha de comigo-ninguém-pode


def construir():
    w, d, h, e = 0.39, 0.29, 0.09, 0.03
    for (sx, sy, x, y) in ((w, e, 0, -d / 2 + e / 2), (w, e, 0, d / 2 - e / 2),
                           (e, d - 2 * e, -w / 2 + e / 2, 0), (e, d - 2 * e, w / 2 - e / 2, 0)):
        L.caixa((sx, sy, h), (x, y, 0), 'concreto')
    L.caixa((w - 2 * e, d - 2 * e, h - 0.015), (0, 0, 0), 'terra')
    zt = h - 0.015

    # Comigo-ninguém-pode: folhas largas inclinadas saindo do centro
    for i, ang in enumerate((45, 135, 225, 315)):
        a = math.radians(ang)
        cx, cy = -math.sin(a) * 0.035, math.cos(a) * 0.035
        L.caixa((0.045, 0.085, 0.005), (cx, cy, zt + 0.045 + 0.01 * (i % 2)), 'verde_escuro', rot=(38, 0, ang))
        L.caixa((0.02, 0.065, 0.005), (cx, cy, zt + 0.0495 + 0.01 * (i % 2)), 'folha_rajada', rot=(38, 0, ang))
    L.cilindro(0.012, 0.05, (0, 0, zt), 'verde_escuro', lados=4)

    # Maria-sem-vergonha: touceiras nas duas pontas com flores
    for x, cor in ((-0.12, 'flor_rosa'), (0.12, 'vermelho')):
        L.esfera(0.05, (x, 0, zt + 0.02), 'verde', escala=(1.0, 1.4, 0.6))
        L.esfera(0.042, (x, -0.012, zt + 0.045), cor, escala=(1.0, 1.25, 0.55))



L.principal(__file__, construir)
