#!/usr/bin/python
    
import sys,serial
from dmm import *
from ps  import *
from ROOT import *
import time
from uncertainties import ufloat

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
file = open('out_2.dat','w') #questo dovrebbe avere tutti i punti misurati

#seriale
ser = serial.Serial('COM2', 9600)

instr = psinit("USB0::0x0AAD::0x0135::035375056::INSTR")
#Selezione canale 1
pssel(instr,1)
#Erogazione di 12 V per caricare il condensatore 
valV = 12
cmd  = f'APPLY {valV},0.1'
instr.write(cmd)


R = ufloat(1000,20)


'''
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
    if (V[i-1]-V[i] < 0.0001):
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
'''
    
app = TApplication("app",0,NULL)    

g = TGraphErrors()
c = TCanvas()

c.Draw()
c.cd()
c.DrawFrame(0, 0, 6, 100);

n =  200
valV = 0.1
for i in range(n):

    #setto la tenisone
    cmd  = f'APPLY {valV},0.1'
    instr.write(cmd)
    time.sleep(0.5)

    #leggo la tensione e calcolo la coreente con il suo errore
    v,ev = dmmread(ser)
    time.sleep(0.3)
    V = ufloat(v,ev)
    corrente = V/R
    I = corrente.n
    eI = corrente.s
    valV += 0.1
    
    #scrivo sul file
    file.write(f'{v}\t{ev}\t{I}\t{eI}')

    
    #setto i punti del grafico e lo disegno
    g.SetPoint(i,v,I)
    g.SetPointError(i,ev,eI)
    g.Draw("P")

    c.Modified()
    c.Update()






app.Run(True)




