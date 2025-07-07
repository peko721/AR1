# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 10:49:47 2025

@author: ZhangW16
"""

import pandas as pd
import numpy as np

# 假设你的 DataFrame 已经存在，并命名为 df
# df 有两列 'x' 和 'y'，表示坐标
# 这里使用随机数据生成示例 DataFrame
#有个表格735行2列 记录的是一个21行35列的圆点坐标。
#从一个坐标开始，找到跟这个坐标距离最近的2个坐标 
#然后从这两个坐标里选行坐标接近的点。直到选够35个为止
dfLeft = pd.read_excel(r'C:\\Users\\zhangw16\\OneDrive - Corning Incorporated\\Desktop\\Left421.xlsx')
dfRight = pd.read_excel(r'C:\\Users\\zhangw16\\OneDrive - Corning Incorporated\\Desktop\\Right421.xlsx')
is_divisible = lambda a, b: b != 0 and a % b == 0
rows=21
cols=35
def euclidean_distance(coord1, coord2):
    return np.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

def find_nearest_neighbors(df, current_point, num_neighbors=2):
    distances = df.apply(lambda row: euclidean_distance(current_point, (row['x'], row['y'])), axis=1)
    nearest_indices = distances.nsmallest(num_neighbors).index
    return nearest_indices

def select_points(df, num_points=35):
    selected_xy = np.zeros((rows, cols, 2)) 
    start_index = 0
    rowindex=0
    columindex=0
    selected_xy[rowindex, columindex] = (df.loc[0, 'x'], df.loc[0, 'y'])

    selected_indices = [start_index]
    current_index = start_index
    while(len(df)>2):
        while not is_divisible(len(selected_indices),35) and len(df)>2:
            if columindex==15:
                V=1
            current_point = (df.loc[current_index, 'x'], df.loc[current_index, 'y'])
            df = df.drop(current_index).reset_index(drop=True)
            # 找到最近的2个邻居
            neighbors_indices = find_nearest_neighbors(df, current_point)
            if len(selected_indices)<701:
                # 从邻居中选择行坐标接近的那个点
                if abs(df.loc[neighbors_indices[0], 'x'] - current_point[0]) < abs(df.loc[neighbors_indices[1], 'x'] - current_point[0]):
                    next_index = neighbors_indices[0]
                else:
                    next_index = neighbors_indices[1]
            else:
                if abs(df.loc[neighbors_indices[0], 'y'] - current_point[1]) < abs(df.loc[neighbors_indices[1], 'y'] - current_point[1]):
                    next_index = neighbors_indices[0]
                else:
                    next_index = neighbors_indices[1]
    
            # 添加到已选择的点
            selected_indices.append(next_index)
            current_index = next_index
            if columindex==34 or columindex==0:
                v=1
            
            if rowindex % 2 == 0:
                if columindex<34:
                    columindex=columindex+1
            if rowindex % 2 != 0:
                if columindex>0:
                    columindex=columindex-1
            selected_xy[rowindex, columindex] = (df.loc[next_index, 'x'], df.loc[next_index, 'y'])

        while is_divisible(len(selected_indices),35) and len(df)>2:
            if len(selected_indices)==700:
                V=1
            current_point = (df.loc[current_index, 'x'], df.loc[current_index, 'y'])
            df = df.drop(current_index).reset_index(drop=True)
            # 找到最近的2个邻居
            neighbors_indices = find_nearest_neighbors(df, current_point)
            
            # 从邻居中选择行坐标接近的那个点
            if abs(df.loc[neighbors_indices[0], 'y'] - current_point[1]) < abs(df.loc[neighbors_indices[1], 'y'] - current_point[1]):
                next_index = neighbors_indices[0]
            else:
                next_index = neighbors_indices[1]
    
            # 添加到已选择的点
            selected_indices.append(next_index)
            current_index = next_index
            if columindex==34 or columindex==0:
                columindex=0
                rowindex=rowindex+1
                if rowindex % 2 != 0:
                    columindex=34
            selected_xy[rowindex, columindex] = (df.loc[next_index, 'x'], df.loc[next_index, 'y'])

    # 返回选择的坐标点
    if len(df)<3:
        #偶数行是反着走的 奇数行是正着走的 总共21行 所以最后一行正着走的 那就是先append 列坐标小的
        if df.loc[0, 'y']<df.loc[1, 'y']:
            # 添加到已选择的点
            selected_xy[rowindex, columindex] = (df.loc[0, 'x'], df.loc[0, 'y'])
            selected_xy[rowindex, columindex+1] = (df.loc[1, 'x'], df.loc[1, 'y'])
         
        else:
            selected_xy[rowindex, columindex] = (df.loc[1, 'x'], df.loc[1, 'y'])
            selected_xy[rowindex, columindex+1] = (df.loc[0, 'x'], df.loc[0, 'y'])
            
    return selected_xy,df

# 假设从第一个点开始
selected_xy_Left,dfLeft= select_points(dfLeft)
selected_xy_Right,dfRight= select_points(dfRight)



import numpy as np

# 定义纸张和圆的参数
paper_width = 700  # 宽度
paper_height = 420  # 高度
diameter = 10  # 圆的直径
spacing = 20  # 圆之间的间距（等于直径）

# 计算圆心的坐标
rows = 21
cols = 35

# 初始化矩阵来存储圆心的坐标
circle_centers = np.zeros((rows, cols, 2))  # Shape: 21 x 35 x 2 (x, y)

for i in range(rows):
    for j in range(cols):
        y = 10 + j * spacing  # 左边缘距离加上列间距
        x = 10 + i * spacing  # 上边缘距离加上行间距
        circle_centers[i, j] = (x, y)
        
# 输入的坐标
point = np.array([2369,943])
plateedgpiexlshort=446
plateedgpiexlLength=992
# point = np.array([1361, 607])
# 计算所有圆心与该点的距离
distances_Left = np.sqrt((abs(selected_xy_Left - point) ** 2).sum(axis=2))
distances_Right = np.sqrt((abs(selected_xy_Right - point) ** 2).sum(axis=2))
# 找到距离最小的圆心
min_index_Left = np.unravel_index(np.argmin(distances_Left), distances_Left.shape)
min_index_Right = np.unravel_index(np.argmin(distances_Right), distances_Right.shape)
LEFTT=0
if distances_Left[min_index_Left[0],min_index_Left[1]]<distances_Right[min_index_Right[0],min_index_Right[1]]:
    
    nearest_center = selected_xy_Left[min_index_Left]
    min_index=min_index_Left
    offset=(490-plateedgpiexlshort)*0.25
    offset1=(985-plateedgpiexlLength)*0.25
    LEFTT=1
else:
    nearest_center = selected_xy_Right[min_index_Right]
    min_index=min_index_Right
    offset=(500-plateedgpiexlshort)*0.25
    offset1=(1000-plateedgpiexlLength)*0.25
# 输出结果
print(f"最近的圆心坐标是: {nearest_center}，位于第 {min_index[0] + 1} 行，第 {min_index[1] + 1} 列")
WoldXY=circle_centers[min_index[0],min_index[1]]
# pixlesize_X=10/piexlsize[0]
# pixlesize_Y=10/piexlsize[1]
pixlesize_X=0.25
pixlesize_Y=0.25
X=WoldXY[0]+(point[0]-nearest_center[0])*pixlesize_X+offset1
Y=WoldXY[1]+(point[1]-nearest_center[1])*pixlesize_Y+offset

if LEFTT==0:
    X=420-X
    Y=700-Y





