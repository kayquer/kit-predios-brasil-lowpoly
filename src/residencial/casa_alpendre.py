"""Casa branca com barra azul e alpendre na frente: varanda de piso vermelho coberta pelo telhado de telha de barro
que desce sobre pilares de madeira, rede colorida, cadeira de balanço, janelas de madeira azuis e murinho baixo."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402

L.PALETA['azul_barra'] = '#3b74b8'
L.PALETA['vermelhao'] = '#a9473a'      # piso de cimento queimado vermelho
L.PALETA['telha_velha'] = '#ad5636'    # telha colonial mais escura, já envelhecida


def bloco(face, plano, u, z0, larg, alt, prof, cor, off=0.0):
    """Caixa encostada numa fachada: u = posição ao longo da face, z0 = base, off = afastamento da parede."""
    if face == 'frente':
        return L.caixa((larg, prof, alt), (u, plano - off - prof / 2, z0), cor)
    if face == 'tras':
        return L.caixa((larg, prof, alt), (u, plano + off + prof / 2, z0), cor)
    if face == 'direita':
        return L.caixa((prof, larg, alt), (plano + off + prof / 2, u, z0), cor)
    return L.caixa((prof, larg, alt), (plano - off - prof / 2, u, z0), cor)


def janela_madeira(face, plano, u, z0, larg, alt):
    """Janela colonial: batente branco e duas folhas de madeira pintadas de azul, uma entreaberta."""
    bloco(face, plano, u, z0 - 0.012, larg + 0.04, alt + 0.03, 0.01, 'branco')
    bloco(face, plano, u, z0, larg, alt, 0.006, 'escuro', off=0.01)
    bloco(face, plano, u - larg / 4, z0, larg / 2 - 0.006, alt, 0.008, 'azul_barra', off=0.012)
    bloco(face, plano, u, z0 - 0.022, larg + 0.06, 0.016, 0.03, 'branco')


def placa_inclinada(y0, z0, y1, z1, t, comprimento, x, cor):
    """Água de telhado: placa fina de (y0, z0) até (y1, z1), estendida em X."""
    return L.prisma([(y0, z0), (y1, z1), (y1, z1 + t), (y0, z0 + t)], comprimento, (x, 0, 0), cor, eixo='X')


def construir():
    W, D = 1.28, 1.0
    L.caixa((W, D, 0.012), (0, 0, 0), 'grama')
    piso = 0.012

    # Corpo da casa (parede branca com barra azul)
    bx, bw = -0.06, 1.02
    yf, yb = -0.08, 0.44                     # frente e fundo das paredes
    by, bd = (yf + yb) / 2, yb - yf
    hw = 0.44
    direita = bx + bw / 2
    L.caixa((bw, bd, hw), (bx, by, piso), 'parede', chanfro=0.01)
    L.caixa((bw + 0.012, bd + 0.012, 0.13), (bx, by, piso), 'azul_barra')

    # Telhado: duas águas com cumeeira em X; a água da frente "quebra" e desce sobre o alpendre
    zt, alt = piso + hw, 0.2
    yr = by
    s = alt / (bd / 2)
    comp = bw + 0.1
    t = 0.025
    L.prisma([(yf, 0), (yb, 0), (yr, alt)], bw, (bx, 0, zt), 'parede', eixo='X')       # oitões
    placa_inclinada(yr, zt + alt, yb + 0.06, zt + alt - s * (yb + 0.06 - yr), t, comp, bx, 'telha_velha')
    placa_inclinada(yr, zt + alt, yf, zt, t, comp, bx, 'telha_velha')
    ye, ze = -0.37, zt - 0.075                                                        # beiral do alpendre
    placa_inclinada(yf + 0.005, zt + 0.004, ye, ze, t, comp, bx, 'telha_velha')
    L.caixa((0.016, comp + 0.0, 0.016), (bx, yr, zt + alt + 0.012), 'terracota_escura', rot=(0, 0, 90))
    L.caixa((comp, 0.03, 0.03), (bx, ye + 0.04, ze - 0.03), 'madeira_escura')       # viga do alpendre

    # Alpendre: piso vermelho, pilares de madeira, guarda-corpo baixo
    dz = 0.035
    L.caixa((bw + 0.02, yf - ye + 0.02, dz), (bx, (yf + ye) / 2 - 0.01, piso), 'vermelhao')
    L.caixa((0.2, 0.06, 0.02), (bx - 0.05, ye - 0.04, piso), 'vermelhao')            # degrau
    pilares = [bx - bw / 2 + 0.04, bx - 0.17, bx + 0.07, bx + bw / 2 - 0.04]
    for x in pilares:
        L.caixa((0.035, 0.035, ze - 0.03 - piso - dz), (x, ye + 0.04, piso + dz), 'madeira', chanfro=0.004)
    for (a, b) in ((pilares[0], pilares[1]), (pilares[2], pilares[3])):
        L.caixa((b - a, 0.025, 0.02), ((a + b) / 2, ye + 0.04, piso + dz + 0.1), 'madeira_escura')
        n = int((b - a) / 0.06)
        for i in range(1, n):
            L.caixa((0.012, 0.012, 0.1), (a + (b - a) * i / n, ye + 0.04, piso + dz), 'madeira')

    # Fachada: porta e janelas de madeira azul
    bloco('frente', yf, bx - 0.05, piso + dz, 0.17, 0.28, 0.012, 'branco')
    bloco('frente', yf, bx - 0.05, piso + dz, 0.14, 0.265, 0.008, 'azul_barra', off=0.012)
    janela_madeira('frente', yf, bx - 0.33, piso + 0.15, 0.2, 0.17)
    janela_madeira('frente', yf, bx + 0.27, piso + 0.15, 0.2, 0.17)
    janela_madeira('direita', direita, by, piso + 0.15, 0.18, 0.17)

    # Rede colorida entre os dois pilares da direita e cadeira de balanço
    xa, xb = pilares[2] + 0.02, pilares[3] - 0.02
    zr, yh = ze - 0.06, ye + 0.04
    pts = []
    for i in range(7):
        f = i / 6
        x = xa + (xb - xa) * f
        z = zr - 0.14 * math.sin(math.pi * f) ** 0.8
        pts.append((x, z))
    perfil = pts + [(x, z + 0.012) for (x, z) in reversed(pts)]
    L.prisma(perfil, 0.07, (0, yh + 0.04, 0), 'vermelho', eixo='Y')
    L.prisma([(x, z + 0.013) for (x, z) in pts[1:-1]] + [(x, z + 0.02) for (x, z) in reversed(pts[1:-1])],
             0.072, (0, yh + 0.04, 0), 'amarelo', eixo='Y')
    cx, cy = bx - 0.33, yf - 0.12
    L.caixa((0.08, 0.07, 0.012), (cx, cy, piso + dz + 0.05), 'madeira_escura')
    L.caixa((0.08, 0.012, 0.1), (cx, cy + 0.04, piso + dz + 0.06), 'madeira_escura', rot=(-12, 0, 0))
    for lado in (-1, 1):
        L.caixa((0.01, 0.1, 0.012), (cx + lado * 0.035, cy, piso + dz + 0.003), 'madeira_escura', rot=(8, 0, 0))
        L.caixa((0.01, 0.01, 0.05), (cx + lado * 0.035, cy, piso + dz + 0.006), 'madeira_escura')
    L.cilindro(0.03, 0.045, (bx - 0.46, yf - 0.05, piso + dz), 'terracota', lados=6, r_topo=0.038)  # vaso
    L.arbusto((bx - 0.46, yf - 0.05, piso + dz + 0.045), 0.05, 'verde')

    # Murinho baixo com abertura e um ipê-de-jardim de flores do lado
    my = -D / 2 + 0.02
    for (a, b) in ((-W / 2 + 0.01, bx - 0.14), (bx + 0.04, W / 2 - 0.01)):
        L.caixa((b - a, 0.035, 0.08), ((a + b) / 2, my, piso), 'parede', chanfro=0.004)
        L.caixa((b - a + 0.008, 0.042, 0.014), ((a + b) / 2, my, piso + 0.08), 'azul_barra')

    L.cilindro(0.014, 0.26, (W / 2 - 0.07, -0.36, piso), 'madeira_escura', lados=5)
    L.esfera(0.065, (W / 2 - 0.07, -0.36, piso + 0.3), 'flor_rosa', escala=(1, 1, 0.85))


L.principal(__file__, construir)
