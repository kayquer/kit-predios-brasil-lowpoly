"""Prédio de polo tecnológico: bloco de três andares de concreto branco com fitas de vidro, torre da escada em verde-água,
entrada envidraçada com marquise, painéis solares e torre de antena com parabólicas na cobertura e, atrás, um anexo
baixo de servidores com condensadoras de ar-condicionado no teto."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402

L.PALETA['concreto_claro'] = '#e9e6df'
L.PALETA['turquesa_fachada'] = '#3fb3a6'


def construir():
    x0, x1 = -0.41, 0.41
    y0, y1 = -0.62, 0.12
    bx, by = (x0 + x1) / 2, (y0 + y1) / 2
    lx, ly = x1 - x0, y1 - y0
    andar, n = 0.29, 3
    ht = andar * n + 0.04

    # Bloco principal: lajes de concreto e fitas de vidro (frente e lateral direita)
    L.caixa((lx - 0.04, ly - 0.04, ht), (bx, by, 0), 'vidro_escuro')
    for i in range(n):
        L.caixa((lx, ly, 0.04), (bx, by, i * andar), 'concreto_claro', chanfro=0.006)
    for i in range(n):
        z = i * andar + 0.04
        # pilares/caixilhos verticais na frente e na direita
        for k in range(1, 6):
            L.placa(0.018, andar - 0.04, (x0 + lx * k / 6, y0 + 0.02, z + (andar - 0.04) / 2), 'concreto_claro',
                    'frente', espessura=0.012)
        for k in range(1, 5):
            L.placa(0.018, andar - 0.04, (x1 - 0.02, y0 + ly * k / 5, z + (andar - 0.04) / 2), 'concreto_claro',
                    'direita', espessura=0.012)
    # platibanda
    L.caixa((lx, ly, 0.1), (bx, by, n * andar), 'concreto_claro', chanfro=0.006)
    L.caixa((lx - 0.06, ly - 0.06, 0.006), (bx, by, n * andar + 0.1), 'concreto')
    # torre da escada colorida no canto da frente à esquerda
    L.caixa((0.16, 0.16, ht + 0.12), (x0 + 0.07, y0 + 0.07, 0), 'turquesa_fachada', chanfro=0.008)
    L.placa(0.04, ht - 0.12, (x0 + 0.07, y0 - 0.01, ht / 2), 'vidro', 'frente', espessura=0.012)
    # entrada envidraçada e marquise
    L.placa(0.26, 0.2, (0.08, y0 + 0.02, 0.1), 'vidro', 'frente', espessura=0.02)
    L.caixa((0.36, 0.1, 0.02), (0.08, y0 - 0.03, 0.24), 'concreto_claro')
    for sx in (-0.15, 0.15):
        L.caixa((0.015, 0.015, 0.24), (0.08 + sx, y0 - 0.065, 0), 'metal_escuro')
    # brises verdes na lateral direita
    for k in range(4):
        y = y0 + 0.1 + k * 0.18
        L.caixa((0.04, 0.018, ht - 0.1), (x1 + 0.02, y, 0.06), 'turquesa_fachada')

    # Cobertura: painéis solares inclinados para a frente e torre de antena
    zt = n * andar + 0.106
    for i in range(3):
        for j in range(2):
            x = -0.2 + i * 0.2 - 0.01
            y = y0 + 0.18 + j * 0.24
            L.caixa((0.17, 0.18, 0.012), (x, y, zt + 0.05), 'painel_solar', rot=(-18, 0, 0))
            L.caixa((0.15, 0.02, 0.05), (x, y + 0.06, zt), 'metal_escuro')
    mx, my = 0.27, y1 - 0.14
    L.caixa((0.08, 0.08, 0.04), (mx, my, zt), 'concreto')
    L.cano((mx, my, zt + 0.04), (mx, my, 1.36), 0.012, 'metal_escuro', lados=4)
    for sx in (-1, 1):
        L.cano((mx + sx * 0.035, my, zt + 0.04), (mx, my, 1.15), 0.006, 'metal_escuro', lados=4)
    L.cilindro(0.055, 0.02, (mx, my - 0.025, 1.05), 'parede', lados=8, r_topo=0.035, rot=(90, 0, 0))
    L.cilindro(0.04, 0.02, (mx + 0.02, my - 0.02, 1.2), 'parede', lados=8, r_topo=0.025, rot=(90, 0, -30))
    L.cilindro(0.014, 0.03, (mx, my, 1.36), 'vermelho', lados=6)

    # Anexo baixo de servidores atrás, com condensadoras no teto
    ay0, ay1 = y1, 0.68
    ax0, ax1 = -0.4, 0.36
    ax, ay = (ax0 + ax1) / 2, (ay0 + ay1) / 2
    alx, aly, ah = ax1 - ax0, ay1 - ay0, 0.34
    L.caixa((alx, aly, ah), (ax, ay, 0), 'galpao', chanfro=0.01)
    L.caixa((alx + 0.012, aly + 0.012, 0.05), (ax, ay, ah - 0.09), 'turquesa_fachada')
    L.caixa((alx + 0.012, aly + 0.012, 0.05), (ax, ay, 0), 'concreto_escuro')
    L.caixa((alx - 0.05, aly - 0.05, 0.012), (ax, ay, ah), 'concreto')
    for k in range(3):
        L.placa(0.12, 0.08, (ax1, ay0 + 0.12 + k * 0.18, 0.15), 'grade', 'direita', espessura=0.02)  # venezianas
    for i, (x, y) in enumerate(((-0.25, 0.3), (-0.05, 0.3), (-0.25, 0.5), (-0.05, 0.5), (0.18, 0.5))):
        L.caixa((0.15, 0.13, 0.07), (x, y, ah + 0.012), 'parede')
        L.cilindro(0.045, 0.006, (x, y, ah + 0.082), 'escuro', lados=8)
    L.caixa((0.1, 0.04, 0.12), (0.2, ay1 - 0.04, ah), 'metal_escuro')               # duto


L.principal(__file__, construir)
