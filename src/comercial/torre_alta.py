"""Prédio residencial alto de condomínio com dezoito andares: sacadas em todos os andares contornando a frente e a
lateral (grade de ferro e vidro alternados), pilares terracota sobre fachada bege, térreo em pilotis com guarita,
muro com grade, piscina pequena e palmeiras, caixa d'água e casa de máquinas no topo."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402

L.PALETA['bege'] = '#e8d4b0'
L.PALETA['vidro_sacada'] = '#a9d3ee'


def palmeira(x, y, z, alt=0.4):
    L.cilindro(0.018, alt, (x, y, z), 'madeira', lados=5, r_topo=0.012)
    L.esfera(0.09, (x, y, z + alt), 'verde', escala=(1, 1, 0.45))


def construir():
    L.caixa((1.27, 1.22, 0.02), (0, 0, 0), 'piso')
    z0 = 0.02

    tw, td, tx, ty = 0.86, 0.78, -0.14, 0.19
    frente, direita, esq, fundo = ty - td / 2, tx + tw / 2, tx - tw / 2, ty + td / 2
    zp, andar, n = z0 + 0.28, 0.19, 18
    ztopo = zp + andar * n
    s = 0.08   # balanço das sacadas

    # Térreo em pilotis: hall de vidro recuado e pilares
    L.caixa((tw - 0.16, td - 0.16, 0.28), (tx, ty, z0), 'vidro_escuro')
    for x in (esq + 0.05, tx, direita - 0.05):
        L.caixa((0.06, 0.06, 0.28), (x, frente + 0.05, z0), 'terracota')
    for y in (ty, fundo - 0.05):
        L.caixa((0.06, 0.06, 0.28), (direita - 0.05, y, z0), 'terracota')

    # Corpo: miolo de vidro escuro (portas das sacadas) com pilares terracota na frente e na lateral
    L.caixa((tw, td, andar * n), (tx, ty, zp), 'vidro_escuro')
    for x in (esq + 0.04, tx, direita - 0.04):
        L.caixa((0.08, 0.02 + s, andar * n), (x, frente - s / 2 + 0.01, zp), 'terracota')
    for y in (ty + 0.02, fundo - 0.04):
        L.caixa((0.02 + s, 0.08, andar * n), (direita + s / 2 - 0.01, y, zp), 'terracota')
    # parede bege no fundo da lateral esquerda e da frente (empenas cegas)
    L.caixa((0.015, td, andar * n), (esq - 0.0075, ty, zp), 'bege')

    # Lajes das sacadas (uma laje em L por andar) e guarda-corpos alternando grade e vidro
    for i in range(n + 1):
        z = zp + i * andar - 0.025
        L.caixa((tw + s, td + s, 0.04), (tx + s / 2, ty - s / 2, z), 'bege')
        if i == n:
            break
        cor = 'grade' if i % 2 == 0 else 'vidro_sacada'
        L.caixa((tw + s, 0.01, 0.06), (tx + s / 2, frente - s + 0.005, z + 0.04), cor)
        L.caixa((0.01, td + s, 0.06), (direita + s - 0.005, ty - s / 2, z + 0.04), cor)

    # Topo: platibanda, casa de máquinas e caixa d'água de concreto
    L.caixa((tw + s + 0.02, td + s + 0.02, 0.07), (tx + s / 2, ty - s / 2, ztopo + 0.01), 'terracota')
    L.caixa((tw + s - 0.04, td + s - 0.04, 0.005), (tx + s / 2, ty - s / 2, ztopo + 0.08), 'concreto_escuro')
    tz = ztopo + 0.085
    L.caixa((0.34, 0.3, 0.16), (tx - 0.12, ty + 0.12, tz), 'bege', chanfro=0.008)
    L.caixa((0.4, 0.34, 0.14), (tx - 0.12, ty + 0.12, tz + 0.16), 'concreto', chanfro=0.008)
    L.caixa((0.42, 0.36, 0.02), (tx - 0.12, ty + 0.12, tz + 0.3), 'terracota')
    L.caixa((0.16, 0.16, 0.08), (tx + 0.2, ty - 0.15, tz), 'metal')

    # Lote: muro com grade na frente e na direita, guarita, piscina e palmeiras
    my, mx = -0.595, 0.62
    L.caixa((1.0, 0.03, 0.06), (-0.12, my, z0), 'muro')
    L.caixa((1.0, 0.01, 0.06), (-0.12, my, z0 + 0.06), 'grade')
    L.caixa((0.03, 1.16, 0.06), (mx, 0.0, z0), 'muro')
    L.caixa((0.01, 1.16, 0.06), (mx, 0.0, z0 + 0.06), 'grade')
    L.caixa((0.2, 0.01, 0.1), (0.48, my, z0), 'portao')
    gx, gy = -0.48, -0.5
    L.caixa((0.14, 0.12, 0.13), (gx, gy, z0), 'bege')
    L.caixa((0.18, 0.16, 0.02), (gx, gy, z0 + 0.13), 'terracota')
    L.placa(0.1, 0.05, (gx, gy - 0.06, z0 + 0.09), 'vidro', 'frente', espessura=0.008)
    # piscina com deck
    px, py = 0.27, -0.43
    L.caixa((0.5, 0.26, 0.025), (px, py, z0), 'madeira_clara')
    L.tanque(0.36, 0.18, 0.035, (px, py, z0), cor_agua='agua', cor='parede', parede=0.025, nivel=0.008)
    palmeira(0.53, -0.15, z0, 0.42)
    palmeira(0.53, 0.4, z0, 0.36)
    L.arbusto((0.08, -0.5, z0), 0.05, 'verde_escuro')


L.principal(__file__, construir)
