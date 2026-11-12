"""Shopping de bairro: caixa grande creme com átrio de vidro na entrada, marquise, vitrines no térreo, faixas
coloridas das lojas (sem texto), totem colorido e estacionamento com carros na frente e na lateral."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402


def carro(x, y, z, cor, eixo='Y'):
    """Carro simples: carroceria + cabine escura (frente para o prédio)."""
    if eixo == 'Y':
        L.caixa((0.09, 0.17, 0.045), (x, y, z), cor)
        L.caixa((0.078, 0.085, 0.035), (x, y - 0.01, z + 0.045), 'vidro_escuro')
        L.caixa((0.08, 0.06, 0.006), (x, y - 0.01, z + 0.08), cor)
    else:
        L.caixa((0.17, 0.09, 0.045), (x, y, z), cor)
        L.caixa((0.085, 0.078, 0.035), (x - 0.01, y, z + 0.045), 'vidro_escuro')
        L.caixa((0.06, 0.08, 0.006), (x - 0.01, y, z + 0.08), cor)


def construir():
    L.caixa((1.66, 0.97, 0.02), (0, 0, 0), 'asfalto')
    z0 = 0.02
    # calçada em volta do prédio
    L.caixa((1.25, 0.655, 0.03), (-0.205, 0.1575, z0), 'piso')
    zc = z0 + 0.03

    bx, bw, by, bd, bh = -0.22, 1.16, 0.23, 0.48, 0.46
    frente, direita = by - bd / 2, bx + bw / 2
    L.caixa((bw, bd, bh), (bx, by, zc), 'creme', chanfro=0.015)
    L.caixa((bw + 0.02, bd + 0.02, 0.04), (bx, by, zc + bh), 'parede')
    L.caixa((bw - 0.04, bd - 0.04, 0.005), (bx, by, zc + bh + 0.04), 'concreto_escuro')
    # friso vermelho correndo pela fachada
    L.caixa((bw + 0.01, bd + 0.01, 0.025), (bx, by, zc + 0.24), 'vermelho')

    # Vitrines no térreo e faixas coloridas das lojas (frente e lado direito)
    for (x, cor) in ((bx - 0.39, 'laranja'), (bx + 0.39, 'toldo_verde')):
        L.placa(0.34, 0.15, (x, frente, zc + 0.1), 'vidro_escuro', 'frente', espessura=0.01)
        L.placa(0.34, 0.1, (x, frente, zc + 0.38), cor, 'frente', espessura=0.012)
        L.placa(0.12, 0.1, (x - 0.08, frente - 0.012, zc + 0.38), 'parede', 'frente', espessura=0.006)
    L.placa(0.38, 0.15, (direita, by - 0.02, zc + 0.1), 'vidro_escuro', 'direita', espessura=0.01)
    L.placa(0.38, 0.1, (direita, by - 0.02, zc + 0.38), 'fibra_azul', 'direita', espessura=0.012)
    L.placa(0.12, 0.1, (direita + 0.012, by + 0.06, zc + 0.38), 'amarelo', 'direita', espessura=0.006)

    # Átrio de vidro na entrada, mais alto que a caixa
    aw = 0.36
    L.caixa((aw, 0.14, bh + 0.1), (bx, frente, zc), 'vidro', chanfro=0.006)
    L.caixa((aw + 0.03, 0.17, 0.04), (bx, frente, zc + bh + 0.1), 'parede')
    for dx in (-0.09, 0.0, 0.09):
        L.caixa((0.012, 0.012, bh + 0.1), (bx + dx, frente - 0.072, zc), 'metal')
    L.placa(0.14, 0.15, (bx, frente - 0.072, zc + 0.075), 'escuro', 'frente', espessura=0.008)
    # marquise sobre a entrada
    L.caixa((0.56, 0.13, 0.03), (bx, frente - 0.135, zc + 0.2), 'parede', chanfro=0.006)
    L.caixa((0.565, 0.135, 0.01), (bx, frente - 0.135, zc + 0.23), 'laranja')
    for dx in (-0.25, 0.25):
        L.cano((bx + dx, frente - 0.18, zc), (bx + dx, frente - 0.18, zc + 0.2), 0.01, 'metal', lados=4)

    # Telhado: claraboia e ar-condicionado
    tz = zc + bh + 0.045
    L.caixa((0.5, 0.12, 0.05), (bx - 0.05, by + 0.08, tz), 'vidro')
    for k in range(3):
        L.caixa((0.09, 0.09, 0.06), (bx + 0.3 + k * 0.11, by + 0.1, tz), 'metal')

    # Estacionamento: faixas brancas, carros, árvores e totem
    py = -0.33
    for x in (-0.8, -0.64, -0.48, 0.0, 0.16, 0.32):
        L.caixa((0.01, 0.2, 0.004), (x, py, z0), 'branco')
    cores = ('vermelho', 'parede', 'prata', 'fibra_azul')
    for i, x in enumerate((-0.72, -0.56, 0.08, 0.24)):
        carro(x, py + 0.01, z0, cores[i])
    for y in (-0.06, 0.1, 0.26, 0.42):
        L.caixa((0.2, 0.01, 0.004), (0.66, y, z0), 'branco')
    for i, y in enumerate((0.02, 0.18, 0.34)):
        carro(0.64, y, z0, ('amarelo', 'vermelho', 'parede')[i], eixo='X')
    for (x, y) in ((-0.4, -0.42), (0.45, -0.42)):
        L.caixa((0.08, 0.08, 0.025), (x, y, z0), 'concreto')
        L.arvore((x, y, z0 + 0.025), 0.32, 'verde')
    # totem colorido na entrada do estacionamento
    L.caixa((0.07, 0.04, 0.62), (0.76, -0.42, z0), 'parede', chanfro=0.005)
    for k, cor in enumerate(('laranja', 'toldo_verde', 'fibra_azul')):
        L.caixa((0.075, 0.045, 0.1), (0.76, -0.42, z0 + 0.3 + k * 0.1), cor)


L.principal(__file__, construir)
