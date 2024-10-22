# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 11:29:03 2018

@author: ishwarya.sriraman
"""
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import STAP
class capping:
       
    def __init__(self,df,target):
        self.df=df
        self.target=target
        
    def capping_data(self,var,method):
        while True:
            try:
                with open('capping_v2.r', 'r') as f:
                    string = f.read()
                    capping_v2 = STAP(string, "capping_v2")
            except FileNotFoundError:
                path = input("set directory to path: ")
                from os import chdir
                chdir(path)
                with open('capping_v2.r', 'r') as f:
                    string = f.read()
                    capping_v2 = STAP(string, "capping_v2")
            else:
                break
        
        pandas2ri.activate()
        data=capping_v2.pcap(self.df,var,method)
        pandas2ri.deactivate()
        data=pandas2ri.ri2py_dataframe(data)
        return data
        