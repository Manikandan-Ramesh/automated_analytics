# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 14:43:34 2018

@author: mritunjay.kumar
"""

# -*- coding: utf-8 -*-
"""
created By  Mritunjay at Bridgei2i

"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from scipy.stats import kurtosis
from scipy.stats import skew
import scipy as sc
import missingno as msno
from rpy2.robjects import r, pandas2ri
from rpy2.robjects.packages import STAP
import rpy2.robjects as robjects
from rpy2.robjects.vectors import StrVector
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
import rpy2.robjects.packages as rpackages
from rpy2.robjects.lib.dplyr import dplyr
from rpy2.robjects import default_converter
from rpy2.robjects.conversion import localconverter

import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns







class eda:
    def __init__(self,Train,Target):
        self.Train = Train
        self.targetname = Target
        self.Target = Train[Target]
    def eventRatio(self,event):
        y = self.Target.value_counts()
        self.ratio = y[event]/self.Target.count()
        return self.ratio
    def impstat(self):
        self.impStat = self.Train.describe()
        return self.impStat
    def range(self):
        x = [x for x in self.Train.columns if self.Train[x].dtypes != 'object']
        z = self.Train[x]
        def Range(y):
            mi = np.min(y)
            ma = np.max(y)
            rng = ma-mi
            return rng
        self.Rnge = z.apply(Range)
        return self.Rnge
    def iqr(self):
        x = [x for x in self.Train.columns if self.Train[x].dtypes != 'object']
        z = self.Train[x]
        def IQR(y):
            x25 = np.percentile(y,25)
            x75 = np.percentile(y,75)
            Iqr = x75 - x25
            return Iqr
            
        self.iQr = z.apply(IQR)
        return  self.iQr
    
    def corr(self):
        x = [x for x in self.Train.columns if self.Train[x].dtypes != 'object']
        z = self.Train[x]
        self.corr = z.corr()
        return self.corr
    def skew(self):
        x = [x for x in self.Train.columns if self.Train[x].dtypes != 'object']
        z = self.Train[x]
        def Skew(y):
            d = skew(y)
            return d
        self.skewness = z.apply(Skew)
        return self.skewness
    def kurt(self):
        x = [x for x in self.Train.columns if self.Train[x].dtypes != 'object']
        z = self.Train[x]
        def Kurt(y):
            d = kurtosis(y)
            return d
        self.Kurtosis = z.apply(Kurt)
        return self.Kurtosis
    def missinginfo(self):
        def getPctMissing(series):
            num = series.isnull().sum()
            den = series.count()
            return 100*(num/den)
        self.missing = self.Train.apply(getPctMissing)
        self.missing.sort_values(ascending=False,inplace=True)
        self.totalmiss = self.Train.isnull().sum().sum()
        return [self.totalmiss,self.missing]
    def missingplot(self):
       msno.matrix(self.Train)
       #show(plt)
    def missingcorr(self):
        msno.heatmap(self.Train)
    def missingpattern(self):
        msno.dendrogram(self.Train)
    def bin(self,method,target,event,*args):
        base = importr('base')
        utils = importr('utils')
        try:
            woeBinning = importr('woeBinning')
        except Exception as e:
            y = str(e)
            z = str(re.findall(r"'(.*?)'", y, re.DOTALL))
            utils.install_packages(z)
            
        try:            
            discretization = importr('discretization')
        except Exception as e:
            y = str(e)
            z = str(re.findall(r"'(.*?)'", y, re.DOTALL))
            utils.install_packages(z)
            
        
        
                   
        column_Name = []
        cl =[]
        if method == 'woe':
            print('woe')
            for arg in args:
                print(arg)
                if self.Train[arg].dtypes != 'object':
                    print(self.Train[arg].dtypes)
                    column_Name.append(arg)
                    cl.append(arg)
                    print(column_Name)
    
                else:
                    print("Column Name "+arg+" is Object so no binning is done for it")
            column_Name.append(target)
            df = self.Train[column_Name]
            try:
                with open('woe.r', 'r') as f:
                    string = f.read()
                woe = STAP(string, "woe")
            except FileNotFoundError:
                path = input("set directory to path: ")
                from os import chdir
                chdir(path)
                with open('woe.r', 'r') as f:
                    string = f.read()
                woe = STAP(string, "woe")
            pandas2ri.activate()
                
            self.woe_based_bin = pandas2ri.ri2py(woe.woe_based_binning(df,target,event,
                                                      cl))
            pandas2ri.deactivate()
            return self.woe_based_bin
        elif method=='Chisq':
            print('Chisq')
            cl =[]
            s =[]
            for arg in args:
                s.append(arg)
                
            #column_name =[]
            if s[0] == 'ALL':
                print("ALL")
                for j in self.Train.columns:
                    if self.Train[j].dtypes != 'object':
                        cl.append(j)
                        #column_name.append(arg)
                cl.append(target)
                df = self.Train[cl]
                try:
                    with open('woe.r', 'r') as f:
                        string = f.read()
                        woe = STAP(string, "woe")
                        print('woe')
                        
                        
                except FileNotFoundError:
                    path = input("set directory to path: ")
                    from os import chdir
                    chdir(path)
                    with open('woe.r', 'r') as f:
                        string = f.read()
                        woe = STAP(string, "woe")
                        print('woe')
                
            
                pandas2ri.activate()
                print('pandas2ri is activated')
                self.chisq_based_bin = pandas2ri.ri2py(woe.chi(df))
                pandas2ri.deactivate()    
                return self.chisq_based_bin
            else:
                cl =[]
                for arg in args:
                    if self.Train[arg].dtypes != 'object':
                        cl.append(arg)
                    else:
                        print(arg + " is not continuous")
                if len(cl)==0:
                    message = ' Binning can not be done as all variable passed is not continuos'
                    return message
                cl.append(target)
                df = self.Train[cl].copy()
                try:
                    with open('woe.r', 'r') as f:
                        string = f.read()
                        woe = STAP(string, "woe")
                        print('woe module loaded')
                        
                        
                except FileNotFoundError:
                    path = input("set directory to path: ")
                    from os import chdir
                    chdir(path)
                    with open('woe.r', 'r') as f:
                        string = f.read()
                        woe = STAP(string, "woe")
                        print('woe module loaded')
                
            
                
                pandas2ri.activate()
                print('pandas2ri is activated')
                self.chisq_based_bin = pandas2ri.ri2py(woe.chi(df))
                pandas2ri.deactivate()  
                print('pandas2ri is deactivated')
                return self.chisq_based_bin
        elif method == 'Entropy':
            print('Entropy')
            cl =[]
            s =[]
            for arg in args:
                s.append(arg)
            if s[0] == 'ALL':
                print("ALL")
                for j in self.Train.columns:
                    if self.Train[j].dtypes != 'object':
                        cl.append(j)
                        #column_name.append(arg)
                cl.append(target)
                df = self.Train[cl]
                try:
                    with open('woe.r', 'r') as f:
                        string = f.read()
                        woe = STAP(string, "woe")
                        print('woe')
                        
                        
                except FileNotFoundError:
                    path = input("set directory to path: ")
                    from os import chdir
                    chdir(path)
                    with open('woe.r', 'r') as f:
                        string = f.read()
                        woe = STAP(string, "woe")
                        print('woe')
                
            
                pandas2ri.activate()
                print('pandas2ri is activated')
                self.entropy_based_bin = pandas2ri.ri2py(woe.entropy_based_bin(df))
                pandas2ri.deactivate()    
                return self.entropy_based_bin
            else:
                cl =[]
                for arg in args:
                    if self.Train[arg].dtypes != 'object':
                        cl.append(arg)
                    else:
                        print(arg + " is not continuous")
                if len(cl)==0:
                    message = ' Binning can not be done as all variable passed is not continuos'
                    return message
                cl.append(target)
                df = self.Train[cl].copy()
                try:
                    with open('woe.r', 'r') as f:
                        string = f.read()
                        woe = STAP(string, "woe")
                        print('woe module loaded')
                        
                        
                except FileNotFoundError:
                    path = input("set directory to path: ")
                    from os import chdir
                    chdir(path)
                    with open('woe.r', 'r') as f:
                        string = f.read()
                        woe = STAP(string, "woe")
                        print('woe module loaded')
                
            
                
                pandas2ri.activate()
                print('pandas2ri is activated')
                self.entropy_based_bin = pandas2ri.ri2py(woe.entropy_based_bin(df))
                pandas2ri.deactivate()  
                print('pandas2ri is deactivated')
                return self.entropy_based_bin
            def crt():
                pass

    def InformationValue(self,target,event,method):
        if method == 'Chisq':
            try:
                data = self.chisq_based_bin
            except AttributeError:
                event = event
                argu = input("Please Enter the Column Name Separated by comma: ",)
                base = importr('base')
                utils = importr('utils')
                try:
                    woeBinning = importr('woeBinning')
                except Exception as e:
                    y = str(e)
                    z = str(re.findall(r"'(.*?)'", y, re.DOTALL))
                    utils.install_packages(z)
                cl = []
                for ar in argu.split(","):
                    cl.append(ar.strip())
                event = event.strip()
                cl.append(target)
                df = self.Train[cl].copy()
                try:
                    with open('woe.r', 'r') as f:
                        string = f.read()
                        woe = STAP(string, "woe")
                        print('woe module loaded')
                except FileNotFoundError:
                    path = input("set directory to path: ")
                    from os import chdir
                    chdir(path)
                    with open('woe.r', 'r') as f:
                        string = f.read()
                        woe = STAP(string, "woe")
                        print('woe module loaded')
                pandas2ri.activate()
                print('pandas2ri is activated')
                data = pandas2ri.ri2py(woe.chi(df))
                pandas2ri.deactivate()
                
            self.INfoValue = {}
            for cal in data.columns:
                if cal != target:
                    dat= pd.crosstab(data[cal],data[target]).apply(lambda r: r/r.sum(), axis=0)
                    s = [x for x in dat.columns if x != event][0]
                    woe = np.log(dat[event]/dat[s])
                    dif = dat[event]-dat[s]
                    iv = dif*woe
                    self.INfoValue[cal]=iv.sum()
            return self.INfoValue
        elif method == 'woe':
            try:
                data = self.woe_based_bin
            except AttributeError:
                event = event
                argu = input("Please Enter the Column Name Separated by comma: ",)
                base = importr('base')
                utils = importr('utils')
                try:
                    woeBinning = importr('woeBinning')
                except Exception as e:
                    y = str(e)
                    z = str(re.findall(r"'(.*?)'", y, re.DOTALL))
                    utils.install_packages(z)
                cl = []
                clmn=[]
                for ar in argu.split(","):
                    cl.append(ar.strip())
                    clmn.append(ar.strip())
                event = event.strip()
                cl.append(target)
                df = self.Train[cl].copy()
                try:
                    with open('woe.r', 'r') as f:
                        string = f.read()
                        woe = STAP(string, "woe")
                        print('woe module loaded')
                except FileNotFoundError:
                    path = input("set directory to path: ")
                    from os import chdir
                    chdir(path)
                    with open('woe.r', 'r') as f:
                        string = f.read()
                        woe = STAP(string, "woe")
                        print('woe module loaded')
                pandas2ri.activate()
                print('pandas2ri is activated')
                data = pandas2ri.ri2py(woe.woe_based_binning(df,target,event,clmn))
                pandas2ri.deactivate()
                
            self.INfoValue = {}
            for cal in data.columns:
                if cal != target:
                    dat= pd.crosstab(data[cal],data[target]).apply(lambda r: r/r.sum(), axis=0)
                    s = [x for x in dat.columns if x != event][0]
                    woe = np.log(dat[event]/dat[s])
                    dif = dat[event]-dat[s]
                    iv = dif*woe
                    self.INfoValue[cal]=iv.sum()
            return self.INfoValue
        elif method=='Entropy':
            try:
                data = self.entropy_based_bin
            except AttributeError:
                event = event
                argu = input("Please Enter the Column Name Separated by comma: ",)
                base = importr('base')
                utils = importr('utils')
                try:
                    woeBinning = importr('woeBinning')
                except Exception as e:
                    y = str(e)
                    z = str(re.findall(r"'(.*?)'", y, re.DOTALL))
                    utils.install_packages(z)
                cl = []
                for ar in argu.split(","):
                    cl.append(ar.strip())
                event = event.strip()
                cl.append(target)
                df = self.Train[cl].copy()
                try:
                    with open('woe.r', 'r') as f:
                        string = f.read()
                        woe = STAP(string, "woe")
                        print('woe module loaded')
                except FileNotFoundError:
                    path = input("set directory to path: ")
                    from os import chdir
                    chdir(path)
                    with open('woe.r', 'r') as f:
                        string = f.read()
                        woe = STAP(string, "woe")
                        print('woe module loaded')
                pandas2ri.activate()
                print('pandas2ri is activated')
                data = pandas2ri.ri2py(woe.entropy_based_bin(df))
                pandas2ri.deactivate()
                
            self.INfoValue = {}
            for cal in data.columns:
                if cal != target:
                    dat= pd.crosstab(data[cal],data[target]).apply(lambda r: r/r.sum(), axis=0)
                    s = [x for x in dat.columns if x != event][0]
                    woe = np.log(dat[event]/dat[s])
                    dif = dat[event]-dat[s]
                    iv = dif*woe
                    self.INfoValue[cal]=iv.sum()
            return self.INfoValue
    
            
    def NMI(self,target,event,method):
        if method == 'Chisq':
            try:
                data = self.chisq_based_bin
            except AttributeError:
                event = event
                argu = input("Please Enter the Column Name Separated by comma: ",)
                base = importr('base')
                utils = importr('utils')
                try:
                    woeBinning = importr('woeBinning')
                except Exception as e:
                    y = str(e)
                    z = str(re.findall(r"'(.*?)'", y, re.DOTALL))
                    utils.install_packages(z)
                cl = []
                for ar in argu.split(","):
                    cl.append(ar.strip())
                event = event.strip()
                cl.append(target)
                df = self.Train[cl].copy()
                try:
                    with open('woe.r', 'r') as f:
                        string = f.read()
                        woe = STAP(string, "woe")
                        print('woe module loaded')
                except FileNotFoundError:
                    path = input("set directory to path: ")
                    from os import chdir
                    chdir(path)
                    with open('woe.r', 'r') as f:
                        string = f.read()
                        woe = STAP(string, "woe")
                        print('woe module loaded')
                pandas2ri.activate()
                print('pandas2ri is activated')
                data = pandas2ri.ri2py(woe.chi(df))
                pandas2ri.deactivate()
            try:
                with open('woe.r', 'r') as f:
                    string = f.read()
                    woe = STAP(string, "woe")
                    print('woe module loaded')
            except FileNotFoundError:
                path = input("set directory to path: ")
                from os import chdir
                chdir(path)
                with open('woe.r', 'r') as f:
                    string = f.read()
                    woe = STAP(string, "woe")
                    print('woe module loaded')
                
            self.MutaulI = {}
            for cal in data.columns:
                if cal != target:
                    pandas2ri.activate()
                    nmi = pandas2ri.ri2py(woe.nmi(data[cal],data[target]))
                    pandas2ri.deactivate()
                    self.MutaulI[cal]=nmi
                
                
            return  self.MutaulI
        elif method == 'woe':
            try:
                data = self.woe_based_bin
            except AttributeError:
                event = event
                argu = input("Please Enter the Column Name Separated by comma: ",)
                base = importr('base')
                utils = importr('utils')
                try:
                    woeBinning = importr('woeBinning')
                except Exception as e:
                    y = str(e)
                    z = str(re.findall(r"'(.*?)'", y, re.DOTALL))
                    utils.install_packages(z)
                cl = []
                clmn=[]
                for ar in argu.split(","):
                    cl.append(ar.strip())
                    clmn.append(ar.strip())
                event = event.strip()
                cl.append(target)
                df = self.Train[cl].copy()
                try:
                    with open('woe.r', 'r') as f:
                        string = f.read()
                        woe = STAP(string, "woe")
                        print('woe module loaded')
                except FileNotFoundError:
                    path = input("set directory to path: ")
                    from os import chdir
                    chdir(path)
                    with open('woe.r', 'r') as f:
                        string = f.read()
                        woe = STAP(string, "woe")
                        print('woe module loaded')
                pandas2ri.activate()
                print('pandas2ri is activated')
                data = pandas2ri.ri2py(woe.woe_based_binning(df,target,event,clmn))
                pandas2ri.deactivate()
            try:
                with open('woe.r', 'r') as f:
                    string = f.read()
                    woe = STAP(string, "woe")
                    print('woe module loaded')
            except FileNotFoundError:
                path = input("set directory to path: ")
                from os import chdir
                chdir(path)
                with open('woe.r', 'r') as f:
                    string = f.read()
                    woe = STAP(string, "woe")
                    print('woe module loaded')
                
            self.MutaulI = {}
            for cal in data.columns:
                if cal != target:
                    pandas2ri.activate()
                    nmi = pandas2ri.ri2py(woe.nmi(data[cal],data[target]))
                    pandas2ri.deactivate()
                    self.MutaulI[cal]=nmi
                
                
            return  self.MutaulI
        elif method=='Entropy':
            try:
                data = self.entropy_based_bin
            except AttributeError:
                event = event
                argu = input("Please Enter the Column Name Separated by comma: ",)
                base = importr('base')
                utils = importr('utils')
                try:
                    woeBinning = importr('woeBinning')
                except Exception as e:
                    y = str(e)
                    z = str(re.findall(r"'(.*?)'", y, re.DOTALL))
                    utils.install_packages(z)
                cl = []
                for ar in argu.split(","):
                    cl.append(ar.strip())
                event = event.strip()
                cl.append(target)
                df = self.Train[cl].copy()
                try:
                    with open('woe.r', 'r') as f:
                        string = f.read()
                        woe = STAP(string, "woe")
                        print('woe module loaded')
                except FileNotFoundError:
                    path = input("set directory to path: ")
                    from os import chdir
                    chdir(path)
                    with open('woe.r', 'r') as f:
                        string = f.read()
                        woe = STAP(string, "woe")
                        print('woe module loaded')
                pandas2ri.activate()
                print('pandas2ri is activated')
                data = pandas2ri.ri2py(woe.entropy_based_bin(df))
                pandas2ri.deactivate()
                
            try:
                with open('woe.r', 'r') as f:
                    string = f.read()
                    woe = STAP(string, "woe")
                    print('woe module loaded')
            except FileNotFoundError:
                path = input("set directory to path: ")
                from os import chdir
                chdir(path)
                with open('woe.r', 'r') as f:
                    string = f.read()
                    woe = STAP(string, "woe")
                    print('woe module loaded')
                
            self.MutaulI = {}
            for cal in data.columns:
                if cal != target:
                    pandas2ri.activate()
                    nmi = pandas2ri.ri2py(woe.nmi(data[cal],data[target]))
                    pandas2ri.deactivate()
                    self.MutaulI[cal]=nmi
                
                
            return  self.MutaulI
    
    def Chisqstat(self,target,event,method):
        if method == 'Chisq':
            try:
                data = self.chisq_based_bin
            except AttributeError:
                event = event
                argu = input("Please Enter the Column Name Separated by comma: ",)
                base = importr('base')
                utils = importr('utils')
                try:
                    woeBinning = importr('woeBinning')
                except Exception as e:
                    y = str(e)
                    z = str(re.findall(r"'(.*?)'", y, re.DOTALL))
                    utils.install_packages(z)
                cl = []
                for ar in argu.split(","):
                    cl.append(ar.strip())
                event = event.strip()
                cl.append(target)
                df = self.Train[cl].copy()
                try:
                    with open('woe.r', 'r') as f:
                        string = f.read()
                        woe = STAP(string, "woe")
                        print('woe module loaded')
                except FileNotFoundError:
                    path = input("set directory to path: ")
                    from os import chdir
                    chdir(path)
                    with open('woe.r', 'r') as f:
                        string = f.read()
                        woe = STAP(string, "woe")
                        print('woe module loaded')
                pandas2ri.activate()
                print('pandas2ri is activated')
                data = pandas2ri.ri2py(woe.chi(df))
                pandas2ri.deactivate()
            try:
                with open('woe.r', 'r') as f:
                    string = f.read()
                    woe = STAP(string, "woe")
                    print('woe module loaded')
            except FileNotFoundError:
                path = input("set directory to path: ")
                from os import chdir
                chdir(path)
                with open('woe.r', 'r') as f:
                    string = f.read()
                    woe = STAP(string, "woe")
                    print('woe module loaded')
                
            self.chistat = {}
            for cal in data.columns:
                if cal != target:
                    pandas2ri.activate()
                    nmi = pandas2ri.ri2py(woe.ChiTest(data[cal],data[target]))
                    pandas2ri.deactivate()
                    self.chistat[cal]=nmi
            return self.chistat
                
                
            
        elif method == 'woe':
            try:
                data = self.woe_based_bin
            except AttributeError:
                event = event
                argu = input("Please Enter the Column Name Separated by comma: ",)
                base = importr('base')
                utils = importr('utils')
                try:
                    woeBinning = importr('woeBinning')
                except Exception as e:
                    y = str(e)
                    z = str(re.findall(r"'(.*?)'", y, re.DOTALL))
                    utils.install_packages(z)
                cl = []
                clmn=[]
                for ar in argu.split(","):
                    cl.append(ar.strip())
                    clmn.append(ar.strip())
                event = event.strip()
                cl.append(target)
                df = self.Train[cl].copy()
                try:
                    with open('woe.r', 'r') as f:
                        string = f.read()
                        woe = STAP(string, "woe")
                        print('woe module loaded')
                except FileNotFoundError:
                    path = input("set directory to path: ")
                    from os import chdir
                    chdir(path)
                    with open('woe.r', 'r') as f:
                        string = f.read()
                        woe = STAP(string, "woe")
                        print('woe module loaded')
                pandas2ri.activate()
                print('pandas2ri is activated')
                data = pandas2ri.ri2py(woe.woe_based_binning(df,target,event,clmn))
                pandas2ri.deactivate()
            try:
                with open('woe.r', 'r') as f:
                    string = f.read()
                    woe = STAP(string, "woe")
                    print('woe module loaded')
            except FileNotFoundError:
                path = input("set directory to path: ")
                from os import chdir
                chdir(path)
                with open('woe.r', 'r') as f:
                    string = f.read()
                    woe = STAP(string, "woe")
                    print('woe module loaded')
                
            self.chistat = {}
            for cal in data.columns:
                if cal != target:
                    pandas2ri.activate()
                    nmi = pandas2ri.ri2py(woe.ChiTest(data[cal],data[target]))
                    pandas2ri.deactivate()
                    self.chistat[cal]=nmi
            return self.chistat
        elif method=='Entropy':
            try:
                data = self.entropy_based_bin
            except AttributeError:
                event = event
                argu = input("Please Enter the Column Name Separated by comma: ",)
                base = importr('base')
                utils = importr('utils')
                try:
                    woeBinning = importr('woeBinning')
                except Exception as e:
                    y = str(e)
                    z = str(re.findall(r"'(.*?)'", y, re.DOTALL))
                    utils.install_packages(z)
                cl = []
                for ar in argu.split(","):
                    cl.append(ar.strip())
                event = event.strip()
                cl.append(target)
                df = self.Train[cl].copy()
                try:
                    with open('woe.r', 'r') as f:
                        string = f.read()
                        woe = STAP(string, "woe")
                        print('woe module loaded')
                except FileNotFoundError:
                    path = input("set directory to path: ")
                    from os import chdir
                    chdir(path)
                    with open('woe.r', 'r') as f:
                        string = f.read()
                        woe = STAP(string, "woe")
                        print('woe module loaded')
                pandas2ri.activate()
                print('pandas2ri is activated')
                data = pandas2ri.ri2py(woe.entropy_based_bin(df))
                pandas2ri.deactivate()
                
            try:
                with open('woe.r', 'r') as f:
                    string = f.read()
                    woe = STAP(string, "woe")
                    print('woe module loaded')
            except FileNotFoundError:
                path = input("set directory to path: ")
                from os import chdir
                chdir(path)
                with open('woe.r', 'r') as f:
                    string = f.read()
                    woe = STAP(string, "woe")
                    print('woe module loaded')
                
            self.chistat = {}
            for cal in data.columns:
                if cal != target:
                    pandas2ri.activate()
                    nmi = pandas2ri.ri2py(woe.ChiTest(data[cal],data[target]))
                    pandas2ri.deactivate()
                    self.chistat[cal]=nmi
            return self.chistat
        
#    def vif(self):
#        df=self.Train.dropna()
#        df = df._get_numeric_data()
#        datecol=[x for x in df.columns if df[x].dtypes=='datetime64[ns]']
#        vif = [variance_inflation_factor(X[variables].values, X.columns.get_loc(var)) for var in X.columns]
#        self.Vif ={'var':list(X.columns),'vif':vif}
#        return self.Vif

    def boxgraph(self):
        data=self.Train
        y = self.targetname
        x = [x for x in data.columns if data[x].dtypes != 'object']
        img ={}
        for col in x:
            z=sns.boxplot(data[col],data[y])
            fig = z.get_figure()
            img[col]=fig
        return img
    def dist(self):
        data=self.Train
        y = self.targetname
        x = [x for x in data.columns if data[x].dtypes != 'object']
        img ={}
        for col in x:
            z=sns.pairplot(data[[col,y]],hue=y)
            fig = z.fig
            img[col]=fig
        return img
    
    def matrixplot(self):
        data=self.Train
        y = self.targetname
        #x = [x for x in data.columns if data[x].dtypes != 'object']
        z=sns.pairplot(data,hue=y)
        img = z.fig
        return img
    def bigraphcat(self):
        data=self.Train
        y = self.targetname
        x = [x for x in data.columns if data[x].dtypes != 'object']
        u = [x for x in data.columns if data[x].dtypes == 'object' and x!=y ]
        img ={}
        for col in x:
            for cl in u:
                z=sns.boxplot(x=cl,y=col,hue=y,data=data,split=True, palette="Set3")
                fig = z.get_figure()
                img[col+cl]=fig
        return img
    def bargraph(self):
        data=self.Train
        y = self.targetname
        x = [x for x in data.columns if data[x].dtypes != 'object']
        u = [x for x in data.columns if data[x].dtypes == 'object' and x!=y ]
        s = u.copy()
        s.pop(0)
        label = LabelEncoder()
        data[y]=label.fit_transform(list(data[y].values))
        
        img ={}
        for col in x:
            for cl in u:
                for cz in s:
                    f, ax = plt.subplots(figsize=(16, 4))
                    z=sns.barplot(x=cl,y=y,hue=cz,data=data)
                    ax.legend(ncol=2, loc="upper left", frameon=True)
                    fig = z.get_figure()
                    img[col+cl+cz]=fig
                    s.remove(cz)
        return img
    def countgraph(self):
        data=self.Train
        y = self.targetname
        #x = [x for x in data.columns if data[x].dtypes != 'object']
        u = [x for x in data.columns if data[x].dtypes == 'object' and x!=y ]
        img ={}
        for cl in u:
            f, ax = plt.subplots(figsize=(16, 4))
            z=sns.countplot(x=cl,y=col,hue=y,data=data)
            ax.legend(ncol=2, loc="upper left", frameon=True)
            fig = z.get_figure()
            img[col+cl]=fig
        return img
    def scatgraph(self):
        data=self.Train
        y = self.targetname
        x = [x for x in data.columns if data[x].dtypes != 'object']
        u = x.copy()
        u.pop(0)
        img ={}
        for col in x:
            for cl in u:
                sns.set_context(rc={"figure.figsize": (8, 4)})
                z=sns.lmplot(x=cl,y=col,hue=y,data=data,palette="Set3")
                fig = z.fig
                img[col+cl]=fig
        return img