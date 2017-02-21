#!/usr/bin/env python

from sys   import stdin
from numpy import *
from math import *
import numpy as np
import subprocess
import warnings
import os.path
import shutil
import copy
import math
import sys
import os

#def __init__(self):
#    self.energy = []
#    self.eta = []

os.chdir('../../test/examples/elastic')

#INFO=open('../../test/examples/elastic/INFO_ElaStic', 'r')
INFO=open('INFO_ElaStic', 'r')

l1  = INFO.readline()
ordr= int(l1.split()[-1])

l2  = INFO.readline()
mthd= l2.split()[-1]

l3  = INFO.readline()
cod = l3.split()[-1]

l4  = INFO.readline()
SGN = int(l4.split()[-1])

l5  = INFO.readline()
V0  = float(l5.split()[-2])

l6  = INFO.readline()
mdr = float(l6.split()[-1])

l7  = INFO.readline()
NoP = int(l7.split()[-1])

INFO.close()

'''
###### The number of independent elastic constants is calculated and then checked ######
###### whether it corresponds to the number of "Dst--" folders ######
#
if (1 <= SGN and SGN <= 2):      # Triclinic
    LC = 'N'
    if (ordr == 2): ECs = 21
    if (ordr == 3): ECs = 56

elif(3 <= SGN and SGN <= 15):    # Monoclinic
    LC = 'M'
    if (ordr == 2): ECs = 13
    if (ordr == 3): ECs = 32

elif(16 <= SGN and SGN <= 74):   # Orthorhombic
    LC = 'O'
    if (ordr == 2): ECs =  9
    if (ordr == 3): ECs = 20

elif(75 <= SGN and SGN <= 88):   # Tetragonal II
    LC = 'TII'
    if (ordr == 2): ECs =  7
    if (ordr == 3): ECs = 16

elif(89 <= SGN and SGN <= 142):  # Tetragonal I
    LC = 'TI'
    if (ordr == 2): ECs =  6
    if (ordr == 3): ECs = 12

elif(143 <= SGN and SGN <= 148): # Rhombohedral II 
    LC = 'RII'
    if (ordr == 2): ECs =  7
    if (ordr == 3): ECs = 20

elif(149 <= SGN and SGN <= 167): # Rhombohedral I
    LC = 'RI'
    if (ordr == 2): ECs =  6
    if (ordr == 3): ECs = 14

elif(168 <= SGN and SGN <= 176): # Hexagonal II
    LC = 'HII'
    if (ordr == 2): ECs =  5
    if (ordr == 3): ECs = 12

elif(177 <= SGN and SGN <= 194): # Hexagonal I
    LC = 'HI'
    if (ordr == 2): ECs =  5
    if (ordr == 3): ECs = 10

elif(195 <= SGN and SGN <= 206): # Cubic II
    LC = 'CII'
    if (ordr == 2): ECs =  3
    if (ordr == 3): ECs =  8

elif(207 <= SGN and SGN <= 230): # Cubic I
    LC = 'CI'
    if (ordr == 2): ECs = 3
    if (ordr == 3): ECs = 6

'''
i = 1
while 1:
    if (i<10):
        Dstn = 'Dst0'+ str(i)
        if (os.path.exists(Dstn) == True):
           i += 1
        else:
           break
    else:
        Dstn = 'Dst' + str(i)
        if (os.path.exists(Dstn) == True):
           i += 1
        else:
           break

defNum = i - 1
ECs = defNum

#if defNum != ECs:
#    print("Error")
energy = []
eta = []

for j in range(1, ECs+1):
    if (j<10):
        Dstn = 'Dst0'+ str(j)
        eta.append([])
        energy.append([])
    else:
        Dstn = 'Dst' + str(i)
        eta.append([])
        energy.append([])

    os.chdir(Dstn)

    f = open(Dstn+'-Energy.dat', 'r')
    while 1:
       s = f.readline()
       print("s=",s)
       if not s: break
       s = s.strip()
       dummy_eta, dummy_energy = s.split()
       eta[-1].append(float(dummy_eta))
       energy[-1].append(float(dummy_energy))
    os.chdir('../')

defTyp = []

f = open('Distorted_Parameters','r')

while 1:
    s = f.readline()
    if not s: break
    s = s.strip()
    if 'Lagrangian' in s:
        defTyp.append([])
        s = s.split("(")
        s = s[-1].split(")")
        s = s[0].split(",")
        for i in range(0,6):
            s[i] = s[i].strip()
            if s[i] == '0.0':
                defTyp[-1].append(float(s[i]))
            elif s[i] == 'eta':
                defTyp[-1].append(mdr)
            elif s[i] == '2eta':
                defTyp[-1].append(2.0*mdr)
            elif s[i] == '-eta':
                defTyp[-1].append(-mdr)
            elif s[i] == '.5eta':
                defTyp[-1].append(0.5*mdr)
            elif s[i] == '-2eta':
                defTyp[-1].append(-2.0*mdr)
            elif s[i] == '3eta':
                defTyp[-1].append(3.0*mdr)
            elif s[i] == '4eta':
                defTyp[-1].append(4.0*mdr)
            elif s[i] == '5eta':
                defTyp[-1].append(5.0*mdr)
            elif s[i] == '6eta':
                defTyp[-1].append(6.0*mdr)
            elif s[i] == '-3eta':
                defTyp[-1].append(-3.0*mdr)
            elif s[i] == '-5eta':
                defTyp[-1].append(-5.0*mdr)
            elif s[i] == '-6eta':
                defTyp[-1].append(-6.0*mdr)
            elif s[i] == '-4eta':
                defTyp[-1].append(-4.0*mdr)

f.close()

os.chdir('Energy-vs-Strain')

d2E6_val = []
d2E4_val = []
d2E2_val = []
d2E6_eta = []
d2E4_eta = []
d2E2_eta = []
d2E_val_tot = []
d2E_eta_tot = []

for i in range(1, ECs+1):
    d2E_val_tot.append([])
    d2E_eta_tot.append([])
    if (i<10):
        Dstn = 'Dst0'+ str(i) + '_d2E.dat'
        f = open (Dstn,'r')
        while 1:
            s = f.readline()
            if not s: break
            s = s.strip()
            if "order" in s.split():
                d2E_val_tot[-1].append([])
                d2E_eta_tot[-1].append([])
            elif len(s) >= 30:
                d2E_eta, d2E_values = s.split()
                d2E_val_tot[-1][-1].append(float(d2E_values))
                d2E_eta_tot[-1][-1].append(float(d2E_eta))
        f.close()
    else:
        Dstn = 'Dst' + str(i) + '_d2E.dat'
        f = open (Dstn,'r')
        while 1:
            s = f.readline()
            if not s: break
            s = s.strip()
            if "order" in s.split():
                d2E_val_tot[-1].append([])
                d2E_eta_tot[-1].append([])
            elif len(s) >= 30:
                d2E_eta, d2E_values = s.split()
                d2E_val_tot[-1][-1].append(float(d2E_values))
                d2E_eta_tot[-1][-1].append(float(d2E_eta))
        f.close()
    d2E6_val.append(d2E_val_tot[i-1][0])
    d2E4_val.append(d2E_val_tot[i-1][1])
    d2E2_val.append(d2E_val_tot[i-1][2])
    d2E6_eta.append(d2E_eta_tot[i-1][0])
    d2E4_eta.append(d2E_eta_tot[i-1][1])
    d2E2_eta.append(d2E_eta_tot[i-1][2])

CrossVal6_val = []
CrossVal4_val = []
CrossVal2_val = []
CrossVal_val_tot = []

CrossVal6_eta = []
CrossVal4_eta = []
CrossVal2_eta = []
CrossVal_eta_tot = []

for i in range(1, ECs+1):
    CrossVal_val_tot.append([])
    CrossVal_eta_tot.append([])
    if (i<10):
        DstnCV = 'Dst0'+ str(i) + '_CVe.dat'
        f = open (DstnCV,'r')
        while 1:
            s = f.readline()
            if not s: break
            s = s.strip()
            if "order" in s.split():
                CrossVal_val_tot[-1].append([])
                CrossVal_eta_tot[-1].append([])
            elif len(s) >= 20 and s.split()[0] != '#':
                CrossVal_eta, CrossVal_values = s.split()
                CrossVal_val_tot[-1][-1].append(float(CrossVal_values))
                CrossVal_eta_tot[-1][-1].append(float(CrossVal_eta))
        f.close()
    else:
        DstnCV = 'Dst' + str(i) + '_CVe.dat'
        f = open (Dstn,'r')
        while 1:
            s = f.readline()
            if not s: break
            s = s.strip()
            if "order" in s.split():
                CrossVal_val_tot[-1].append([])
                CrossVal_eta_tot[-1].append([])
            elif len(s) >= 20 and s.split()[0] != '#':
                CrossVal_eta, CrossVal_values = s.split()
                CrossVal_val_tot[-1][-1].append(float(CrossVal_values))
                CrossVal_val_tot[-1][-1].append(float(CrossVal_values))
        f.close()
    CrossVal6_val.append(CrossVal_val_tot[i-1][0])
    CrossVal4_val.append(CrossVal_val_tot[i-1][1])
    CrossVal2_val.append(CrossVal_val_tot[i-1][2])
    CrossVal6_eta.append(CrossVal_eta_tot[i-1][0])
    CrossVal4_eta.append(CrossVal_eta_tot[i-1][1])
    CrossVal2_eta.append(CrossVal_eta_tot[i-1][2])

os.chdir('../')

f = open ('ElaStic_'+str(ordr)+'nd.in','r')

etaEC = []
fitEC = []
for i in range(1, ECs+1):
    s = f.readline()
    s = s.strip()
    dummy, etaEC_dummy, fitEC_dummy = s.split()
    etaEC.append(etaEC_dummy)
    fitEC.append(fitEC_dummy)

f = open ('ElaStic_'+str(ordr)+'nd.out','r')

allMat = [[],[],[],[],[],[]]
voigtMat = [[],[],[],[],[],[]]
ECMat = [[],[],[],[],[],[]]
complMat = [[],[],[],[],[],[]]

while 1:
    s = f.readline()
    if not s: break
    s = s.strip()
    s = s.split()
    if len(s) == 1:
        try: float(s[0])
        except ValueError:
            continue
        else:
            EC_eigen = float(s[0])
    elif "B_V" in s:
        B_V = float(s[5])
    elif "G_V" in s:
        G_V = float(s[5])
    elif "B_R" in s:
        B_R = float(s[5])
    elif "G_R" in s:
        G_R = float(s[5])
    elif "B_H" in s:
        B_H = float(s[5])
    elif "G_H" in s:
        G_H = float(s[5])
    elif "E_V" in s:
        E_V = float(s[5])
    elif "nu_V" in s:
        nu_V = float(s[5])
    elif "E_R" in s:
        E_R = float(s[5])
    elif "nu_R" in s:
        nu_R = float(s[5])
    elif "E_H" in s:
        E_H = float(s[5])
    elif "nu_H" in s:
        nu_H = float(s[5])
    elif len(s) == 6 and s[0] != "Elastic" and s[0] != "Eigenvalues":
        for i in range(0,6):
            allMat[i].append(s[i])
    elif "AVR" in s:
        AVR = float(s[6])

f.close()

for i in range(0,6):
    voigtMat[i] = allMat[i][0:6]
    ECMat[i] = allMat[i][6:12]
    complMat[i] = allMat[i][12:18]

for i in range(0,6):
    for j in range(0,6):
        ECMat[i][j] = float(ECMat[i][j])
        complMat[i][j] = float(complMat[i][j])

