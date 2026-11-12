"""Contêiner marítimo laranja de vinte pés com nervuras nas laterais, trilhos de base e topo e porta com tranca no
fundo (frente para -Y)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402

L.PALETA['conteiner'] = '#e8742c'
L.PALETA['conteiner_escuro'] = '#b5531d'


def construir():
    w, d, h = 0.37, 0.80, 0.35
    L.caixa((w - 0.02, d - 0.02, h - 0.06), (0, 0, 0.03), 'conteiner')              # corpo
    L.caixa((w, d, 0.03), (0, 0, 0), 'conteiner_escuro')                            # trilho de base
    L.caixa((w, d, 0.03), (0, 0, h - 0.03), 'conteiner')                            # teto com trilho
    for y in (-0.30, -0.15, 0.0, 0.15, 0.30):                                       # nervuras
        L.caixa((w, 0.03, h - 0.08), (0, y, 0.04), 'conteiner_escuro')
    L.caixa((w - 0.06, 0.012, h - 0.09), (0, -d / 2 - 0.002, 0.045), 'conteiner_escuro')  # quadro da porta
    L.caixa((0.012, 0.02, h - 0.09), (0, -d / 2 - 0.005, 0.045), 'grade')            # tranca


L.principal(__file__, construir)
