"""Fábrica de tijolinho aparente com telhado shed (dente de serra) de fibrocimento e vidraças viradas para a frente,
chaminé alta de tijolo com anéis, bloco administrativo de dois andares pintado de creme na frente e portão de carga
com um caminhão baú encostado."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402

L.PALETA['tijolinho'] = '#b45a3c'
L.PALETA['tijolinho_escuro'] = '#8f4630'
L.PALETA['caminhao'] = '#2e6fb8'


def placa_ondulada(comp, rampa, pos, cor, ang, onda=0.14, amp=0.018, esp=0.012):
    """Telha ondulada: zigue-zague ao longo de X, estendido na rampa (Y) e inclinado `ang` graus em X."""
    n = max(2, round(comp / (onda / 2)))
    n += n % 2
    topo = [(-comp / 2 + comp * i / n, amp if i % 2 else 0.0) for i in range(n + 1)]
    perfil = topo + [(comp / 2, -esp), (-comp / 2, -esp)]
    return L.prisma(perfil, rampa, pos, cor, eixo='Y', rot=(ang, 0, 0))


def caminhao(x, y):
    """Caminhão baú de ré no portão: traseira para +Y, cabine para -Y."""
    for dy in (-0.17, 0.1):
        for dx in (-0.08, 0.08):
            L.cilindro(0.045, 0.035, (x + dx + (-0.0175 if dx > 0 else 0.0175), y + dy, 0.045), 'escuro', lados=6,
                       rot=(0, 90 if dx > 0 else -90, 0))
    L.caixa((0.16, 0.48, 0.05), (x, y, 0.04), 'escuro')
    L.caixa((0.2, 0.32, 0.25), (x, y + 0.07, 0.07), 'parede', chanfro=0.008)           # baú
    L.caixa((0.205, 0.325, 0.03), (x, y + 0.07, 0.14), 'caminhao')                    # faixa do baú
    L.caixa((0.19, 0.13, 0.17), (x, y - 0.16, 0.07), 'caminhao', chanfro=0.01)        # cabine
    L.placa(0.15, 0.06, (x, y - 0.225, 0.2), 'vidro_escuro', 'frente', espessura=0.01)
    L.caixa((0.17, 0.02, 0.03), (x, y - 0.232, 0.08), 'metal')                        # para-choque


def construir():
    x0, x1 = -0.82, 0.5
    y0, y1 = -0.12, 0.6
    gx, gy = (x0 + x1) / 2, (y0 + y1) / 2
    lx, ly = x1 - x0, y1 - y0
    hp = 0.5

    # Galpão de tijolinho com cimalha branca e embasamento escuro
    L.caixa((lx, ly, hp), (gx, gy, 0), 'tijolinho', chanfro=0.012)
    L.caixa((lx + 0.012, ly + 0.012, 0.06), (gx, gy, 0), 'tijolinho_escuro')
    L.caixa((lx + 0.03, ly + 0.03, 0.035), (gx, gy, hp - 0.035), 'parede')

    # Telhado shed: 3 dentes com a vidraça vertical virada para a frente (-Y)
    n, ht = 3, 0.17
    passo = ly / n
    ang = math.degrees(math.atan2(ht, passo))
    rampa = math.hypot(passo, ht) + 0.02
    for i in range(n):
        ya, yb = y0 + i * passo, y0 + (i + 1) * passo
        L.prisma([(ya, 0), (ya, ht), (yb, 0)], lx - 0.02, (gx, 0, hp), 'parede', eixo='X')
        L.placa(lx - 0.06, ht - 0.04, (gx, ya, hp + ht / 2 - 0.005), 'vidro', 'frente', espessura=0.012)
        for k in range(1, 4):
            L.placa(0.015, ht - 0.04, (x0 + lx * k / 4, ya - 0.008, hp + ht / 2 - 0.005), 'parede', 'frente',
                    espessura=0.008)
        placa_ondulada(lx + 0.02, rampa, (gx, (ya + yb) / 2, hp + ht / 2 + 0.01), 'fibrocimento', -ang)

    # Janelas da fábrica (frente à direita do bloco administrativo e lateral direita)
    L.janelas('direita', x1, 0.3, y0 + 0.08, y1 - 0.08, 3, 0.14, 0.2, cor='vidro_escuro')
    # Portão de carga na frente
    gxp = 0.22
    L.placa(0.3, 0.36, (gxp, y0, 0.18), 'ferro_enrolar', 'frente', espessura=0.02)
    L.placa(0.36, 0.05, (gxp, y0 - 0.005, 0.39), 'parede', 'frente', espessura=0.03)
    L.placa(0.3, 0.01, (gxp, y0 - 0.012, 0.12), 'metal_escuro', 'frente', espessura=0.006)
    L.placa(0.3, 0.01, (gxp, y0 - 0.012, 0.24), 'metal_escuro', 'frente', espessura=0.006)
    caminhao(gxp, -0.37)

    # Bloco administrativo de dois andares, pintado, com platibanda
    ax0, ax1, ay0, ay1 = -0.82, -0.2, -0.6, -0.12
    ax, ay = (ax0 + ax1) / 2, (ay0 + ay1) / 2
    alx, aly, ah = ax1 - ax0, ay1 - ay0, 0.6
    L.caixa((alx, aly, ah), (ax, ay, 0), 'creme', chanfro=0.012)
    L.caixa((alx + 0.012, aly + 0.012, 0.05), (ax, ay, 0), 'concreto_escuro')
    L.caixa((alx + 0.02, aly + 0.02, 0.03), (ax, ay, ah), 'parede')
    L.caixa((alx - 0.04, aly - 0.04, 0.012), (ax, ay, ah + 0.03), 'concreto')
    L.caixa((alx + 0.014, aly + 0.014, 0.025), (ax, ay, 0.3), 'tijolinho')          # faixa entre andares
    for zc in (0.19, 0.45):
        L.janelas('frente', ay0, zc, ax0 + 0.04, ax1 - 0.04, 4, 0.1, 0.13, cor='vidro')
        L.janelas('direita', ax1, zc, ay0 + 0.06, ay1 - 0.06, 2, 0.1, 0.13, cor='vidro')
    L.caixa((0.16, 0.05, 0.015), (ax - 0.02, ay0 - 0.025, 0.27), 'concreto')           # marquise da entrada
    L.placa(0.09, 0.2, (ax - 0.02, ay0 - 0.006, 0.1), 'portao', 'frente', espessura=0.02)
    # caixa d'água azul em cima do bloco
    L.cilindro(0.07, 0.11, (ax0 + 0.12, ay1 - 0.12, ah + 0.03), 'fibra_azul', lados=10, r_topo=0.08)

    # Chaminé de tijolo alta no canto de trás à direita
    cx, cy = 0.68, 0.42
    L.caixa((0.22, 0.22, 0.24), (cx, cy, 0), 'tijolinho_escuro', chanfro=0.01)
    L.caixa((0.25, 0.25, 0.03), (cx, cy, 0.24), 'parede')
    L.cilindro(0.085, 1.34, (cx, cy, 0.27), 'tijolinho', lados=8, r_topo=0.06)
    for z, r in ((0.75, 0.08), (1.15, 0.071)):
        L.cilindro(r + 0.006, 0.03, (cx, cy, z), 'parede', lados=8)
    L.cilindro(0.072, 0.05, (cx, cy, 1.58), 'tijolinho_escuro', lados=8)
    L.cilindro(0.045, 0.012, (cx, cy, 1.625), 'escuro', lados=8)
    # tubo da caldeira até a chaminé
    L.cano((x1, 0.42, 0.32), (cx - 0.11, 0.42, 0.32), 0.03, 'metal_escuro', lados=6)
    # Pátio: tambores e pallets ao lado do galpão
    L.cilindro(0.045, 0.12, (0.62, -0.05, 0), 'vermelho', lados=8)
    L.cilindro(0.045, 0.12, (0.72, -0.08, 0), 'fibra_azul', lados=8)
    L.caixa((0.16, 0.14, 0.03), (0.7, 0.12, 0), 'madeira')
    L.caixa((0.15, 0.13, 0.03), (0.7, 0.12, 0.03), 'madeira')


L.principal(__file__, construir)
