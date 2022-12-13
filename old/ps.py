#!/usr/bin/python
##moudlo per il generatore

from   pyvisa import ResourceManager

def psinit(name):
    rm = ResourceManager()
    instr = rm.open_resource(name)
    return instr

def pssel(instr,ch):
    instsel = f"INST: NSEL {ch}"
    instout = f"INST OUT{ch}"
    instr.write(instsel)
    instr.write(instout)
    instr.write("OUTP ON")
