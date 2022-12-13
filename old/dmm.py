#!/usr/bin/python


## modulo per il multimetro 


import time
import serial
    
def dmmread(ser):
    # Lettura del valore
    command(ser, 'val1?')
    time.sleep(.5)
    line = ser.readline()
    val  = line.decode('ascii').split()
    fval = float(val[0])
    reset(ser)
    
    # Lettura del range
    command(ser,'range1?')
    time.sleep(.5)
    line  = ser.readline()
    ival  = line.decode('ascii').split()
    ind = int(ival[0])-1
    reset(ser)
    
    

    error = 0
    if val[1]=="ADC":
        range = [ 0.000200, 0.002000 , 0.020 ,  0.200,  2    , 10  ]
        rel   = [ 0.03    , 0.02    , 0.04  ,  0.03 ,  0.08 , 0.20 ]
        relr  = [ 0.005   , 0.005    , 0.02  ,  0.008,  0.02 , 0.01 ]
        error = abs(fval*rel[ind]/100) + relr[ind]/100*range[ind]
    elif val[1]=="VDC":
        range = [ 0.200,     2 ,    20,  200 ,  1000]
        rel   = [ 0.015 ,  0.015 , 0.015 , 0.015 ,  0.015]
        relr  = [ 0.004,  0.003, 0.004, 0.003, 0.003]  
        error = abs(fval*rel[ind])/100 + relr[ind]/100*range[ind]
    elif val[1]=="OHMS":
        range = [ 200,     2e3 ,    20e3,  200e3 ]
        rel   = [ 0.03 ,  0.02 , 0.02 , 0.02 ]
        relr  = [ 0.004,  0.003, 0.003, 0.003]
        error = abs(fval*rel[ind])/100 + relr[ind]/100*range[ind] + 0.2

    return fval,error
                     
def reset(ser):
    ser.reset_input_bufer()
    ser.reset_output_buffer()
    
def command(ser, string):
    
    string = string + '\r\n'
    ser.write(string.encode())
    time.sleep(1)
    
       
