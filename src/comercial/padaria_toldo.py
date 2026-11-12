"""Padaria de esquina de dois andares: térreo amarelo com balcão aberto e vitrine, porta de aço de enrolar meio
aberta, toldo listrado vermelho e branco nas duas fachadas, mesinhas de plástico na calçada e moradia verde-água
em cima com janelas gradeadas, telhado de barro e caixa d'água azul."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402


def toldo_frente(x0, x1, y, z, n, prof=0.19, queda=0.08, saia=0.045, cores=('toldo_vermelho', 'branco')):
    """Toldo inclinado preso na fachada da frente (plano y), de x0 a x1, em n listras."""
    e = 0.012
    perfil = [(0, e), (0, 0), (-prof, -queda), (-prof, -queda - saia), (-prof - e, -queda - saia), (-prof - e, -queda + e)]
    lw = (x1 - x0) / n
    for i in range(n):
        L.prisma(perfil, lw, (x0 + lw * (i + 0.5), y, z), cores[i % 2], eixo='X')


def toldo_direita(y0, y1, x, z, n, prof=0.1, queda=0.06, saia=0.045, cores=('toldo_vermelho', 'branco')):
    """Toldo inclinado preso na fachada direita (plano x), de y0 a y1, em n listras."""
    e = 0.012
    perfil = [(0, e), (0, 0), (prof, -queda), (prof, -queda - saia), (prof + e, -queda - saia), (prof + e, -queda + e)]
    lw = (y1 - y0) / n
    for i in range(n):
        L.prisma(perfil, lw, (x, y0 + lw * (i + 0.5), z), cores[i % 2], eixo='Y')


def mesa(x, y, z, cor):
    """Mesa de bar de plástico com duas cadeiras."""
    L.caixa((0.05, 0.05, 0.085), (x, y, z), cor)
    L.caixa((0.1, 0.1, 0.012), (x, y, z + 0.085), cor)
    for sx in (-1, 1):
        cx = x + sx * 0.085
        L.caixa((0.045, 0.045, 0.045), (cx, y, z), cor)
        L.caixa((0.055, 0.055, 0.01), (cx, y, z + 0.045), cor)
        L.caixa((0.01, 0.055, 0.06), (cx + sx * 0.024, y, z + 0.055), cor)


def construir():
    L.caixa((0.84, 1.07, 0.02), (0, 0, 0), 'piso')
    z0 = 0.02

    bx, by, bw, bd = -0.04, 0.12, 0.72, 0.78
    frente, direita = by - bd / 2, bx + bw / 2
    g, a = 0.34, 0.27
    L.caixa((bw, bd, g), (bx, by, z0), 'amarelo_pastel')
    L.caixa((bw + 0.02, bd + 0.02, 0.025), (bx, by, z0 + g - 0.005), 'parede')
    L.caixa((bw, bd, a), (bx, by, z0 + g + 0.02), 'verde_agua', chanfro=0.012)
    topo = z0 + g + 0.02 + a
    L.telhado4(bw, bd, 0.17, (bx, by, topo), 'terracota', beiral=0.04)
    # caixa d'água de fibra azul aparecendo no telhado
    L.cilindro(0.075, 0.09, (bx - 0.15, by + 0.22, topo + 0.08), 'fibra_azul', lados=8)
    L.cilindro(0.08, 0.02, (bx - 0.15, by + 0.22, topo + 0.17), 'fibra_azul', lados=8)

    # Faixa de letreiro (sem texto) acima do toldo, na frente e no lado
    L.placa(bw, 0.06, (bx, frente, z0 + g - 0.01), 'fibra_azul', 'frente', espessura=0.012)
    L.placa(bd, 0.06, (direita, by, z0 + g - 0.01), 'fibra_azul', 'direita', espessura=0.012)
    L.placa(bw * 0.6, 0.015, (bx, frente - 0.012, z0 + g - 0.032), 'branco', 'frente', espessura=0.006)

    # Térreo, frente: balcão aberto com vitrine + porta de aço de enrolar meio aberta
    cxa = bx - 0.17
    L.placa(0.3, 0.22, (cxa, frente, z0 + 0.16), 'escuro', 'frente', espessura=0.008)
    L.caixa((0.3, 0.05, 0.09), (cxa, frente - 0.025, z0), 'parede')            # balcão
    L.caixa((0.28, 0.035, 0.035), (cxa, frente - 0.025, z0 + 0.09), 'vidro')   # vitrine de pães
    L.caixa((0.08, 0.03, 0.008), (cxa - 0.06, frente - 0.025, z0 + 0.125), 'caramelo')  # pães
    cxp = bx + 0.19
    L.placa(0.22, 0.27, (cxp, frente, z0 + 0.135), 'escuro', 'frente', espessura=0.008)
    L.placa(0.22, 0.12, (cxp, frente - 0.008, z0 + 0.21), 'ferro_enrolar', 'frente', espessura=0.006)
    for dz in (0.04, 0.08):
        L.placa(0.22, 0.006, (cxp, frente - 0.014, z0 + 0.27 - dz), 'metal_escuro', 'frente', espessura=0.003)
    L.caixa((0.24, 0.035, 0.03), (cxp, frente - 0.017, z0 + 0.255), 'metal_escuro')   # caixa do rolo

    # Térreo, lado direito: porta de aço fechada e janela de serviço
    L.placa(0.24, 0.27, (direita, by - 0.1, z0 + 0.135), 'ferro_enrolar', 'direita', espessura=0.008)
    for dz in (0.03, 0.09, 0.15, 0.21):
        L.placa(0.24, 0.006, (direita + 0.008, by - 0.1, z0 + 0.25 - dz), 'metal_escuro', 'direita', espessura=0.003)
    L.caixa((0.035, 0.26, 0.03), (direita + 0.017, by - 0.1, z0 + 0.255), 'metal_escuro')
    L.placa(0.14, 0.12, (direita, by + 0.24, z0 + 0.17), 'vidro', 'direita', espessura=0.01)

    # Toldos listrados
    toldo_frente(bx - bw / 2, direita, frente, z0 + g - 0.045, 6)
    toldo_direita(frente, by + 0.08, direita, z0 + g - 0.045, 4)

    # Andar de cima: janelas com grade de ferro
    zj = z0 + g + 0.02 + 0.13
    for x in (bx - 0.18, bx + 0.18):
        L.placa(0.16, 0.12, (x, frente, zj), 'vidro_escuro', 'frente', espessura=0.01)
        for dx in (-0.05, 0.0, 0.05):
            L.placa(0.008, 0.12, (x + dx, frente - 0.01, zj), 'grade', 'frente', espessura=0.006)
        L.placa(0.18, 0.015, (x, frente - 0.01, zj - 0.065), 'parede', 'frente', espessura=0.02)
    for y in (by - 0.18, by + 0.18):
        L.placa(0.16, 0.12, (direita, y, zj), 'vidro_escuro', 'direita', espessura=0.01)
        for dy in (-0.05, 0.0, 0.05):
            L.placa(0.008, 0.12, (direita + 0.01, y + dy, zj), 'grade', 'direita', espessura=0.006)
        L.placa(0.18, 0.015, (direita + 0.01, y, zj - 0.065), 'parede', 'direita', espessura=0.02)
    # vasinho de planta na janela
    L.arbusto((bx - 0.18, frente - 0.03, zj - 0.06), 0.035, 'verde')

    # Mesinhas de plástico na calçada
    mesa(bx - 0.2, -0.45, z0, 'toldo_amarelo')
    mesa(bx + 0.22, -0.45, z0, 'toldo_vermelho')


L.principal(__file__, construir)
