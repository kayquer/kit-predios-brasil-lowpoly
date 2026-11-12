"""Indústria de alimentos (fábrica de ração ou beneficiadora de grãos): dois silos altos de chapa galvanizada com
anéis e teto cônico, elevador de grãos com tubos de descarga, esteira inclinada coberta saindo do galpão de
recebimento (paredes brancas com faixa verde e telha de fibrocimento) e tubulação amarela ligando tudo."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402

L.PALETA['galvanizado'] = '#c3ccd3'
L.PALETA['galvanizado_anel'] = '#97a3ad'


def placa_ondulada_y(comp, rampa, pos, cor, ang, onda=0.07, amp=0.016, esp=0.014):
    """Telha ondulada com a cumeeira em Y: zigue-zague ao longo de Y, estendido em X, inclinado `ang` em Y."""
    n = max(2, round(comp / (onda / 2)))
    n += n % 2
    topo = [(-comp / 2 + comp * i / n, amp if i % 2 else 0.0) for i in range(n + 1)]
    perfil = topo + [(comp / 2, -esp), (-comp / 2, -esp)]
    return L.prisma(perfil, rampa, pos, cor, eixo='X', rot=(0, ang, 0))


def viga(p1, p2, larg, alt, cor):
    """Caixa inclinada de p1 a p2 (no plano YZ): a base passa pela linha p1-p2."""
    dy, dz = p2[1] - p1[1], p2[2] - p1[2]
    comp = math.hypot(dy, dz)
    meio = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2, (p1[2] + p2[2]) / 2)
    return L.caixa((larg, comp, alt), meio, cor, rot=(math.degrees(math.atan2(dz, dy)), 0, 0))


def silo(x, y, r, h):
    L.cilindro(r + 0.02, 0.06, (x, y, 0), 'concreto', lados=12)                   # base
    L.cilindro(r, h, (x, y, 0.06), 'galvanizado', lados=12)
    for z in (0.35, 0.7, 1.05):
        L.cilindro(r + 0.006, 0.02, (x, y, 0.06 + z), 'galvanizado_anel', lados=12)
    L.cilindro(r + 0.015, 0.025, (x, y, 0.06 + h), 'galvanizado_anel', lados=12)  # beiral
    L.cone(r + 0.015, 0.16, (x, y, 0.085 + h), 'galvanizado', lados=12)
    L.cilindro(0.03, 0.03, (x, y, 0.235 + h), 'galvanizado_anel', lados=6)        # boca de carga
    L.placa(0.08, 0.14, (x, y - r, 0.2), 'galvanizado_anel', 'frente', espessura=0.02)  # porta de inspeção


def construir():
    # Silos ao fundo, lado a lado
    sy, r, h = 0.44, 0.205, 1.3
    for sx in (-0.25, 0.25):
        silo(sx, sy, r, h)

    # Elevador de grãos entre os silos, com a cabeça e os tubos de descarga
    zt = 1.86
    L.caixa((0.07, 0.07, zt - 0.12), (0, sy + 0.04, 0), 'amarelo')
    L.caixa((0.16, 0.14, 0.12), (0, sy + 0.04, zt - 0.12), 'amarelo', chanfro=0.008)
    L.caixa((0.17, 0.15, 0.02), (0, sy + 0.04, zt), 'metal_escuro')
    for sx in (-0.25, 0.25):
        L.cano((0.0, sy + 0.04, zt - 0.08), (sx * 0.92, sy, 0.06 + h + 0.24), 0.018, 'amarelo', lados=6)

    # Galpão de recebimento na frente: branco com faixa verde, telha de fibrocimento (cumeeira em Y)
    gx0, gx1, gy0, gy1 = -0.43, 0.43, -0.66, -0.1
    gx, gy = (gx0 + gx1) / 2, (gy0 + gy1) / 2
    lx, ly = gx1 - gx0, gy1 - gy0
    hp, alt = 0.44, 0.13
    L.caixa((lx, ly, hp), (gx, gy, 0), 'parede', chanfro=0.012)
    L.caixa((lx + 0.012, ly + 0.012, 0.06), (gx, gy, 0), 'concreto_escuro')
    L.caixa((lx + 0.012, ly + 0.012, 0.05), (gx, gy, hp - 0.11), 'toldo_verde')
    for y in (gy0 + 0.01, gy1 - 0.01):
        L.prisma([(-lx / 2, 0), (lx / 2, 0), (0, alt)], 0.02, (gx, y, hp), 'parede', eixo='Y')
    meia = lx / 2 + 0.03
    ang = math.degrees(math.atan2(alt, lx / 2))
    queda = alt * 0.03 / (lx / 2)
    rampa = math.hypot(meia, alt + queda)
    for s in (-1, 1):
        placa_ondulada_y(ly + 0.05, rampa, (gx + s * meia / 2, gy, hp - queda + (alt + queda) / 2 + 0.008),
                         'fibrocimento', s * ang)
    L.caixa((0.07, ly + 0.06, 0.03), (gx, gy, hp + alt - 0.005), 'concreto_escuro')
    # portão de descarga (moega) e porta
    L.placa(0.34, 0.3, (gx - 0.12, gy0, 0.15), 'escuro', 'frente', espessura=0.02)
    L.placa(0.38, 0.04, (gx - 0.12, gy0 - 0.01, 0.32), 'toldo_verde', 'frente', espessura=0.02)
    L.caixa((0.4, 0.08, 0.012), (gx - 0.12, gy0 - 0.04, 0), 'grade')                 # grelha da moega
    L.placa(0.1, 0.22, (gx + 0.27, gy0, 0.11), 'portao', 'frente', espessura=0.02)
    L.placa(0.12, 0.08, (gx + 0.27, gy0, 0.3), 'vidro', 'frente', espessura=0.02)
    L.janelas('direita', gx1, 0.27, gy0 + 0.1, gy1 - 0.1, 2, 0.14, 0.09, cor='vidro_escuro')
    # Esteira inclinada coberta: do telhado do galpão até a cabeça do elevador
    p1 = (0.0, -0.4, hp + alt - 0.02)
    p2 = (0.0, sy - 0.04, zt - 0.1)
    viga(p1, p2, 0.1, 0.075, 'galpao')
    viga((0.0, p1[1], p1[2] - 0.012), (0.0, p2[1], p2[2] - 0.012), 0.11, 0.014, 'metal_escuro')
    for t in (0.55,):
        y = p1[1] + (p2[1] - p1[1]) * t
        z = p1[2] + (p2[2] - p1[2]) * t
        for sx in (-0.045, 0.045):
            L.caixa((0.02, 0.02, z - 0.01), (sx, y, 0), 'metal_escuro')

    # Tubulação amarela do galpão até o pé dos silos
    for sx in (-0.25, 0.25):
        L.cano((sx * 0.7, gy1, 0.3), (sx * 0.7, sy - r - 0.02, 0.3), 0.02, 'amarelo', lados=6)
        L.cano((sx * 0.7, sy - r - 0.02, 0.3), (sx * 0.7, sy - r - 0.02, 0.1), 0.02, 'amarelo', lados=6)
    L.caixa((0.04, 0.04, 0.3), (0.0, 0.0, 0), 'metal_escuro')
    L.caixa((0.42, 0.04, 0.02), (0.0, 0.0, 0.28), 'metal_escuro')


L.principal(__file__, construir)
