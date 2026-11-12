"""Galpão pequeno de telhado em arco (telha metálica curva com emendas), paredes creme, portão de aço de enrolar
na frente e escritório colado na fachada, pintado de amarelo com faixa laranja e platibanda."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402


def pontos_arco(meia, alt, n):
    """Arco de círculo (abatido) de x = +meia a -meia passando por (0, alt)."""
    r = (meia * meia + alt * alt) / (2 * alt)
    zc = alt - r
    a0 = math.asin(meia / r)
    return [(r * math.sin(a0 - 2 * a0 * k / n), zc + r * math.cos(a0 - 2 * a0 * k / n)) for k in range(n + 1)]


def casca(meia, alt, esp, comp, pos, cor, n=8):
    """Casca em arco com o perfil em (x, z), estendida ao longo de Y."""
    fora = pontos_arco(meia, alt, n)
    dentro = [(x * (meia - esp) / meia, z - esp) for (x, z) in reversed(fora)]
    return L.prisma(fora + dentro, comp, pos, cor, eixo='Y')


def construir():
    lx = 0.86
    y0, y1 = -0.32, 0.6                 # galpão em Y
    hp = 0.42
    gy, comp = (y0 + y1) / 2, y1 - y0
    meia, alt = 0.49, 0.28

    # Galpão: paredes creme com rodapé cinza
    L.caixa((lx, comp, hp), (0, gy, 0), 'creme', chanfro=0.012)
    L.caixa((lx + 0.012, comp + 0.012, 0.07), (0, gy, 0), 'concreto_escuro')
    # oitão da frente e do fundo (meia-lua)
    for y in (y0 + 0.012, y1 - 0.012):
        L.prisma(pontos_arco(lx / 2, alt - 0.02, 8), 0.02, (0, y, hp), 'creme', eixo='Y')
    # telhado em arco (telha metálica) com emendas mais escuras
    casca(meia, alt, 0.025, comp + 0.08, (0, gy, hp - 0.01), 'metal')
    for k in range(4):
        y = y0 + 0.04 + (comp - 0.08) * (k + 0.5) / 4
        casca(meia + 0.006, alt + 0.006, 0.02, 0.025, (0, y, hp - 0.01), 'metal_escuro')
    # rufo/calha nas bordas do arco
    for sx in (-1, 1):
        L.caixa((0.05, comp + 0.08, 0.035), (sx * (meia - 0.012), gy, hp - 0.025), 'metal_escuro')

    # Portão de aço de enrolar na frente (à direita do escritório)
    px = 0.2
    L.placa(0.36, 0.33, (px, y0, 0.165), 'ferro_enrolar', 'frente', espessura=0.02)
    L.placa(0.4, 0.045, (px, y0 - 0.012, 0.35), 'grade', 'frente', espessura=0.016)
    for z in (0.08, 0.16, 0.24):
        L.placa(0.36, 0.01, (px, y0 - 0.012, z), 'metal_escuro', 'frente', espessura=0.006)
    # janela redonda-de-ventilação no oitão (veneziana)
    L.placa(0.2, 0.06, (0, y0 + 0.0, hp + 0.1), 'metal_escuro', 'frente', espessura=0.03)

    # Escritório colado na frente: caixa pintada com platibanda e faixa (sem letreiro)
    ex0, ex1 = -0.46, -0.04
    ey0, ey1 = -0.62, y0
    ex, ey = (ex0 + ex1) / 2, (ey0 + ey1) / 2
    lex, ley = ex1 - ex0, ey1 - ey0
    L.caixa((lex, ley, 0.36), (ex, ey, 0), 'amarelo_pastel', chanfro=0.012)
    L.caixa((lex + 0.014, ley + 0.014, 0.06), (ex, ey, 0.3), 'laranja')        # faixa da firma
    L.caixa((lex + 0.02, ley + 0.02, 0.025), (ex, ey, 0.36), 'concreto')         # pingadeira
    L.caixa((lex - 0.04, ley - 0.04, 0.012), (ex, ey, 0.36), 'concreto_escuro')
    L.placa(0.1, 0.22, (ex - 0.1, ey0, 0.11), 'portao', 'frente', espessura=0.02)       # porta
    L.placa(0.16, 0.11, (ex + 0.07, ey0, 0.17), 'vidro', 'frente', espessura=0.02)      # janela
    for i in range(4):
        L.placa(0.008, 0.11, (ex + 0.025 + i * 0.03, ey0 - 0.012, 0.17), 'grade', 'frente', espessura=0.008)
    L.placa(0.14, 0.1, (ex1, ey, 0.17), 'vidro', 'direita', espessura=0.02)
    # ar-condicionado
    L.caixa((0.04, 0.1, 0.07), (ex1 + 0.02, ey, 0.04), 'parede')

    # Lateral direita do galpão: janelas altas e tubo de descida
    L.janelas('direita', lx / 2, 0.29, y0 + 0.08, y1 - 0.08, 3, 0.18, 0.08, cor='vidro_escuro')
    L.caixa((0.025, 0.025, hp), (lx / 2 + 0.013, y0 + 0.02, 0), 'concreto_escuro')
    # Pátio: pallet com caixas
    L.caixa((0.16, 0.12, 0.025), (0.36, -0.55, 0), 'madeira')
    L.caixa((0.13, 0.1, 0.08), (0.36, -0.55, 0.025), 'madeira_clara')


L.principal(__file__, construir)
