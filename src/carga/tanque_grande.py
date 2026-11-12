"""Dois tanques cilíndricos verticais brancos de usina de etanol, com faixa verde, teto cônico, passarela entre os
topos, escada em espiral com corrimão amarelo e bacia de contenção de concreto."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402

L.PALETA['faixa_usina'] = '#2f8a4a'


def tanque(x, y, r, h, z0):
    L.cilindro(r, h, (x, y, z0), 'parede', lados=12)
    L.cilindro(r + 0.006, 0.06, (x, y, z0 + h - 0.16), 'faixa_usina', lados=12)
    L.cone(r + 0.01, 0.10, (x, y, z0 + h), 'concreto', lados=12)


def escada_espiral(cx, cy, r, z0, z1, a0, a1, n):
    """Escada que sobe enrolada no costado do tanque (de a0 a a1 graus, sentido anti-horário)."""
    R = r + 0.04
    passo = math.radians(a1 - a0) / n
    seg = R * passo
    subida = (z1 - z0) / n
    incl = math.degrees(math.atan2(subida, seg))
    for i in range(n):
        a = math.radians(a0) + passo * (i + 0.5)
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        z = z0 + subida * (i + 0.5)
        L.caixa((seg * 1.04, 0.07, 0.012), (x, y, z - 0.006), 'metal_escuro',
                rot=(0, -incl, math.degrees(a) + 90))
        # corrimão (por fora)
        b0, b1 = math.radians(a0) + passo * i, math.radians(a0) + passo * (i + 1)
        Ro = R + 0.035
        L.cano((cx + Ro * math.cos(b0), cy + Ro * math.sin(b0), z0 + subida * i + 0.07),
               (cx + Ro * math.cos(b1), cy + Ro * math.sin(b1), z0 + subida * (i + 1) + 0.07), 0.007, 'amarelo',
               lados=3)


def construir():
    z0 = 0.02
    # Bacia de contenção: piso e mureta baixa
    W, D, e, hm = 1.48, 1.62, 0.04, 0.07
    L.caixa((W, D, z0), (0, 0, 0), 'concreto')
    for (px, py, sx, sy) in ((0, -D / 2 + e / 2, W, e), (0, D / 2 - e / 2, W, e),
                             (-W / 2 + e / 2, 0, e, D - 2 * e), (W / 2 - e / 2, 0, e, D - 2 * e)):
        L.caixa((sx, sy, hm), (px, py, z0), 'concreto_escuro')

    r, h = 0.35, 0.80
    ta, tb = (0.09, -0.36), (-0.09, 0.37)
    tanque(ta[0], ta[1], r, h, z0)
    tanque(tb[0], tb[1], r, h, z0)

    # Passarela entre os topos
    zp = z0 + h + 0.03
    L.caixa((0.08, 0.36, 0.015), (0.0, 0.0, zp), 'metal_escuro', rot=(0, 0, 14))
    for dx in (-0.04, 0.04):
        L.caixa((0.008, 0.36, 0.05), (dx, 0.0, zp + 0.015), 'amarelo', rot=(0, 0, 14))

    escada_espiral(ta[0], ta[1], r, z0, z0 + h, -160, 75, 9)

    # Tubulação saindo pela lateral
    for (x, y) in ((ta[0] + r, ta[1] + 0.15), (tb[0] + r - 0.04, tb[1] - 0.12)):
        L.cano((x - 0.03, y, z0 + 0.08), (W / 2 + 0.0, y, z0 + 0.08), 0.025, 'metal', lados=6)


L.principal(__file__, construir)
