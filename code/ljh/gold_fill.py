import csv
from datetime import datetime, timedelta
from matplotlib.animation import TimedAnimation
import numpy as np
import pandas as pd
a=pd.read_csv("code\ljh\gold_ini.csv")
a=a.fillna(0)
a['Date']=pd.to_datetime(a['Date'])
date1=datetime(2016,9,11)
a['dis']=a['Date']-date1

b=a
i=1
for index,row in a.iterrows():
    # print(a.iloc[[index]])
    if(row['dis']==timedelta(days=i)):
        
        i+=1
        continue
    else:
        while row['dis']!=timedelta(days=i):
            temp=pd.DataFrame([[date1+timedelta(days=i),0,timedelta(days=i)]],columns=['Date','USD (PM)','dis'])
            # print(temp)
            i+=1
            b=b.append(temp,ignore_index=True)
        i+=1
        continue
temp=pd.DataFrame([[date1,1324.6,timedelta(days=0)]],columns=['Date','USD (PM)','dis'])
b=b.append(temp,ignore_index=True)
b.index=b['Date']
b=b.sort_index()

b.to_csv('code\\ljh\\1.csv',index=None)