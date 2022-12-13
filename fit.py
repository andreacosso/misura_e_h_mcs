
from ROOT import *
import numpy as np

#da aggiustare, voglio aggiungere un if che che la derivata arriva sotto ad una certa 
# soglia calcola la tensione in quel punto. Forse conviene farlo direttamente 
# in fase di presa dati 

app = TApplication("app",0,0)
g = TGraphErrors()

file = open("out_uv.dat",'r')

#V, eV = np.loadtxt('out.dat', unpack=True)
lam = np.array( [467e-09, 590e-09, 624e-09,520e-09,405e-09,890e-09])
nu =299792458/lam #lista con tutte le lunghezze d onda
e_nu = [1e-09,3e-09 ,3e-09,1e-09,1e-09,1e-09] #lista con tutti gli errori associati alle lunghezze d onda
i = 0
for line in file:
    #if i<6:
        l = line.split()
        t = float(l[0])
        v = float(l[1])
        ev = float(l[2])
        g.SetPoint(i,t,v)
        g.SetPointError(i,0,ev)
        #g.SetPoint(i,nu[i],v)
        #g.SetPointError(i,e_nu[i],ev)
        i += 1
    
#f = TF1("f","[0] + [1] * x")
#f.SetParameter(0,0)
#f.SetParameter(1,0.24e15)
g.SetMarkerStyle(20)
g.Draw("AP")
#g.Fit("f")
g.Print()
app.Run(True)
