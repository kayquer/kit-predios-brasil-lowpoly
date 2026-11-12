"""Porto de rio: cais de concreto com defensas de pneu e cabeços, armazém azul, guindaste de pórtico amarelo
içando um contêiner, pilhas de contêineres coloridos e barcaça com empurrador encostada (a água fica na frente)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402

L.PALETA['casco'] = '#8a3a2c'
L.PALETA['cont_laranja'] = '#e8742c'
L.PALETA['cont_azul'] = '#2f62a8'
L.PALETA['cont_verde'] = '#3d8a4a'
L.PALETA['cont_vermelho'] = '#b8362e'
L.PALETA['cont_branco'] = '#e9e6de'
CORES = ['cont_laranja', 'cont_azul', 'cont_verde', 'cont_vermelho', 'cont_branco']


def conteiner(x, y, z, cor, comp=0.30, larg=0.12, alt=0.115, nervura=False):
    """Contêiner deitado ao longo de X (com nervura escura no meio só nos que aparecem de perto)."""
    L.caixa((comp, larg, alt), (x, y, z), cor)
    if nervura:
        L.caixa((0.012, larg + 0.006, alt - 0.02), (x, y, z + 0.01), 'escuro')


def construir():
    zc = 0.12                                   # topo do cais
    # Água na frente e cais de concreto
    L.caixa((2.10, 0.42, 0.03), (0, -0.49, 0), 'agua_funda')
    L.caixa((2.10, 1.00, zc), (0, 0.20, 0), 'concreto', chanfro=0.01)
    L.caixa((2.11, 0.012, 0.04), (0, -0.30, 0.02), 'concreto_escuro')       # marca d'água no paredão
    L.caixa((2.10, 0.02, 0.003), (0, -0.27, zc), 'amarelo')                  # faixa de segurança
    for x in range(6):
        L.caixa((0.06, 0.03, 0.06), (-0.90 + x * 0.36, -0.315, 0.04), 'escuro')  # defensas de pneu
    for x in (-0.78, -0.26, 0.26, 0.92):
        L.cilindro(0.025, 0.04, (x, -0.24, zc), 'escuro', lados=6, r_topo=0.03)  # cabeços
    for y in (-0.20, 0.10):
        L.caixa((2.10, 0.012, 0.004), (0, y, zc), 'metal_escuro')            # trilhos do pórtico

    # Barcaça com contêineres (vaga livre embaixo do guindaste) e empurrador
    by = -0.51
    L.prisma([(-0.26, 0.01), (0.66, 0.01), (0.70, 0.10), (-0.30, 0.10)], 0.30, (0, by, 0), 'casco', eixo='Y')
    L.caixa((0.96, 0.26, 0.008), (0.20, by, 0.10), 'escuro')
    for i, x in enumerate((-0.12, 0.20)):
        conteiner(x, by - 0.065, 0.108, CORES[(i + 2) % 5], nervura=True)
        conteiner(x, by + 0.065, 0.108, CORES[(i + 4) % 5], nervura=True)
    conteiner(-0.12, by + 0.065, 0.223, 'cont_laranja', nervura=True)
    # Voadeira de pescador encostada mais à esquerda
    L.prisma([(-0.88, 0.012), (-0.70, 0.012), (-0.64, 0.06), (-0.92, 0.06)], 0.09, (0, -0.42, 0), 'metal', eixo='Y')
    L.caixa((0.16, 0.07, 0.006), (-0.78, -0.42, 0.054), 'madeira')
    tx = 0.87
    L.caixa((0.30, 0.24, 0.10), (tx, by, 0.0), 'casco', chanfro=0.01)        # empurrador
    L.caixa((0.30, 0.245, 0.02), (tx, by, 0.08), 'escuro')
    L.caixa((0.16, 0.18, 0.09), (tx + 0.04, by, 0.10), 'parede', chanfro=0.01)
    L.caixa((0.11, 0.15, 0.07), (tx + 0.05, by, 0.19), 'parede', chanfro=0.01)
    L.placa(0.12, 0.03, (tx + 0.05, by - 0.075, 0.24), 'vidro_escuro', 'frente', espessura=0.01)
    L.placa(0.12, 0.03, (tx - 0.005, by, 0.24), 'vidro_escuro', 'esquerda', espessura=0.01)
    L.caixa((0.12, 0.16, 0.012), (tx + 0.05, by, 0.26), 'cont_azul')
    L.cilindro(0.022, 0.08, (tx + 0.10, by + 0.03, 0.27), 'escuro', lados=6)

    # Armazém azul com telhado de duas águas de fibrocimento
    ax, ay, aw, ad, ah = -0.62, 0.39, 0.80, 0.54, 0.30
    L.caixa((aw, ad, ah), (ax, ay, zc), 'galpao_azul', chanfro=0.01)
    L.caixa((aw + 0.012, ad + 0.012, 0.05), (ax, ay, zc), 'concreto')
    p, t, ta = ad / 2 + 0.04, 0.02, 0.13
    L.prisma([(-p, 0), (0, ta), (p, 0), (p, -t), (0, ta - t), (-p, -t)], aw + 0.06,
             (ax, ay, zc + ah + t), 'fibrocimento', eixo='X')
    L.prisma([(ay - ad / 2, zc + ah), (ay + ad / 2, zc + ah), (ay, zc + ah + ta - 0.01)], aw - 0.004,
             (ax, 0, 0), 'galpao_azul', eixo='X')
    for x in (ax - 0.20, ax + 0.20):
        L.placa(0.24, 0.22, (x, ay - ad / 2, zc + 0.22), 'ferro_enrolar', 'frente')
        L.placa(0.26, 0.02, (x, ay - ad / 2 - 0.01, zc + 0.24), 'amarelo', 'frente', espessura=0.02)
    L.placa(0.16, 0.20, (ax + aw / 2, ay - 0.08, zc + 0.20), 'ferro_enrolar', 'direita')
    L.janelas('direita', ax + aw / 2, zc + 0.30, ay - ad / 2 + 0.05, ay + ad / 2 - 0.05, 1, 0.10, 0.05, 'vidro')

    # Pilhas de contêineres coloridos
    alturas = [[3, 2, 1, 2], [2, 3, 2, 1], [1, 2, 3, 2]]
    for i, x in enumerate((0.20, 0.52, 0.84)):
        for j, y in enumerate((0.20, 0.34, 0.48, 0.62)):
            for k in range(alturas[i][j]):
                conteiner(x, y, zc + k * 0.118, CORES[(i * 2 + j * 3 + k) % 5])

    # Guindaste de pórtico amarelo (pernas no cais, lança sobre a barcaça)
    Y = 'amarelo'
    g0, g1, l0, l1, zv = 0.36, 0.72, -0.20, 0.10, 0.76
    gx = (g0 + g1) / 2
    for x in (g0, g1):
        for y in (l0, l1):
            L.caixa((0.04, 0.04, zv - zc), (x, y, zc + 0.03), Y)
        L.caixa((0.06, 0.40, 0.03), (x, (l0 + l1) / 2, zc), 'escuro')         # truque com rodas
        L.caixa((0.05, l1 - l0 + 0.04, 0.05), (x, (l0 + l1) / 2, zv), Y)       # travessa de cima
        L.caixa((0.035, l1 - l0, 0.03), (x, (l0 + l1) / 2, zc + 0.30), Y)      # travessa do meio
    for y in (l0, l1):
        L.caixa((g1 - g0 + 0.04, 0.05, 0.05), (gx, y, zv), Y)
    L.caixa((0.20, 1.12, 0.06), (gx, -0.13, zv + 0.05), Y, chanfro=0.005)   # lança
    L.caixa((0.20, 0.22, 0.11), (gx, 0.25, zv + 0.11), 'parede', chanfro=0.01)  # casa de máquinas
    L.caixa((0.08, 0.08, 0.07), (gx + 0.05, -0.30, zv - 0.02), 'parede')      # cabine do operador
    L.placa(0.07, 0.04, (gx + 0.05, -0.34, zv + 0.035), 'vidro_escuro', 'frente', espessura=0.01)
    topo = (gx, l0 + 0.06, 1.28)
    for x in (g0 + 0.02, g1 - 0.02):
        L.cano((x, l0 + 0.06, zv + 0.10), topo, 0.016, Y, lados=4)
    L.cano(topo, (gx, -0.66, zv + 0.11), 0.007, 'grade', lados=4)              # estais
    L.cano(topo, (gx, 0.40, zv + 0.12), 0.007, 'grade', lados=4)
    # Carro da lança, cabos e o contêiner içado sobre a barcaça
    L.caixa((0.12, 0.10, 0.04), (gx, -0.50, zv + 0.01), 'metal_escuro')
    for x in (gx - 0.04, gx + 0.04):
        L.cano((x, -0.50, zv + 0.01), (x, -0.50, 0.42), 0.004, 'grade', lados=3)
    L.caixa((0.30, 0.10, 0.02), (gx, -0.50, 0.40), 'amarelo')
    conteiner(gx, -0.50, 0.285, 'cont_verde', nervura=True)

    # Poste de iluminação do pátio
    L.cano((-0.10, 0.55, zc), (-0.10, 0.55, 0.78), 0.012, 'metal', lados=4)
    L.caixa((0.10, 0.05, 0.03), (-0.10, 0.55, 0.78), 'metal_escuro')


L.principal(__file__, construir)
