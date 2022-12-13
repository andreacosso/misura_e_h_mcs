#!/usr/bin/python
    
import sys,serial
from dmm import *
from ps  import *
#from ROOT import *
import numpy as np


#File di output
file = open('out.dat','w') #questo dovrebbe avere tutti i punti misurati
file2 = open('valori.dat','w') #questo dovrebbe avere solo i punti con cui poi fare il grafico

#seriale
ser = serial.Serial('COM4', 9600)

instr = psinit('USB0::0x0AAD::0x0135::034083383::INSTR')
#Selezione canale 1
pssel(instr,1)
#Erogazione di 12 V per caricare il condensatore 
valV = 4
cmd  = f'APPLY {valV},0.1'
instr.write(cmd)
time.sleep(0.5)

#qui si chiude l interruttore e succedono cose, fa il grafico con un milione di punti come per il rumore in lab2
#serve cosi che possimao decidere in fase di analisi dati dove prendere la tenisone da misurare

#g = TGraph()
#c = TCanvas()

#c.Draw()
#c.cd()
V = np.array([])
eV = np.array([])
t = 0
t_init = 0
v = 0
ev = 0
i = 0
b = True
k = True
q = False
while b:
    
    a,b = dmmread(ser)
    V = np.append(V,a)
    eV = np.append(eV,b)
    print(a,b)
    #print(V[i],eV[i])

    if (i >= 1):
        if ((abs(V[i-1]-V[i])> 0.2) and  k):
            t_init = time.time()
            k = False
            q = True

        if (q):
           t = time.time()        
        if (abs(t - t_init) > 90): #non è detto sia giusto il valore
            v = V[i]
            ev = eV[i]
            b = False
            file2.write(str(v)+'\t')
            file2.write(str(ev)+'\t')
            file2.write('\n')
            print("_________________________________________________________")
            print("*********************************************************")
            print("---------------------------------------------------------")
    file.write(str(t-t_init) +'\t' + str(V[i])+'\t')
    file.write(str(eV[i])+'\t')
    file.write('\n')
    
    i += 1
    
    time.sleep(0.01)
