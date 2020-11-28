# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 19:29:35 2020

1. This code used to analysis AR carrier performance based on Ex situ color

Version 1.0
1. Check color (L/a/b) variation
2. Using isolation method identify outlier points - on going

Operation steps
1. Using ACAN software export that every day shift color data
   - setting right AR Ex situ start/end time (hours:minutes:second)
3. Double click AR Carrier Performance Compare V1.0
4. At the same folder will creat a need folder storage that every day shift 
   carrier performance. At the same time screen will output need pay more attention
   carrier information


@author: RuanY
"""
import pandas as pd
import time
import datetime
import plotly
import plotly.graph_objects as go
import PySimpleGUI as sg
#避免loop报错
import warnings
import os.path
#引用2020.06的avalibility he Performance
mm=6
sg.change_look_and_feel('TanBlue')	# Add a touch of color
# All the stuff inside your window.
#menu_def = [['Help', 'if you meet any problem, please contact PEx team.'], ]  
current=str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
warnings.filterwarnings("ignore")

github = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAAAAABWESUoAAAACXBIWXMAAA3XAAAN1wF\
CKJt4AAAByUlEQVQ4jW2TTUsbURiFn4wESTd+BbEUZyEoXZS6KZiV0K5LtgFBBX9BQdwU3LnrKiAILT\
SrdlMEsw24CFWK0tVsbCkifmEnCf3AQu1MMqeLO5NJZnJWl3Oee9937rw3I7rq3Hz5/JOxJw/vD8UminS\
6MRd5cxunXTsCrpfp0/J1HxBUJkloshLEQHszGQNstiMgWB+Uw3oQAuUBYQ6gbABnGHj7t16M4+cH/7a\
BYUdC/gLAN0mHW0cXzebF0dahpK8AC77QHgAtJdQCYE9oEQAnCTgALIozU/UkCZwY/2zIrgG8LCU/I+9/\
BLBZA6CRPEBqALBmXQLY+fRN5G2AS6sBMJ9JA5l5gIbVAvg+4C6N2aIAwF26hzsACtYEAM30AcaasKYBe\
JMGXgMwzS4A481kBXcMgF3cLACPr/rz80cAZF20BKUS2Nu/4vhH+YGpsyR0DC+8T+MwUiybAX1VHIkaOR\
bSKqx09nPAvtlf7Ta6KiG5U1DVh2ezpT+9fwGYcs1M1nPM/u5psB3mubrCsa/A04Nb/zYEOiFQUQSoOgpA\
pxcYrSoG5BQA2j1AIRzC6G16OzNkfbMO7jGz46kfkLzau2j5vuZ17f8xB9R6U6ql0AAAAABJRU5ErkJggg\
=='

display_runtime=''

layout_sg = [  [sg.Text('AR Alarm System', font='Times 15'),sg.T(' '  * 4),
             sg.Image(data=github, key='git'),
             sg.Text('AGS BEE', font='Times 11', justification='bottom')],
             [sg.Text('Total Pages'),sg.InputText(current, size=(9,1))], 
             [sg.Text('Entry your start time:',size=(32,1)),sg.Text('Entry your end time:',size=(20,1))],
            [sg.Text('Follow yyyy-MM-dd'),sg.InputText(current, size=(18,1)), 
            sg.Text('Follow yyyy-MM-dd'),sg.InputText(current, size=(18,1))], 
            [sg.Button('Run',size=(8,1)), sg.Button('Cancel',size=(8,1)), 
             sg.T(' '  * 60), sg.Text(key='RT', size=(5,1))],
            [sg.ProgressBar(8, orientation='h', size=(55, 20), key='progbar',bar_color=('green', 'white'))],
            [sg.Button('Total Chart', size=(8,2)), sg.Button('Total Table', size=(8,2)),
             sg.Button('TOP1', size=(8,2)), sg.Button('TOP2', size=(8,2)), sg.Button('TOP3', size=(8,2))]]
         
            

# Create the Window
window = sg.Window('AR Alarm System 1.1V', layout_sg)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':	# if user closes window or clicks cancel
        break
    #print('You entered ', values[0])
    #checkdata=re.match("\d\d\d\d-\d\d-\d\d-\d-\d", values[1])
    if event =='Run':
            import warnings
            warnings.filterwarnings("ignore")
            
            #import pandas as pd
            import matplotlib.pyplot as plt
            from matplotlib.ticker import FuncFormatter
            import numpy as np
            import os
            
            print("#------------------------------------------------------#")
            print("    ######  ######## ####### ")
            print("    #     # #        #      ")
            print("    #    #  #        #      ")
            print("    ####    #######  ####### ")
            print("    #    #  #        #")
            print("    #     # #        #")
            print("    ######  #######  ####### ")
            print("#------------------------------------------------------#")
            print("\n")
            
            data_paths=r"C:\Users\zhangw16\Desktop\ACAN_Export"
            
            for file in os.listdir(data_paths):
                file_name="\\"+file
            #file_name="\\ACAN_Results_20201120115959_20201120235959.csv"
            
            folder_name=file_name.split("-")[0].split("\\")[1].split("_")[2]+"-"+file_name.split("-")[0].split("\\")[1].split("_")[3].split(".")[0]
            os.mkdir(data_paths+"\\"+folder_name)
            storage_folder_path=data_paths+"\\"+folder_name
            
            # 输出当前分析数据的日期和时间跨度
            print("Production Date: %s/%s/%s"%(folder_name[:4],folder_name[4:6],folder_name[6:8]))
            print("Start time:%s/%s/%s"%(folder_name[8:10],folder_name[10:12],folder_name[12:14]))
            print("End time:%s/%s/%s"%(folder_name[23:25],folder_name[25:27],folder_name[27:29]))
            
            data=pd.read_csv(data_paths+file_name)
            
            # Rename column
            
            column_renames=["Date","Time","Carrier","X_Pos","Y-Pos","Data_1","Data_2",\
                            "Avg","Avg-1","L_1","a_1","b_1","L_2","a_2","b_2"]
            data.columns=column_renames
            
            # Get Ex situ L,a,b spec
            
            L_mean=data["L_1"].mean()
            L_std=data["L_1"].std()
            a_mean=data["a_1"].mean()
            a_std=data["a_1"].std()
            b_mean=data["b_1"].mean()
            b_std=data["b_1"].std()
            
            L_uper_control_limit=L_mean+3*L_std
            L_lower_control_limit=L_mean-3*L_std
            L_uper_error_limit=L_mean+4*L_std
            L_lower_error_limit=L_mean-4*L_std
            a_uper_control_limit=a_mean+3*a_std
            a_lower_control_limit=a_mean-3*a_std
            a_uper_error_limit=a_mean+4*a_std
            a_lower_error_limit=a_mean-4*a_std
            b_uper_control_limit=b_mean+3*b_std
            b_lower_control_limit=b_mean-3*b_std
            b_uper_error_limit=b_mean+4*b_std
            b_lower_error_limit=b_mean-4*b_std
            
            # Plot L,a,b color time distribution
            
            Labs=["L_1","a_1","b_1"]
            
            os.mkdir(storage_folder_path+"\\Lab_boxplot")
            Lab_boxplot_path=storage_folder_path+"\\Lab_boxplot"
                    
            L=[]
            a=[]
            b=[]
            xtciks_names=[]
            carrier_unique_ids=data["Carrier"].unique()
            
            for Lab in Labs:
                carrier_unique_id_boxplot=[]
                labels=[]
                fig,ax=plt.subplots()
                for carrier_unique_id in carrier_unique_ids:
                    carrier_color_data=data[data["Carrier"].isin([carrier_unique_id])]
                    carrier_box_plot=carrier_color_data[Lab]
                    if Lab == "L_1":
                        xtciks_names.append(str(carrier_unique_id))
                        L.append([str(carrier_unique_id),carrier_box_plot.max(),carrier_box_plot.min(),carrier_box_plot.mean(),carrier_box_plot.std()])
                    if Lab == "a_1":
                        a.append([str(carrier_unique_id),carrier_box_plot.max(),carrier_box_plot.min(),carrier_box_plot.mean(),carrier_box_plot.std()])
                    if Lab == "b_1":
                        b.append([str(carrier_unique_id),carrier_box_plot.max(),carrier_box_plot.min(),carrier_box_plot.mean(),carrier_box_plot.std()])
                    carrier_unique_id_boxplot.append(carrier_box_plot)
                    labels.append(carrier_unique_id)
                plt.boxplot(carrier_unique_id_boxplot,meanline=True,showmeans=True,showfliers=True)
                ax.set_xticklabels(labels)
                if Lab == "L_1":
                    plt.title("Carrier L* boxplot")
                if Lab == "a_1":
                    plt.title("Carrier a* boxplot")
                if Lab == "b_1":
                    plt.title("Carrier b* boxplot")
                plt.xlabel("Carrier ID")
                #plt.grid(True)
                if Lab == "L_1":
                    plt.ylim(L_lower_error_limit-0.2,L_uper_error_limit+0.2)
                    plt.ylabel("L*")
                    #plt.xticks(rotation=30,fontsize=6)
                    plt.axhline(L_lower_control_limit,color="b",linestyle="--",linewidth=0.5,label="L* contol limit")
                    plt.axhline(L_uper_control_limit,color="b",linestyle="--",linewidth=0.5)
                    plt.axhline(L_lower_error_limit,color="r",linestyle="--",linewidth=1.0,label="L* error limit")
                    plt.axhline(L_uper_error_limit,color="r",linestyle="--",linewidth=1.0)
                    plt.savefig(Lab_boxplot_path+"\\Carrier L boxplot.jpg",dpi=300)
                    plt.close()
                if Lab == "a_1":
                    plt.ylim(a_lower_error_limit-0.2,a_uper_error_limit+0.2)
                    plt.ylabel("a*")
                    #plt.xticks(rotation=30,fontsize=6)
                    plt.axhline(a_lower_control_limit,color="b",linestyle="--",linewidth=0.5,label="a* contol limit")
                    plt.axhline(a_uper_control_limit,color="b",linestyle="--",linewidth=0.5)
                    plt.axhline(a_lower_error_limit,color="r",linestyle="--",linewidth=1.0,label="a* error limit")
                    plt.axhline(a_uper_error_limit,color="r",linestyle="--",linewidth=1.0)
                    plt.savefig(Lab_boxplot_path+"\\Carrier a boxplot.jpg",dpi=300)
                    plt.close()
                if Lab == "b_1":
                    plt.ylim(b_lower_error_limit-0.2,b_uper_error_limit+0.2)
                    plt.ylabel("b*")
                    #plt.xticks(rotation=30,fontsize=6)
                    plt.axhline(b_lower_control_limit,color="b",linestyle="--",linewidth=0.5,label="b* contol limit")
                    plt.axhline(b_uper_control_limit,color="b",linestyle="--",linewidth=0.5)
                    plt.axhline(b_lower_error_limit,color="r",linestyle="--",linewidth=1.0,label="b* error limit")
                    plt.axhline(b_uper_error_limit,color="r",linestyle="--",linewidth=1.0)
                    plt.savefig(Lab_boxplot_path+"\\Carrier b boxplot.jpg",dpi=300)
                    plt.close()
            
            # Outpur L*/a*/b* stats data   
            os.mkdir(storage_folder_path+"\\Stats_data")
            stats_data_path=storage_folder_path+"\\Stats_data"
            
            names=["Carrier id","max","min","mean","std"]
            Carrier_L=pd.DataFrame(data=np.array(L),index=None,columns=names)
            Carrier_a=pd.DataFrame(data=np.array(a),index=None,columns=names)
            Carrier_b=pd.DataFrame(data=np.array(b),index=None,columns=names)
            
            Carrier_L=Carrier_L.sort_values(["mean"],ascending=True)
            Carrier_a=Carrier_a.sort_values(["mean"],ascending=True)
            Carrier_b=Carrier_b.sort_values(["mean"],ascending=True)
            
            Carrier_L.to_csv(stats_data_path+"\\carrier L stastistal.csv",columns=names)
            Carrier_a.to_csv(stats_data_path+"\\carrier a stastistal.csv",columns=names)
            Carrier_b.to_csv(stats_data_path+"\\carrier b stastistal.csv",columns=names)
            
            L=pd.read_csv(stats_data_path+"\\carrier L stastistal.csv")
            a=pd.read_csv(stats_data_path+"\\carrier a stastistal.csv")
            b=pd.read_csv(stats_data_path+"\\carrier b stastistal.csv")
            
            def to_float(temp,position):
                return "%.2f"%(temp)
            
            plt.figure()
            L.plot.bar(x="Carrier id",y="mean",label="L")
            plt.ylim(L["mean"].min()-0.05,L["mean"].max()+0.05)
            plt.gca().yaxis.set_major_formatter(FuncFormatter(to_float))
            plt.axhline(L_mean,color="r",linestyle="--",linewidth=0.5,label="L mean")
            plt.ylabel("AR Ex situ L*")
            plt.title("AR Ex situ L* vs Carrier ID")
            plt.legend(loc="best")
            plt.savefig(storage_folder_path+"\\AR Ex situ L vs Carrier ID.jpg",dpi=300)
            plt.close()
            
            plt.figure()
            a.plot.bar(x="Carrier id",y="mean",label="a")
            plt.ylim(a["mean"].min()-0.05,a["mean"].max()+0.05)
            plt.gca().yaxis.set_major_formatter(FuncFormatter(to_float))
            plt.axhline(a_mean,color="r",linestyle="--",linewidth=0.5,label="a mean")
            plt.ylabel("AR Ex situ a*")
            plt.title("AR Ex situ a* vs Carrier ID")
            plt.legend(loc="best")
            plt.savefig(storage_folder_path+"\\AR Ex situ a vs Carrier ID.jpg",dpi=300)
            plt.close()
            
            plt.figure()
            b.plot.bar(x="Carrier id",y="mean",label="b")
            plt.ylim(b["mean"].min()-0.05,b["mean"].max()+0.05)
            plt.gca().yaxis.set_major_formatter(FuncFormatter(to_float))
            plt.axhline(b_mean,color="r",linestyle="--",linewidth=0.5,label="b mean")
            plt.ylabel("AR Ex situ b*")
            plt.title("AR Ex situ b* vs Carrier ID")
            plt.legend(loc="best")
            plt.savefig(storage_folder_path+"\\AR Ex situ b vs Carrier ID.jpg",dpi=300)
            plt.close()
            
            print("Carrier ID %s b* rather upper"%(b["Carrier id"][0]))
            print("Carrier ID %s b* rather upper"%(b["Carrier id"][1]))
            print("Carrier ID %s b* rather lower"%(b["Carrier id"][len(b)-2]))
            print("Carrier ID %s b* rather lower"%(b["Carrier id"][len(b)-1]))
            
            # 在操作执行完成之后删除该目录下的.csv文件
            
            if os.path.exists(data_paths+file_name):
                os.remove(data_paths+file_name)
            else:
                print("No %s file in current folder"%(file_name))

window.close()