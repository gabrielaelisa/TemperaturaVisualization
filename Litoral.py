import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mplt
import math
import Temperatura as tmp

'''
:author Gabriela Mendoza
visualización de temperatura en un litoral
bajo fórmula de Laplace y fórmula de Poisson
Librerías numpy y matplotlib

'''

class Grilla:
    '''constructor
        :param alto : alto de la grilla
        :param largo: largo de la grilla
        :param RRR: ultimos tres digitos del rut
        :param discret: discrtizacion de la grilla
        :param tol: tolerancia de equilibrio termico

    '''
    def __init__(self, alto, largo, RRR, discret, tol):
        self.alto= int(alto/discret)
        self.largo= int(largo/discret)
        self.bias= RRR/1000
        self.ds= discret
        self.tol=tol
        self.matrix = np.zeros((self.largo,self.alto))
        self.mar= math.ceil(1200/self.ds +(400/self.ds)*self.bias)
        self.industria= math.ceil(120/self.ds)
        self.altura_chimenea= math.ceil(60/self.ds)

    def init_variables(self):
        for x in range(0,int(self.mar)):
            self.matrix[x][0]=2

        for x in range(self.mar, self.mar+self.industria):
            for y in range(0, self.altura_chimenea):
                self.matrix[x][y]=3

    def init_temperaturas(self,terreno, time):
        for x in range(0, self.largo):
            for y in range(0, self.alto):
                # Atmósfera
                if(terreno[x][y]==0):
                    self.matrix[x][y]= tmp.temperatura_A(y, time, self.ds)
                # Montaña
                if(terreno[x][y]==1):
                    self.matrix[x][y]= tmp.temperatura_S(y, self.ds)
                # Mar
                if(terreno[x][y]==2):
                    self.matrix[x][y]= tmp.temperatura_M(time)
                # Industria
                if(terreno[x][y]==3):
                   self.matrix[x][y]=tmp.temperatura_I(time)
                # NAN
                if(math.isnan(terreno[x][y])):
                    self.matrix[x][y]= float('nan')

    def distancia(self,pos):
        '''
        :param x: posicion x en la grilla
        :return: la distancia al centro de la industria
        '''
        global desplazamiento
        global centro_industria
        x = pos[0]
        y = pos[1]
        centro = desplazamiento - centro_industria
        if (centro > x):
            return [(centro - x)*self.ds, y*self.ds]

        else:
            return [(x - centro)*self.ds, y*self.ds]

    def w_optimo(self):
        return 4 / (2 + (math.sqrt(4 - (math.cos(math.pi / (self.alto - 1)) + math.cos(math.pi / (self.largo - 1))) ** 2)))

    @staticmethod
    def equilibrio(M_vieja, M_nueva, tol):
        '''

        :param M_vieja: matriz de la iteracion anterior
        :param M_nueva: matriz resultante de una nueva iteracion
        :param tol: tolerancia para el equilibrio térmico
        :return: boolean tol reached?
        '''
        not_zero = (M_nueva != 0)#matriz de booleanos
        not_nan =(np.logical_not(np.isnan(M_nueva*not_zero)))
        diff_relativa = (M_vieja - M_nueva)[not_nan]
        max_diff = np.max(np.fabs(diff_relativa))
        print(max_diff)
        return [max_diff < tol, max_diff]



    def run_tol(self,Terreno,omega,rho):
        '''
        Por cada iteracion verifica si se alcanza la tolerancia
        :param Terreno:
        :param omega:
        :param rho: función laplace o Poisson
        :return:
        '''

        M_nueva = np.copy(self.matrix)
        omega = omega-1
        niter = 0
        stop=False
        while(not stop):
            M_vieja = np.copy(M_nueva)
            tmp.Iteration(self.alto, self.largo, M_nueva, M_vieja, Terreno.matrix,omega,
                          rho, 25, self.distancia)
            niter+=1
            converg = self.equilibrio(M_vieja, M_nueva, self.tol)
            stop = converg[0]
        self.matrix = np.copy(M_nueva)
        return niter

    def run(self, Terreno, omega, rho):
        M_nueva = np.copy(self.matrix)
        omega = omega - 1
        niter= 100
        for i in range(0,niter):
            print(i*100/niter)
            M_vieja = np.copy(M_nueva)
            tmp.Iteration(self.alto, self.largo, M_nueva, M_vieja, Terreno.matrix, omega,
                          rho, 25, self.distancia)
        self.matrix = np.copy(M_nueva)



"""
Variables Globales
"""
punta_ant=0
dist_ant= 0

# Editar estas variables para cambiar las dimensiones del terreno
Terreno= Grilla(2000,4000,930,25, 0.01)
Terreno.init_variables()
desplazamiento= math.ceil(Terreno.mar+Terreno.industria)
centro_industria=Terreno.industria/2


def f(x1,y1,x2, y2,x):
    '''
    crea funcion lineal a partir de dos puntos
    y entrega el resultado de x
    '''
    m= (y2-y1)/(x2-x1)
    return m*(x-x1) +y1



class Montaña:
    ''' constructor
        :param alto: alto de la montaña a partir del nivel de la montaña anterior
        :param ancho: distancia al borde de la industria
    '''
    def __init__(self,alto,ancho):
        global Terreno
        self.punta= math.ceil(alto/Terreno.ds)
        self.dist= math.ceil(ancho/Terreno.ds)

    def bordes(self):
        '''
        Define los bordes de la montaña con una función lineal discretizada
        :return: void
        '''
        global punta_ant
        global dist_ant
        global desplazamiento
        global Terreno


        x=dist_ant

        while(x<self.dist):
            y= f(dist_ant, punta_ant,self.dist, self.punta, x)
            Terreno.matrix[math.floor(x)+int(desplazamiento)][int(math.floor(y))]=1
            x+=0.2 # el paso dependerá de la pendiente!

        self.rellenar()
        punta_ant= self.punta
        dist_ant= self.dist

    def rellenar(self):
        '''
        rellena el interior de la montaña con nan
        :return: void
        '''
        global Terreno
        global dist_ant
        for i in range(int(dist_ant), int(self.dist)):
            for j in range(0, Terreno.alto):
                if(Terreno.matrix[int(i+ desplazamiento)][j]==1):
                    break
                else:
                    Terreno.matrix[int(i+desplazamiento)][int(j)]=float('nan')