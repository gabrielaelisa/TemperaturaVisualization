
import math


def temperatura_M(t):
    if (t in range(0, 8)):
        return 4
    if (8 <= t <= 16):
        return 2 * t - 12
    elif (16 < t <= 24):
        return 52 - 2 * t


def temperatura_A(y, t, ds):
    return temperatura_M(t) - 6 * y / (1000 / ds)


def temperatura_S(y, ds):
    if (0 <= y <= (1800 / ds)):
        return 20
    elif (y > (1800 / ds)):
        return 0

def temperatura_I(t):
   return 450*(math.cos((math.pi/12)*t) +2)

def rho_1(x, y):
    '''
    :param x: distancia horizontal al centro de la planta
    :param y: distancia vertical al centro de la planta
    :return: resultado de la evaluación de la fuinción
    '''
    return 1/(math.sqrt((x**2) + (y**2) + 120))


def rho_2(x, y):
    ''' ecuación de Laplace vista en clases'''
    return 0


def Iteration(alto, ancho, M_nueva, M_vieja, Terreno, omega, rho, h, f):
    '''

    :param alto:
    :param ancho:
    :param M_nueva:
    :param M_vieja:
    :param omega:
    :param rho: funcion entregada
    :param h: discretizacion
    :param f: funcion que calcula distancia al centro de la industria
    :return:
    '''

    for x in range(1, ancho - 1):
         for y in range(0, alto - 1):
                # Valor anterior de la matriz promediado
                prom = 0

                # Caso General atmósfera
                if (Terreno[x][y] == 0 ):
                    prom = 0.25 * (M_vieja[x][y - 1] + M_vieja[x][y + 1] + M_vieja[x - 1][y] +
                                   M_vieja[x + 1][y] - 4 * M_vieja[x][y] - (h ** 2)*rho(f([x, y])[0], f([x, y])[1]))

                # Calcula nuevo valor
                M_nueva[x][y] = M_vieja[x][y] + prom* omega