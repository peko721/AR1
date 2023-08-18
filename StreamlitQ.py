# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 16:18:53 2023

@author: gux9
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#from datetime import datetime
import datetime

# 侧边栏
st.sidebar.title('请选择过滤条件')
date = st.sidebar.date_input('大于日期', datetime.datetime(2023,8,13,13,30,0,0))
time = st.sidebar.time_input('大于时间', datetime.datetime(2023,8,13,13,30,0,0))
filter= datetime.datetime.combine(date, time)
 
# 主栏
st.title('XYC Kanban')
#@st.cache(persist=True)
def get_data():
    file = r'C:\Cutter\bar.xlsx'
    return pd.read_excel(file, header=0)
df = get_data()
# print(values)
df = df[df['Time'] > str(filter)]

 
colorsumaey=['b','b','b']
colorS=[]
bottomS=df.iloc[:,1]
fig, ax = plt.subplots(figsize=(8, 6))
alphaS=[0.5,0.6,0.7]
for i in range(df.shape[1]-1):
    if i>0:
        for c in range(df.shape[1]-1):
            colorS.append('w')
        colorS[i]=colorsumaey[i]
        if i>1:
             for k in range(i,i+1):
                bottomS=bottomS+ df.iloc[:,i]
        ax.bar(df.iloc[:,0].astype(str), df.iloc[:,i+1],bottom=bottomS,label=df.columns[i+1],color=colorS,alpha=alphaS[i])
    else:
        for c in range(df.shape[1]-1):
            colorS.append('w')
        colorS[i]=colorsumaey[i]
        ax.bar(df.iloc[:,0].astype(str), df.iloc[:,i+1],label=df.columns[i+1],color=colorS,alpha=alphaS[i])
# ax.bar(df['Time'].astype(str), df['LiAuto'],label='LiAuto',color=['r','w','w'],alpha=0.8)
# ax.bar(df['Time'].astype(str), df['BMW'], bottom=df['LiAuto'], label='BMW',color=['w','g','w'],alpha=0.8)
# ax.bar(df['Time'].astype(str), df['Geely'], bottom=df['LiAuto'] + df['BMW'],label='Geely',color=['w','w','b'],alpha=0.8)


ax.set_xlabel('Time')
ax.set_ylabel('Pcs')
ax.set_title('XYC 105 Pcs Over Time')
ax.legend()


plt.xticks(df['Time'].astype(str),rotation=90,size=8)

# 在Streamlit中显示图表
st.pyplot(fig)

def get_data():
    file = r'C:\Cutter\CTS_workcount.xlsx'
    return pd.read_excel(file)
df1 = get_data()
# print(values)

df1=df1[df1['recipe']!='']
df1=df1.dropna()
df1=df1.drop_duplicates(['recipe'], keep='last')
df1=df1.drop(columns=['Time'])
df1=df1.drop(columns=['sheet_Count'])
df1=pd.DataFrame(df1,columns=['recipe','HFWR.XYC105.EQUIP_CUTTME'])
df1.style.set_properties(**{'background-color': 'black','color': 'green'})

st.write("### CT Data By Cutter ($105)", df1.sort_index())