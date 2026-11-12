"""Depósito de material de construção: galpão aberto na frente com platibanda vermelha e faixa amarela (sem
letreiro), cobertura de telha ondulada de fibrocimento caindo para o fundo, sacos de cimento lá dentro, pallets de
tijolo baiano no pátio e baias de areia e brita na lateral."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402

L.PALETA['cimento_saco'] = '#b8925e'
L.PALETA['brita'] = '#8e8a84'
L.PALETA['tijolo_junta'] = '#9c5034'


def placa_ondulada(comp, rampa, pos, cor, ang, onda=0.07, amp=0.016, esp=0.014):
    """Telha ondulada: zigue-zague ao longo de X, estendido na rampa (Y) e inclinado `ang` graus em X."""
    n = max(2, round(comp / (onda / 2)))
    n += n % 2
    topo = [(-comp / 2 + comp * i / n, amp if i % 2 else 0.0) for i in range(n + 1)]
    perfil = topo + [(comp / 2, -esp), (-comp / 2, -esp)]
    return L.prisma(perfil, rampa, pos, cor, eixo='Y', rot=(ang, 0, 0))


def tijolos(x, y, rot=0):
    """Pallet de tijolo baiano: bloco alaranjado com juntas mais escuras."""
    L.caixa((0.2, 0.16, 0.025), (x, y, 0), 'madeira', rot=(0, 0, rot))
    L.caixa((0.18, 0.14, 0.14), (x, y, 0.025), 'tijolo_baiano', rot=(0, 0, rot))
    for z in (0.07, 0.115):
        L.caixa((0.184, 0.144, 0.008), (x, y, z), 'tijolo_junta', rot=(0, 0, rot))


def construir():
    x0, x1 = -0.63, 0.3          # galpão
    y0, y1 = -0.08, 0.41
    gx, gy = (x0 + x1) / 2, (y0 + y1) / 2
    lx, ly = x1 - x0, y1 - y0
    zf, zt = 0.56, 0.46          # altura do beiral da frente e do fundo

    # Piso, fundo e laterais (tijolo baiano aparente no fundo; laterais rebocadas e pintadas)
    L.caixa((lx, ly, 0.015), (gx, gy, 0), 'concreto')
    L.caixa((lx, 0.05, zt), (gx, y1 - 0.025, 0), 'tijolo_baiano', chanfro=0.01)
    for px in (x0 + 0.025, x1 - 0.025):
        L.prisma([(y0, 0), (y1, 0), (y1, zt), (y0 + 0.06, zf - 0.02), (y0, zf - 0.02)], 0.05, (px, 0, 0), 'muro',
                 eixo='X')
        L.caixa((0.054, ly + 0.004, 0.07), (px, gy, 0), 'toldo_vermelho')        # barrado
    # pilares da frente aberta
    for px in (-0.32, -0.01):
        L.caixa((0.05, 0.05, zf), (px, y0 + 0.025, 0), 'muro')
    # platibanda vermelha com faixa amarela + cobertura caindo para o fundo
    L.caixa((lx + 0.02, 0.06, 0.2), (gx, y0 + 0.01, zf - 0.03), 'toldo_vermelho', chanfro=0.008)
    L.caixa((lx + 0.028, 0.068, 0.045), (gx, y0 + 0.01, zf + 0.04), 'toldo_amarelo')
    L.caixa((lx + 0.028, 0.068, 0.02), (gx, y0 + 0.01, zf + 0.17), 'parede')
    ang = math.degrees(math.atan2(zf - zt, ly))
    rampa = math.hypot(ly + 0.04, zf - zt)
    placa_ondulada(lx + 0.04, rampa, (gx, gy + 0.02, (zf + zt) / 2 - 0.01), 'fibrocimento', -ang)

    # Dentro: sacos de cimento empilhados e prateleira de ferragens
    for i, (cx, cy) in enumerate(((-0.5, 0.25), (-0.36, 0.25), (-0.5, 0.1))):
        L.caixa((0.13, 0.12, 0.025), (cx, cy, 0.015), 'madeira')
        for k in range(3):
            L.caixa((0.12, 0.11, 0.04), (cx, cy, 0.04 + k * 0.042), 'cimento_saco', rot=(0, 0, 8 * (k % 2) - 4))
    L.caixa((0.3, 0.08, 0.3), (0.08, 0.36, 0.015), 'portao')                 # prateleira
    for z in (0.1, 0.2):
        L.caixa((0.31, 0.085, 0.012), (0.08, 0.355, z), 'metal')
    L.caixa((0.08, 0.08, 0.1), (0.0, 0.36, 0.215), 'amarelo')                  # latas de tinta
    L.caixa((0.08, 0.08, 0.1), (0.14, 0.36, 0.215), 'fibra_azul')
    L.caixa((0.28, 0.06, 0.06), (-0.17, 0.2, 0.015), 'pvc')                   # canos de PVC

    # Pátio da frente: pallets de tijolo baiano e vergalhões
    tijolos(-0.5, -0.27)
    tijolos(-0.27, -0.29, 8)
    tijolos(-0.39, -0.12, -4)
    tijolos(-0.04, -0.3)
    for k in range(3):
        L.cano((0.06, -0.15 + k * 0.025, 0.02), (0.3, -0.15 + k * 0.025, 0.02), 0.009, 'ferrugem', lados=5)
    L.caixa((0.03, 0.1, 0.02), (0.1, -0.125, 0), 'madeira')
    L.caixa((0.03, 0.1, 0.02), (0.26, -0.125, 0), 'madeira')

    # Baias de areia e brita na lateral direita (muretas de concreto)
    bx0, bx1 = 0.36, 0.64
    by0, by1 = -0.42, 0.41
    L.caixa((bx1 - bx0, 0.04, 0.14), ((bx0 + bx1) / 2, by1 - 0.02, 0), 'concreto')
    L.caixa((0.04, by1 - by0, 0.14), (bx1 - 0.02, (by0 + by1) / 2, 0), 'concreto')
    L.caixa((bx1 - bx0, 0.04, 0.14), ((bx0 + bx1) / 2, 0.0, 0), 'concreto')
    L.cone(0.15, 0.15, (0.49, 0.22, 0), 'areia', lados=8)
    L.cone(0.14, 0.13, (0.48, -0.2, 0), 'brita', lados=7)
    # carrinho de mão
    L.prisma([(-0.07, 0.0), (0.07, 0.0), (0.1, 0.06), (-0.09, 0.07)], 0.09, (0.18, -0.39, 0.05), 'fibra_azul',
             eixo='Y')
    L.cilindro(0.03, 0.02, (0.26, -0.4, 0.03), 'escuro', lados=6, rot=(90, 0, 0))
    L.cano((0.18, -0.37, 0.06), (0.04, -0.37, 0.07), 0.007, 'grade', lados=4)


L.principal(__file__, construir)
