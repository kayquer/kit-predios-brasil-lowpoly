"""Instituto público de pesquisa no estilo modernista brasileiro (Embrapa, Fiocruz): bloco branco de dois andares sobre
pilotis com brises verticais na fachada, painel de azulejos azul e branco na empena, estufa de vidro com canteiros
ao lado e caixa d'água de concreto sobre quatro pilares."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402

L.PALETA['brise'] = '#ecebe6'
L.PALETA['azulejo'] = '#2f5fa8'
L.PALETA['vidro_estufa'] = '#cfe9e4'


def construir():
    x0, x1 = -0.82, 0.3
    y0, y1 = -0.28, 0.3
    bx, by = (x0 + x1) / 2, (y0 + y1) / 2
    lx, ly = x1 - x0, y1 - y0
    z1, z2 = 0.3, 0.68            # piso do andar de cima e cobertura

    # Térreo recuado e envidraçado sob o bloco (pilotis)
    L.caixa((lx - 0.12, ly - 0.14, z1), (bx, by + 0.02, 0), 'vidro_escuro')
    L.caixa((lx - 0.1, ly - 0.12, 0.03), (bx, by + 0.02, 0), 'concreto')
    for k in range(6):
        x = x0 + 0.05 + (lx - 0.1) * k / 5
        L.cilindro(0.022, z1, (x, y0 + 0.04, 0), 'parede', lados=6)
    L.placa(0.2, 0.22, (bx + 0.15, y0 + 0.07, 0.11), 'vidro', 'frente', espessura=0.015)        # entrada
    # Bloco de cima: caixa branca com laje de cobertura saliente
    L.caixa((lx, ly, z2 - z1), (bx, by, z1), 'vidro_escuro')
    L.caixa((lx + 0.01, ly + 0.01, 0.05), (bx, by, z1), 'parede')
    L.caixa((lx + 0.04, ly + 0.04, 0.05), (bx, by, z2), 'parede', chanfro=0.008)
    L.caixa((lx - 0.04, ly - 0.04, 0.008), (bx, by, z2 + 0.05), 'concreto')
    # empenas cegas brancas nas pontas
    for sx in (-1, 1):
        L.caixa((0.04, ly + 0.01, z2 - z1), (bx + sx * (lx / 2 - 0.02), by, z1), 'parede')
    # brises verticais na frente
    n = 16
    for k in range(n):
        x = x0 + 0.07 + (lx - 0.14) * k / (n - 1)
        L.caixa((0.016, 0.07, z2 - z1 - 0.05), (x, y0 - 0.03, z1 + 0.05), 'brise')
    # painel de azulejos (azul e branco) na empena da direita
    for i in range(3):
        for j in range(2):
            cor = 'azulejo' if (i + j) % 2 == 0 else 'azul_pastel'
            L.placa(0.15, 0.13, (x1 + 0.001, y0 + 0.13 + i * 0.16, z1 + 0.12 + j * 0.14), cor, 'direita',
                    espessura=0.012)
    # casa de máquinas na cobertura
    L.caixa((0.22, 0.16, 0.1), (x0 + 0.3, by + 0.06, z2 + 0.05), 'parede')

    # Caixa d'água modernista: prisma de concreto sobre quatro pilares, atrás à esquerda
    tx, ty = -0.62, 0.47
    for dx in (-0.09, 0.09):
        for dy in (-0.07, 0.07):
            L.caixa((0.035, 0.035, 0.98), (tx + dx, ty + dy, 0), 'concreto')
    L.caixa((0.24, 0.035, 0.03), (tx, ty - 0.07, 0.5), 'concreto')
    L.caixa((0.24, 0.035, 0.03), (tx, ty + 0.07, 0.5), 'concreto')
    L.caixa((0.28, 0.22, 0.26), (tx, ty, 0.98), 'parede', chanfro=0.01)
    L.caixa((0.284, 0.224, 0.05), (tx, ty, 1.08), 'azulejo')
    L.caixa((0.3, 0.24, 0.02), (tx, ty, 1.24), 'concreto')

    # Estufa de vidro à direita: corpo + telhado de duas águas com montantes brancos
    ex0, ex1, ey0, ey1 = 0.38, 0.82, -0.5, 0.26
    ex, ey = (ex0 + ex1) / 2, (ey0 + ey1) / 2
    elx, ely, eh, ea = ex1 - ex0, ey1 - ey0, 0.24, 0.13
    L.caixa((elx, ely, 0.05), (ex, ey, 0), 'concreto')
    L.caixa((elx - 0.02, ely - 0.02, eh - 0.05), (ex, ey, 0.05), 'vidro_estufa')
    L.prisma([(-elx / 2 + 0.01, 0), (elx / 2 - 0.01, 0), (0, ea)], ely - 0.02, (ex, ey, eh), 'vidro_estufa', eixo='Y')
    for k in range(5):
        y = ey0 + 0.01 + (ely - 0.02) * k / 4
        L.caixa((elx + 0.004, 0.018, 0.018), (ex, y, eh - 0.018), 'parede')
        L.prisma([(-elx / 2, 0), (-elx / 2 + 0.03, 0), (0, ea + 0.012), (0, ea - 0.008)], 0.018, (ex, y, eh), 'parede',
                 eixo='Y')
        L.prisma([(elx / 2 - 0.03, 0), (elx / 2, 0), (0, ea - 0.008), (0, ea + 0.012)], 0.018, (ex, y, eh), 'parede',
                 eixo='Y')
        for sx in (-1, 1):
            L.caixa((0.018, 0.018, eh), (ex + sx * (elx / 2 - 0.01), y, 0), 'parede')
    L.caixa((0.02, ely, 0.02), (ex, ey, eh + ea - 0.01), 'parede')                     # cumeeira
    L.placa(0.1, 0.17, (ex, ey0, 0.135), 'parede', 'frente', espessura=0.015)           # porta
    # mudas vistas através do vidro e canteiros na frente
    L.placa(elx - 0.06, 0.07, (ex, ey0 + 0.01, 0.12), 'verde', 'frente', espessura=0.006)
    L.placa(ely - 0.06, 0.07, (ex1 - 0.01, ey, 0.12), 'verde', 'direita', espessura=0.006)
    for x in (-0.42, -0.08, 0.2):
        L.caixa((0.26, 0.1, 0.05), (x, -0.55, 0), 'tijolo')
        L.caixa((0.24, 0.08, 0.02), (x, -0.55, 0.05), 'terra')
        for dx in (-0.08, 0.0, 0.08):
            L.arbusto((x + dx, -0.55, 0.06), 0.035, 'folha')
    L.arvore((-0.7, -0.52, 0), 0.38, 'verde_escuro')


L.principal(__file__, construir)
