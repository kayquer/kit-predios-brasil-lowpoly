"""Chaminé grossa de tijolo de olaria ou usina antiga: base quadrada com boca do forno e cornija, fuste oitavado
que afina para cima, anéis de tijolo mais escuro e coroa com fuligem."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402


def construir():
    L.caixa((1.04, 1.04, 0.10), (0, 0, 0), 'concreto')                       # sapata
    L.caixa((0.72, 0.72, 0.38), (0, 0, 0.10), 'tijolo')                      # base quadrada
    L.caixa((0.80, 0.80, 0.06), (0, 0, 0.48), 'terracota_escura')            # cornija
    L.placa(0.20, 0.22, (0, -0.36, 0.25), 'escuro', 'frente', espessura=0.02)   # boca do forno
    L.placa(0.28, 0.04, (0, -0.36, 0.385), 'terracota_escura', 'frente', espessura=0.04)

    z0, z1, r0, r1 = 0.54, 1.62, 0.29, 0.19
    L.cilindro(r0, z1 - z0, (0, 0, z0), 'tijolo', lados=8, r_topo=r1)       # fuste

    def raio(z):
        return r0 + (r1 - r0) * (z - z0) / (z1 - z0)

    for z in (0.62, 0.98, 1.34):                                             # anéis
        L.cilindro(raio(z) + 0.018, 0.05, (0, 0, z), 'terracota_escura', lados=8, r_topo=raio(z + 0.05) + 0.018)
    L.cilindro(r1 + 0.05, 0.08, (0, 0, z1), 'terracota_escura', lados=8, r_topo=r1 + 0.06)   # coroa
    L.cilindro(r1 - 0.02, 0.006, (0, 0, z1 + 0.08), 'escuro', lados=8)      # fuligem na boca


L.principal(__file__, construir)
