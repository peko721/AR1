# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 10:25:18 2021

@author: ZhangW16
"""
'''
'''
import cv2
import matplotlib.pyplot as plt
import numpy as np

img = cv2.imread('C:/Users/zhangw16/Desktop/carrot.PNG')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,thresh1 = cv2.threshold(gray,50,255,cv2.THRESH_BINARY)
ret,thresh2 = cv2.threshold(gray,50,255,cv2.THRESH_BINARY_INV)
ret,thresh3 = cv2.threshold(gray,50,255,cv2.THRESH_TRUNC)
ret,thresh4 = cv2.threshold(gray,50,255,cv2.THRESH_TOZERO)
ret,thresh5 = cv2.threshold(gray,50,255,cv2.THRESH_TOZERO_INV)
titles = ['img','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
images = [img,thresh1,thresh2,thresh3,thresh4,thresh5]
for i in range(6):
    plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()

kernel = np.ones((5,5),np.uint8)
opening = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)
#根据阈值识别出分叉类型的胡萝卜
contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
cnt = contours[0]
plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
plt.imshow(cnt,'gray')
plt.show()




import cv2  

img = cv2.imread("./test.jpg")  

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  
ret, binary = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)  

contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)  
cv2.drawContours(img,contours,-1,(0,0,255),3)  

cv2.imshow("img", img)  
cv2.waitKey(0)



















import cv2
import numpy as np

#读取原图像
img=cv2.imread('C:/Users/zhangw16/Desktop/CARR.PNG')

b,g,r=cv2.split(img)
r[r>=230]=255
g[g>=230]=255
b[b>=230]=255
#r[r<=10]=0
#g[g>=10]=0
#b[b>=10]=0

delete_row=[]
delete_column=[]

for i in range(r.shape[0]):
    if r[i].var()==0:
        delete_row.append(i)
        
for j in range(r.shape[1]):
    if r[:,j].var()==0:
        
        delete_column.append(j)

b=np.delete(b,delete_row,axis=0)
b=np.delete(b,delete_column,axis=1)  
g=np.delete(g,delete_row,axis=0)
g=np.delete(g,delete_column,axis=1)  
r=np.delete(r,delete_row,axis=0)
r=np.delete(r,delete_column,axis=1)        

imgq = cv2.merge([b, g, r])
rows, cols= imgq.shape[:2]
img=cv2.resize(img,(216,288))
#cv2.namedWindow("imgq", cv2.WINDOW_NORMAL)
#cv2.resizeWindow("imgq", rows, cols)        
#cv2.imshow("imgq", imgq)
#cv2.imwrite('C:\\Users\\zhangw16\\Desktop\\O.PNG',cnt)

#读取灰度图像
img2 = cv2.imread('C:/Users/zhangw16/Desktop/CARR.PNG',0)
img2=cv2.resize(img2,(216,288))
#cv2.imshow("img1", img1)
#使用中值滤波
#img2 = cv2.medianBlur(img1,39)
#cv2.imshow("img2", img2)
#二值化
ret,thresh1=cv2.threshold(img2,50,255,cv2.THRESH_BINARY)
#形态学运算中的开运算（opening）:先腐蚀再膨胀
kernel = np.ones((5,5),np.uint8)
#cv2.MORPH_CLOSE 
opening = cv2.morphologyEx(thresh1,cv2.MORPH_OPEN, kernel)
cv2.imshow('opening', opening)
cv2.waitKey(0)
cv2.destroyAllWindows()
#根据阈值识别出分叉类型的胡萝卜
contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
#cv2.drawContours(img,contours,0,(0,0,255),3)  



cnt = contours[0]
bounding_boxes = [cv2.boundingRect(cnt) for cnt in contours]

#for bbox in bounding_boxes:
#     [x , y, w, h] = bbox
#     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

#cv2.imshow("name", img)
#cv2.waitKey(0)



cnt = contours[0]
rect = cv2.minAreaRect(cnt)
box = cv2.boxPoints(rect)
box = np.int0(box)
#cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
x,y,w,h = cv2.boundingRect(cnt) #（x,y）是旋转的边界矩形左上角的点，w ,h分别是宽和高

o1,o2 = rect[0]
o1 = int(o1)
if w < h:
    angle = int(rect[2])
    M = cv2.getRotationMatrix2D((o1, o2), angle, 1)
    rows, cols = img.shape[:2]
    print('left')
# print(rows,cols)
    dst = cv2.warpAffine(img, M, (cols, rows))
if w > h:
    angle = 90 + int(rect[2])
    M = cv2.getRotationMatrix2D((o1, o2), angle, 1)
    rows, cols = img.shape[:2]
    # print(rows,cols)
    dst = cv2.warpAffine(img, M, (cols, rows))
    print('right')
img=cv2.resize(img,(216,288))
dst=cv2.resize(dst,(216,288))
cv2.imwrite('C:\\Users\\zhangw16\\Desktop\\O.PNG',dst)