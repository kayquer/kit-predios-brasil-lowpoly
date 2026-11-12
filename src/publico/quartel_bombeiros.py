"""Quartel do Corpo de Bombeiros vermelho e branco com dois portões largos (um aberto, com o caminhão vermelho
saindo), pátio de manobra com faixas amarelas, hidrante e torre de treino alta e fina ao lado."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402

V = 'vermelho_bombeiro'


def platibanda(cx, cy, w, d, z, h, cor, e=0.03):
    """Mureta em volta do terraço (quatro caixas finas, o miolo fica livre)."""
    for (px, py, sx, sy) in ((cx, cy - d / 2 + e / 2, w, e), (cx, cy + d / 2 - e / 2, w, e),
                             (cx - w / 2 + e / 2, cy, e, d - 2 * e), (cx + w / 2 - e / 2, cy, e, d - 2 * e)):
        L.caixa((sx, sy, h), (px, py, z), cor)


def caminhao(x, y, z0):
    """Caminhão de bombeiro vermelho com a frente para -Y (y = para-choque)."""
    cw = 0.20
    L.caixa((cw, 0.13, 0.13), (x, y + 0.065, z0 + 0.035), V, chanfro=0.01)        # cabine
    L.placa(cw - 0.04, 0.05, (x, y, z0 + 0.145), 'vidro_escuro', 'frente', espessura=0.01)
    L.caixa((cw, 0.30, 0.15), (x, y + 0.13 + 0.15, z0 + 0.035), V, chanfro=0.01)  # baú de equipamentos
    L.caixa((cw + 0.006, 0.43, 0.018), (x, y + 0.215, z0 + 0.085), 'parede')        # faixa branca
    L.caixa((cw + 0.01, 0.025, 0.03), (x, y - 0.01, z0 + 0.03), 'metal')            # para-choque
    L.caixa((0.08, 0.025, 0.02), (x, y + 0.03, z0 + 0.165), 'azul_policia')        # giroflex
    L.caixa((0.10, 0.30, 0.02), (x, y + 0.28, z0 + 0.185), 'metal')                 # escada no teto
    for dx in (-0.045, 0.045):
        L.caixa((0.012, 0.30, 0.02), (x + dx, y + 0.28, z0 + 0.205), 'metal_escuro')
    for yy in (y + 0.08, y + 0.33):
        L.cilindro(0.038, cw + 0.012, (x - cw / 2 - 0.006, yy, z0 + 0.038), 'escuro', lados=6, rot=(0, 90, 0))


def construir():
    z0 = 0.02
    L.caixa((1.30, 1.30, z0), (0, 0, 0), 'piso')
    L.caixa((0.88, 0.48, 0.006), (-0.20, -0.42, z0), 'concreto')                 # pátio de manobra
    for x in (-0.60, -0.24, 0.16):
        L.caixa((0.02, 0.46, 0.004), (x, -0.42, z0 + 0.006), 'amarelo')
    L.caixa((0.36, 0.72, 0.008), (0.46, -0.28, z0), 'grama')

    # Prédio: térreo branco com os portões, andar de cima vermelho
    cx, cy, w, d = -0.20, 0.16, 0.88, 0.68
    frente, direita = cy - d / 2, cx + w / 2
    L.caixa((w, d, 0.32), (cx, cy, z0), 'parede', chanfro=0.01)
    L.caixa((w, d, 0.20), (cx, cy, z0 + 0.32), V, chanfro=0.01)
    L.caixa((w + 0.014, d + 0.014, 0.03), (cx, cy, z0 + 0.305), 'parede')         # faixa entre andares
    L.caixa((w - 0.02, d - 0.02, 0.02), (cx, cy, z0 + 0.51), 'concreto_escuro')    # laje
    platibanda(cx, cy, w + 0.02, d + 0.02, z0 + 0.50, 0.06, V)
    # Portão aberto (vão escuro) e portão fechado (vermelho com faixa de visores)
    L.placa(0.30, 0.25, (-0.43, frente, z0 + 0.25), 'escuro', 'frente', espessura=0.01)
    L.placa(0.33, 0.015, (-0.43, frente, z0 + 0.265), 'metal_escuro', 'frente', espessura=0.03)
    L.placa(0.30, 0.25, (-0.06, frente, z0 + 0.25), V, 'frente')
    L.placa(0.26, 0.035, (-0.06, frente - 0.04, z0 + 0.20), 'vidro_escuro', 'frente', espessura=0.01)
    for zz in (0.07, 0.12):
        L.placa(0.28, 0.008, (-0.06, frente - 0.04, z0 + zz), 'terracota_escura', 'frente', espessura=0.006)
    L.placa(0.33, 0.015, (-0.06, frente, z0 + 0.265), 'metal_escuro', 'frente', espessura=0.03)
    L.placa(0.07, 0.17, (0.17, frente, z0 + 0.17), 'vidro_escuro', 'frente')      # porta de pedestre
    # Janelas do andar de cima (frente e lado direito) e do térreo no lado
    L.janelas('frente', frente, z0 + 0.42, cx - w / 2 + 0.05, cx + w / 2 - 0.05, 5, 0.12, 0.08, 'vidro')
    L.janelas('direita', direita, z0 + 0.42, cy - d / 2 + 0.05, cy + d / 2 - 0.05, 3, 0.12, 0.08, 'vidro')
    L.janelas('direita', direita, z0 + 0.18, cy - d / 2 + 0.05, cy + d / 2 - 0.05, 3, 0.10, 0.08, 'vidro')
    L.caixa((0.08, 0.06, 0.05), (cx + 0.25, cy + 0.10, z0 + 0.53), 'metal')        # sirene no terraço
    L.cilindro(0.025, 0.03, (cx + 0.25, cy + 0.10, z0 + 0.58), V, lados=6)

    caminhao(-0.43, -0.52, z0)

    # Torre de treino: alta e fina, branca com aberturas escuras e topo vermelho
    tx, ty, tw = 0.47, 0.32, 0.22
    th = 0.80
    L.caixa((tw, tw, th), (tx, ty, z0), 'parede', chanfro=0.01)
    for k in range(4):
        L.caixa((tw + 0.012, tw + 0.012, 0.025), (tx, ty, z0 + 0.17 + k * 0.19), V)
    for k in range(4):
        zc = z0 + 0.10 + k * 0.19
        L.placa(0.08, 0.10, (tx, ty - tw / 2, zc + 0.05), 'escuro', 'frente', espessura=0.01)
        L.placa(0.08, 0.10, (tx + tw / 2, ty, zc + 0.05), 'escuro', 'direita', espessura=0.01)
    L.caixa((tw + 0.03, tw + 0.03, 0.03), (tx, ty, z0 + th), V)
    for (dx, dy) in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        L.caixa((0.012, 0.012, 0.06), (tx + dx * 0.115, ty + dy * 0.115, z0 + th + 0.03), 'grade')
    platibanda(tx, ty, tw + 0.03, tw + 0.03, z0 + th + 0.08, 0.012, 'grade', e=0.012)

    # Hidrante e árvore no gramado
    L.cilindro(0.022, 0.06, (0.36, -0.50, z0), V, lados=6)
    L.cilindro(0.026, 0.015, (0.36, -0.50, z0 + 0.06), V, lados=6, r_topo=0.012)
    L.arvore((0.52, -0.40, z0), 0.40, 'verde')
    L.arbusto((0.56, -0.08, z0), 0.06, 'verde_escuro')


L.principal(__file__, construir)
