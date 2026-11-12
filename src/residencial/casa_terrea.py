"""Casa térrea de bairro pintada de amarelo pastel, com telhado de quatro águas de telha de barro, caixa d'água
azul aparecendo atrás, janelas com grade, barra colorida no rodapé e muro baixo com portão de ferro na frente."""
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


def caixa_dagua(x, y, z, r=0.075, h=0.1):
    L.cilindro(r, h, (x, y, z), 'fibra_azul', lados=8, r_topo=r * 1.12)
    L.cilindro(r * 1.16, 0.025, (x, y, z + h), 'fibra_azul', lados=8, r_topo=r * 0.7)


def construir():
    W, D = 1.28, 1.0
    L.caixa((W, D, 0.012), (0, 0, 0), 'piso')                     # quintal cimentado
    piso = 0.012

    # Corpo da casa
    bx, by, bw, bd, bh = -0.05, 0.13, 1.0, 0.62, 0.46
    frente, direita = by - bd / 2, bx + bw / 2
    L.caixa((bw, bd, bh), (bx, by, piso), 'amarelo_pastel', chanfro=0.01)
    L.caixa((bw + 0.012, bd + 0.012, 0.07), (bx, by, piso), 'terracota_escura')   # barra do rodapé
    L.caixa((bw + 0.02, bd + 0.02, 0.025), (bx, by, piso + bh - 0.025), 'branco')  # testeira
    L.telhado4(bw, bd, 0.3, (bx, by, piso + bh), 'terracota', beiral=0.07)
    L.caixa((0.4, 0.014, 0.012), (bx, by, piso + bh + 0.3 - 0.006), 'terracota_escura')  # cumeeira
    caixa_dagua(bx + 0.24, by + 0.2, piso + bh + 0.15, r=0.085)

    # Frente: porta, duas janelas com grade e degrau
    bloco('frente', frente, bx - 0.12, piso, 0.17, 0.32, 0.012, 'branco')
    bloco('frente', frente, bx - 0.12, piso, 0.14, 0.3, 0.008, 'madeira', off=0.012)
    bloco('frente', frente, bx - 0.12, piso, 0.24, 0.025, 0.08, 'concreto')
    janela('frente', frente, bx - 0.36, piso + 0.17, 0.2, 0.18)
    janela('frente', frente, bx + 0.25, piso + 0.17, 0.26, 0.18, barras=4)
    # Lado direito: duas janelas
    janela('direita', direita, by - 0.1, piso + 0.19, 0.16, 0.16)
    janela('direita', direita, by + 0.17, piso + 0.24, 0.1, 0.1, barras=2)  # basculante do banheiro

    # Muro baixo da frente com portão de ferro (metade chapa, metade grade) e portãozinho
    my, mh, me = -D / 2 + 0.025, 0.17, 0.04
    gx0, gx1 = 0.12, 0.56                                         # vão do portão da garagem
    px0, px1 = -0.3, -0.12                                        # vão do portãozinho
    for (a, b) in ((-W / 2 + 0.01, px0), (px1, gx0), (gx1, W / 2 - 0.01)):
        L.caixa((b - a, me, mh), ((a + b) / 2, my, piso), 'muro', chanfro=0.005)
        L.caixa((b - a + 0.012, me + 0.014, 0.018), ((a + b) / 2, my, piso + mh), 'concreto')
    for gx in (gx0 - 0.02, gx1 + 0.02, px0 - 0.02, px1 + 0.02):  # pilaretes
        L.caixa((0.05, 0.055, mh + 0.05), (gx, my, piso), 'muro')
    for (a, b, alt) in ((gx0, gx1, 0.22), (px0, px1, 0.2)):
        L.caixa((b - a, 0.012, alt * 0.5), ((a + b) / 2, my, piso + 0.01), 'portao')   # chapa
        L.caixa((b - a, 0.016, 0.014), ((a + b) / 2, my, piso + 0.01 + alt * 0.5), 'grade')
        L.caixa((b - a, 0.016, 0.014), ((a + b) / 2, my, piso + alt), 'grade')
        n = int((b - a) / 0.045)
        for i in range(n):
            x = a + (b - a) * (i + 0.5) / n
            L.caixa((0.008, 0.008, alt * 0.5), (x, my, piso + 0.01 + alt * 0.5), 'grade')
    # Muros laterais baixos até a casa
    for x in (-W / 2 + 0.02, W / 2 - 0.02):
        L.caixa((0.035, 0.34, mh * 0.85), (x, my + 0.19, piso), 'muro')

    # Canteiro com arbusto e flores ao lado da porta
    L.caixa((0.26, 0.09, 0.04), (bx - 0.4, frente - 0.07, piso), 'tijolo')
    L.arbusto((bx - 0.45, frente - 0.07, piso + 0.04), 0.06, 'verde')
    L.arbusto((bx - 0.35, frente - 0.07, piso + 0.04), 0.045, 'flor_rosa')


L.principal(__file__, construir)
