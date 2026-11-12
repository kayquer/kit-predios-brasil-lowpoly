"""Casa azul pastel com quintal ao lado: telhado de duas águas de telha de barro com o oitão para a rua, janelas com
grade, mangueira carregada de mangas, varal com roupas, casinha de cachorro e muro com portão de ferro."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402

L.PALETA['manga'] = '#f2a23a'


def bloco(face, plano, u, z0, larg, alt, prof, cor, off=0.0):
    """Caixa encostada numa fachada: u = posição ao longo da face, z0 = base, off = afastamento da parede."""
    if face == 'frente':
        return L.caixa((larg, prof, alt), (u, plano - off - prof / 2, z0), cor)
    if face == 'tras':
        return L.caixa((larg, prof, alt), (u, plano + off + prof / 2, z0), cor)
    if face == 'direita':
        return L.caixa((prof, larg, alt), (plano + off + prof / 2, u, z0), cor)
    return L.caixa((prof, larg, alt), (plano - off - prof / 2, u, z0), cor)


def janela(face, plano, u, z0, larg, alt, moldura='branco', barras=3):
    """Janela com moldura, vidro, peitoril e grade de ferro."""
    bloco(face, plano, u, z0 - 0.012, larg + 0.04, alt + 0.03, 0.01, moldura)
    bloco(face, plano, u, z0, larg, alt, 0.006, 'vidro_escuro', off=0.01)
    bloco(face, plano, u, z0 - 0.022, larg + 0.06, 0.016, 0.03, 'concreto')
    for i in range(barras):
        uu = u - larg / 2 + larg * (i + 1) / (barras + 1)
        bloco(face, plano, uu, z0, 0.009, alt, 0.008, 'grade', off=0.018)
    bloco(face, plano, u, z0 + alt / 2 - 0.0045, larg, 0.009, 0.008, 'grade', off=0.018)


def construir():
    W, D = 1.23, 0.87
    L.caixa((W, D, 0.012), (0, 0, 0), 'piso')
    piso = 0.012

    # Casa (lado esquerdo), oitão virado para a rua
    bx0, bx1 = -0.565, 0.06
    yf, yb = -0.24, 0.38
    bx, bw = (bx0 + bx1) / 2, bx1 - bx0
    by, bd = (yf + yb) / 2, yb - yf
    hw, alt = 0.42, 0.25
    zt = piso + hw
    L.caixa((bw, bd, hw), (bx, by, piso), 'azul_pastel', chanfro=0.01)
    L.caixa((bw + 0.012, bd + 0.012, 0.05), (bx, by, piso), 'branco')
    L.prisma([(-bw / 2, 0), (bw / 2, 0), (0, alt)], bd, (bx, by, zt), 'azul_pastel', eixo='Y')
    s, a, t = alt / (bw / 2), bw / 2 + 0.05, 0.025
    for lado in (-1, 1):
        L.prisma([(lado * a, alt - s * a), (0, alt), (0, alt + t), (lado * a, alt - s * a + t)], bd + 0.1,
                 (bx, by, zt), 'terracota', eixo='Y')
    L.caixa((0.016, bd + 0.1, 0.016), (bx, by, zt + alt + 0.012), 'terracota_escura')
    L.prisma([(-0.05, 0), (0.05, 0), (0, 0.05)], 0.01, (bx, yf - 0.005, zt + 0.06), 'branco', eixo='Y')  # respiro

    # Fachada: janela grande com grade; porta no lado do quintal
    janela('frente', yf, bx, piso + 0.15, 0.3, 0.17, barras=5)
    bloco('direita', bx1, yf + 0.14, piso, 0.15, 0.3, 0.012, 'branco')
    bloco('direita', bx1, yf + 0.14, piso, 0.12, 0.285, 0.008, 'madeira', off=0.012)
    janela('direita', bx1, by + 0.18, piso + 0.15, 0.18, 0.15)
    L.caixa((0.08, 0.2, 0.025), (bx1 + 0.04, yf + 0.14, piso), 'concreto')                         # degrau

    # Quintal de terra e grama
    qx0, qx1 = bx1 + 0.01, W / 2 - 0.01
    qc = (qx0 + qx1) / 2
    L.caixa((qx1 - qx0, yb + 0.03 - (yf + 0.02), 0.008), (qc, (yb + 0.03 + yf + 0.02) / 2, piso), 'grama')
    L.caixa((0.12, -(yf + 0.02) + (-D / 2 + 0.05), 0.006), (qc - 0.05, (yf + 0.02 - D / 2 + 0.05) / 2, piso),
            'concreto')

    # Mangueira com mangas no fundo do quintal
    mx, my_ = qc + 0.06, 0.2
    zc = piso + 0.66
    L.cilindro(0.04, 0.4, (mx, my_, piso), 'madeira_escura', lados=6, r_topo=0.028)
    L.cano((mx, my_, piso + 0.28), (mx - 0.1, my_ - 0.04, piso + 0.46), 0.018, 'madeira_escura', lados=5)
    L.esfera(0.2, (mx, my_, zc), 'verde_escuro', escala=(1.05, 1.0, 0.8))
    L.esfera(0.14, (mx - 0.14, my_ - 0.06, zc - 0.1), 'verde_escuro', escala=(1, 1, 0.85))
    L.esfera(0.13, (mx + 0.09, my_ - 0.1, zc - 0.12), 'verde', escala=(1, 1, 0.85))
    for ang in (-150, -100, -60, -20, 30):
        a = math.radians(ang)
        L.esfera(0.028, (mx + 0.13 * math.cos(a), my_ + 0.13 * math.sin(a), zc - 0.15), 'manga',
                 escala=(0.9, 0.9, 1.2))

    # Varal com roupas entre dois postes
    vy = -0.08
    v0, v1 = qx0 + 0.08, qx1 - 0.04
    for x in (v0, v1):
        L.caixa((0.014, 0.014, 0.26), (x, vy, piso), 'madeira')
    L.caixa((v1 - v0, 0.005, 0.005), ((v0 + v1) / 2, vy, piso + 0.25), 'escuro')
    for i, (cor, larg, h) in enumerate((('vermelho', 0.07, 0.09), ('flor_amarela', 0.06, 0.12), ('branco', 0.08, 0.07),
                                        ('verde', 0.06, 0.1))):
        x = v0 + 0.06 + i * 0.1
        L.caixa((larg, 0.006, h), (x, vy, piso + 0.25 - h), cor, rot=(0, 0, 0))

    # Casinha de cachorro com tigela
    cx, cy = qx1 - 0.08, yb - 0.08
    L.caixa((0.12, 0.13, 0.08), (cx, cy, piso), 'madeira')
    L.telhado(0.12, 0.13, 0.05, (cx, cy, piso + 0.08), 'vermelho', beiral=0.015, eixo='Y')
    bloco('frente', cy - 0.065, cx, piso, 0.05, 0.06, 0.004, 'escuro')
    L.cilindro(0.018, 0.012, (cx - 0.06, cy - 0.1, piso), 'azul_arara', lados=6)

    # Muro com portão de ferro (metade chapa, metade grade) para o quintal
    myr, mh = -D / 2 + 0.025, 0.2
    gx0, gx1 = qx0 + 0.02, qx0 + 0.3
    for (a, b) in ((-W / 2 + 0.01, gx0), (gx1, W / 2 - 0.01)):
        L.caixa((b - a, 0.04, mh), ((a + b) / 2, myr, piso), 'branco', chanfro=0.004)
        L.caixa((b - a + 0.01, 0.05, 0.016), ((a + b) / 2, myr, piso + mh), 'azul_pastel')
    for x in (gx0 - 0.02, gx1 + 0.02):
        L.caixa((0.05, 0.055, mh + 0.04), (x, myr, piso), 'branco')
    L.caixa((gx1 - gx0, 0.012, mh * 0.5), ((gx0 + gx1) / 2, myr, piso + 0.01), 'telhado_verde')
    L.caixa((gx1 - gx0, 0.016, 0.014), ((gx0 + gx1) / 2, myr, piso + 0.01 + mh * 0.5), 'grade')
    L.caixa((gx1 - gx0, 0.016, 0.014), ((gx0 + gx1) / 2, myr, piso + mh), 'grade')
    n = 6
    for i in range(n):
        x = gx0 + (gx1 - gx0) * (i + 0.5) / n
        L.caixa((0.008, 0.008, mh * 0.5), (x, myr, piso + 0.01 + mh * 0.5), 'grade')
    for x in (-W / 2 + 0.02, W / 2 - 0.02):
        L.caixa((0.035, 0.3, mh * 0.9), (x, myr + 0.17, piso), 'branco')
    # Vasos na frente da casa
    for k, cor in enumerate(('flor_rosa', 'verde')):
        x = bx - 0.2 + k * 0.4
        L.cilindro(0.03, 0.045, (x, yf - 0.08, piso), 'terracota', lados=6, r_topo=0.037)
        L.arbusto((x, yf - 0.08, piso + 0.045), 0.045, cor)


L.principal(__file__, construir)
