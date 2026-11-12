"""Sobrado misto lilás pastel: comércio no térreo com porta de aço de enrolar meio aberta, toldo listrado e faixa
de letreiro colorida sem texto; moradia em cima com janelas, sacadinha de grade, platibanda e caixa d'água azul."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402


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
    W, D = 1.39, 1.07
    L.caixa((W, D, 0.012), (0, 0, 0), 'piso')                                   # calçada
    piso = 0.012

    bw = W - 0.12
    yf, yb = -0.34, 0.5
    by, bd = (yf + yb) / 2, yb - yf
    h1, h2, hp = 0.45, 0.36, 0.13
    z2 = piso + h1
    zt = z2 + h2

    # Corpo e platibanda
    L.caixa((bw, bd, h1 + h2), (0, by, piso), 'lilas_pastel', chanfro=0.008)
    L.caixa((bw + 0.012, bd + 0.012, 0.03), (0, by, z2 - 0.03), 'branco')
    L.caixa((bw, 0.05, hp), (0, yf + 0.025, zt), 'lilas_pastel')
    L.caixa((0.05, bd, hp), (bw / 2 - 0.025, by, zt), 'lilas_pastel')
    L.caixa((0.05, bd, hp), (-bw / 2 + 0.025, by, zt), 'lilas_pastel')
    L.caixa((bw + 0.02, 0.07, 0.02), (0, yf + 0.025, zt + hp), 'branco')
    L.caixa((0.07, bd, 0.02), (bw / 2 - 0.025, by, zt + hp), 'branco')
    L.caixa((0.07, bd, 0.02), (-bw / 2 + 0.025, by, zt + hp), 'branco')
    # telhado de uma água escondido atrás da platibanda
    L.prisma([(yf + 0.05, 0.1), (yb + 0.01, 0.0), (yb + 0.01, 0.025), (yf + 0.05, 0.125)], bw - 0.1,
             (0, 0, zt), 'terracota', eixo='X')
    # caixa d'água azul sobre base de alvenaria
    L.caixa((0.22, 0.22, 0.1), (-0.38, by + 0.12, zt + 0.06), 'concreto_escuro')
    L.cilindro(0.09, 0.11, (-0.38, by + 0.12, zt + 0.16), 'fibra_azul', lados=8, r_topo=0.1)
    L.cilindro(0.105, 0.03, (-0.38, by + 0.12, zt + 0.27), 'fibra_azul', lados=8, r_topo=0.07)

    # Térreo comercial: pilares de pastilha, porta de aço meio aberta, porta da escada
    for x in (-bw / 2 + 0.04, 0.24, bw / 2 - 0.04):
        bloco('frente', yf, x, piso, 0.08, h1 - 0.12, 0.01, 'pastilha')
    lx0, lx1 = -bw / 2 + 0.08, 0.2
    lc, lw = (lx0 + lx1) / 2, lx1 - lx0
    bloco('frente', yf, lc, piso, lw, h1 - 0.14, 0.004, 'escuro')                                 # vão da loja
    za = piso + 0.17
    bloco('frente', yf, lc, za, lw, h1 - 0.14 - 0.17, 0.012, 'ferro_enrolar', off=0.004)
    for k in range(5):
        bloco('frente', yf, lc, za + 0.02 + k * 0.025, lw, 0.006, 0.006, 'metal_escuro', off=0.016)
    bloco('frente', yf, lc, za - 0.015, lw, 0.015, 0.018, 'metal_escuro', off=0.004)               # barra de baixo
    # balcão e produtos aparecendo pela porta
    bloco('frente', yf, lc - 0.12, piso, 0.3, 0.1, 0.06, 'madeira', off=0.004)
    for k, cor in enumerate(('vermelho', 'amarelo', 'verde', 'laranja')):
        L.caixa((0.035, 0.035, 0.035), (lc + 0.12 + k * 0.045, yf - 0.03, piso), cor)
    bloco('frente', yf, 0.43, piso, 0.15, 0.3, 0.012, 'branco')
    bloco('frente', yf, 0.43, piso, 0.12, 0.285, 0.008, 'madeira_escura', off=0.012)

    # Letreiro (faixa colorida, sem texto) e toldo listrado sobre a calçada
    bloco('frente', yf, lc, z2 - 0.11, lw + 0.06, 0.08, 0.02, 'amarelo')
    bloco('frente', yf, lc, z2 - 0.09, lw + 0.06, 0.03, 0.006, 'vermelho', off=0.02)
    tz, tp, tq = piso + h1 - 0.12, 0.17, 0.065                                                  # toldo
    n = 8
    for k in range(n):
        x0 = lx0 - 0.02 + (lw + 0.04) * k / n
        x1 = lx0 - 0.02 + (lw + 0.04) * (k + 1) / n
        cor = 'toldo_verde' if k % 2 == 0 else 'branco'
        L.prisma([(yf, tz), (yf - tp, tz - tq), (yf - tp, tz - tq + 0.012), (yf, tz + 0.012)], x1 - x0,
                 ((x0 + x1) / 2, 0, 0), cor, eixo='X')
        L.caixa((x1 - x0, 0.008, 0.035), ((x0 + x1) / 2, yf - tp - 0.004, tz - tq - 0.035 + 0.006), cor)

    # Andar de cima: duas janelas com grade e porta com sacadinha
    janela('frente', yf, -0.43, z2 + 0.12, 0.24, 0.16, barras=4)
    janela('frente', yf, 0.43, z2 + 0.12, 0.24, 0.16, barras=4)
    bloco('frente', yf, 0.0, z2 + 0.03, 0.2, 0.26, 0.01, 'branco')
    bloco('frente', yf, 0.0, z2 + 0.04, 0.17, 0.24, 0.006, 'vidro', off=0.01)
    bloco('frente', yf, 0.0, z2 + 0.01, 0.3, 0.025, 0.1, 'concreto')
    L.caixa((0.3, 0.012, 0.012), (0.0, yf - 0.095, z2 + 0.13), 'grade')
    for k in range(8):
        L.caixa((0.008, 0.008, 0.1), (-0.14 + k * 0.04, yf - 0.095, z2 + 0.035), 'grade')
    for s in (-1, 1):
        L.caixa((0.012, 0.09, 0.012), (s * 0.144, yf - 0.05, z2 + 0.13), 'grade')
    # Lado direito: janelas e ar-condicionado
    janela('direita', bw / 2, by - 0.1, z2 + 0.12, 0.18, 0.15)
    janela('direita', bw / 2, by + 0.22, z2 + 0.12, 0.18, 0.15)
    bloco('direita', bw / 2, by + 0.25, piso + 0.22, 0.2, 0.12, 0.01, 'branco')
    bloco('direita', bw / 2, by + 0.25, piso + 0.23, 0.17, 0.1, 0.006, 'vidro_escuro', off=0.01)
    bloco('direita', bw / 2, by - 0.15, piso + 0.28, 0.12, 0.08, 0.05, 'branco')                  # split
    bloco('direita', bw / 2, by - 0.13, piso + 0.295, 0.055, 0.05, 0.006, 'metal_escuro', off=0.05)
    # Engradados na calçada
    L.caixa((0.07, 0.06, 0.05), (lx1 + 0.1, yf - 0.1, piso), 'amarelo')
    L.caixa((0.07, 0.06, 0.05), (lx1 + 0.1, yf - 0.1, piso + 0.05), 'vermelho', rot=(0, 0, 12))


L.principal(__file__, construir)
