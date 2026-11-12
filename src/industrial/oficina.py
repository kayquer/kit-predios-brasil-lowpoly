"""Oficina mecânica de bairro: fachada com platibanda pintada de azul e faixas branca e amarela (sem letreiro), portão
largo aberto com o elevador de carro lá dentro, galpão de reboco cru com telha ondulada cinza, caixa d'água azul,
pneus empilhados e um carro esperando no pátio."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402

L.PALETA['azul_oficina'] = '#2f6db5'
L.PALETA['pneu'] = '#2a2c30'
L.PALETA['carro'] = '#d8423a'


def placa_ondulada_y(comp, rampa, pos, cor, ang, onda=0.07, amp=0.016, esp=0.014):
    """Telha ondulada com a cumeeira em Y: zigue-zague ao longo de Y, estendido em X e inclinado `ang` em Y."""
    n = max(2, round(comp / (onda / 2)))
    n += n % 2
    topo = [(-comp / 2 + comp * i / n, amp if i % 2 else 0.0) for i in range(n + 1)]
    perfil = topo + [(comp / 2, -esp), (-comp / 2, -esp)]
    return L.prisma(perfil, rampa, pos, cor, eixo='X', rot=(0, ang, 0))


def telhado_y(larg, comp, alt, z0, cx, cy, cor, beiral=0.03):
    """Telhado de duas águas de telha ondulada com a cumeeira ao longo de Y (caimento para os lados)."""
    meia = larg / 2 + beiral
    ang = math.degrees(math.atan2(alt, larg / 2))
    queda = alt * beiral / (larg / 2)
    rampa = math.hypot(meia, alt + queda)
    for s in (-1, 1):
        placa_ondulada_y(comp, rampa, (cx + s * meia / 2, cy, z0 - queda + (alt + queda) / 2 + 0.008), cor, s * ang)
    L.caixa((0.07, comp + 0.01, 0.03), (cx, cy, z0 + alt - 0.005), 'concreto_escuro')


def pneus(x, y, n):
    """Pilha de pneus (raio alternado marca cada pneu)."""
    z = 0
    for i in range(n):
        r = 0.065 if i % 2 == 0 else 0.058
        L.cilindro(r, 0.04, (x, y, z), 'pneu', lados=7)
        z += 0.04
    L.cilindro(0.032, 0.006, (x, y, z), 'escuro', lados=6)


def carro(x, y):
    """Carro popular de lado (ao longo de X), frente para +X."""
    for dx in (-0.14, 0.15):
        for dy in (-0.105, 0.105):
            L.cilindro(0.05, 0.035, (x + dx, y + dy - 0.0175, 0.05), 'pneu', lados=8, rot=(90, 0, 0))
    L.caixa((0.48, 0.21, 0.1), (x, y, 0.035), 'carro', chanfro=0.012)
    L.prisma([(-0.17, 0), (0.07, 0), (0.12, 0), (0.05, 0.085), (-0.14, 0.085)], 0.18, (x, y, 0.135), 'carro', eixo='Y')
    L.placa(0.17, 0.06, (x - 0.035, y - 0.091, 0.18), 'vidro_escuro', 'frente', espessura=0.01)
    L.prisma([(0.072, 0), (0.115, 0), (0.05, 0.075), (0.035, 0.075)], 0.16, (x, y, 0.14), 'vidro_escuro', eixo='Y')
    L.caixa((0.02, 0.17, 0.03), (x + 0.24, y, 0.07), 'parede')  # para-choque/farol


def construir():
    x0, x1 = -0.6, 0.3
    y0, y1 = -0.1, 0.6
    gx, gy = (x0 + x1) / 2, (y0 + y1) / 2
    lx, ly = x1 - x0, y1 - y0
    hp, alt = 0.42, 0.14

    # Galpão de reboco cru (só a fachada é pintada) com telha ondulada cinza
    fundo = 0.24                                  # o box da oficina (vão aberto) tem esse fundo
    L.caixa((lx, ly - fundo, hp), (gx, gy + fundo / 2, 0), 'reboco', chanfro=0.012)
    for px in (x0 + 0.015, x1 - 0.015):
        L.caixa((0.03, fundo + 0.01, hp), (px, y0 + fundo / 2, 0), 'reboco')
    L.placa(lx - 0.04, hp - 0.01, (gx, y0 + fundo - 0.004, (hp - 0.01) / 2), 'escuro', 'frente', espessura=0.01)
    L.caixa((lx - 0.04, fundo, 0.01), (gx, y0 + fundo / 2, 0), 'asfalto')
    L.prisma([(-lx / 2, 0), (lx / 2, 0), (0, alt)], 0.02, (gx, y1 - 0.01, hp), 'reboco', eixo='Y')
    telhado_y(lx, ly + 0.04, alt, hp, gx, gy + 0.02, 'fibrocimento')
    L.janelas('direita', x1, 0.3, y0 + 0.2, y1 - 0.08, 2, 0.16, 0.1, cor='vidro_escuro', moldura='grade')
    L.caixa((0.03, 0.03, hp), (x1 + 0.015, y1 - 0.03, 0), 'concreto_escuro')

    # Caixa d'água de fibra azul em cima de uma laje no fundo
    L.caixa((0.2, 0.2, 0.06), (x0 + 0.2, y1 - 0.16, hp + 0.06), 'concreto')
    L.cilindro(0.085, 0.13, (x0 + 0.2, y1 - 0.16, hp + 0.12), 'fibra_azul', lados=10, r_topo=0.095)
    L.cilindro(0.1, 0.02, (x0 + 0.2, y1 - 0.16, hp + 0.25), 'fibra_azul', lados=10)

    # Fachada com platibanda: pilares, verga e faixas (azul, branca e amarela)
    fy, ft = y0, 0.05
    ftop = 0.64
    fl = lx + 0.03
    L.caixa((fl, ft, 0.13), (gx, fy - ft / 2, ftop - 0.13), 'azul_oficina', chanfro=0.008)   # platibanda
    L.caixa((fl + 0.008, ft + 0.008, 0.04), (gx, fy - ft / 2, ftop - 0.215), 'parede')     # faixa branca
    L.caixa((fl, ft, 0.045), (gx, fy - ft / 2, ftop - 0.175), 'azul_oficina')
    L.caixa((fl + 0.008, ft + 0.008, 0.03), (gx, fy - ft / 2, ftop - 0.055), 'amarelo')    # faixa amarela
    L.caixa((fl, ft, 0.12), (gx, fy - ft / 2, ftop - 0.335), 'azul_oficina')               # verga sobre o portão
    lp = 0.12
    for px in (x0 - 0.015 + lp / 2, x1 + 0.015 - lp / 2):
        L.caixa((lp, ft, ftop - 0.335), (px, fy - ft / 2, 0), 'azul_oficina')
        L.caixa((lp + 0.008, ft + 0.008, 0.08), (px, fy - ft / 2, 0), 'escuro')            # barrado
    # vão aberto: interior escuro, porta de enrolar recolhida, elevador amarelo
    vl = fl - 2 * lp
    L.caixa((vl + 0.01, 0.06, 0.05), (gx, fy - 0.005, ftop - 0.385), 'ferro_enrolar')
    L.caixa((0.04, 0.04, 0.26), (gx - 0.18, fy + 0.12, 0), 'amarelo')
    L.caixa((0.04, 0.04, 0.26), (gx + 0.18, fy + 0.12, 0), 'amarelo')
    L.caixa((0.4, 0.12, 0.02), (gx, fy + 0.15, 0.16), 'amarelo')
    L.caixa((0.12, 0.07, 0.16), (gx + 0.28, fy + 0.19, 0.01), 'vermelho')   # armário de ferramentas

    # Pátio: piso de cimento, carro esperando, pilhas de pneus e tambor de óleo
    L.caixa((lx + 0.05, 0.54, 0.012), (gx, y0 - 0.27, 0), 'concreto')
    carro(gx - 0.02, -0.44)
    pneus(0.43, -0.1, 4)
    pneus(0.56, -0.02, 3)
    pneus(0.47, 0.12, 4)
    pneus(0.55, -0.5, 2)
    L.cilindro(0.055, 0.15, (0.53, 0.36, 0), 'vermelho', lados=8)
    L.cilindro(0.057, 0.012, (0.53, 0.36, 0.07), 'escuro', lados=8)
    L.cilindro(0.055, 0.15, (0.42, 0.48, 0), 'fibra_azul', lados=8)


L.principal(__file__, construir)
