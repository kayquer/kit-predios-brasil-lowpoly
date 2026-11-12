"""Torre de escritórios de vidro azul de avenida de capital: térreo de vidro sob marquise branca, praça de granito
com jardineiras e palmeiras, faixas claras marcando cada andar, prumada de concreto na lateral e coroamento com
heliponto e antenas."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402

L.PALETA['vidro_torre'] = '#3f7fc4'
L.PALETA['faixa_vidro'] = '#cfe3f2'


def palmeira(x, y, z, alt=0.42):
    L.cilindro(0.018, alt, (x, y, z), 'madeira', lados=5, r_topo=0.012)
    L.esfera(0.09, (x, y, z + alt), 'verde', escala=(1, 1, 0.45))


def construir():
    L.caixa((1.34, 1.34, 0.03), (0, 0, 0), 'granito')
    z0 = 0.03

    tw, tx, ty = 0.9, -0.04, 0.12
    frente, direita = ty - tw / 2, tx + tw / 2
    zt, ztopo = z0 + 0.3, 2.5

    # Térreo: caixa de vidro recuada sob a torre
    L.caixa((tw - 0.1, tw - 0.1, 0.3), (tx, ty, z0), 'vidro_escuro')
    L.placa(0.2, 0.2, (tx, frente + 0.05, z0 + 0.1), 'escuro', 'frente', espessura=0.01)
    for (x, y) in ((tx - tw / 2 + 0.05, frente + 0.05), (direita - 0.05, frente + 0.05), (direita - 0.05, ty + tw / 2 - 0.05)):
        L.caixa((0.06, 0.06, 0.3), (x, y, z0), 'parede')
    # marquise branca em balanço
    L.caixa((0.86, 0.3, 0.04), (tx, frente - 0.1, z0 + 0.25), 'parede', chanfro=0.01)
    for dx in (-0.35, 0.35):
        L.cano((tx + dx, frente - 0.21, z0), (tx + dx, frente - 0.21, z0 + 0.25), 0.012, 'metal', lados=4)

    # Torre de vidro com faixas claras em cada andar
    L.caixa((tw, tw, ztopo - zt), (tx, ty, zt), 'vidro_torre', chanfro=0.02)
    andares = 13
    h = (ztopo - zt) / andares
    for i in range(andares + 1):
        L.caixa((tw + 0.012, tw + 0.012, 0.025), (tx, ty, zt + i * h - 0.0125), 'faixa_vidro')
    # montantes verticais (frente e lado direito)
    for k in (-1, 0, 1):
        L.caixa((0.02, 0.012, ztopo - zt), (tx + k * 0.22, frente - 0.006, zt), 'faixa_vidro')
        L.caixa((0.012, 0.02, ztopo - zt), (direita + 0.006, ty + k * 0.22, zt), 'faixa_vidro')
    # prumada de concreto na lateral direita, subindo acima do topo
    L.caixa((0.08, 0.24, ztopo - zt + 0.32), (direita + 0.04, ty + 0.3, zt - 0.3), 'parede', chanfro=0.008)

    # Coroamento: laje, casa de máquinas e heliponto
    L.caixa((tw + 0.04, tw + 0.04, 0.06), (tx, ty, ztopo), 'parede', chanfro=0.01)
    L.caixa((0.42, 0.3, 0.14), (tx - 0.18, ty + 0.22, ztopo + 0.06), 'concreto', chanfro=0.008)
    hz = ztopo + 0.06
    L.cilindro(0.3, 0.03, (tx + 0.12, ty - 0.12, hz), 'escuro', lados=12)
    L.anel(0.27, 0.24, 0.035, (tx + 0.12, ty - 0.12, hz), 'amarelo', lados=12)
    # centro do heliponto: círculo branco (sem letra)
    L.cilindro(0.08, 0.04, (tx + 0.12, ty - 0.12, hz), 'parede', lados=10)
    # antenas com ponta vermelha
    for (x, y, a) in ((tx - 0.3, ty + 0.3, 0.32), (tx - 0.12, ty + 0.3, 0.22)):
        L.cano((x, y, hz + 0.14), (x, y, hz + 0.14 + a), 0.008, 'metal_escuro', lados=4)
        L.caixa((0.025, 0.025, 0.025), (x, y, hz + 0.14 + a), 'vermelho')

    # Praça: jardineiras com arbustos e palmeiras
    for (x, y, lx, ly) in ((-0.5, -0.5, 0.26, 0.26), (0.52, -0.5, 0.24, 0.26), (0.55, 0.3, 0.18, 0.6)):
        L.caixa((lx, ly, 0.06), (x, y, z0), 'concreto')
        L.caixa((lx - 0.03, ly - 0.03, 0.005), (x, y, z0 + 0.06), 'grama')
    palmeira(-0.5, -0.5, z0 + 0.06)
    palmeira(0.52, -0.5, z0 + 0.06, 0.36)
    L.arbusto((0.55, 0.15, z0 + 0.065), 0.07, 'verde_escuro')
    L.arbusto((0.55, 0.45, z0 + 0.065), 0.07, 'verde')
    L.arbusto((-0.42, -0.58, z0 + 0.065), 0.05, 'flor_rosa')


L.principal(__file__, construir)
