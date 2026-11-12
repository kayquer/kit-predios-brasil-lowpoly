"""Árvore pequena de calçada (oiti): tronco fino, copa verde redonda e facetada e canteiro quadrado de concreto
com terra no pé."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402


def construir():
    e, lado, h = 0.025, 0.19, 0.03
    for (sx, sy, x, y) in ((lado, e, 0, -lado / 2 + e / 2), (lado, e, 0, lado / 2 - e / 2),
                           (e, lado - 2 * e, -lado / 2 + e / 2, 0), (e, lado - 2 * e, lado / 2 - e / 2, 0)):
        L.caixa((sx, sy, h), (x, y, 0), 'concreto')
    L.caixa((lado - 2 * e, lado - 2 * e, h - 0.008), (0, 0, 0), 'terra')
    L.cilindro(0.016, 0.3, (0, 0, h - 0.008), 'madeira_escura', lados=5, r_topo=0.011)
    L.esfera(0.1, (0, 0, 0.42), 'verde', escala=(1.0, 1.15, 0.95))
    L.esfera(0.07, (0.03, -0.04, 0.36), 'verde_escuro', escala=(1.0, 1.0, 0.9))


L.principal(__file__, construir)
