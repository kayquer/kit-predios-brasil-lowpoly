"""Caixa d'água elevada de concreto em forma de taça, das cidades do interior paulista e mineiro: fuste cilíndrico,
taça larga pintada de branco com faixa azul, escada de marinheiro com gaiola subindo o fuste, guarda-corpo no
topo, casinha de bombas e alambrado na base."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402

L.PALETA['concreto_fuste'] = '#c4bfb4'


def construir():
    zf = 1.26                 # topo do fuste
    rf = 0.12                 # raio do fuste
    zc, zt = 1.58, 1.9        # início e topo do cilindro da taça
    rt = 0.4                 # raio da taça

    # Base: laje, alambrado e casinha de bombas
    L.caixa((0.8, 0.78, 0.03), (0, 0, 0), 'concreto', chanfro=0.008)
    L.cerca(-0.385, -0.375, 0.385, 0.375, alt=0.13, cor='metal')
    L.cilindro(rf + 0.05, 0.08, (0, 0, 0.03), 'concreto_escuro', lados=12)        # bloco de fundação
    L.caixa((0.2, 0.15, 0.15), (0.24, -0.22, 0.03), 'creme', chanfro=0.008)
    L.caixa((0.23, 0.18, 0.025), (0.24, -0.22, 0.18), 'concreto')
    L.placa(0.07, 0.11, (0.24, -0.295, 0.085), 'portao', 'frente', espessura=0.015)
    L.cano((0.24, -0.15, 0.1), (0.24, -0.06, 0.1), 0.02, 'cano', lados=6)
    L.cano((0.24, -0.06, 0.1), (0.1, -0.06, 0.1), 0.02, 'cano', lados=6)

    # Fuste cilíndrico de concreto
    L.cilindro(rf, zf - 0.11, (0, 0, 0.11), 'concreto_fuste', lados=12)
    L.cilindro(rf + 0.012, 0.03, (0, 0, 0.6), 'concreto', lados=12)               # junta de concretagem
    # Taça: cone invertido, cilindro com faixa azul e tampa
    L.cilindro(rf + 0.02, zc - zf, (0, 0, zf), 'parede', lados=16, r_topo=rt)
    L.cilindro(rt, zt - zc, (0, 0, zc), 'parede', lados=16)
    L.cilindro(rt + 0.008, 0.1, (0, 0, zc + 0.1), 'fibra_azul', lados=16)
    L.cilindro(rt + 0.01, 0.025, (0, 0, zt - 0.025), 'concreto', lados=16)       # beiral
    L.cilindro(rt - 0.02, 0.07, (0, 0, zt), 'concreto', lados=16, r_topo=0.1)      # tampa cônica
    L.cilindro(0.1, 0.05, (0, 0, zt + 0.07), 'concreto_escuro', lados=8)          # alçapão
    L.cano((0, 0, zt + 0.12), (0, 0, zt + 0.24), 0.008, 'metal_escuro', lados=4)   # para-raios
    # guarda-corpo do topo
    for k in range(10):
        a = 2 * math.pi * k / 10
        L.caixa((0.012, 0.012, 0.08), ((rt - 0.03) * math.cos(a), (rt - 0.03) * math.sin(a), zt), 'metal_escuro')
    L.anel(rt - 0.02, rt - 0.035, 0.012, (0, 0, zt + 0.075), 'metal_escuro', lados=10)

    # Escada de marinheiro na frente-direita: trilhos, degraus e gaiola
    a = math.radians(-60)
    ux, uy = math.cos(a), math.sin(a)              # direção para fora do fuste
    tx, ty = -uy, ux                               # tangente
    d = rf + 0.04
    for s in (-1, 1):
        L.cano((d * ux + s * 0.035 * tx, d * uy + s * 0.035 * ty, 0.11),
               (d * ux + s * 0.035 * tx, d * uy + s * 0.035 * ty, zf), 0.006, 'metal_escuro', lados=4)
    z = 0.2
    while z < zf:
        L.cano((d * ux - 0.035 * tx, d * uy - 0.035 * ty, z), (d * ux + 0.035 * tx, d * uy + 0.035 * ty, z), 0.005,
               'metal_escuro', lados=4)
        z += 0.1
    rot = math.degrees(a) + 90
    for zg in (0.6, 0.85, 1.1):
        L.caixa((0.11, 0.1, 0.012), ((d + 0.045) * ux, (d + 0.045) * uy, zg), 'metal_escuro', rot=(0, 0, rot))
    L.caixa((0.012, 0.012, zf - 0.5), ((d + 0.09) * ux, (d + 0.09) * uy, 0.5), 'metal_escuro')
    # trecho inclinado pela taça e reto até o topo
    pa = ((rf + 0.06) * ux, (rf + 0.06) * uy, zf)
    pb = ((rt + 0.03) * ux, (rt + 0.03) * uy, zc)
    pc = ((rt + 0.03) * ux, (rt + 0.03) * uy, zt + 0.06)
    for p1, p2, passos in ((pa, pb, (0.25, 0.5, 0.75)), (pb, pc, (0.3, 0.7))):
        for s in (-1, 1):
            L.cano((p1[0] + s * 0.035 * tx, p1[1] + s * 0.035 * ty, p1[2]),
                   (p2[0] + s * 0.035 * tx, p2[1] + s * 0.035 * ty, p2[2]), 0.006, 'metal_escuro', lados=4)
        for t in passos:
            cx, cy, cz = (p1[i] + (p2[i] - p1[i]) * t for i in range(3))
            L.cano((cx - 0.035 * tx, cy - 0.035 * ty, cz), (cx + 0.035 * tx, cy + 0.035 * ty, cz), 0.005,
                   'metal_escuro', lados=4)
    # cano de entrada/saída descendo do fundo da taça
    L.cano((-0.09, 0.09, 0.11), (-0.09, 0.09, zf), 0.022, 'cano', lados=6)


L.principal(__file__, construir)
