# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 15:12:53 2018

@author: ishwarya.sriraman
"""

import pandas as pd
import numpy as np
class woe:
    def __init__(self,df,target):
        self.df=df
        self.target=target
       
   
    def population(self,bins,var):
        count=0
        lis=[]
        l=[]
        d1=[]
#        for i1 in range(3,10):
        bins = np.linspace(self.df[var].min(), self.df[var].max(), bins)
        lis=list(self.df[var])
        for i in range(len(bins)-1):
            count=0
            for j in lis:
                if j>=bins[i] and j<=bins[i+1]:
                    count=count+1
            l.append(count)
        columns=[var+'_bins','population']
        for i in range(len(bins)-1):
            d1.append(str(bins[i]) + "-" + str(bins[i+1]))
                
        d1=pd.Series(d1)
        l=pd.Series(l)
        
        data1=pd.DataFrame(data=[[d1,l]],columns=columns)
        return(data1)
    
    def calc_iv(self, feature, pr=0):

        lst = []
    
        for i in range(self.df[feature].nunique()):
            val = list(self.df[feature].unique())[i]
            lst.append([feature, val, self.df[self.df[feature] == val].count()[feature], self.df[(self.df[feature] == val) & (self.df[self.target] == 1)].count()[feature]])
        
        data = pd.DataFrame(lst, columns=['Variable', 'Value', 'All', 'Bad'])
        data = data[data['Bad'] > 0]
    
        data['Share'] = data['All'] / data['All'].sum()
        data['Bad Rate'] = data['Bad'] / data['All']
        data['Distribution Good'] = ((data['All'] - data['Bad']) / (data['All'].sum() - data['Bad'].sum()))
        data['Distribution Bad'] = (data['Bad'] / data['Bad'].sum())
        data['WoE'] = np.log(data['Distribution Good'] / data['Distribution Bad'])
        data['IV'] = (data['WoE'] * (data['Distribution Good'] - data['Distribution Bad']))
        data['IV']=data['IV'].replace([np.inf, -np.inf], 0)
    
        data = data.sort_values(by=['Variable', 'Value'], ascending=True)
    
        if pr == 1:
            print(data)
            
        print(data['IV'].sum())
        return data