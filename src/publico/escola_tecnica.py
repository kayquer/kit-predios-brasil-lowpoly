"""Escola técnica no estilo ETEC/Instituto Federal: prédio de dois andares de tijolo aparente com faixas azuis e
caixa d'água no terraço, oficina anexa com telhado shed envidraçado e bicicletário na frente."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402

L.PALETA['azul_faixa'] = '#2a63b0'


def bicicleta(x, y, cor, z0):
    """Bicicleta estacionada apontando para -Y (rodas no plano YZ)."""
    r, zc = 0.034, z0 + 0.034
    for yy in (y + 0.045, y - 0.045):
        L.cilindro(r, 0.008, (x - 0.004, yy, zc), 'escuro', lados=8, rot=(0, 90, 0))
    L.cano((x, y + 0.045, zc), (x, y - 0.01, zc + 0.045), 0.005, cor, lados=3)
    L.cano((x, y - 0.01, zc + 0.045), (x, y - 0.045, zc), 0.005, cor, lados=3)
    L.cano((x - 0.02, y - 0.035, zc + 0.055), (x + 0.02, y - 0.035, zc + 0.055), 0.004, 'grade', lados=3)


def construir():
    z0 = 0.02
    L.caixa((1.40, 1.08, z0), (0, 0, 0), 'piso')
    L.caixa((0.30, 0.22, 0.008), (-0.54, -0.41, z0), 'grama')

    # Prédio principal: dois andares de tijolo aparente com faixas azuis
    cx, cy, w, d = -0.29, 0.15, 0.82, 0.70
    frente, direita = cy - d / 2, cx + w / 2
    L.caixa((w, d, 0.60), (cx, cy, z0), 'tijolo', chanfro=0.01)
    L.caixa((w + 0.014, d + 0.014, 0.04), (cx, cy, z0 + 0.29), 'azul_faixa')            # laje entre andares
    L.caixa((w - 0.02, d - 0.02, 0.03), (cx, cy, z0 + 0.59), 'concreto_escuro')           # laje do terraço
    e = 0.035                                                                            # platibanda azul
    for (px, py, sx, sy) in ((cx, frente + e / 2 - 0.01, w + 0.02, e), (cx, cy + d / 2 - e / 2 + 0.01, w + 0.02, e),
                             (cx - w / 2 + e / 2 - 0.01, cy, e, d), (direita - e / 2 + 0.01, cy, e, d)):
        L.caixa((sx, sy, 0.07), (px, py, z0 + 0.59), 'azul_faixa')
    L.caixa((w + 0.012, d + 0.012, 0.03), (cx, cy, z0), 'concreto')                     # rodapé
    for x in (cx - w / 2 + 0.01, cx + w / 2 - 0.01):                                    # pilares de canto
        L.caixa((0.04, 0.04, 0.59), (x, frente + 0.01, z0), 'concreto')
    L.caixa((0.04, 0.04, 0.59), (direita - 0.01, cy + d / 2 - 0.01, z0), 'concreto')
    # Janelas em fita (vidro direto no tijolo)
    for zc in (z0 + 0.17, z0 + 0.46):
        if zc > 0.3:
            L.janelas('frente', frente, zc, cx - w / 2 + 0.05, cx + w / 2 - 0.05, 5, 0.12, 0.12, 'vidro')
        else:
            L.janelas('frente', frente, zc, cx - w / 2 + 0.05, cx - 0.10, 2, 0.12, 0.12, 'vidro')
            L.janelas('frente', frente, zc, cx + 0.10, cx + w / 2 - 0.05, 2, 0.12, 0.12, 'vidro')
    L.janelas('direita', direita, z0 + 0.46, cy - d / 2 + 0.06, cy + d / 2 - 0.06, 4, 0.12, 0.12, 'vidro')
    # Entrada: porta de vidro, marquise de concreto com testeira azul e degrau
    L.placa(0.13, 0.19, (cx, frente, z0 + 0.20), 'vidro_escuro', 'frente')
    L.caixa((0.28, 0.14, 0.022), (cx, frente - 0.07, z0 + 0.22), 'concreto')
    L.caixa((0.29, 0.012, 0.035), (cx, frente - 0.142, z0 + 0.215), 'azul_faixa')
    L.caixa((0.20, 0.06, 0.015), (cx, frente - 0.03, z0), 'concreto')
    # Terraço: torre da caixa d'água com duas caixas de fibra azul
    tx, ty = cx - 0.22, cy + 0.14
    L.caixa((0.24, 0.24, 0.19), (tx, ty, z0 + 0.60), 'concreto', chanfro=0.01)
    L.caixa((0.25, 0.25, 0.025), (tx, ty, z0 + 0.79), 'azul_faixa')
    for dx in (-0.055, 0.055):
        L.cilindro(0.05, 0.06, (tx + dx, ty, z0 + 0.815), 'fibra_azul', lados=8)
        L.cilindro(0.054, 0.015, (tx + dx, ty, z0 + 0.875), 'fibra_azul', lados=8, r_topo=0.02)

    # Oficina/laboratório anexo com telhado shed (dentes com vidro virado para a frente)
    ox, oy, ow, od, oh = 0.42, 0.10, 0.52, 0.80, 0.26
    L.caixa((ow, od, oh), (ox, oy, z0), 'galpao', chanfro=0.01)
    L.caixa((ow + 0.012, od + 0.012, 0.07), (ox, oy, z0), 'tijolo')
    L.caixa((ow + 0.012, od + 0.012, 0.025), (ox, oy, z0 + oh - 0.035), 'azul_faixa')
    L.placa(0.22, 0.18, (ox + 0.10, oy - od / 2, z0 + 0.18), 'ferro_enrolar', 'frente')     # portão de enrolar
    L.janelas('direita', ox + ow / 2, z0 + 0.17, oy - od / 2 + 0.08, oy + od / 2 - 0.08, 3, 0.16, 0.06, 'vidro')
    y0, y1, n, H, v = oy - od / 2 - 0.015, oy + od / 2 + 0.015, 3, 0.12, 0.015
    p = (y1 - y0) / n
    perfil = [(y0, 0)]
    for i in range(n):
        perfil += [(y0 + i * p, H), (y0 + (i + 1) * p, v)]
    perfil += [(y1, 0)]
    zt = z0 + oh
    L.prisma([(yy, zt + zz) for (yy, zz) in perfil], ow + 0.03, (ox, 0, 0), 'fibrocimento', eixo='X')
    for i in range(1, n):
        L.placa(ow - 0.04, H - v - 0.02, (ox, y0 + i * p - 0.002, zt + H - 0.01), 'vidro', 'frente', espessura=0.01)
    L.placa(ow - 0.04, H - 0.03, (ox, y0 - 0.002, zt + H - 0.01), 'vidro', 'frente', espessura=0.01)

    # Bicicletário na frente da oficina
    L.caixa((0.30, 0.012, 0.04), (0.26, -0.39, z0), 'grade')
    for x, cor in ((0.15, 'vermelho'), (0.23, 'amarelo'), (0.31, 'azul_faixa'), (0.38, 'verde')):
        bicicleta(x, -0.42, cor, z0)

    L.arvore((-0.58, -0.42, z0), 0.42, 'verde')
    L.arbusto((-0.45, -0.45, z0), 0.05, 'verde_escuro')


L.principal(__file__, construir)
