# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 10:06:08 2020

@author: ZhangW16
"""
import os
import xlwt
file_dir=r'C:\Users\zhangw16\Pictures\GEO' # ----- 调整目录实际路径
#os.remove(ic+'v '+STRILZ+'._1310B.sor')# filename: "要删除的文件名"
path='C:\\Users\\zhangw16\\Pictures\\GEO\\GEO.xls'# ----- 存成低版本Excel
xls=xlwt.Workbook()
sheet = xls.add_sheet('sheet1',cell_overwrite_ok=True) 
row1=0
U=os.listdir('C:\\Users\\zhangw16\\Pictures\\GEO')
row=-1
#PDI=pd.read_excel('C:\\Users\\zhangw16\\Music\\A\\PDI.xls', index_col=None, na_values=['NA'])   
out=list()  
sheet.write(0, 0, 'Reel ID')
sheet.write(0, 1, 'Diameter1')
sheet.write(0, 2, 'Ovality1')
sheet.write(0, 3, 'Concentricity1')
sheet.write(0, 4, 'Diameter2')
sheet.write(0, 5, 'Ovality2')
sheet.write(0, 6, 'Concentricity2')
sheet.write(0, 7, 'Diameter3')
sheet.write(0, 8, 'Ovality3')
sheet.write(0, 9, 'Concentricity3')
sheet.write(0, 10, 'Diameter4')
sheet.write(0, 11, 'Ovality4')
sheet.write(0, 12, 'Concentricity4')
f='q'
search = 'v'     
start = 0     
index = f.find(search, start) 
    #LotID=f[0:index]#怎么不从第一个做起呢，把PDI放进另一个文件夹中
lastID= f[0:index]
i=0
while len(U)>1: 
    f=U[0]
    row=row+1
    #txtpath='C:\\Users\\zhangw16\\Pictures\\spc' +f
    search = 'v'     
    start = 0     
    index = f.find(search, start) 
    #LotID=f[0:index]#怎么不从第一个做起呢，把PDI放进另一个文件夹中
    NowID= f[0:index]
    if NowID==lastID:
       os.remove('C:\\Users\\zhangw16\\Pictures\\GEO\\'+f)# filename: "要删除的文件名" 
    else:
       k=1   
       kk=0
       i=i+1
       while k<=4:
        if kk>len(U)-1:
           break
        else:
         f=U[kk]
         txtpath='C:\\Users\\zhangw16\\Pictures\\GEO\\' +f 
         file = open(txtpath,'r',encoding = "utf8")  
         record=file.readlines()
         if len(record)>24:
    # 2.将所有txt存到Excel的sheet1中
          lineID=record[1]
          lineD=lineID.rstrip('\n').split(',') 
          FwLOT=lineD[1][1:len(lineD[1])]
          if FwLOT==NowID:
           lineDiameter=record[10]
           lineOvality=record[24]
           lineConcentricity=record[20]
           lineD1=lineDiameter.rstrip('\n').split(',')
           lineO1=lineOvality.rstrip('\n').split(',')
           lineC1=lineConcentricity.rstrip('\n').split(',')
           sheet.write(i, 0, lineD[1])
        #将整行数据分割，如分割符是空格，括号里不传入参数，如是逗号， 则传入‘，'字符
           sheet.write(i, (k-1)*3+1, lineD1[1])
           sheet.write(i, (k-1)*3+2, lineO1[1])
           sheet.write(i, (k-1)*3+3, lineC1[1])
           k=k+1
          else:
           break
         else:
          file.close()
         kk=kk+1
         file.close()
         os.remove('C:\\Users\\zhangw16\\Pictures\\GEO\\'+f)# filename: "要删除的文件名" 
        lastID=NowID
    U=os.listdir('C:\\Users\\zhangw16\\Pictures\\GEO')
xls.save(path)  
