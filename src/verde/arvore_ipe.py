"""Ipê-amarelo de calçada florido: tronco fino que se abre em dois galhos, copa amarela facetada e um tapete de
flores caídas no canteiro."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402


def construir():
    L.caixa((0.19, 0.19, 0.012), (0, 0, 0), 'terra')                                    # canteiro
    L.cilindro(0.085, 0.004, (0.01, -0.01, 0.012), 'ipe_amarelo', lados=6)               # flores caídas
    L.cilindro(0.017, 0.5, (0, 0, 0.012), 'madeira_escura', lados=5, r_topo=0.011)
    L.cano((0, 0, 0.36), (-0.045, -0.03, 0.5), 0.009, 'madeira_escura', lados=4)
    L.esfera(0.1, (0.005, 0.01, 0.6), 'ipe_amarelo', escala=(1.0, 1.12, 0.72))
    L.esfera(0.08, (-0.03, -0.035, 0.52), 'flor_amarela', escala=(0.95, 1.0, 0.6))
    L.esfera(0.065, (0.035, 0.04, 0.68), 'ipe_amarelo', escala=(1.0, 1.0, 0.8))


L.principal(__file__, construir)
