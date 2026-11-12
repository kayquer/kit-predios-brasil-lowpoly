"""Edifício comercial de quatro andares revestido de granito rosa: agência bancária no térreo com vidro fumê, porta
giratória e marquise com faixa colorida (sem marca), andares de escritório com janelas em fita, ar-condicionado
e casa de máquinas no topo."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402

L.PALETA['granito_rosa'] = '#b8968a'   # granito rosa/vermelho das fachadas de banco
L.PALETA['vidro_fume'] = '#2f4a63'
L.PALETA['faixa_banco'] = '#1c7a8c'    # cor de identidade genérica (sem marca)


def construir():
    L.caixa((0.84, 0.88, 0.02), (0, 0, 0), 'piso')
    z0 = 0.02

    bw, bd, by = 0.76, 0.78, 0.035
    frente, direita = by - bd / 2, bw / 2
    t, a, n = 0.29, 0.195, 4
    corpo = z0 + t
    topo = corpo + a * n

    # Térreo: caixa de vidro fumê recuada entre pilares de granito preto
    L.caixa((bw - 0.06, bd - 0.06, t), (0, by + 0.01, z0), 'vidro_fume')
    for x in (-bw / 2 + 0.03, -0.13, 0.13, bw / 2 - 0.03):
        L.caixa((0.05, 0.05, t), (x, frente + 0.03, z0), 'escuro')
    for y in (by - 0.13, by + 0.13, by + bd / 2 - 0.03):
        L.caixa((0.05, 0.05, t), (direita - 0.03, y, z0), 'escuro')
    # porta giratória (cilindro de vidro com tampa de metal)
    L.cilindro(0.075, 0.2, (0, frente + 0.03, z0), 'vidro', lados=8)
    L.cilindro(0.08, 0.025, (0, frente + 0.03, z0 + 0.2), 'metal', lados=8)
    L.caixa((0.008, 0.14, 0.2), (0, frente + 0.03, z0), 'metal', rot=(0, 0, 45))

    # Marquise com faixa colorida na frente e no lado
    L.caixa((bw + 0.02, 0.14, 0.04), (0, frente - 0.03, z0 + t - 0.05), 'concreto', chanfro=0.008)
    L.placa(bw + 0.02, 0.03, (0, frente - 0.092, z0 + t - 0.02), 'faixa_banco', 'frente', espessura=0.008)

    # Corpo de granito com janelas em fita (frente e direita)
    L.caixa((bw, bd, a * n), (0, by, corpo), 'granito_rosa', chanfro=0.015)
    for i in range(n):
        zc = corpo + i * a + a / 2 + 0.01
        L.placa(bw - 0.1, 0.1, (0, frente, zc), 'vidro', 'frente', espessura=0.012)
        L.placa(bd - 0.1, 0.1, (direita, by, zc), 'vidro', 'direita', espessura=0.012)
        # montantes
        for k in range(1, 5):
            x = -(bw - 0.1) / 2 + k * (bw - 0.1) / 5
            L.placa(0.012, 0.1, (x, frente - 0.012, zc), 'metal_escuro', 'frente', espessura=0.006)
        for k in range(1, 4):
            y = by - (bd - 0.1) / 2 + k * (bd - 0.1) / 4
            L.placa(0.012, 0.1, (direita + 0.012, y, zc), 'metal_escuro', 'direita', espessura=0.006)
        # ar-condicionado na fachada lateral
        if i % 2 == 0:
            L.caixa((0.035, 0.08, 0.05), (direita + 0.017, by + 0.2 - 0.3 * (i // 2), zc - 0.105), 'metal')
    # Faixa vertical escura na quina (prumada)
    L.caixa((0.06, 0.06, a * n + 0.06), (direita - 0.025, frente + 0.025, corpo), 'escuro', chanfro=0.006)

    # Platibanda, laje e casa de máquinas
    L.caixa((bw + 0.02, bd + 0.02, 0.05), (0, by, topo), 'granito_rosa')
    L.caixa((bw - 0.04, bd - 0.04, 0.005), (0, by, topo + 0.05), 'concreto_escuro')
    tz = topo + 0.055
    L.caixa((0.26, 0.24, 0.13), (-0.16, by + 0.12, tz), 'concreto', chanfro=0.008)
    L.caixa((0.28, 0.26, 0.02), (-0.16, by + 0.12, tz + 0.13), 'concreto_escuro')
    for k in range(3):
        L.caixa((0.09, 0.09, 0.06), (0.13 + (k % 2) * 0.12, by - 0.12 + k * 0.13, tz), 'metal')
        L.cilindro(0.03, 0.005, (0.13 + (k % 2) * 0.12, by - 0.12 + k * 0.13, tz + 0.06), 'metal_escuro', lados=6)
    L.cano((-0.27, by - 0.15, tz), (-0.27, by - 0.15, tz + 0.2), 0.006, 'metal_escuro', lados=4)


L.principal(__file__, construir)
