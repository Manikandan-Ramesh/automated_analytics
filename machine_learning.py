# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 10:40:25 2018

@author: ishwarya.sriraman
"""
from sklearn.linear_model import LogisticRegressionCV
from sklearn.cross_validation import train_test_split
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix  
from sklearn.metrics import precision_recall_fscore_support
from sklearn import metrics
from sklearn.metrics import roc_auc_score
from sklearn.metrics import matthews_corrcoef
#import statsmodels.stats.gof as ssg
#from scipy import stats
import scipy.stats

class machine_learning:
    
    def __init__(self,df,target):
        self.df=df
        self.target=target
        
    def precision_recall_score(self,Y_test,pred):
        Y=self.target
        p = pd.crosstab(Y_test, pred, rownames=['Actual'], colnames=['Predicted'], margins=True)
#        confmat=confusion_matrix(Y_test, pred)
#        l=sorted(set(self.df[Y].values))
#        p=pd.DataFrame(data=confmat,index=l,columns=l)
        p.to_excel("Confusion_matrix.xlsx")
        score=precision_recall_fscore_support(Y_test, pred, average='macro') 
        return score
        
    def roc_area(self,Y_test,pred):
        fpr, tpr, thresholds = metrics.roc_curve(Y_test, pred,pos_label=0)
        roc_score=roc_auc_score(Y_test, pred)
        return(roc_score)
        
    def goodness_of_fit(self,Y_test,pred):
        freq_0=Y_test.values.sum()
        freq_pred_0=pred.sum()
        freq_1=len(Y_test)-freq_0
        freq_pred_1=len(pred)-freq_pred_0
        print("Goodness of fit is")
        observed=[freq_pred_0,freq_pred_1]
        expected=[freq_0,freq_1]
        return(scipy.stats.chisquare(observed, f_exp=expected))
    
    def logistic_regression(self,X):
        Y=self.target
        X_train,X_test,Y_train,Y_test = train_test_split(self.df[X],self.df[Y],test_size=0.33,random_state=3)
        model=LogisticRegressionCV(Cs=10, fit_intercept=True, cv=None, dual=False, penalty='l2', scoring=None, solver='lbfgs', tol=0.0001, max_iter=100, class_weight=None, n_jobs=1, verbose=0, refit=True, intercept_scaling=1.0, multi_class='ovr', random_state=None)
        model_fit=model.fit(X_train,Y_train)
        KS=self.KS_Calculator(X_train,Y_train,model_fit)
        KS.to_csv('KStrain.csv')
        con_value=self.concordunce(X_train,Y_train,model_fit)
        print('Area under the curve is')
        print(con_value)
        print ('Mean accuracy Scikit learn: ')
        print(model.score(X_test,Y_test))
        pred=model.predict(X_test)
        KS1=self.KS_Calculator(X_test,Y_test,model_fit)
        KS1.to_csv('KS_test.csv')
        return (Y_test,pred,model_fit)    
        
    def KS_Calculator(self,X_train,Y_train,model_fit):
        df_data = X_train.copy()
        X_data=X_train.copy()
        df_data['Actual'] = Y_train
        df_data['Predict']= model_fit.predict(X_data)
        y_Prob = pd.DataFrame(model_fit.predict_proba(X_data))
        df_data['Prob_1']=list(y_Prob[1])
        
        df_data.sort_values(by=['Prob_1'],ascending=False,inplace=True)
    
        df_data.reset_index(drop=True,inplace=True)
    
        df_data['Decile']=pd.qcut(df_data.index,10,labels=False)
    
        KS = pd.DataFrame()
    
        grouped = df_data.groupby('Decile',as_index=False)
        
        KS['Max_Scr']=grouped.max().Prob_1
        KS['Min_Scr']=grouped.min().Prob_1
        KS['Event']=grouped.sum().Actual
        KS['Total']=grouped.count().Actual
        KS['Per_Events'] = KS['Event']/KS['Event'].sum()
        KS['Event ratio']=KS['Event']/KS['Total']

        KS['Per_Non_Events'] = (KS['Total']-KS['Event'])/(KS['Total'].sum()-KS['Event'].sum())
    
        KS['Cum_Events'] = KS.Per_Events.cumsum()
        KS['Cum_Non_Events'] = KS.Per_Non_Events.cumsum()
        KS['KS'] = KS['Cum_Events']-KS['Cum_Non_Events']
        KS['BadRate'] = KS['Event']/KS['Total']
        KS['popcum']=[0.1,0.20,0.30,0.40,0.50,0.60,0.70,0.80,0.90,1]
        KS['lift']=KS['Cum_Events']/KS['popcum']
        
        return KS
    
    def concordunce(self,X_train,Y_train,model_fit):
            y_pred=model_fit.predict(X_train)
            y_prob=model_fit.predict_proba(X_train)
            l=[]
            for x in y_pred:
                if(x=='no'):
                    l.append(0)
                else:
                    l.append(1)
            y_pred=l
        
            l2=[]
            l3=[]
            
            for i,j in y_prob:
                if(i>j):
                    l2.append(i)
                elif(j>i):
                    l3.append(j)
            concor=0
            discor=0
            tied=0
            
            for i in l2:
                for j in l3:
                    if(i>j):
                        concor=concor+1
                    elif(j>i):
                        discor=discor+1
                    else:
                        tied=tied+1
                        
            total_pairs=len(l2)*len(l3)
            con_per=concor/total_pairs
            dis_per=discor/total_pairs
            tied_per=tied/total_pairs
            area_under_curve=con_per+0.5*tied_per
            return(area_under_curve)


        

        
        