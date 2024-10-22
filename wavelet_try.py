# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 14:39:02 2018

@author: ishwarya.sriraman
"""

import pywt
import pandas as pd
pathname="D:\\Other projects\\python modules\\Sample_Policy_Master.csv"
df=pd.read_csv(pathname)
df_cont = df.select_dtypes(include=["int64","float64"])
df_cat = df.select_dtypes(include=["object"])
df_date = df.select_dtypes(include=["datetime64[ns]"])


for i in df_cont:
    cA, cD = pywt.dwt(df[i], 'db1')
    print (cA)
    print (cD)