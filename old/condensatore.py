#!/usr/bin/python
    
import sys,serial
from dmm import *
from ps  import *
from ROOT import *


'''
#Pilotaggio power supply
#Inizializzazione
instr = psinit("USB0::0x0AAD::0x0135::035375056::INSTR")
#Selezione canale 1
pssel(instr,1)
#Erogazione di 12 V
valV = 12
cmd  = f'APPLY {valV},0.1'
instr.write(cmd)

#File di output
file = open('out.dat','w')
#Configurazione seriale
ser = serial.Serial('COM2', 9600)
#Lettura dal multimetro
V,eV = dmmread(ser)
print(V,eV)
file.write(str(V)+'\t')
file.write(str(eV)+'\t')
file.write('\n')
'''


#File di output
file = open('out.dat','w') #questo dovrebbe avere tutti i punti misurati
file2 = open('valori.dat','w') #questo dovrebbe avere solo i punti con cui poi fare il grafico

#seriale
ser = serial.Serial('COM2', 9600)

instr = psinit("USB0::0x0AAD::0x0135::035375056::INSTR")
#Selezione canale 1
pssel(instr,1)
#Erogazione di 12 V per caricare il condensatore 
valV = 12
cmd  = f'APPLY {valV},0.1'
instr.write(cmd)

#qui si chiude l interruttore e succedono cose, fa il grafico con un milione di punti come per il rumore in lab2
#serve cosi che possimao decidere in fase di analisi dati dove prendere la tenisone da misurare

g = TGraph()
c = TCanvas()

c.Draw()
c.cd()
V = []
eV = []
v = 0
ev = 0
i = 0
b = True
while b == True:
    t = time.time()
    V[i],eV[i] = dmmread(ser)
    #print(V[i],eV[i])
    if (V[i-1]-V[i] < 0.0001): #non è detto sia giusto il valore
        v = V[i]
        ev = eV[i]
        b = False
        file2.write(str(v)+'\t')
        file2.write(str(ev)+'\t')
        file2.write('\n')
        print("_________________________________________________________")
        print("*********************************************************")
        print("---------------------------------------------------------")
    file.write(str(V[i])+'\t')
    file.write(str(eV[i])+'\t')
    file.write('\n')
    
    g.SetPoint(i,t,V[i])
    g.Draw("P")
    i += 1
    c.Modified()
    c.Update
    time.sleep(0.2)
    

    
    
    

"""
g = TGraphErrors()
c = TCanvas()
h = TH1D("h", "titolo" ,40 ,0., 0.)

c.Draw()
c.cd()

n =  200
for i in range(n):
    
    valV = 12
    cmd  = f'APPLY {valV},0.1'
    instr.write(cmd)
    
    
    V,eV = dmmread(ser)
    h.Fill(V)
    
V_medio = h.GetMean()
eV_medio = h.GetStdDev()

file.write(f'{V_medio}\t{eV_medio}')

"""



