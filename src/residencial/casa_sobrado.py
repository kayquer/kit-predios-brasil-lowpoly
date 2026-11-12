"""Sobrado verde-água de dois andares com oitão virado para a rua, telhado de duas águas de telha de barro,
sacada com grade no andar de cima, garagem coberta ao lado e mureta com gradil e portão de ferro na frente."""
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


def telhado_oitao(larg, prof, alt, pos, cor, cor_oitao, beiral=0.05, t=0.025):
    """Duas águas com a cumeeira em Y (oitão triangular na frente, da cor da fachada) e telhas em placa fina."""
    x, y, z = pos
    L.prisma([(-larg / 2, 0), (larg / 2, 0), (0, alt)], prof, (x, y, z), cor_oitao, eixo='Y')
    s = alt / (larg / 2)
    a = larg / 2 + beiral
    for lado in (-1, 1):
        perfil = [(lado * a, alt - s * a), (0, alt), (0, alt + t), (lado * a, alt - s * a + t)]
        L.prisma(perfil, prof + 2 * beiral, (x, y, z), cor, eixo='Y')


def construir():
    W, D = 1.27, 1.0
    L.caixa((W, D, 0.012), (0, 0, 0), 'piso')
    piso = 0.012

    # Corpo de dois andares
    bx, by, bw, bd = -0.2, 0.15, 0.76, 0.6
    h1, h2 = 0.34, 0.3
    frente, direita = by - bd / 2, bx + bw / 2
    L.caixa((bw, bd, h1 + h2), (bx, by, piso), 'verde_agua', chanfro=0.01)
    L.caixa((bw + 0.012, bd + 0.012, 0.06), (bx, by, piso), 'branco')                # rodapé
    L.caixa((bw + 0.016, bd + 0.016, 0.022), (bx, by, piso + h1 - 0.011), 'branco')  # friso entre andares
    L.caixa((bw + 0.016, bd + 0.016, 0.02), (bx, by, piso + h1 + h2 - 0.02), 'branco')
    telhado_oitao(bw, bd, 0.27, (bx, by, piso + h1 + h2), 'terracota', 'verde_agua', beiral=0.055)
    L.caixa((0.016, bd + 0.1, 0.016), (bx, by, piso + h1 + h2 + 0.285), 'terracota_escura')  # cumeeira
    # óculo de ventilação no oitão
    bloco('frente', frente, bx, piso + h1 + h2 + 0.07, 0.09, 0.07, 0.01, 'branco')

    # Térreo: porta de entrada e janela
    bloco('frente', frente, bx - 0.2, piso, 0.17, 0.29, 0.012, 'branco')
    bloco('frente', frente, bx - 0.2, piso, 0.14, 0.275, 0.008, 'madeira_escura', off=0.012)
    janela('frente', frente, bx + 0.14, piso + 0.13, 0.26, 0.15, barras=4)

    # Andar de cima: porta de vidro e sacada com grade (laje em balanço)
    sz = piso + h1
    bloco('frente', frente, bx - 0.04, sz + 0.02, 0.3, 0.23, 0.01, 'branco')
    bloco('frente', frente, bx - 0.04, sz + 0.03, 0.26, 0.21, 0.006, 'vidro', off=0.01)
    bloco('frente', frente, bx - 0.04, sz + 0.03, 0.012, 0.21, 0.006, 'branco', off=0.016)
    sl, sp = 0.52, 0.14
    bloco('frente', frente, bx - 0.04, sz - 0.025, sl, 0.03, sp, 'concreto')
    gy = frente - sp + 0.008
    L.caixa((sl, 0.014, 0.014), (bx - 0.04, gy, sz + 0.13), 'grade')
    for i in range(11):
        x = bx - 0.04 - sl / 2 + 0.008 + (sl - 0.016) * i / 10
        L.caixa((0.008, 0.008, 0.13), (x, gy, sz + 0.005), 'grade')
    for lado in (-1, 1):
        L.caixa((0.014, sp - 0.01, 0.014), (bx - 0.04 + lado * (sl / 2 - 0.007), frente - sp / 2, sz + 0.13), 'grade')

    # Lado direito (dentro da garagem) e janela do andar de cima
    janela('direita', direita, by + 0.05, sz + 0.1, 0.18, 0.14)
    janela('esquerda', bx - bw / 2, by + 0.05, sz + 0.1, 0.18, 0.14)

    # Garagem coberta ao lado: pilares e laje com telha
    gx0, gx1 = direita, W / 2 - 0.015
    gc = (gx0 + gx1) / 2
    for y in (frente + 0.03, by + bd / 2 - 0.04):
        L.caixa((0.035, 0.035, 0.3), (gx1 - 0.02, y, piso), 'branco')
    L.caixa((gx1 - gx0 + 0.01, bd + 0.02, 0.035), (gc, by, piso + 0.3), 'branco')
    L.prisma([(-bd / 2 - 0.03, 0), (bd / 2 + 0.03, 0), (bd / 2 + 0.03, 0.025), (-bd / 2 - 0.03, 0.025)],
             gx1 - gx0, (gc, by, piso + 0.335), 'terracota', eixo='X', rot=(4, 0, 0))
    L.caixa((gx1 - gx0 - 0.02, bd - 0.02, 0.006), (gc, by, piso), 'concreto')      # piso da garagem

    # Mureta com gradil, portão de garagem e portãozinho
    my = -D / 2 + 0.02
    pg0, pg1 = gx0 + 0.01, gx1 - 0.03
    pp0, pp1 = bx - 0.29, bx - 0.11
    trechos = ((-W / 2 + 0.01, pp0), (pp1, pg0 - 0.03))
    for (a, b) in trechos:
        L.caixa((b - a, 0.035, 0.08), ((a + b) / 2, my, piso), 'muro', chanfro=0.005)
        L.caixa((b - a, 0.012, 0.012), ((a + b) / 2, my, piso + 0.2), 'grade')
        n = max(2, int((b - a) / 0.05))
        for i in range(n):
            L.caixa((0.008, 0.008, 0.12), (a + (b - a) * (i + 0.5) / n, my, piso + 0.08), 'grade')
    for x in (-W / 2 + 0.03, pp0 - 0.02, pp1 + 0.02, pg0 - 0.03, gx1 - 0.01):
        L.caixa((0.05, 0.05, 0.24), (x, my, piso), 'muro')
    for (a, b, alt) in ((pg0, pg1, 0.21), (pp0, pp1, 0.19)):
        L.caixa((b - a, 0.012, alt * 0.55), ((a + b) / 2, my, piso + 0.01), 'portao')
        L.caixa((b - a, 0.016, 0.014), ((a + b) / 2, my, piso + 0.01 + alt * 0.55), 'grade')
        L.caixa((b - a, 0.016, 0.014), ((a + b) / 2, my, piso + alt), 'grade')
        n = int((b - a) / 0.045)
        for i in range(n):
            L.caixa((0.008, 0.008, alt * 0.45), (a + (b - a) * (i + 0.5) / n, my, piso + 0.01 + alt * 0.55), 'grade')

    # Jardim na frente
    L.caixa((0.22, 0.14, 0.012), (bx + 0.16, frente - 0.12, piso), 'grama')
    L.arbusto((bx + 0.1, frente - 0.11, piso + 0.012), 0.055, 'verde')
    L.arbusto((bx + 0.21, frente - 0.12, piso + 0.012), 0.045, 'flor_amarela')


L.principal(__file__, construir)
