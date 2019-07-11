import pandas as pd
import numpy as np
from libocpy import *
import random
import time

print('Hello there!')
print('This example screens stable FCC-CrFeMnNi alloys using SSOL2 (saf2507.tdb)')
print('One can find how error returned from tqce() handled. The error most of')
print('the time is 4204, i.e. Too many iteractions. Slight change of T and/or X')
print('can fix this error. *** Mind: error (> 0) must always be handled by user.')
print('OpenCALPHAD (as of version 5) does not handle these errors effectively!!!')

time.sleep(60)

chemsys = pd.read_excel('HEA_alloy.xlsx',sheetname='Sheet1')
element_list = []
for key in list(chemsys.keys()):
    element_list.append(key.split()[0].upper())

np_crit = 0.99
T = np.linspace(573.0,2273.0,18)
stable_alloys = []
for it in range(len(T)):
    is_stable_fcc = []
    for ic in range(len(chemsys[chemsys.columns[0]])):
        error = 1.0
        attempt_to_fix_error = 0
        while error > 0.0:
            tqini()
            tqrpfil('SAF.TDB',element_list)
            tqsetc('N',0,1.0)
            tqsetc('P',0,1e5)
            print('set T('+str(T[it])+'K)')
            tqsetc('T',0,T[it] + attempt_to_fix_error*float(random.randint(0,10))/10000.)
            for key in list(chemsys.keys())[:-1]:
                print('set X('+key.split()[0]+'='+str(float(chemsys[key][ic])/100.0)+')')
                tqsetc('X',key.split()[0],float(chemsys[key][ic])/100.0 + attempt_to_fix_error*float(random.randint(0,10))/1000000.)
            error = tqce()
            attempt_to_fix_error = attempt_to_fix_error + 1
            tqrseterr()
            if attempt_to_fix_error >= 10:
                print('Error in calling tqce!')
                exit()
        if tqgetv('NP','FCC','NA') >= np_crit:
            is_stable_fcc.append('Y')
        else:
            is_stable_fcc.append('')
        tqrseterr()
    stable_alloys.append(is_stable_fcc)

for i in range(len(T)):
    chemsys.insert(4+i,str(T[i])+' K', stable_alloys[i])
chemsys.to_excel('HEA_alloys_'+str(np_crit)+'.xlsx',sheet_name='Sheet1')
