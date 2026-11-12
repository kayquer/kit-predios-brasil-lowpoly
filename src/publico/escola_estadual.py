"""Escola estadual térrea em L com barrado verde, janelas basculantes, corredor coberto, muro com portão, quadra
poliesportiva com cobertura em arco e mastro com a bandeira verde-amarela."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402

L.PALETA['verde_escola'] = '#3f8f5f'     # barrado e portão pintados de verde
L.PALETA['quadra'] = '#3f8f8a'           # piso da quadra
L.PALETA['quadra_borda'] = '#c0674a'     # faixa vermelha em volta da quadra
L.PALETA['bandeira'] = '#1f9a48'


def arco(x0, x1, y, comp, zb, flecha, esp, cor, n=8):
    """Cobertura metálica em arco (casca fina) vencendo X de x0 a x1, estendida em Y."""
    cx, a = (x0 + x1) / 2, (x1 - x0) / 2
    fora = [(cx - a * math.cos(math.pi * i / n), zb + flecha * math.sin(math.pi * i / n)) for i in range(n + 1)]
    dentro = [(cx - (a - esp) * math.cos(math.pi * i / n), zb - esp + (flecha) * math.sin(math.pi * i / n))
              for i in range(n, -1, -1)]
    return L.prisma(fora + dentro, comp, (0, y, 0), cor, eixo='Y')


def bandeira(x, y, z_topo):
    """Mastro com bandeira verde e losango amarelo, tremulando para +X."""
    L.cano((x, y, 0.02), (x, y, z_topo + 0.02), 0.008, 'metal', lados=4)
    fw, fh = 0.17, 0.115
    fx, fz = x + 0.012 + fw / 2, z_topo - fh / 2
    L.caixa((fw, 0.006, fh), (fx, y, fz - fh / 2), 'bandeira')
    rw, rh = fw * 0.40, fh * 0.38
    L.prisma([(fx - rw, fz), (fx, fz - rh), (fx + rw, fz), (fx, fz + rh)], 0.012, (0, y, 0), 'amarelo', eixo='Y')


def construir():
    z0 = 0.02
    L.caixa((1.40, 1.40, z0), (0, 0, 0), 'piso')
    L.caixa((0.48, 0.20, 0.008), (0.41, -0.56, z0), 'grama')     # jardim da frente
    L.caixa((0.06, 1.06, 0.008), (0.635, 0.09, z0), 'grama')     # faixa de grama do lado

    # Muro com portão de grade (vão entre x -0.02 e 0.15)
    mh, me = 0.08, 0.03
    for (cx, cy, sx, sy) in ((-0.36, -0.685, 0.68, me), (0.425, -0.685, 0.55, me),
                             (0.685, 0.0, me, 1.40), (0.0, 0.685, 1.34, me), (-0.685, 0.0, me, 1.40)):
        L.caixa((sx, sy, mh), (cx, cy, z0), 'muro')
        L.caixa((sx + 0.006, sy + 0.006, 0.012), (cx, cy, z0 + mh), 'concreto')
    gx0, gx1 = -0.02, 0.15
    L.caixa((gx1 - gx0, 0.012, 0.012), ((gx0 + gx1) / 2, -0.685, z0 + 0.012), 'verde_escola')
    L.caixa((gx1 - gx0, 0.012, 0.012), ((gx0 + gx1) / 2, -0.685, z0 + mh - 0.012), 'verde_escola')
    for i in range(5):
        x = gx0 + 0.015 + i * (gx1 - gx0 - 0.03) / 4
        L.caixa((0.008, 0.008, mh), (x, -0.685, z0), 'verde_escola')

    # Quadra poliesportiva coberta (frente esquerda)
    qx, qy, qw, qd = -0.35, -0.29, 0.62, 0.70
    L.caixa((qw, qd, 0.008), (qx, qy, z0), 'quadra_borda')
    L.caixa((qw - 0.09, qd - 0.10, 0.006), (qx, qy, z0 + 0.008), 'quadra')
    zl = z0 + 0.014
    for (cx, cy, sx, sy) in ((qx, qy - 0.30, 0.53, 0.008), (qx, qy + 0.30, 0.53, 0.008), (qx, qy, 0.53, 0.008),
                             (qx - 0.265, qy, 0.008, 0.60), (qx + 0.265, qy, 0.008, 0.60)):
        L.caixa((sx, sy, 0.002), (cx, cy, zl), 'branco')
    for gy, s in ((qy - 0.30, 1), (qy + 0.30, -1)):  # traves de futsal
        L.cano((qx - 0.05, gy, zl), (qx - 0.05, gy, zl + 0.06), 0.005, 'branco', lados=4)
        L.cano((qx + 0.05, gy, zl), (qx + 0.05, gy, zl + 0.06), 0.005, 'branco', lados=4)
        L.cano((qx - 0.05, gy, zl + 0.06), (qx + 0.05, gy, zl + 0.06), 0.005, 'branco', lados=4)
    zc = z0 + 0.31
    for x in (qx - qw / 2 + 0.02, qx + qw / 2 - 0.02):
        for y in (qy - qd / 2 + 0.02, qy, qy + qd / 2 - 0.02):
            L.caixa((0.022, 0.022, zc - z0), (x, y, z0), 'metal_escuro')
    L.caixa((0.022, qd - 0.02, 0.025), (qx - qw / 2 + 0.02, qy, zc - 0.025), 'metal_escuro')
    L.caixa((0.022, qd - 0.02, 0.025), (qx + qw / 2 - 0.02, qy, zc - 0.025), 'metal_escuro')
    arco(qx - qw / 2 - 0.02, qx + qw / 2 + 0.02, qy, qd + 0.04, zc, 0.12, 0.018, 'telhado_azul')

    # Prédio em L: ala da direita (ao longo de Y, de frente para a câmera) e ala do fundo (ao longo de X)
    ph = 0.25
    alas = ((0.41, 0.09, 0.38, 1.06), (-0.20, 0.44, 0.92, 0.36))
    for (cx, cy, sx, sy) in alas:
        L.caixa((sx, sy, ph), (cx, cy, z0), 'creme', chanfro=0.01)
        L.caixa((sx + 0.012, sy + 0.012, 0.075), (cx, cy, z0), 'verde_escola')    # barrado
        L.caixa((sx + 0.012, sy + 0.012, 0.02), (cx, cy, z0 + ph - 0.035), 'verde_escola')  # faixa de cima
    L.telhado4(0.38, 1.06, 0.085, (0.41, 0.09, z0 + ph), 'terracota', beiral=0.035)
    L.telhado4(0.92, 0.36, 0.085, (-0.20, 0.44, z0 + ph), 'terracota', beiral=0.035)

    # Janelas basculantes (vidro com moldura branca)
    jz = z0 + 0.15
    L.janelas('direita', 0.60, jz, -0.36, 0.56, 5, 0.11, 0.075, 'vidro', moldura='parede')
    L.janelas('frente', 0.26, jz, -0.62, 0.10, 4, 0.11, 0.075, 'vidro', moldura='parede')
    L.janelas('frente', -0.44, jz, 0.46, 0.60, 1, 0.09, 0.075, 'vidro', moldura='parede')
    # Entrada principal na frente da ala: porta e marquise azul
    L.placa(0.12, 0.16, (0.31, -0.44, z0 + 0.16), 'portao', 'frente')
    L.caixa((0.20, 0.10, 0.018), (0.31, -0.49, z0 + 0.19), 'concreto')
    L.caixa((0.21, 0.012, 0.03), (0.31, -0.545, z0 + 0.185), 'telhado_azul')

    # Corredor coberto ao longo do L (laje fina sobre pilaretes)
    cz = z0 + 0.21
    L.caixa((0.13, 0.66, 0.018), (0.155, -0.09, cz), 'fibrocimento')
    L.caixa((0.90, 0.13, 0.018), (-0.19, 0.195, cz), 'fibrocimento')
    for (x, y) in ((0.10, -0.40), (0.10, -0.10), (0.10, 0.14), (-0.15, 0.14), (-0.40, 0.14), (-0.62, 0.14)):
        L.caixa((0.016, 0.016, cz - z0), (x, y, z0), 'parede')

    # Mastro com a bandeira no jardim da frente, perto do portão
    bandeira(0.20, -0.60, 0.72)
    L.arvore((0.55, -0.575, z0), 0.40, 'verde')
    L.arbusto((0.44, -0.61, z0), 0.05, 'verde_escuro')


L.principal(__file__, construir)
