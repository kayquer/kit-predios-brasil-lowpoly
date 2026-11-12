"""Galpão comprido de confecção ou metalúrgica: telhado de duas águas de telha ondulada de fibrocimento, paredes
brancas com barra cinza e faixa verde, janelas altas em fita, portão de enrolar na lateral e exaustores eólicos
(as bolinhas de metal) na cumeeira."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lib as L  # noqa: E402

L.PALETA['barra_cinza'] = '#8f969c'


def placa_ondulada(comp, rampa, pos, cor, ang, onda=0.07, amp=0.018, esp=0.014):
    """Telha ondulada: perfil em zigue-zague ao longo de X, estendido na rampa (Y) e inclinado `ang` graus em X."""
    n = max(2, round(comp / (onda / 2)))
    if n % 2:
        n += 1
    topo = [(-comp / 2 + comp * i / n, amp if i % 2 else 0.0) for i in range(n + 1)]
    perfil = topo + [(comp / 2, -esp), (-comp / 2, -esp)]
    return L.prisma(perfil, rampa, pos, cor, eixo='Y', rot=(ang, 0, 0))


def telhado_duas_aguas(comp, prof, alt, z0, cor, beiral=0.05, y0=0.0):
    """Duas placas onduladas (cumeeira em X) + capa da cumeeira."""
    meia = prof / 2 + beiral
    ang = math.degrees(math.atan2(alt, prof / 2))
    rampa = math.hypot(meia, alt * meia / (prof / 2))
    queda = alt * beiral / (prof / 2)
    for s in (-1, 1):
        cy = y0 + s * (meia / 2)
        cz = z0 - queda + (alt + queda) / 2
        placa_ondulada(comp, rampa, (0, cy, cz + 0.008), cor, -s * ang)
    L.caixa((comp + 0.01, 0.07, 0.03), (0, y0, z0 + alt - 0.005), 'concreto_escuro')


def construir():
    lx, ly, hp = 1.54, 0.86, 0.5        # paredes
    alt = 0.12                          # subida do telhado
    x1, y0 = lx / 2, -ly / 2

    # Corpo: paredes brancas, barra cinza embaixo e faixa verde (cor da firma, sem letreiro)
    L.caixa((lx, ly, hp), (0, 0, 0), 'parede', chanfro=0.015)
    L.caixa((lx + 0.012, ly + 0.012, 0.14), (0, 0, 0), 'barra_cinza')
    L.caixa((lx + 0.012, ly + 0.012, 0.035), (0, 0, 0.14), 'toldo_verde')
    # oitões (triângulos das pontas)
    for sx in (-1, 1):
        L.prisma([(-ly / 2, 0), (ly / 2, 0), (0, alt)], 0.02, (sx * (lx / 2 - 0.01), 0, hp), 'parede', eixo='X')
    telhado_duas_aguas(lx + 0.1, ly, alt, hp, "fibrocimento", beiral=0.04)

    # Janelas altas em fita na frente e no fundo
    for y, face in ((y0, 'frente'),):
        L.placa(lx - 0.16, 0.09, (0, y, hp - 0.075), 'vidro_escuro', face, espessura=0.02)
        for i in range(7):
            x = -lx / 2 + 0.08 + (lx - 0.16) * i / 6
            L.placa(0.02, 0.09, (x, y - 0.011, hp - 0.075), 'parede', face, espessura=0.01)

    # Frente: porta de pedestre e portão de enrolar pequeno
    L.placa(0.12, 0.26, (-0.5, y0, 0.13), 'portao', 'frente', espessura=0.02)
    L.placa(0.34, 0.32, (0.38, y0, 0.16), 'ferro_enrolar', 'frente', espessura=0.02)
    L.placa(0.37, 0.035, (0.38, y0 - 0.012, 0.335), 'escuro', 'frente', espessura=0.012)
    for z in (0.1, 0.2):
        L.placa(0.34, 0.012, (0.38, y0 - 0.012, z), 'metal_escuro', 'frente', espessura=0.006)
    L.placa(0.22, 0.12, (-0.12, y0, 0.31), 'vidro', 'frente', espessura=0.02)  # janela do escritório
    L.placa(0.26, 0.03, (-0.12, y0 - 0.01, 0.34), 'grade', 'frente', espessura=0.02)

    # Lateral direita (oitão): portão grande de enrolar + janelinha no triângulo
    L.placa(0.44, 0.38, (x1, 0.0, 0.19), 'ferro_enrolar', 'direita', espessura=0.02)
    L.placa(0.47, 0.04, (x1 + 0.012, 0.0, 0.395), 'escuro', 'direita', espessura=0.012)
    for z in (0.12, 0.24):
        L.placa(0.44, 0.012, (x1 + 0.012, 0.0, z), 'metal_escuro', 'direita', espessura=0.006)
    L.placa(0.2, 0.06, (x1, 0.0, hp + 0.07), 'vidro_escuro', 'direita', espessura=0.02)

    # Exaustores eólicos na cumeeira
    zc = hp + alt + 0.02
    for x in (-0.5, -0.17, 0.17, 0.5):
        L.cilindro(0.025, 0.03, (x, 0, zc - 0.02), 'metal_escuro', lados=6)
        L.esfera(0.048, (x, 0, zc + 0.05), 'metal', escala=(1, 1, 0.9))

    # Calha/tubo de descida e caixa de luz na lateral
    L.caixa((0.03, 0.03, hp), (x1 + 0.015, y0 + 0.04, 0), 'barra_cinza')
    L.caixa((0.04, 0.1, 0.12), (x1 + 0.02, 0.33, 0.16), 'metal_escuro')


L.principal(__file__, construir)
