import pandas as pd
import numpy as np
import pyoc_utils as pdu
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt



chemsys = pd.read_excel('HEA_Mn_alloys_0.99.xlsx',sheet_name='Sheet1')
element_list = ['Cr','Fe','Mn','Ni'] # [O,A,B,C]

tet_coords = np.array([])
T = 873.0
for i, stable_alloy in enumerate(chemsys[str(T) + ' K']):
    if stable_alloy is 'Y':
        if tet_coords.any():
            tet_coords = np.append(tet_coords, [[
                       chemsys['Fe (at %)'][i]/100.0, 
                       chemsys['Mn (at %)'][i]/100.0, 
                       chemsys['Ni (at %)'][i]/100.0
                       ]], axis=0) # [comp_OA, comp_OB, comp_OC]
        else:
            tet_coords = np.array([[
                       chemsys['Fe (at %)'][i]/100.0, 
                       chemsys['Mn (at %)'][i]/100.0, 
                       chemsys['Ni (at %)'][i]/100.0
                       ]])

fig = plt.figure()
pdu.plot_tetrahedron(fig, element_list)
pdu.scatter_compositions_at_one_temperature(fig, tet_coords, T)
plt.show()
