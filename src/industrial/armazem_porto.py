"""Armazém de porto: galpão longo de chapas metálicas azuis com telha trapezoidal e lanternim na cumeeira, cinco
portões identificados por cor (sem números) e, na frente, o cais de concreto com borda amarela, cabeços de
amarração, pneus de defensa e dois contêineres empilhados."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402

L.PALETA['chapa_azul'] = '#3f78b0'
L.PALETA['chapa_azul_escura'] = '#2f5f8e'
L.PALETA['telha_metal'] = '#b4bcc3'


def placa_trapezoidal(comp, rampa, pos, cor, ang, onda=0.2, amp=0.02, esp=0.014):
    """Telha trapezoidal com a cumeeira em X: nervuras ao longo de X, estendida na rampa (Y), inclinada em X."""
    n = max(1, round(comp / onda))
    p = comp / n
    topo = []
    for i in range(n):
        a = -comp / 2 + p * i
        topo += [(a, 0.0), (a + p * 0.5, 0.0), (a + p * 0.62, amp), (a + p * 0.88, amp)]
    topo.append((comp / 2, 0.0))
    perfil = topo + [(comp / 2, -esp), (-comp / 2, -esp)]
    return L.prisma(perfil, rampa, pos, cor, eixo='Y', rot=(ang, 0, 0))


def telhado(comp, prof, alt, z0, y0, cor, beiral=0.03):
    meia = prof / 2 + beiral
    ang = math.degrees(math.atan2(alt, prof / 2))
    queda = alt * beiral / (prof / 2)
    rampa = math.hypot(meia, alt + queda)
    for s in (-1, 1):
        placa_trapezoidal(comp, rampa, (0, y0 + s * meia / 2, z0 - queda + (alt + queda) / 2 + 0.008), cor, -s * ang)


def conteiner(x, y, z, cor):
    L.caixa((0.42, 0.17, 0.17), (x, y, z), cor, chanfro=0.006)
    for dx in (-0.07, 0.07):
        L.placa(0.012, 0.15, (x + dx, y - 0.085, z + 0.085), 'escuro', 'frente', espessura=0.006)


def construir():
    lx, ly = 1.96, 0.5
    y0 = 0.16                     # centro do galpão em Y
    yf = y0 - ly / 2              # fachada
    hp, alt = 0.54, 0.15

    # Galpão de chapa azul com rodapé de concreto e frisos verticais
    L.caixa((lx, ly, hp), (0, y0, 0), 'chapa_azul', chanfro=0.012)
    L.caixa((lx + 0.01, ly + 0.01, 0.07), (0, y0, 0), 'concreto')
    for sx in (-1, 1):
        L.prisma([(-ly / 2, 0), (ly / 2, 0), (0, alt)], 0.02, (sx * (lx / 2 - 0.01), y0, hp), 'chapa_azul',
                 eixo='X')
    telhado(lx + 0.08, ly, alt, hp, y0, 'telha_metal')
    # lanternim (ventilação na cumeeira)
    zl = hp + alt - 0.01
    L.caixa((lx * 0.7, 0.12, 0.06), (0, y0, zl), 'chapa_azul_escura')
    L.telhado(lx * 0.7, 0.12, 0.04, (0, y0, zl + 0.06), 'telha_metal', beiral=0.025)

    # Cinco portões, cada um marcado por uma cor (no lugar do número)
    cores = ('amarelo', 'vermelho', 'verde', 'laranja', 'parede')
    for i, cor in enumerate(cores):
        x = -lx / 2 + lx * (i + 0.5) / 5
        L.placa(0.26, 0.34, (x, yf, 0.17), 'ferro_enrolar', 'frente', espessura=0.02)
        L.placa(0.3, 0.06, (x, yf, 0.37), cor, 'frente', espessura=0.026)            # verga colorida
        L.placa(0.26, 0.008, (x, yf - 0.012, 0.12), 'metal_escuro', 'frente', espessura=0.006)
        L.placa(0.26, 0.008, (x, yf - 0.012, 0.24), 'metal_escuro', 'frente', espessura=0.006)
        L.placa(0.03, 0.34, (x - 0.15, yf, 0.17), cor, 'frente', espessura=0.026)
        L.placa(0.03, 0.34, (x + 0.15, yf, 0.17), cor, 'frente', espessura=0.026)
    # portão lateral
    L.placa(0.3, 0.3, (lx / 2, y0, 0.2), 'ferro_enrolar', 'direita', espessura=0.02)
    L.placa(0.34, 0.05, (lx / 2, y0, 0.37), 'amarelo', 'direita', espessura=0.026)

    # Cais de concreto na frente, borda amarela, cabeços de amarração e pneus de defensa
    cy0, cy1 = -0.44, yf
    cy = (cy0 + cy1) / 2
    L.caixa((lx + 0.08, cy1 - cy0, 0.05), (0, cy, 0), 'concreto', chanfro=0.006)
    L.caixa((lx + 0.084, 0.03, 0.006), (0, cy0 + 0.02, 0.05), 'amarelo')
    for x in (-0.85, -0.3, 0.3, 0.85):
        L.cilindro(0.025, 0.05, (x, cy0 + 0.06, 0.05), 'escuro', lados=6)
        L.cilindro(0.035, 0.012, (x, cy0 + 0.06, 0.09), 'escuro', lados=6)
    for x in (-0.6, 0.0, 0.6):
        L.cilindro(0.035, 0.025, (x, cy0 + 0.02, 0.02), 'escuro', lados=8,
                   rot=(90, 0, 0))
    # contêineres empilhados no cais
    conteiner(-0.62, -0.28, 0.05, 'laranja')
    conteiner(-0.62, -0.28, 0.22, 'verde_garrafa')
    conteiner(0.56, -0.27, 0.05, 'telhado_azul')


L.principal(__file__, construir)
