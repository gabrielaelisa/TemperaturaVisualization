from Litoral import *


Montaña1= Montaña(70,280)
Montaña2=Montaña(1500+ 200*Terreno.bias,1080)
Montaña3=Montaña(1300+200*Terreno.bias, 1380)
Montaña4= Montaña(1850+100*Terreno.bias,1880)
Montaña5=Montaña(1000,4000-desplazamiento*Terreno.ds)
Montaña1.bordes()
Montaña2.bordes()
Montaña3.bordes()
Montaña4.bordes()
Montaña5.bordes()
cdict= {
    'red':[(0.0, 0.0, 0.0),
           (0.5, 1.0, 1.0),
           (1.0,1.0, 1.0)],

    'green':[(0.0, 0.0, 0.0),
             (0.25, 0.0, 0.0),
             (0.75,1.0, 1.0),
             (1.0, 1.0, 1.0)],

    'blue':[(0.0, 0.0, 0.0),
            (0.5, 0.0, 0.0),
            (1.0, 1.0, 1.0)]
}
my_cmap=mplt.colors.LinearSegmentedColormap('mycmap', cdict, 256, 0.45)

def show_Plots():
    Temperaturas= Grilla(2000,4000,930,25,0.1)
    #lista de temperaturas a graficar
    temperaturas=[0,8,12,16,20]
    rhos=[tmp.rho_2, tmp.rho_1]
    rho_name=["0","f(x,y)"]
    n=0
    for r in rhos:
        for t in temperaturas:
            Temperaturas.init_temperaturas(Terreno.matrix, t)
            Temperaturas.run_tol(Terreno,Temperaturas.w_optimo(),r)
            fig = plt.figure()
            ax = fig.add_subplot(111)
            cax = ax.imshow(Temperaturas.matrix.transpose(), interpolation='none', cmap= my_cmap)
            #,cmap='jet')
            fig.colorbar(cax)
            plt.gca().invert_yaxis()
            plt.xlabel('distancia al origen del mar')
            plt.ylabel('altura sobre la superficie del mar')
            plt.title('Rho='+ rho_name[n]+', ' 't= '+str(t) +', Tolerancia=' +str(Temperaturas.tol))
            plt.show()
        n+=1

def omegaVStime(tiempo, tolerancia, fun):
    '''
     Grafica el numero de iteraciones para alcanzar el equilibrio
     en funcion de el Omega escogido para laplace/Poisson.
    :param tiempo: tiempo del dia
    :param tolerancia: tolerancia para la congervencia termica
    :param fun: rho=0 o rho=f(x,y)
    :return: void
    '''

    Temperaturas = Grilla(2000, 4000, 930, 25, tolerancia)

    Omegas=[1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
    iteraciones=[]
    for w in Omegas:
        Temperaturas.init_temperaturas(Terreno.matrix, tiempo)
        i= Temperaturas.run_tol(Terreno,w,fun)
        iteraciones.append(i)
    plt.plot(Omegas, iteraciones)
    plt.xlabel('Omega')
    plt.ylabel('Numero de iteraciones')
    plt.show()

show_Plots()
#cambiar estos valores para ver resultados diferentes
omegaVStime(0,0.1,tmp.rho_2)
