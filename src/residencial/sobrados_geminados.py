"""Dois sobrados geminados lado a lado, um pêssego e outro azul pastel, cada um com portão de garagem de chapa,
porta, marquise e janela com grade em cima, telhado contínuo de telha de barro dividido por uma parede corta-fogo."""
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
    W, D = 1.36, 0.9
    L.caixa((W, D, 0.012), (0, 0, 0), 'piso')
    piso = 0.012

    bw, bd = 1.24, 0.56
    yf, yb = -0.16, 0.4
    by = (yf + yb) / 2
    h1, h2, alt = 0.36, 0.32, 0.26
    zt = piso + h1 + h2
    beiral = 0.05

    unidades = ((-bw / 4, 'pessego', 'terracota_escura'), (bw / 4, 'azul_pastel', 'galpao_azul'))
    for (cx, cor, cor_portao) in unidades:
        L.caixa((bw / 2, bd, h1 + h2), (cx, by, piso), cor, chanfro=0.008)
        L.caixa((bw / 2 + 0.01, bd + 0.012, 0.05), (cx, by, piso), 'concreto_escuro')               # rodapé
        L.caixa((bw / 2 + 0.01, bd + 0.014, 0.02), (cx, by, piso + h1 - 0.01), 'branco')           # friso
        L.prisma([(yf, 0), (yb, 0), (by, alt)], bw / 2, (cx, 0, zt), cor, eixo='X')                 # oitão

        # Térreo: portão de garagem de chapa com frisos, porta e marquise
        gx, px = cx - 0.1, cx + 0.19
        bloco('frente', yf, gx, piso, 0.34, 0.27, 0.01, 'branco')
        bloco('frente', yf, gx, piso, 0.31, 0.255, 0.008, cor_portao, off=0.01)
        for k in range(4):
            bloco('frente', yf, gx, piso + 0.04 + k * 0.055, 0.31, 0.008, 0.006, 'metal_escuro', off=0.018)
        bloco('frente', yf, px, piso, 0.13, 0.27, 0.01, 'branco')
        bloco('frente', yf, px, piso, 0.105, 0.255, 0.008, 'madeira', off=0.01)
        bloco('frente', yf, cx, piso + 0.29, bw / 2 - 0.04, 0.025, 0.12, 'branco')                 # marquise

        # Andar de cima: janela grande com grade e floreira
        janela('frente', yf, cx - 0.04, piso + h1 + 0.1, 0.32, 0.15, barras=5)
        bloco('frente', yf, cx - 0.04, piso + h1 + 0.045, 0.3, 0.035, 0.05, 'tijolo')
        for k in range(4):
            L.arbusto((cx - 0.15 + k * 0.075, yf - 0.025, piso + h1 + 0.08), 0.03,
                      ('flor_rosa', 'verde', 'flor_amarela', 'verde')[k])

        # Rampa da garagem
        L.caixa((0.34, yf - (-D / 2 + 0.02), 0.006), (gx, (yf - D / 2 + 0.02) / 2, piso), 'concreto')

    # Telhado contínuo (cumeeira em X) e parede corta-fogo no meio
    s = alt / (bd / 2)
    a = bd / 2 + beiral
    for lado in (-1, 1):
        perfil = [(by + lado * a, zt + alt - s * a), (by, zt + alt), (by, zt + alt + 0.025),
                  (by + lado * a, zt + alt - s * a + 0.025)]
        L.prisma(perfil, bw + 2 * beiral, (0, 0, 0), 'terracota', eixo='X')
    L.caixa((bw + 2 * beiral + 0.01, 0.02, 0.016), (0, by, zt + alt + 0.012), 'terracota_escura')
    L.prisma([(yf - 0.03, 0), (yb + 0.03, 0), (yb + 0.03, 0.03), (by, alt + 0.06), (yf - 0.03, 0.03)],
             0.05, (0, 0, zt), 'branco', eixo='X')

    # Lado direito (azul): janelas nos dois andares
    janela('direita', bw / 2, by, piso + 0.13, 0.16, 0.15)
    janela('direita', bw / 2, by, piso + h1 + 0.1, 0.16, 0.15)
    janela('esquerda', -bw / 2, by, piso + h1 + 0.1, 0.16, 0.15)

    # Mureta baixa dividindo as duas entradas e canteiros
    my = -D / 2 + 0.02
    L.caixa((0.035, yf - my, 0.1), (0, (yf + my) / 2, piso), 'branco')
    for cx in (-bw / 4, bw / 4):
        L.caixa((0.1, 0.08, 0.035), (cx + 0.2, my + 0.06, piso), 'concreto_escuro')
        L.arbusto((cx + 0.2, my + 0.06, piso + 0.035), 0.045, 'verde')


L.principal(__file__, construir)
