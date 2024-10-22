# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 12:37:46 2018

@author: ishwarya.sriraman

"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import scale
from sklearn.decomposition import PCA
from eda2 import eda
from sklearn.feature_selection import VarianceThreshold
from sklearn.svm import SVR
from sklearn.feature_selection import RFECV

class feature_selection:
     def __init__(self,df,target):
         self.df=df
         self.target=target
         pass
    
     def recursive_feature_elimination(self,score_type):
        y=self.target
        X=[x for x in self.df.columns if x not in self.target]
        estimator = SVR(kernel="linear")
        selector = RFECV(estimator, step=1, cv=5,scoring=score_type)
        selector = selector.fit(self.df[X], self.df[y])
        print("Recursive feature elimination")
        print(selector)
        print("Feature ranking")
        print(selector.ranking_)

     def PCA(self,thres):
         scaled_data = pd.DataFrame(scale(self.df), columns=self.df.columns, index = self.df.index)
         pca1 = PCA()
         pca=pca1.fit(scaled_data.values)
         variance_explained = pca.explained_variance_ratio_
         cumulative_variance_explained = np.cumsum(np.round(pca.explained_variance_ratio_, decimals=4)*100)
         cum_var_exp_df=pd.DataFrame(cumulative_variance_explained, index = pd.Series(["PC_"+str(i) for i in range(pca.n_components_)]),columns=["Cumulative Variance Explained"])
         cum_var_df_thres=cum_var_exp_df.loc[cum_var_exp_df['Cumulative Variance Explained']<thres]
         rng=len(cum_var_df_thres)
         pc=pd.DataFrame()
         for i in range(rng):
             PC_variance = pd.DataFrame([pd.Series(scaled_data.columns),pd.Series(pca.components_[i]), pd.Series(pca.components_[i]).abs()]).T
             PC_variance.columns = ["Variable","Value","Sort Column"]
             pc=pc.append(PC_variance.sort_values(["Sort Column"] ,ascending=False).head())
             
         return(pc['Variable'].unique(),pca)