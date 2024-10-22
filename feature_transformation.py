import pandas as pd
import numpy as np
from scipy import stats
from sklearn.kernel_approximation import RBFSampler,Nystroem
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import f1_score
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import STAP
from rpy2.robjects import r
import rpy2.robjects as robjects
from rpy2.robjects.vectors import StrVector
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
import rpy2.robjects.packages as rpackages
from rpy2.robjects.lib.dplyr import dplyr
from rpy2.robjects import default_converter
from rpy2.robjects.conversion import localconverter
import re


class feature_transformation:
    def __init__(self,rolled_df,target):
        self.rolled_df=rolled_df
        self.target=target
    
    def poly_features(self):
#        datecol=[x for x in self.rolled_df.columns if self.rolled_df[x].dtypes=='datetime64[ns]'].copy()
#        cont = [x for x in self.rolled_df.columns if self.rolled_df[x].dtypes != 'object' and x not in datecol].copy()
        df1=pd.read_csv("var_transformation.csv")
        cont=df1[df1['Polynomial_Transformation']==1]['Variables']
        cont=list(cont)
        X=self.rolled_df[cont]
        poly = PolynomialFeatures(interaction_only=True,include_bias=False)
        f=poly.fit(X)
        names=[]
        for i in cont:
            names.append(i+'polytransform')
        l=f.get_feature_names(names)
        p= poly.transform(X)
        poly_df=pd.DataFrame(data = p, columns=l)
        data=pd.concat([self.rolled_df,poly_df],axis=1)
        return data
    
    def label_encoding(self):
        mask = self.rolled_df.astype(str).apply(lambda x : x.str.match(r'(\d{1,2}/\d{1,2}/\d{2,4})|(\d{1,2}-\w{3}-\d{2,4})|(\d{2,4}-\w{3}-\d{1,2})').any())
        self.rolled_df.loc[:,mask] = self.rolled_df.loc[:,mask].apply(pd.to_datetime)
        datecol=[x for x in self.rolled_df.columns if self.rolled_df[x].dtypes=='datetime64[ns]'] 
        cat=[x for x in self.rolled_df.columns if self.rolled_df[x].dtypes == 'object' and x not in datecol].copy()
        for i in cat:
            self.rolled_df[i]=self.rolled_df[i].astype('category')
            self.rolled_df[i]=self.rolled_df[i].cat.codes
        return(cat,self.rolled_df)
        
    def one_hot_encoding(self,cat1):    
        enc = OneHotEncoder(categorical_features='all',handle_unknown='error', n_values='auto', sparse=True)
        cat=[x for x in cat1 if x!=self.target]
        enc.fit(self.rolled_df[cat])  
        n=enc.transform(self.rolled_df[cat]).toarray()
        cols=[]
        for i in cat:
            unique_values=self.rolled_df[i].unique()
            for j in unique_values:
                cols.append(i + '_'+ str(j))
        one_hot_df=pd.DataFrame(data = n, columns=cols)
        data=pd.concat([self.rolled_df,one_hot_df],axis=1)
        return data
    
    def woe_transformation(self):
        df=pd.read_excel('D:\\Other projects\\python modules\\univariates_bivariates.xlsx','bivariates')
        df.reset_index(inplace=True)
        df=df[df.columns[~df.columns.str.contains('Unnamed:')]]
        df = df.dropna()
        df = df.replace(['Missing','Total'],['=="Missing"','=="Total"'])
        from collections import defaultdict 
        woe_dict = defaultdict(list)
        for i, x in df[['keys','CAT','WOE']].iterrows():
            woe_dict[x['keys']].append((x['CAT'],x['WOE']))  
        new_woe_dict = {k:dict(v) for k,v in woe_dict.items()}
        del new_woe_dict['keys']
        num_cols = self.rolled_df._get_numeric_data().columns
        l = []
#        print(new_woe_dict)
        for k,v in new_woe_dict.items():
            if k not in num_cols:
                for val in self.rolled_df[k]:
                    l.append((v[val]))
            else:
                print (k )
                for val in self.rolled_df[k]:
#                    print (v , val)
                    try :
                        l.append((list(filter(lambda v1: eval(str(val)+v1[0]), v.items()))[0][1]))
                    except Exception as e :
                        print (e)
            
                        l.append(None)
            self.rolled_df['WOE_transformation_'+k]=l
            l=[]
            
        for k in new_woe_dict.keys():
            print("k is")
            print(k)
            del self.rolled_df[k]
        return self.rolled_df
             
    def kernel_transformation_using_nystroem_rbf(self):
#        
#        datecol=[x for x in self.df.columns if self.df[x].dtypes=='datetime64[ns]']
#        X1=[x for x in self.df.columns if self.df[x].dtypes != 'object' and x not in datecol and x not in self.target]     
#        X=[x for x in X1 if x not in cat]
#        y=self.target
        j = np.linspace((10**-2),(10**2),50)
        g=0
        max1=0
        df1=pd.read_csv("var_transformation.csv")
        X=df1[df1['Kernel_transformation']==1]['Variables']
        X=list(X)
        y=self.target
        for i in j:
            rbf_feature = Nystroem(kernel = 'rbf', gamma=i, random_state=2,n_components=10)
            rbf_feature.fit(self.rolled_df[X])
            X_features = rbf_feature.transform(self.rolled_df[X])
            X_features=np.nan_to_num(X_features)
            clf = SGDClassifier()   
            clf.fit(X_features,self.rolled_df[y])
            y_pred = clf.predict(X_features)
            score=f1_score(self.rolled_df[y], y_pred, average='micro') 
            if(score>max1):
                max1=score
                g=i
        rbf_feature = RBFSampler(gamma=g, random_state=2,n_components=10)
        rbf_feature.fit(self.rolled_df[X])
        X_features = rbf_feature.transform(self.rolled_df[X])
        l=[]
        for p in range(10):
            l.append('k_'+str(p))
        X_features=pd.DataFrame(data=X_features,columns=l)
        clf = SGDClassifier()   
        clf.fit(X_features, self.rolled_df[y]) 
        score=f1_score(self.rolled_df[y], y_pred, average='macro') 
        print("Score is")
        print(score)
        print(g)
        data=pd.concat([self.rolled_df,X_features],axis=1)
        return data
            
        
    def transformation(self):
        """This function transforms the continous variables"""
        df=pd.read_csv("D:\\Other projects\\python modules\\var_transformation.csv")
        for i in df.columns:
            l=[]
            if(i=='Variables'):
                continue
            else:
                l=df[df[i]==1]['Variables']
                l=l.tolist()
        #     print(len(l))
            if len(l)!=0:
                for j in l:
                    if i=="Square root":
                        self.rolled_df[j+"_square root"]=self.rolled_df[j].apply(np.sqrt)
                    elif i=="Square":
                        self.rolled_df[j+"_Square"]=self.rolled_df[j]**2
                    elif i=='Log':
                        self.rolled_df[j+'_log']=np.log10(self.rolled_df[j])
                    elif i=='Inverse':
                        self.rolled_df[j+'_Inverse']=1/self.rolled_df[j]
                    elif i=='Box-Cox':
                        try:
                            self.rolled_df[i + '_box_cox']=stats.boxcox(self.rolled_df[i])[0]
                            self.rolled_[i + '_box_cox']=self.rolled_df[i + '_box_cox'].astype(float)
                        except:
                            self.rolled_df[i + '_box_cox']='NEGATIVE VALUE'
        
        return self.rolled_df