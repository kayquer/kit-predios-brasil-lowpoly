"""Prédio residencial de quatro andares sem elevador, estilo COHAB/BNH: fachada de pastilha azul com faixas
brancas nas lajes, sacadas com grade de ferro, torre de escada com cobogó, caixa d'água de concreto no topo e
portaria com grade no térreo."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402

L.PALETA['pastilha_verde'] = '#5fb3a0'   # pastilha verde dos prédios dos anos 70


def construir():
    # Lote: calçada fina
    L.caixa((0.84, 0.92, 0.02), (0, 0, 0), 'piso')
    z0 = 0.02

    # Bloco: térreo + 4 andares
    bw, bd, by = 0.78, 0.74, 0.08
    frente, direita = by - bd / 2, bw / 2
    terreo, andar, n = 0.24, 0.21, 4
    topo = z0 + terreo + andar * n
    L.caixa((bw, bd, terreo), (0, by, z0), 'muro')
    L.caixa((bw, bd, andar * n), (0, by, z0 + terreo), 'pastilha_verde', chanfro=0.015)
    # faixas brancas nas lajes (frente + lado direito)
    for i in range(n + 1):
        z = z0 + terreo + i * andar - 0.012
        L.caixa((bw + 0.02, bd + 0.02, 0.024), (0, by, z), 'parede')
    # platibanda
    L.caixa((bw + 0.03, bd + 0.03, 0.05), (0, by, topo + 0.012), 'parede')
    L.caixa((bw - 0.04, bd - 0.04, 0.005), (0, by, topo + 0.062), 'concreto_escuro')

    # Torre da escada no meio da frente, com cobogó
    cw = 0.18
    L.caixa((cw, 0.06, topo - z0 - terreo + 0.1), (0, frente - 0.03, z0 + terreo), 'parede')
    for i in range(n):
        zc = z0 + terreo + i * andar + andar / 2 + 0.01
        for dx in (-0.045, 0.045):
            for dz in (-0.04, 0.04):
                L.placa(0.05, 0.05, (dx, frente - 0.06, zc + dz), 'concreto_escuro', 'frente', espessura=0.01)

    # Sacadas (dos dois lados da torre) e janelas
    for i in range(n):
        zb = z0 + terreo + i * andar
        for sx in (-1, 1):
            cx = sx * 0.235
            # porta de vidro da sacada
            L.placa(0.13, 0.15, (cx - sx * 0.03, frente, zb + 0.17), 'vidro_escuro', 'frente', espessura=0.01)
            # laje + mureta branca + grade de ferro em cima
            L.caixa((0.28, 0.09, 0.02), (cx, frente - 0.045, zb), 'parede')
            L.caixa((0.28, 0.014, 0.045), (cx, frente - 0.083, zb + 0.02), 'parede')
            L.caixa((0.28, 0.008, 0.035), (cx, frente - 0.083, zb + 0.065), 'grade')
        # janelas do lado direito (+X)
        L.janelas('direita', direita, zb + 0.125, by - 0.26, by + 0.26, 2, 0.15, 0.1, 'vidro_escuro')
        # aparelho de ar-condicionado debaixo de algumas janelas
        if i in (1, 3):
            L.caixa((0.05, 0.08, 0.05), (direita + 0.025, by - 0.13 + (0.26 if i == 3 else 0), zb + 0.02), 'metal')

    # Térreo: portaria com porta de vidro, marquise e grade na frente
    L.placa(0.16, 0.16, (0, frente, z0 + 0.16), 'vidro_escuro', 'frente', espessura=0.01)
    L.caixa((0.26, 0.12, 0.02), (0, frente - 0.06, z0 + 0.19), 'concreto')
    for sx in (-1, 1):
        L.janelas('frente', frente, z0 + 0.13, sx * 0.13, sx * 0.37, 2, 0.08, 0.09, 'vidro_escuro')
    L.janelas('direita', direita, z0 + 0.13, by - 0.26, by + 0.26, 2, 0.12, 0.09, 'vidro_escuro')
    # muro baixo + grade (com o portão no meio, de outra cor)
    gy = -0.44
    for sx in (-1, 1):
        L.caixa((0.29, 0.03, 0.06), (sx * 0.255, gy, z0), 'muro')
        L.caixa((0.29, 0.01, 0.07), (sx * 0.255, gy, z0 + 0.06), 'grade')
        L.caixa((0.03, 0.03, 0.14), (sx * 0.395, gy, z0), 'muro')
    L.caixa((0.22, 0.01, 0.12), (0, gy, z0), 'portao')
    # lado direito do muro, até o prédio
    L.caixa((0.03, 0.08, 0.06), (0.395, gy + 0.05, z0), 'muro')

    # Caixa d'água de concreto no topo (sobre pilares) e casa de máquinas
    tz = topo + 0.062
    L.caixa((0.22, 0.18, 0.04), (0.08, by + 0.08, tz), 'concreto_escuro')
    L.caixa((0.3, 0.26, 0.13), (0.08, by + 0.08, tz + 0.04), 'concreto', chanfro=0.01)
    L.caixa((0.32, 0.28, 0.02), (0.08, by + 0.08, tz + 0.17), 'parede')
    L.caixa((0.14, 0.14, 0.1), (-0.24, by + 0.1, tz), 'parede', chanfro=0.006)
    # antena
    L.cano((-0.24, by + 0.1, tz + 0.1), (-0.24, by + 0.1, tz + 0.2), 0.006, 'metal_escuro', lados=4)


L.principal(__file__, construir)
