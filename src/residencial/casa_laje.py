"""Casa de autoconstrução com laje: metade no reboco cru e metade em tijolo baiano aparente com pilares e vigas de
concreto, laje plana com ferros de espera, caixa d'água azul, puxadinho em tijolo, varal e escada externa de concreto."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402


def bloco(face, plano, u, z0, larg, alt, prof, cor, off=0.0):
    """Caixa encostada numa fachada: u = posição ao longo da face, z0 = base, off = afastamento da parede."""
    if face == 'frente':
        return L.caixa((larg, prof, alt), (u, plano - off - prof / 2, z0), cor)
    if face == 'tras':
        return L.caixa((larg, prof, alt), (u, plano + off + prof / 2, z0), cor)
    if face == 'direita':
        return L.caixa((prof, larg, alt), (plano + off + prof / 2, u, z0), cor)
    return L.caixa((prof, larg, alt), (plano - off - prof / 2, u, z0), cor)


def janela(face, plano, u, z0, larg, alt, moldura='metal', barras=3):
    """Janela de alumínio com vidro e (se barras > 0) grade de ferro."""
    bloco(face, plano, u, z0 - 0.01, larg + 0.03, alt + 0.02, 0.01, moldura)
    bloco(face, plano, u, z0, larg, alt, 0.006, 'vidro_escuro', off=0.01)
    bloco(face, plano, u, z0, 0.01, alt, 0.006, moldura, off=0.014)
    for i in range(barras):
        uu = u - larg / 2 + larg * (i + 1) / (barras + 1)
        bloco(face, plano, uu, z0, 0.009, alt, 0.008, 'grade', off=0.02)
    if barras:
        bloco(face, plano, u, z0 + alt / 2 - 0.0045, larg, 0.009, 0.008, 'grade', off=0.02)


def construir():
    W, D = 1.44, 1.16
    L.caixa((W, D, 0.012), (0, 0, 0), 'piso')
    piso = 0.012

    # Térreo: parte em reboco cru (esquerda) e parte em tijolo baiano com estrutura de concreto (direita)
    x0, x1, xm = -0.68, 0.42, -0.12
    yf, yb = -0.18, 0.56
    by, bd = (yf + yb) / 2, yb - yf
    hw = 0.4
    L.caixa((xm - x0, bd, hw), ((x0 + xm) / 2, by, piso), 'reboco', chanfro=0.008)
    L.caixa((x1 - xm, bd - 0.02, hw), ((xm + x1) / 2, by, piso), 'tijolo_baiano')
    for x in (xm + 0.02, x1 - 0.02):                                                    # pilares

        L.caixa((0.045, bd + 0.008, hw), (x, by, piso), 'concreto')
    L.caixa((x1 - xm, bd + 0.008, 0.045), ((xm + x1) / 2, by, piso + hw - 0.045), 'concreto')   # viga
    L.caixa((x1 - xm, bd + 0.008, 0.03), ((xm + x1) / 2, by, piso), 'concreto')                   # baldrame

    # Laje plana
    zl = piso + hw
    L.caixa((x1 - x0 + 0.04, bd + 0.04, 0.04), ((x0 + x1) / 2, by, zl), 'concreto_escuro')
    zl += 0.04

    # Ferros de espera saindo dos pilares da frente (a casa vai crescer)
    for x in (x0 + 0.04, xm + 0.02, x1 - 0.02):
        L.caixa((0.05, 0.05, 0.03), (x, yf + 0.03, zl), 'concreto')
        for dx, dy in ((-0.012, -0.012), (0.012, 0.012), (0.012, -0.012)):
            L.caixa((0.007, 0.007, 0.12), (x + dx, yf + 0.03 + dy, zl + 0.03), 'ferrugem')

    # Puxadinho em tijolo no fundo da laje, telha de fibrocimento de uma água
    px0, px1, py0, py1 = x0 + 0.02, -0.12, 0.18, yb - 0.02
    L.caixa((px1 - px0, py1 - py0, 0.27), ((px0 + px1) / 2, (py0 + py1) / 2, zl), 'tijolo_baiano')
    L.caixa((0.04, py1 - py0 + 0.006, 0.27), (px1 - 0.02, (py0 + py1) / 2, zl), 'concreto')
    L.caixa((px1 - px0 + 0.01, py1 - py0 + 0.006, 0.035), ((px0 + px1) / 2, (py0 + py1) / 2, zl + 0.235), 'concreto')
    L.prisma([(py0 - 0.05, 0.0), (py1 + 0.02, 0.05), (py1 + 0.02, 0.065), (py0 - 0.05, 0.015)],
             px1 - px0 + 0.08, ((px0 + px1) / 2, 0, zl + 0.27), 'fibrocimento', eixo='X')
    bloco('frente', py0, (px0 + px1) / 2 - 0.08, zl, 0.12, 0.21, 0.008, 'madeira')          # porta
    janela('frente', py0, (px0 + px1) / 2 + 0.13, zl + 0.12, 0.1, 0.08, barras=0)

    # Caixa d'água azul sobre base de tijolo
    cx, cy = 0.22, 0.36
    L.caixa((0.2, 0.2, 0.04), (cx, cy, zl), 'tijolo_baiano')
    L.cilindro(0.085, 0.11, (cx, cy, zl + 0.04), 'fibra_azul', lados=8, r_topo=0.095)
    L.cilindro(0.1, 0.028, (cx, cy, zl + 0.15), 'fibra_azul', lados=8, r_topo=0.065)

    # Varal na laje com roupas coloridas
    vy = 0.02
    for x in (x0 + 0.12, xm + 0.18):
        L.caixa((0.012, 0.012, 0.2), (x, vy, zl), 'metal_escuro')
    L.caixa((xm + 0.18 - x0 - 0.12, 0.005, 0.005), ((x0 + 0.12 + xm + 0.18) / 2, vy, zl + 0.19), 'escuro')
    for i, (cor, larg, alt) in enumerate((('vermelho', 0.07, 0.08), ('amarelo', 0.06, 0.1), ('azul_pastel', 0.08, 0.07),
                                           ('branco', 0.06, 0.09), ('verde', 0.06, 0.07))):
        x = x0 + 0.17 + i * 0.085
        L.caixa((larg, 0.006, alt), (x, vy, zl + 0.19 - alt), cor)

    # Escada externa de concreto no lado direito, subindo de frente para o fundo
    n, sx = 7, 0.14
    ex = x1 + sx / 2 + 0.005
    passo = (zl - piso) / n
    for i in range(n):
        y = -0.1 + i * 0.085
        L.caixa((sx, 0.085, passo * (i + 1)), (ex, y, piso), 'concreto')
    L.caixa((sx, yb - (-0.1 + n * 0.085 - 0.0425), zl - piso), (ex, (yb + (-0.1 + n * 0.085 - 0.0425)) / 2, piso),
            'concreto')
    L.cano((ex + sx / 2 - 0.01, -0.1, piso + passo + 0.13), (ex + sx / 2 - 0.01, 0.5, zl + 0.13), 0.007, 'grade', lados=4)
    for y, z in ((-0.1, piso + passo), (0.5, zl)):
        L.caixa((0.01, 0.01, 0.13), (ex + sx / 2 - 0.01, y, z), 'grade')

    # Fachada: porta de aço, janela com grade no reboco, janela de alumínio no tijolo
    bloco('frente', yf, x0 + 0.17, piso, 0.2, 0.3, 0.012, 'portao')
    for k in range(4):
        bloco('frente', yf, x0 + 0.17, piso + 0.04 + k * 0.065, 0.2, 0.008, 0.006, 'metal_escuro', off=0.012)
    janela('frente', yf, x0 + 0.44, piso + 0.15, 0.18, 0.15)
    janela('frente', yf, (xm + x1) / 2 - 0.12, piso + 0.16, 0.16, 0.14, barras=0)
    bloco('frente', yf, (xm + x1) / 2 + 0.13, piso, 0.15, 0.3, 0.01, 'madeira_escura')
    janela('direita', x1, by + 0.15, piso + 0.16, 0.16, 0.14, barras=0)

    # Muro da frente sem pintura (reboco) com portão de chapa azul
    my = -D / 2 + 0.025
    gx0, gx1 = -0.38, 0.12
    for (a, b) in ((-W / 2 + 0.01, gx0), (gx1, W / 2 - 0.01)):
        L.caixa((b - a, 0.04, 0.2), ((a + b) / 2, my, piso), 'reboco', chanfro=0.004)
    for x in (gx0 - 0.025, gx1 + 0.025):
        L.caixa((0.05, 0.05, 0.24), (x, my, piso), 'concreto')
    L.caixa((gx1 - gx0, 0.014, 0.22), ((gx0 + gx1) / 2, my, piso + 0.008), 'galpao_azul')
    for k in range(5):
        x = gx0 + (gx1 - gx0) * (k + 0.5) / 5
        L.caixa((0.012, 0.022, 0.2), (x, my, piso + 0.018), 'telhado_azul')
    # entulho e um saco de cimento no quintal (obra sem fim)
    L.caixa((0.12, 0.08, 0.03), (0.32, -0.36, piso), 'areia', rot=(0, 0, 15))
    L.caixa((0.06, 0.04, 0.025), (0.22, -0.4, piso), 'concreto', rot=(0, 0, -10))


L.principal(__file__, construir)
