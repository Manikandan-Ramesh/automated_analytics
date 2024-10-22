# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 12:24:59 2018

@author: ishwarya.sriraman
"""

from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import STAP
import re
from rpy2.robjects import r
import rpy2.robjects as robjects
from rpy2.robjects.vectors import StrVector
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
import rpy2.robjects.packages as rpackages
from rpy2.robjects.lib.dplyr import dplyr
from rpy2.robjects import default_converter
from rpy2.robjects.conversion import localconverter
class imputation:
       
    def __init__(self,df,target):
        self.df=df
        self.target=target
        
    def imputation_data(self,var,technique):
         utils = importr('utils')
         while True:
                try:
                    rrcovNA = importr('rrcovNA')
                    mice=importr('mice')
                    DMwR=importr('DMwR')
                except Exception as e:
                    y = str(e)
                    print(y)
                    z = re.findall(r"'(.*?)'", y, re.DOTALL)[0]
                    utils.install_packages(z)
                else:
                    break
         while True:
            try:
                with open('impute_final.r', 'r') as f:
                    string = f.read()
                    impute_final = STAP(string, "impute_final")
            except FileNotFoundError:
                path = input("set directory to path: ")
                from os import chdir
                chdir(path)
                with open('impute_final.r', 'r') as f:
                    string = f.read()
                    impute_final = STAP(string, "impute_final")
            else:
                break
         datecol=[x for x in self.df.columns if self.df[x].dtypes=='datetime64[ns]']
         cont = [x for x in self.df.columns if self.df[x].dtypes != 'object' and x not in datecol]
        
         pandas2ri.activate()
         if technique!='knn':
             data=impute_final.imputation_tech(self.df,var,technique,self.target)
         else:
             data=impute_final.imputation_tech(self.df[cont],var,technique,self.target)
         pandas2ri.deactivate()
         data=pandas2ri.ri2py_dataframe(data)
         return data
        