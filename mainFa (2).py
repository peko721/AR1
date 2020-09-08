# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 18:31:46 2020

@author: Administrator
"""




from ratter import *
import numpy as np
from sympy import conjugate
def aimfunc(variable, CV,sall,Me,Del_Measure):
 f=np.zeros([3,1])
 for c in range(3):
  result_R=[]
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

    d1=variable[c,0]
    d2=variable[c,1]
    d3=variable[c,2]
    d4=variable[c,3]
    reflectivity_values = np.real(R_of_coating_thickness(d1,d2,d3,d4))
    result_R.append(reflectivity_values)#reflectivity_values = np.real(R_of_coating_thickness(d1,d2,d1,d2))
  deltsum=0
  for i in range(0,len(Me.loc[:,'R'])):
    deltsum+=((result_R[i]-Me.loc[i,'R'])/Del_Measure[i])**2  
  f[c,0]=(deltsum/len(Me.loc[:,'R']))**(0.5)
 return [f, CV]
 
 
 