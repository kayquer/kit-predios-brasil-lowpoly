"""Casa nova de dois andares em creme e cinza grafite, com telhado de quatro águas de telha de barro, porta de vidro
grande, ar-condicionado split na fachada, varanda gourmet com churrasqueira de tijolo e muro alto com portão de correr."""
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


def split(face, plano, u, z0):
    """Unidade externa de ar-condicionado com suporte."""
    bloco(face, plano, u, z0, 0.13, 0.085, 0.05, 'branco')
    bloco(face, plano, u + 0.025, z0 + 0.015, 0.06, 0.055, 0.006, 'metal_escuro', off=0.05)
    bloco(face, plano, u, z0 - 0.012, 0.14, 0.012, 0.055, 'metal_escuro')


def construir():
    W, D = 1.26, 1.0
    L.caixa((W, D, 0.012), (0, 0, 0), 'piso')
    piso = 0.012

    bx0, bx1 = -0.565, 0.27
    yf, yb = -0.1, 0.44
    bx, bw = (bx0 + bx1) / 2, bx1 - bx0
    by, bd = (yf + yb) / 2, yb - yf
    h1, h2 = 0.38, 0.34
    zt = piso + h1 + h2

    # Corpo: térreo creme, andar de cima com volume grafite na frente à esquerda
    L.caixa((bw, bd, h1 + h2), (bx, by, piso), 'creme', chanfro=0.008)
    L.caixa((0.42, bd + 0.03, h2 + 0.02), (bx0 + 0.21 - 0.005, by - 0.015, piso + h1), 'granito', chanfro=0.006)
    L.caixa((bw + 0.012, bd + 0.012, 0.03), (bx, by, piso + h1 - 0.015), 'branco')
    L.telhado4(bw, bd, 0.34, (bx, by, zt), 'terracota', beiral=0.06)
    L.caixa((bw + 0.11, bd + 0.11, 0.02), (bx, by, zt - 0.01), 'branco')                        # beiral forrado

    # Térreo: porta de vidro grande (de correr) e porta de entrada de madeira
    bloco('frente', yf, bx - 0.12, piso, 0.4, 0.3, 0.012, 'metal_escuro')
    bloco('frente', yf, bx - 0.12, piso + 0.012, 0.37, 0.275, 0.006, 'vidro', off=0.012)
    bloco('frente', yf, bx - 0.12, piso + 0.012, 0.012, 0.275, 0.006, 'metal_escuro', off=0.018)
    bloco('frente', yf, bx0 + 0.09, piso, 0.13, 0.31, 0.012, 'madeira_escura')
    bloco('frente', yf, bx0 + 0.09, piso + 0.02, 0.1, 0.27, 0.006, 'madeira', off=0.012)

    # Andar de cima: janela comprida no volume grafite e janela com split no creme
    z2 = piso + h1
    f2 = yf - 0.03
    bloco('frente', f2, bx0 + 0.21, z2 + 0.1, 0.34, 0.14, 0.008, 'vidro_escuro')
    bloco('frente', f2, bx0 + 0.21, z2 + 0.1, 0.012, 0.14, 0.006, 'metal_escuro', off=0.008)
    bloco('frente', yf, bx1 - 0.2, z2 + 0.1, 0.22, 0.15, 0.012, 'metal_escuro')
    bloco('frente', yf, bx1 - 0.2, z2 + 0.108, 0.2, 0.135, 0.006, 'vidro_escuro', off=0.012)
    split('frente', yf, bx1 - 0.2, z2 + 0.27 - 0.005)
    split('direita', bx1, by + 0.12, z2 + 0.18)
    bloco('direita', bx1, by - 0.08, z2 + 0.1, 0.18, 0.15, 0.012, 'metal_escuro')
    bloco('direita', bx1, by - 0.08, z2 + 0.108, 0.16, 0.135, 0.006, 'vidro_escuro', off=0.012)

    # Varanda gourmet à direita: laje sobre pilar, churrasqueira de tijolo com chaminé, mesa e banquinhos
    gx0, gx1 = bx1, W / 2 - 0.02
    gy0, gy1 = yf - 0.04, yb
    gc = (gx0 + gx1) / 2
    L.caixa((gx1 - gx0, gy1 - gy0, 0.012), (gc, (gy0 + gy1) / 2, piso), 'granito')
    L.caixa((0.04, 0.04, h1 - 0.04), (gx1 - 0.03, gy0 + 0.03, piso), 'branco')
    L.caixa((gx1 - gx0 + 0.01, gy1 - gy0 + 0.02, 0.04), (gc, (gy0 + gy1) / 2, piso + h1 - 0.04), 'branco')
    L.caixa((gx1 - gx0 - 0.04, 0.02, 0.1), (gc, gy1 - 0.02, piso + h1), 'creme')               # platibanda fundo
    cy = yb - 0.08
    L.caixa((0.22, 0.1, 0.22), (gc, cy, piso), 'tijolo_baiano')
    L.caixa((0.18, 0.012, 0.07), (gc, cy - 0.052, piso + 0.12), 'escuro')
    L.caixa((0.24, 0.12, 0.02), (gc, cy, piso + 0.22), 'granito')
    L.caixa((0.15, 0.08, 0.1), (gc, cy, piso + 0.24), 'tijolo_baiano')
    L.caixa((0.07, 0.07, 0.26), (gc, cy, piso + 0.34), 'tijolo_baiano')
    L.caixa((0.09, 0.09, 0.02), (gc, cy, piso + 0.6), 'concreto')
    L.caixa((0.18, 0.11, 0.012), (gc, by - 0.06, piso + 0.12), 'madeira')
    for dx in (-0.07, 0.07):
        L.caixa((0.012, 0.09, 0.12), (gc + dx, by - 0.06, piso), 'madeira_escura')
    for dy in (-0.11, 0.11):
        L.cilindro(0.025, 0.08, (gc, by - 0.06 + dy * 0.85, piso), 'vermelho', lados=6)

    # Muro alto com portão de correr de madeira e portinha de pedestre
    my = -D / 2 + 0.05

    mh = 0.3
    gtx0, gtx1 = -0.3, 0.22
    for (a, b) in ((-W / 2 + 0.01, -0.5), (-0.36, gtx0), (gtx1, W / 2 - 0.01)):
        L.caixa((b - a, 0.04, mh), ((a + b) / 2, my, piso), 'concreto', chanfro=0.004)
        L.caixa((b - a + 0.01, 0.05, 0.015), ((a + b) / 2, my, piso + mh), 'granito')
    L.caixa((-0.36 + 0.5, 0.012, mh - 0.03), (-0.43, my - 0.004, piso), 'metal_escuro')            # portinha
    L.caixa((gtx1 - gtx0 + 0.04, 0.02, mh - 0.02), ((gtx0 + gtx1) / 2 + 0.02, my - 0.03, piso + 0.01), 'madeira_escura')
    for k in range(6):
        z = piso + 0.035 + k * 0.045
        L.caixa((gtx1 - gtx0 + 0.04, 0.006, 0.022), ((gtx0 + gtx1) / 2 + 0.02, my - 0.043, z), 'madeira')
    L.caixa((gtx1 - gtx0 + 0.2, 0.02, 0.01), ((gtx0 + gtx1) / 2 + 0.1, my - 0.03, piso), 'metal_escuro')  # trilho
    L.caixa((0.06, 0.03, 0.03), (-0.43 + 0.0, my - 0.03, piso + mh + 0.015), 'escuro')            # interfone/luz
    # Muros laterais
    for x in (-W / 2 + 0.02, W / 2 - 0.02):
        L.caixa((0.035, yf - my - 0.04, mh), (x, (yf - 0.04 + my) / 2 + 0.02, piso), 'concreto')
    # Palmeirinha e gramado na entrada
    L.caixa((0.22, 0.22, 0.01), (-0.48, -0.28, piso), 'grama')
    L.cilindro(0.015, 0.3, (-0.5, -0.28, piso), 'madeira', lados=5)
    for ang in (0, 72, 144, 216, 288):
        L.caixa((0.03, 0.13, 0.006), (-0.5, -0.28, piso + 0.29), 'verde', rot=(-25, 0, ang))


L.principal(__file__, construir)
