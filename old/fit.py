
from ROOT import *
import numpy as np

#da aggiustare, voglio aggiungere un if che che la derivata arriva sotto ad una certa 
# soglia calcola la tensione in quel punto. Forse conviene farlo direttamente 
# in fase di presa dati 


g = TGraphErrors()

file = open("valori.dat",'r')

#V, eV = np.loadtxt('out.dat', unpack=True)
nu = [1,2,3,4,5,6,7] #lista con tutte le lunghezze d onda
e_nu = [1,2,3,4,5,6,7] #lista con tutti gli errori associati alle lunghezze d onda
i = 0 
for line in file:
    l = line.split()
    v = float(l[0])
    ev = float(l[1])
    g.SetPoint(i,nu[i],v)
    g.SetPointError(i,e_nu[i],ev)
    i += 1
    
f = TF1("f","[0] + [1] * x")

g.Fit("f")