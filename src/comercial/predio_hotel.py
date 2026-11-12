"""Hotel de centro de cidade com cinco andares: fachada salmão com janelas de moldura branca, faixa de cobogó
branco subindo pela fachada, aparelhos de ar-condicionado nas janelas, marquise na entrada de vidro e letreiro
vertical colorido na esquina (sem texto)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402

L.PALETA['salmao'] = '#e09068'


def construir():
    L.caixa((0.95, 0.92, 0.02), (0, 0, 0), 'piso')
    z0 = 0.02

    bw, bd, bx, by = 0.80, 0.74, -0.04, 0.08
    frente, direita = by - bd / 2, bx + bw / 2
    terreo, andar, n = 0.22, 0.185, 5
    corpo = z0 + terreo
    topo = corpo + andar * n

    # Térreo (recuado) com saguão de vidro, e corpo dos andares
    L.caixa((bw - 0.04, bd - 0.04, terreo), (bx, by + 0.02, z0), 'parede')
    L.caixa((bw, bd, andar * n), (bx, by, corpo), 'salmao', chanfro=0.015)
    L.caixa((bw + 0.02, bd + 0.02, 0.03), (bx, by, corpo - 0.015), 'parede')       # laje do 1º andar
    L.caixa((bw + 0.03, bd + 0.03, 0.06), (bx, by, topo), 'parede')               # platibanda
    L.caixa((bw - 0.03, bd - 0.03, 0.005), (bx, by, topo + 0.06), 'concreto_escuro')
    fr0 = frente + 0.02
    L.placa(0.5, 0.17, (bx + 0.1, fr0, z0 + 0.185), 'vidro_escuro', 'frente', espessura=0.01)
    L.placa(0.12, 0.15, (bx + 0.1, fr0 - 0.01, z0 + 0.15), 'vidro', 'frente', espessura=0.008)   # porta
    L.janelas('direita', direita - 0.02, z0 + 0.13, by - 0.25, by + 0.28, 2, 0.16, 0.1, 'vidro_escuro')

    # Marquise da entrada (laje fina em balanço sobre dois pilares)
    L.caixa((0.46, 0.16, 0.03), (bx + 0.1, frente - 0.08, z0 + 0.2), 'concreto', chanfro=0.006)
    L.caixa((0.47, 0.165, 0.012), (bx + 0.1, frente - 0.08, z0 + 0.23), 'vermelho')
    for dx in (-0.2, 0.2):
        L.cano((bx + 0.1 + dx, frente - 0.14, z0), (bx + 0.1 + dx, frente - 0.14, z0 + 0.2), 0.01, 'metal', lados=4)

    # Faixa de cobogó (elemento vazado) subindo à esquerda da fachada
    cx = bx - bw / 2 + 0.11
    L.caixa((0.17, 0.03, andar * n), (cx, frente - 0.015, corpo), 'parede')
    for i in range(n):
        zc = corpo + i * andar + andar / 2
        for dx in (-0.04, 0.04):
            for dz in (-0.04, 0.04):
                L.placa(0.05, 0.05, (cx + dx, frente - 0.03, zc + dz), 'concreto_escuro', 'frente', espessura=0.006)

    # Janelas dos andares: frente (3 por andar) e lado direito (3), com ar-condicionado
    for i in range(n):
        zc = corpo + i * andar + andar / 2 + 0.01
        L.janelas('frente', frente, zc, bx - bw / 2 + 0.21, direita - 0.04, 3, 0.11, 0.1, 'vidro_escuro')
        L.caixa((0.58, 0.02, 0.012), (bx + 0.08, frente - 0.01, zc - 0.062), 'parede')   # peitoril contínuo
        L.janelas('direita', direita, zc, by - bd / 2 + 0.06, by + bd / 2 - 0.06, 3, 0.11, 0.1, 'vidro_escuro')
        # ar-condicionado (caixinha branca) debaixo de algumas janelas
        xs = (bx - 0.03, bx + 0.33) if i % 2 == 0 else (bx + 0.15,)
        for x in xs:
            L.caixa((0.07, 0.04, 0.04), (x, frente - 0.02, zc - 0.095), 'metal')
        if i in (0, 2, 3):
            L.caixa((0.04, 0.07, 0.04), (direita + 0.02, by - 0.12 + 0.24 * (i % 2), zc - 0.095), 'metal')

    # Letreiro vertical na esquina direita (faixas coloridas, sem texto)
    lx, ly = direita - 0.03, frente - 0.06
    L.caixa((0.035, 0.1, 0.62), (lx, ly, corpo + 0.2), 'vermelho', chanfro=0.006)
    for k in range(4):
        L.caixa((0.04, 0.105, 0.04), (lx, ly, corpo + 0.27 + k * 0.13), 'amarelo')
    L.caixa((0.02, 0.02, 0.06), (lx, ly + 0.03, corpo + 0.14), 'grade')
    L.caixa((0.02, 0.02, 0.06), (lx, ly - 0.03, corpo + 0.82), 'grade')

    # Telhado: casa de máquinas e caixa d'água
    tz = topo + 0.065
    L.caixa((0.22, 0.18, 0.13), (bx - 0.15, by + 0.14, tz), 'parede', chanfro=0.008)
    L.caixa((0.24, 0.2, 0.02), (bx - 0.15, by + 0.14, tz + 0.13), 'concreto_escuro')
    L.cilindro(0.07, 0.08, (bx + 0.2, by + 0.12, tz), 'fibra_azul', lados=8)
    L.cilindro(0.075, 0.015, (bx + 0.2, by + 0.12, tz + 0.08), 'fibra_azul', lados=8)

    # Vasos com palmeirinha na calçada
    for x in (-0.38, 0.4):
        L.caixa((0.06, 0.06, 0.05), (x if x < 0 else bx + 0.42, -0.4, z0), 'concreto')
        L.arbusto((x if x < 0 else bx + 0.42, -0.4, z0 + 0.05), 0.05, 'verde_escuro')


L.principal(__file__, construir)
