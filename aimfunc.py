# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 18:31:46 2020

@author: Administrator
"""


import pandas as pd
sall=pd.read_excel('C:\\Users\\zhangw16\\Desktop\\Re.xlsx', index_col=None, na_values=['NA'])
Me=pd.read_excel('C:\\Users\\zhangw16\\Desktop\\Measurement.xlsx', index_col=None, na_values=['NA'])
Del_Measure=[]
for k in range(0,len(Me.loc[:,'R'])):
    Del_Measure.append(0.00001)     #%对应波点光谱反射率容差 

from ratter import *
from sympy import conjugate
import numpy as np
result_R=[]
Va=[50,50,50,50]
CV=[]
def aimfunc(Va, CV):
 f=np.zeros([100,1])
 for c in range(3):
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

    d1=Va[0]
    d2=Va[2]
    d3=Va[3]
    d4=Va[0]
    reflectivity_values = np.real(R_of_coating_thickness(d1,d2,d3,d4))
    result_R.append(reflectivity_values)#reflectivity_values = np.real(R_of_coating_thickness(d1,d2,d1,d2))
  deltsum=0
  for i in range(0,500):
    deltsum+=((result_R.append(i)-Me.loc[i,'R'])/Del_Measure[i])**2  
  f[c,0]=(deltsum/500)**(0.5)
 return [f, CV]
 
 
 