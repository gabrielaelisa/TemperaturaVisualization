# TemperatureVisualization
visuals of temperature changes in given geography (numpy and matplotlib)
## Modelamiento de un Litoral Chileno
### CC3501-1 - Modelación y Computación Gráfica para Ingenieros

 - Se modela el perfil de un litoral de la costa chilena ,(corte transversal de oeste a este), de 4km de largo x 2km de alto.
    * El primer y segundo argumento de la Clase `Grilla` corresponde a las dimesiones Reales del Litoral.
    * El tercer argumento es un parámetro de tres dígitos que genera aleatoriedad en la creación del terreno
    * el cuarto parámetro corresponde a la discretización (escalamiento) escogido para representar el problema.
 - Por simplicidad, se asume que la temperatura de la atmósfera cumple con la ecuación de Poisson:
 

![r0t0](https://github.com/gabrielaelisa/TemperatureVisualization/blob/master/images/r0t0.png)

![r1t0](https://github.com/gabrielaelisa/TemperatureVisualization/blob/master/images/r1t0.png)
