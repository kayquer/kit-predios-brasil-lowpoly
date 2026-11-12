"""Chaminé metálica fina de fábrica, branca com faixas vermelhas de sinalização no alto, flange chumbada numa
base de concreto e boca escura."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402


def construir():
    L.caixa((0.42, 0.42, 0.06), (0, 0, 0), 'concreto')                        # base
    L.cilindro(0.16, 0.04, (0, 0, 0.06), 'metal_escuro', lados=8)            # flange
    z0, z1, r0, r1 = 0.06, 1.88, 0.11, 0.09
    L.cilindro(r0, z1 - z0, (0, 0, z0), 'parede', lados=8, r_topo=r1)       # fuste

    def raio(z):
        return r0 + (r1 - r0) * (z - z0) / (z1 - z0)

    for za, zb in ((1.30, 1.42), (1.54, 1.66), (1.78, 1.89)):                # faixas vermelhas
        L.cilindro(raio(za) + 0.006, zb - za, (0, 0, za), 'vermelho', lados=8, r_topo=raio(zb) + 0.006)
    L.cilindro(r1 - 0.012, 0.006, (0, 0, 1.885), 'escuro', lados=8)         # boca


L.principal(__file__, construir)
