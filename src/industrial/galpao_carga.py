"""Galpão de distribuição (centro de distribuição): caixa de chapa metálica cinza-clara com faixa laranja, platibanda
na frente com o escritório envidraçado, telha metálica trapezoidal de duas águas e, na lateral, três docas de carga
com portas altas, vedação preta, marquise e plataforma de concreto com faixa amarela de segurança."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402

L.PALETA['chapa'] = '#dcdad4'
L.PALETA['chapa_sombra'] = '#c4c2bc'
L.PALETA['telha_metal'] = '#a7b0b8'


def placa_trapezoidal_y(comp, rampa, pos, cor, ang, onda=0.09, amp=0.016, esp=0.014):
    """Telha trapezoidal com a cumeeira em Y: nervuras ao longo de Y, estendida em X, inclinada `ang` em Y."""
    n = max(1, round(comp / onda))
    topo = []
    for i in range(n):
        a = -comp / 2 + comp * i / n
        p = comp / n
        topo += [(a, 0.0), (a + p * 0.55, 0.0), (a + p * 0.68, amp), (a + p * 0.87, amp)]
    topo.append((comp / 2, 0.0))
    perfil = topo + [(comp / 2, -esp), (-comp / 2, -esp)]
    return L.prisma(perfil, rampa, pos, cor, eixo='X', rot=(0, ang, 0))


def construir():
    x0, x1 = -0.39, 0.27
    y0, y1 = -0.55, 0.58
    gx, gy = (x0 + x1) / 2, (y0 + y1) / 2
    lx, ly = x1 - x0, y1 - y0
    hp, alt = 0.68, 0.09

    # Corpo de chapa com faixa laranja e rodapé de concreto
    L.caixa((lx, ly, hp), (gx, gy, 0), 'chapa', chanfro=0.012)
    L.caixa((lx + 0.01, ly + 0.01, 0.09), (gx, gy, 0), 'concreto_escuro')
    L.caixa((lx + 0.012, ly + 0.012, 0.05), (gx, gy, hp - 0.12), 'laranja')
    # nervuras verticais da chapa na lateral direita (entre as docas)
    for y in (-0.44, 0.44):
        L.placa(0.015, hp - 0.2, (x1, y, 0.09 + (hp - 0.2) / 2 + 0.01), 'chapa_sombra', 'direita', espessura=0.01)
    # oitão do fundo e telhado trapezoidal de duas águas (cumeeira em Y)
    L.prisma([(-lx / 2, 0), (lx / 2, 0), (0, alt)], 0.02, (gx, y1 - 0.01, hp), 'chapa', eixo='Y')
    meia = lx / 2 + 0.03
    ang = math.degrees(math.atan2(alt, lx / 2))
    queda = alt * 0.03 / (lx / 2)
    rampa = math.hypot(meia, alt + queda)
    for s in (-1, 1):
        placa_trapezoidal_y(ly + 0.02, rampa, (gx + s * meia / 2, gy + 0.01, hp - queda + (alt + queda) / 2 + 0.008),
                            'telha_metal', s * ang)
    L.caixa((0.08, ly + 0.03, 0.035), (gx, gy + 0.01, hp + alt - 0.004), 'metal_escuro')

    # Frente: platibanda alta com o escritório envidraçado e porta
    L.caixa((lx + 0.02, 0.05, 0.2), (gx, y0 - 0.02, hp - 0.02), 'chapa', chanfro=0.008)
    L.caixa((lx + 0.028, 0.058, 0.05), (gx, y0 - 0.02, hp + 0.05), 'laranja')
    L.placa(lx - 0.16, 0.13, (gx - 0.04, y0, 0.42), 'vidro_escuro', 'frente', espessura=0.02)   # fita de vidro
    for i in range(5):
        L.placa(0.012, 0.13, (gx - 0.04 - (lx - 0.16) / 2 + (lx - 0.16) * i / 4, y0 - 0.012, 0.42), 'chapa',
                'frente', espessura=0.01)
    L.placa(0.12, 0.25, (x1 - 0.1, y0, 0.125), 'vidro', 'frente', espessura=0.02)                     # entrada
    L.caixa((0.18, 0.08, 0.02), (x1 - 0.1, y0 - 0.04, 0.27), 'laranja')                               # marquise
    L.placa(0.2, 0.1, (gx - 0.08, y0, 0.2), 'vidro', 'frente', espessura=0.02)                       # janela
    L.caixa((0.1, 0.08, 0.04), (x0 + 0.08, y0 - 0.04, 0.0), 'concreto')                              # degrau/canteiro
    L.arbusto((x0 + 0.08, y0 - 0.04, 0.04), 0.05, 'verde')

    # Lateral direita: plataforma das docas com faixa amarela, 3 portas altas, vedação e marquise
    px0, px1 = x1, 0.41
    zp = 0.12
    L.caixa((px1 - px0, 0.98, zp), ((px0 + px1) / 2, 0.0, 0), 'concreto', chanfro=0.008)
    L.caixa((0.012, 0.984, 0.03), (px1 - 0.004, 0.0, zp - 0.03), 'amarelo')            # faixa de segurança
    L.caixa((px1 - px0 + 0.004, 0.984, 0.006), ((px0 + px1) / 2, 0.0, zp), 'amarelo')
    for y in (-0.3, 0.0, 0.3):
        L.placa(0.22, 0.4, (x1, y, zp + 0.2), 'escuro', 'direita', espessura=0.012)              # vedação
        L.placa(0.18, 0.36, (x1 + 0.008, y, zp + 0.18), 'ferro_enrolar', 'direita', espessura=0.012)
        for z in (zp + 0.09, zp + 0.18, zp + 0.27):
            L.placa(0.18, 0.008, (x1 + 0.015, y, z), 'metal_escuro', 'direita', espessura=0.004)
        L.caixa((0.035, 0.05, 0.05), (px1 + 0.012, y - 0.075, zp - 0.07), 'escuro')            # para-choque
        L.caixa((0.035, 0.05, 0.05), (px1 + 0.012, y + 0.075, zp - 0.07), 'escuro')
    L.caixa((0.13, 0.98, 0.02), (x1 + 0.065, 0.0, zp + 0.43), 'metal_escuro')                    # marquise
    # escadinha da plataforma
    L.caixa((0.08, 0.1, 0.04), (0.35, -0.54, 0), 'concreto')
    L.caixa((0.08, 0.1, 0.04), (0.35, -0.53, 0.04), 'concreto')


L.principal(__file__, construir)
