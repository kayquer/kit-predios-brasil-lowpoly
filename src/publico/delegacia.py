"""Delegacia/base da polícia: prédio branco de térreo e meio com faixa azul, janelas com grade, marquise na
entrada, estacionamento com a viatura branca e azul e mastro com a bandeira verde-amarela."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402

L.PALETA['bandeira'] = '#1f9a48'
A = 'azul_policia'


def bandeira(x, y, z_topo, z0):
    """Mastro com bandeira verde e losango amarelo, tremulando para +X."""
    L.cilindro(0.025, 0.03, (x, y, z0), 'concreto', lados=6)
    L.cano((x, y, z0), (x, y, z_topo + 0.02), 0.008, 'metal', lados=4)
    fw, fh = 0.17, 0.115
    fx, fz = x + 0.012 + fw / 2, z_topo - fh / 2
    L.caixa((fw, 0.006, fh), (fx, y, fz - fh / 2), 'bandeira')
    rw, rh = fw * 0.40, fh * 0.38
    L.prisma([(fx - rw, fz), (fx, fz - rh), (fx + rw, fz), (fx, fz + rh)], 0.012, (0, y, 0), 'amarelo', eixo='Y')


def janela_grade(face, plano, c, zc, larg=0.11, alt=0.11):
    """Janela de vidro escuro com três barras de grade na frente."""
    if face == 'frente':
        L.placa(larg, alt, (c, plano, zc), 'vidro_escuro', face, espessura=0.02)
        for k in (-1, 0, 1):
            L.placa(0.008, alt, (c + k * larg * 0.3, plano - 0.02, zc), 'grade', face, espessura=0.008)
    else:
        L.placa(larg, alt, (plano, c, zc), 'vidro_escuro', face, espessura=0.02)
        for k in (-1, 0, 1):
            L.placa(0.008, alt, (plano + 0.02, c + k * larg * 0.3, zc), 'grade', face, espessura=0.008)


def viatura(x, y, z0):
    """Viatura branca com faixa azul e giroflex, frente para -Y (y = centro do carro)."""
    cw, cl = 0.17, 0.34
    L.caixa((cw, cl, 0.07), (x, y, z0 + 0.028), 'parede', chanfro=0.01)
    L.caixa((cw + 0.006, cl - 0.06, 0.022), (x, y, z0 + 0.06), A)                    # faixa azul
    L.caixa((cw - 0.02, 0.17, 0.055), (x, y + 0.02, z0 + 0.098), 'vidro_escuro')     # vidros
    L.caixa((cw - 0.016, 0.14, 0.012), (x, y + 0.025, z0 + 0.153), 'parede')          # teto
    L.caixa((0.05, 0.03, 0.018), (x - 0.025, y + 0.0, z0 + 0.165), 'vermelho')       # giroflex
    L.caixa((0.05, 0.03, 0.018), (x + 0.025, y + 0.0, z0 + 0.165), A)
    for yy in (y - 0.10, y + 0.10):
        L.cilindro(0.03, cw + 0.01, (x - cw / 2 - 0.005, yy, z0 + 0.03), 'escuro', lados=6, rot=(0, 90, 0))


def construir():
    z0 = 0.02
    L.caixa((0.86, 1.22, z0), (0, 0, 0), 'piso')
    L.caixa((0.46, 0.50, 0.006), (0.18, -0.34, z0), 'asfalto')                     # estacionamento
    for x in (-0.03, 0.39):
        L.caixa((0.012, 0.42, 0.004), (x, -0.34, z0 + 0.006), 'branco')
    L.caixa((0.30, 0.30, 0.008), (-0.26, -0.44, z0), 'grama')

    # Prédio térreo e meio: branco, faixa azul larga no topo do térreo
    cx, cy, w, d = 0.0, 0.265, 0.80, 0.63
    frente, direita = cy - d / 2, cx + w / 2
    L.caixa((w, d, 0.30), (cx, cy, z0), 'parede', chanfro=0.01)
    L.caixa((w + 0.014, d + 0.014, 0.025), (cx, cy, z0), 'concreto')                 # rodapé
    L.caixa((w + 0.02, d + 0.02, 0.075), (cx, cy, z0 + 0.255), A)                   # faixa azul / platibanda
    L.caixa((w - 0.02, d - 0.02, 0.012), (cx, cy, z0 + 0.32), 'concreto_escuro')    # laje
    # Meio andar recuado no fundo
    mx, my, mw, md = -0.05, 0.40, 0.66, 0.34
    L.caixa((mw, md, 0.17), (mx, my, z0 + 0.33), 'parede', chanfro=0.01)
    L.caixa((mw + 0.014, md + 0.014, 0.025), (mx, my, z0 + 0.48), A)
    L.caixa((mw - 0.01, md - 0.01, 0.017), (mx, my, z0 + 0.495), 'concreto_escuro')   # laje do meio andar
    L.placa(mw - 0.12, 0.05, (mx, my - md / 2, z0 + 0.43), 'vidro_escuro', 'frente', espessura=0.02)
    L.placa(md - 0.10, 0.05, (mx + mw / 2, my, z0 + 0.43), 'vidro_escuro', 'direita', espessura=0.02)
    L.caixa((0.14, 0.12, 0.06), (mx - 0.18, my + 0.05, z0 + 0.505), 'concreto')     # casa de máquinas

    # Janelas com grade: frente (dos dois lados da entrada) e lado direito
    jz = z0 + 0.15
    for c in (-0.30, 0.26):
        janela_grade('frente', frente, c, jz)
    for c in (cy - 0.21, cy, cy + 0.21):
        janela_grade('direita', direita, c, jz)
    # Entrada: porta de vidro dupla, marquise com testeira azul sobre dois pilares e degrau
    ex = -0.04
    L.placa(0.16, 0.19, (ex, frente, z0 + 0.21), 'vidro', 'frente')
    L.placa(0.008, 0.19, (ex, frente - 0.04, z0 + 0.21), 'metal_escuro', 'frente', espessura=0.008)
    L.caixa((0.34, 0.18, 0.02), (ex, frente - 0.09, z0 + 0.235), 'parede')
    L.caixa((0.35, 0.014, 0.035), (ex, frente - 0.18, z0 + 0.225), A)
    for dx in (-0.15, 0.15):
        L.caixa((0.02, 0.02, 0.235), (ex + dx, frente - 0.165, z0), 'concreto')
    L.caixa((0.24, 0.08, 0.015), (ex, frente - 0.04, z0), 'concreto')

    viatura(0.20, -0.33, z0)
    bandeira(-0.30, -0.47, 0.90, z0)
    L.arbusto((-0.18, -0.52, z0), 0.06, 'verde_escuro')
    L.arbusto((-0.36, -0.36, z0), 0.05, 'verde')


L.principal(__file__, construir)
