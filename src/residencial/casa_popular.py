"""Casa popular de conjunto habitacional pintada de rosa pastel, pequena e simples, com telhado de duas águas de
telha de barro, porta e duas janelas, murinho baixo na frente, padrão de luz e um pé de bananeira no quintal."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402

L.PALETA['telha_clara'] = '#d67a4a'    # telha nova, mais clara


def bloco(face, plano, u, z0, larg, alt, prof, cor, off=0.0):
    """Caixa encostada numa fachada: u = posição ao longo da face, z0 = base, off = afastamento da parede."""
    if face == 'frente':
        return L.caixa((larg, prof, alt), (u, plano - off - prof / 2, z0), cor)
    if face == 'tras':
        return L.caixa((larg, prof, alt), (u, plano + off + prof / 2, z0), cor)
    if face == 'direita':
        return L.caixa((prof, larg, alt), (plano + off + prof / 2, u, z0), cor)
    return L.caixa((prof, larg, alt), (plano - off - prof / 2, u, z0), cor)


def janela(face, plano, u, z0, larg, alt, moldura='branco', barras=2):
    """Janela com moldura, vidro, peitoril e grade simples."""
    bloco(face, plano, u, z0 - 0.012, larg + 0.04, alt + 0.03, 0.01, moldura)
    bloco(face, plano, u, z0, larg, alt, 0.006, 'vidro_escuro', off=0.01)
    bloco(face, plano, u, z0 - 0.022, larg + 0.06, 0.016, 0.03, 'concreto')
    for i in range(barras):
        uu = u - larg / 2 + larg * (i + 1) / (barras + 1)
        bloco(face, plano, uu, z0, 0.009, alt, 0.008, 'grade', off=0.018)


def telhado_lados(larg, prof, alt, pos, cor, cor_oitao, beiral=0.05, t=0.025):
    """Duas águas com a cumeeira em X: oitões nos lados (cor da fachada) e telhas em placa fina."""
    x, y, z = pos
    L.prisma([(-prof / 2, 0), (prof / 2, 0), (0, alt)], larg, (x, y, z), cor_oitao, eixo='X')
    s = alt / (prof / 2)
    a = prof / 2 + beiral
    for lado in (-1, 1):
        perfil = [(lado * a, alt - s * a), (0, alt), (0, alt + t), (lado * a, alt - s * a + t)]
        L.prisma(perfil, larg + 2 * beiral, (x, y, z), cor, eixo='X')


def bananeira(x, y, z, alt=0.4):
    L.cilindro(0.028, alt, (x, y, z), 'verde_escuro', lados=5, r_topo=0.02)
    for i, ang in enumerate((15, 85, 160, 230, 300)):
        a = math.radians(ang)
        cx, cy = x - math.sin(a) * 0.09, y + math.cos(a) * 0.09
        L.caixa((0.06, 0.2, 0.008), (cx, cy, z + alt - 0.03 - 0.02 * (i % 2)), 'banana', rot=(-30 + 15 * (i % 2), 0, ang))
    L.cilindro(0.022, 0.06, (x + 0.02, y - 0.02, z + alt - 0.11), 'amarelo', lados=5, r_topo=0.012)  # cacho


def construir():
    W, D = 1.28, 0.9
    L.caixa((W, D, 0.012), (0, 0, 0), 'grama')
    piso = 0.012

    # Corpo da casa
    bx, by, bw, bd, bh = -0.12, 0.1, 0.9, 0.56, 0.42
    frente, direita = by - bd / 2, bx + bw / 2
    L.caixa((bw, bd, bh), (bx, by, piso), 'rosa_pastel', chanfro=0.01)
    L.caixa((bw + 0.012, bd + 0.012, 0.05), (bx, by, piso), 'concreto_escuro')     # rodapé
    telhado_lados(bw, bd, 0.24, (bx, by, piso + bh), 'telha_clara', 'rosa_pastel', beiral=0.06)
    L.caixa((bw + 0.12, 0.018, 0.016), (bx, by, piso + bh + 0.255), 'terracota_escura')  # cumeeira

    # Calçadinha em volta e caminho até o portão
    L.caixa((bw + 0.08, 0.1, 0.008), (bx, frente - 0.05, piso), 'concreto')
    L.caixa((0.16, frente - 0.05 - (-D / 2 + 0.03), 0.008), (bx - 0.1, (frente - 0.1 - D / 2 + 0.03) / 2, piso),
            'concreto')

    # Frente: porta e duas janelas
    bloco('frente', frente, bx - 0.1, piso, 0.16, 0.29, 0.012, 'branco')
    bloco('frente', frente, bx - 0.1, piso, 0.13, 0.275, 0.008, 'azul_pastel', off=0.012)
    janela('frente', frente, bx - 0.32, piso + 0.15, 0.18, 0.15)
    janela('frente', frente, bx + 0.22, piso + 0.15, 0.24, 0.15, barras=3)
    # Lado direito: janela do quarto e basculante
    janela('direita', direita, by - 0.08, piso + 0.15, 0.17, 0.15)
    janela('direita', direita, by + 0.16, piso + 0.24, 0.09, 0.08, barras=1)

    # Murinho baixo pintado com abertura no meio e padrão de luz
    my = -D / 2 + 0.02
    for (a, b) in ((-W / 2 + 0.01, bx - 0.19), (bx - 0.01, W / 2 - 0.01)):
        L.caixa((b - a, 0.035, 0.09), ((a + b) / 2, my, piso), 'branco', chanfro=0.005)
        L.caixa((b - a + 0.01, 0.04, 0.014), ((a + b) / 2, my, piso + 0.09), 'rosa_pastel')
    for x in (-W / 2 + 0.01, W / 2 - 0.01):
        L.caixa((0.035, D * 0.45, 0.09), (x + (0.0175 if x < 0 else -0.0175), my + D * 0.225, piso), 'branco')
    px = 0.1
    L.caixa((0.08, 0.06, 0.26), (px, my + 0.035, piso), 'concreto')                  # mureta do padrão
    L.caixa((0.06, 0.02, 0.08), (px, my - 0.005, piso + 0.14), 'metal')                # caixa do medidor
    L.cano((px, my + 0.035, piso + 0.26), (px, my + 0.035, piso + 0.52), 0.008, 'metal_escuro', lados=4)

    # Quintal do lado: bananeira e um vaso
    bananeira(direita + 0.15, by - 0.15, piso)
    L.cilindro(0.035, 0.05, (bx - 0.36, frente - 0.12, piso), 'terracota', lados=6, r_topo=0.045)
    L.arbusto((bx - 0.36, frente - 0.12, piso + 0.05), 0.045, 'verde')


L.principal(__file__, construir)
