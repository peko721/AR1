# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 21:28:18 2020

@author: ZhangW16
"""

from ratter import *
from sympy import conjugate
import numpy as np
import pandas as pd
sall=pd.read_excel('C:\\Users\\zhangw16\\Desktop\\Re.xlsx', index_col=None, na_values=['NA'])
result_R=[]
j=0
for k in range(len(sall.loc[:,"R"])):
    wavelength =sall.loc[k,"W"] # length units: nm   
    Re=sall.loc[k,'R']
# define materials with their refractive index at the wavelength
    Si = Material('Si', refractive_index_value=1.511)  # Green 2008
    air = Material('air', refractive_index_value=1.0) # Ciddor 1996
    SiO2 = Material('SiO2', refractive_index_value=1.46) # Malitson 1965
    AlOx = Material('Al2O3', refractive_index_value=Re) # Malitson and Dodge 1972

# define the layers
    environment = Layer('env', air)
    coating1 = Layer('coat1', SiO2)
    coating2 = Layer('coat2', AlOx)
    coating3 = Layer('coat3', SiO2)
    coating4 = Layer('coat4', AlOx)
    bulk = Layer('bulk', Si)

# define the order of materials
    stack = Layerstack([environment,coating1,coating2,coating3,coating4, bulk])

# calculate absolute reflectivity R
    r = stack.reflectance_amplitude()
    R = conjugate(r)*r

# substitute symbols with numbers
    R_ = R.subs(LAMBDA_VAC, wavelength)

# create a vectorized numpy function out of symbolic definition
    R_of_coating_thickness = as_function_of(R_, [coating1.thickness_symbol,
                                                 coating2.thickness_symbol,
                                                 coating3.thickness_symbol,
                                                 coating4.thickness_symbol])

    d1=50
    d2=50
    reflectivity_values = np.real(R_of_coating_thickness(50,50,50,50))
    result_R.append(reflectivity_values)#reflectivity_values = np.real(R_of_coating_thickness(d1,d2,d1,d2))
"""
import numpy as np
import matplotlib.pyplot as plt

d1 = np.arange(0,50)

for d2 in [50,200,500]:
    reflectivity_values = np.real(R_of_coating_thickness(d1,d2,d2,d2))
    plt.plot(d1, reflectivity_values, label='{}'.format(d2))

plt.legend(title='$Al_2O_3$ thickness (nm)')
plt.ylabel('reflectivity')
plt.xlabel('$SiO_2$ thickness (nm)')
"""