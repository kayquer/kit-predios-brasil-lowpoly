"""Tanque deitado de combustível/álcool, branco com cintas escuras, sobre dois berços de concreto, com boca de
inspeção no topo, registro embaixo e escadinha amarela na frente."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402


def construir():
    r, comp, zb = 0.16, 0.66, 0.05
    zc = zb + r                                       # eixo do tanque
    for x in (-0.22, 0.22):                           # berços de concreto
        L.caixa((0.08, 0.48, zb + 0.06), (x, 0, 0), 'concreto')
    L.cilindro(r, comp, (-comp / 2, 0, zc), 'parede', lados=10, rot=(0, 90, 0))
    L.cilindro(r, 0.05, (comp / 2, 0, zc), 'parede', lados=10, r_topo=r * 0.55, rot=(0, 90, 0))     # tampos
    L.cilindro(r, 0.05, (-comp / 2, 0, zc), 'parede', lados=10, r_topo=r * 0.55, rot=(0, -90, 0))
    for x in (-0.22, 0.22):                           # cintas sobre os berços
        L.cilindro(r + 0.006, 0.025, (x - 0.0125, 0, zc), 'metal_escuro', lados=10, rot=(0, 90, 0))
    L.cilindro(0.045, 0.035, (0.0, 0, zc + r - 0.01), 'metal_escuro', lados=6)    # boca de inspeção
    L.cano((-0.33, 0, zb + 0.05), (-0.41, 0, zb + 0.05), 0.018, 'metal_escuro', lados=4)  # registro de descarga
    L.caixa((0.02, 0.07, 0.02), (-0.395, 0, zb + 0.07), 'vermelho')
    # Escadinha amarela encostada na frente do tanque
    a0, a1 = (-0.245, 0.0), (-0.12, zc + r)
    for x in (0.06, 0.12):
        L.cano((x, a0[0], a0[1]), (x, a1[0], a1[1]), 0.008, 'amarelo', lados=3)
    for t in (0.25, 0.5, 0.75):
        y, z = a0[0] + (a1[0] - a0[0]) * t, a0[1] + (a1[1] - a0[1]) * t
        L.cano((0.06, y, z), (0.12, y, z), 0.006, 'amarelo', lados=3)


L.principal(__file__, construir)
