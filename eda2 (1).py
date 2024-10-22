# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 13:51:47 2018

@author: mritunjay.kumar
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
from rpy2.robjects import pandas2ri
from rpy2.robjects import default_converter
from rpy2.robjects.conversion import localconverter
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import re
from sklearn.feature_selection import VarianceThreshold


class eda:
    ''' This is the module designed for exploratory data analysis. Using this module User
    can do univariate, bi-variate analysis. Along with it user may get binning sugestion, can
    remove variable univariate way or bivariate way'''
    def __init__(self,data,target,event):
        
        ''' This method is initialize class eda object'''
#        self.pool =  mp.Pool(processes=2)
        self.train = data
        self.target = data[target]
        self.targetVarName = target
        self.event = event
    
    def univariate(self):
        '''
            this function is for univariate analysis,
        '''
        #if  
        x = [x for x in self.train.columns if self.train[x].dtypes != 'object']
        data = self.train[x]
        #y = data.describe()
        evcount = self.target.value_counts()
        evratio = evcount[self.event]/self.target.count()
        def Range(y):
            mi = np.min(y)
            ma = np.max(y)
            rng = ma-mi
            return rng
        Rnge = data.apply(Range)
        def iqr(y):
            x25 = np.percentile(y,25)
            x75 = np.percentile(y,75)
            Iqr = x75 - x25
            return Iqr
            
        iQr = data.apply(iqr)
        def Skew(y):
            d = skew(y)
            return d
        skewness = data.apply(Skew)
        def Kurt(y):
            d = kurtosis(y)
            return d
        Kurtosis = data.apply(Kurt)
        
        mean = data.apply(np.mean)
        stdv = data.apply(np.std)
        median = data.apply(np.median)
        missingno = data.isnull().sum()
        def outlier(y):
            q1 = np.percentile(y,25)
            q3 = np.percentile(y,75)
            iqr = q3-q1
            outlier = ((y > (q3 +1.5*iqr)) |(y <(q1-1.5*iqr ))).sum()
            return outlier
        Q1 = data.quantile(.25)  
        Q3 = data.quantile(.75)
        out = data.apply(outlier)
        Frame = [Rnge,Q1,Q3,iQr,skewness,Kurtosis,mean,stdv,median,missingno,out]
        unistat = pd.concat(Frame,axis =1)
        unistat.columns = ['Range','Q1','Q3','IQR','Skewness','Kurtosis','mean','stdv','median','MissingValue','outlier']
        z = [x for x in self.train.columns if self.train[x].dtypes == 'object']
        dat = self.train[z]
        cat = {}
        for i in z:
            cat[i]= dat[i].value_counts()
        
        return {'catdist':cat,'event Ratio':evratio , 'unistat':unistat.transpose()}
    def metrics(self,method='IV'):
        ''' this is the function to calcualte, NMI, ChiSq stat and IV value for each algorithm.
        Continous variable are first converted in to categorical variable afgter binning process.
        Example to use:
            h= eda(data,'y','yes')
            f = h.metrics()
            it requires one argument method which is by defualt set to IV
            method arguments accepts value such as None, entropy,Chisq and IV'''
                
        utils = importr('utils')
        if method is None or method == 'entropy':
            cat = [x for x in self.train.columns if self.train[x].dtypes == 'object']
            num = [x for x in self.train.columns if self.train[x].dtypes != 'object']
            numdata = self.train[num]
            catdata = self.train[cat]
            while True:
                try:
                    smbinning = importr('smbinning')
                    woeBinning = importr('woeBinning')
                    InformationValue = importr('InformationValue')
                    foreach = importr('foreach')
                    doParallel = importr('doParallel')
                except Exception as e:
                    
                    y = str(e)
                    z = re.findall(r"'(.*?)'", y, re.DOTALL)[0]
                    utils.install_packages(z)
                else:
                    break
            while True:
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
                else:
                    break
            self.MutualI = {}
            for cal in catdata.columns:
                if cal != self.targetVarName:
                    pandas2ri.activate()
                    nmi = pandas2ri.ri2py(woe.nmi(catdata[cal],catdata[self.targetVarName]))
                    pandas2ri.deactivate()
                    self.MutualI[cal]=nmi
            numdat = numdata.copy()
            numdat[self.targetVarName]= self.target
            pandas2ri.activate()
            entdata = pandas2ri.ri2py(woe.entropy_based_bin(numdat))
            pandas2ri.deactivate()
            for cal in numdata.columns:
                if cal != self.targetVarName:
                    pandas2ri.activate()
                    nmi = pandas2ri.ri2py(woe.nmi(entdata[cal],entdata[self.targetVarName]))
                    pandas2ri.deactivate()
                    self.MutualI[cal]=nmi
                    
            return self.MutualI
        elif method == 'Chisq':
            cat = [x for x in self.train.columns if self.train[x].dtypes == 'object']
            num = [x for x in self.train.columns if self.train[x].dtypes != 'object']
            numdata = self.train[num]
            catdata = self.train[cat]
            
            while True:
                try:
                    smbinning = importr('smbinning')
                    woeBinning = importr('woeBinning')
                    InformationValue = importr('InformationValue')
                    foreach = importr('foreach')
                    doParallel = importr('doParallel')
                except Exception as e:
                    
                    y = str(e)
                    z = re.findall(r"'(.*?)'", y, re.DOTALL)[0]
                    utils.install_packages(z)
                else:
                    break
            while True:
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
                else:
                    break
            self.Chistat = {}
            for cal in catdata.columns:
                if cal != self.targetVarName:
                    pandas2ri.activate()
                    nmi = pandas2ri.ri2py(woe.ChiTest(catdata[cal],catdata[self.targetVarName]))
                    pandas2ri.deactivate()
                    self.Chistat[cal]=nmi
            numdat = numdata.copy()
            numdat[self.targetVarName]= self.target
            pandas2ri.activate()
            entdata = pandas2ri.ri2py(woe.entropy_based_bin(numdat))
            pandas2ri.deactivate()
            for cal in numdata.columns:
                if cal != self.targetVarName:
                    pandas2ri.activate()
                    nmi = pandas2ri.ri2py(woe.ChiTest(entdata[cal],entdata[self.targetVarName]))
                    pandas2ri.deactivate()
                    self.Chistat[cal]=nmi
            return self.Chistat
        elif method == "IV":
            cat = [x for x in self.train.columns if self.train[x].dtypes == 'object']
            num = [x for x in self.train.columns if self.train[x].dtypes != 'object']
            numdata = self.train[num]
            catdata = self.train[cat]
            while True:
                try:
                    smbinning = importr('smbinning')
                    woeBinning = importr('woeBinning')
                    InformationValue = importr('InformationValue')
                    foreach = importr('foreach')
                    doParallel = importr('doParallel')
                except Exception as e:
                    
                    y = str(e)
                    z = re.findall(r"'(.*?)'", y, re.DOTALL)[0]
                    utils.install_packages(z)
                else:
                    break
            while True:
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
                else:
                    break
            self.IVtable = {}
            for cal in catdata.columns:
                if cal != self.targetVarName:
                    pandas2ri.activate()
                    nmi = pandas2ri.ri2py(woe.wtable(catdata[cal],catdata[self.targetVarName],self.event))
                    pandas2ri.deactivate()
                    self.IVtable[cal]=nmi
            numdat = numdata.copy()
            numdat[self.targetVarName]= self.target
            pandas2ri.activate()
            while True:
                #i=0
                try:
                    #i=0
                    entdata = pandas2ri.ri2py(woe.woebin(numdat,self.targetVarName,self.event))
                    print('trying monobin')
                except Exception as e:
                    y = str(e)
                    z = re.findall(r"'(.*?)'", y, re.DOTALL)[0]
                    utils.install_packages(z)
                else:
                    break
                    
            entdata[self.targetVarName]=  self.target
            pandas2ri.deactivate()
            for cal in entdata.columns:
                if cal != self.targetVarName:
                    pandas2ri.activate()
                    nmi = pandas2ri.ri2py(woe.wtable(entdata[cal],entdata[self.targetVarName],self.event))
                    pandas2ri.deactivate()
                    self.IVtable[cal]=nmi
            return self.IVtable
        else:
            print('Please choose method argument equal to one of the list of IV,Chisq, None or entropy')
            
        
       
            
        
                                   
    
        
    def bininfo(self,method='IV'):
        num = [x for x in self.train.columns if self.train[x].dtypes != 'object']
        cat = [x for x in self.train.columns if self.train[x].dtypes == 'object']
        numdata = self.train[num]
        catdata = self.train[cat]
        while True:
            try:
                smbinning = importr('smbinning')
                woeBinning = importr('woeBinning')
                InformationValue = importr('InformationValue')
                foreach = importr('foreach')
                doParallel = importr('doParallel')
            except Exception as e:
                                  
                y = str(e)
                z = re.findall(r"'(.*?)'", y, re.DOTALL)[0]
                utils.install_packages(z)
            else:
                break
        while True:
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
            else:
                break
        self.IVtable = {}
        for cal in catdata.columns:
            if cal != self.targetVarName:
                pandas2ri.activate()
                nmi = pandas2ri.ri2py(woe.wdtable(catdata[cal],catdata[self.targetVarName],self.event))
                pandas2ri.deactivate()
                self.IVtable[cal]=nmi
        numdat = numdata.copy()
        numdat[self.targetVarName]= self.target
        pandas2ri.activate()
        while True:
            #i=0
            try:
                #i=0
                entdata = woe.woebinsuggest(numdat,self.targetVarName,self.event)
                h = dict(zip(entdata.names,map(list,entdata)))
                l = ["Cutpoint","CntRec","CntGood","CntBad","CntCumRec","CntCumGood",
                     "CntCumBad","PctRec","GoodRate","BadRate","Odds","LnOdds","WoE","IV"]
                
                for key, value in h.items():
                    self.IVtable[key] = dict(zip(l, map(list,h[key])))
                    self.IVtable[key] = pd.DataFrame(self.IVtable[key])
                    self.IVtable[key] = self.IVtable[key][l]


                print('trying Woebin')
            except Exception as e:
                y = str(e)
                z = re.findall(r"'(.*?)'", y, re.DOTALL)[0]
                utils.install_packages(z)
            else:
                break
        return self.IVtable
                    
        
    



    

        
    
    




        
    
        