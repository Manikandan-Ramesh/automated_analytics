import pandas as pd
from scipy.stats import kurtosis
class deriving_feature:
    """this class is supposed to help end user derive feature on the go as well create 
    some feature automatically"""
    
    """Please use Python 3"""
    
    def __init__(self,df):
        self.df=df
                   
    def change_to_char(self,clmn_nm_list):
        """To change datatype of given columns to object datatype"""
        for i in clmn_nm_list:
            p=str(self.df[i])
            self.df[i]=p
            del p
        
        return self.df
    
    def change_to_num(self,clmn_nm_list1):
           """To change datatype of given columns to float datatype"""
           for i in clmn_nm_list1: 
                try:
                    self.df[i]=self.df[i].astype(float)
                except:
                   print(i + "Column cannot be converted to float.")
                
           return self.df
    
    def change_to_date(self,clmn_nm_list1):
            """To change datatype of given columns to date datatype"""
            for i in clmn_nm_list1: 
                try:
                    self.df[i]=pd.to_datetime(self.df[i])
                except:
                    print(i + " column cannot be changed to date datatype.")
                            
            return self.df
            
    def user_create_function(self,group_by_col,mean_l=None,sum_l=None,count_l=None):
        cl=[]    
#        gmean=pd.Series()
#        gcount=pd.Series()
#        gsum=pd.Series()
#            
        mask = self.df.astype(str).apply(lambda x : x.str.match(r'(\d{1,2}/\d{1,2}/\d{2,4})|(\d{1,2}-\w{3}-\d{2,4})|(\d{2,4}-\w{3}-\d{1,2})').any())
        self.df.loc[:,mask] = self.df.loc[:,mask].apply(pd.to_datetime)
        datecol=[x for x in self.df.columns if self.df[x].dtypes=='datetime64[ns]']
        cont1 = [x for x in self.df.columns if self.df[x].dtypes != 'object' and x not in datecol].copy()
        cont=[x for x in cont1 if x not in mean_l and x not in sum_l and x not in count_l ]
        if(mean_l is not None):
            gmean = self.df.groupby(by=group_by_col)[mean_l].mean().copy()
            
            for x in mean_l:
                cl.append(x+'_Mean')
            gmean.columns = cl
        else:
            gmean=pd.DataFrame()
        
        cl=[]
        if(sum_l is not None):
            gsum = self.df.groupby(by=group_by_col)[sum_l].sum()
            for x in sum_l:
                cl.append(x+'_Sum')
            gsum.columns = cl
        else:
            gsum=pd.DataFrame()
        
        cl=[]
        if(count_l is not None):
            gcount = self.df.groupby(by=group_by_col)[count_l].count().copy()
            
#            cl = count_l
            for x in count_l:
                cl.append(x+'_Count')   
            gcount.columns = cl
        else:
            gcount=pd.DataFrame()
        
        gmedian = self.df.groupby(by=group_by_col)[cont].median().copy()
#        gmedian.reset_index(inplace=True)
        
        cl = []
        for x in cont:
            cl.append(x+'_Median')   
        gmedian.columns = cl
        
        
        gkurtosis = self.df.groupby(by=group_by_col)[cont].apply(pd.DataFrame.kurt)
#        gkurtosis=kurtosis(self.df.groupby(by=groupby_col)[cont])
#        gkurtosis.reset_index(inplace=True)
        
        cl = []
        for x in cont:
            cl.append(x+'_Kurtosis')   
        gkurtosis.columns = cl
        
        gskew = self.df.groupby(by=group_by_col)[cont].apply(pd.DataFrame.skew).copy()
#        gskew.reset_index(inplace=True)
        
        cl = []
        for x in cont:
            cl.append(x+'_Skew')   
        gskew.columns = cl
        
        gmin = self.df.groupby(by=group_by_col)[cont].min().copy()
#        gmin.reset_index(inplace=True)
        
        cl =[]
        for x in cont:
            cl.append(x+'_Min')   
        gmin.columns = cl
        
        
        gquantile = self.df.groupby(by=group_by_col)[cont].quantile(.25).copy()
#        gquantile.reset_index(inplace=True)
        
        cl =[]
        for x in cont:
            cl.append(x+'_Quantile(.25)')   
        gquantile.columns = cl
        
        gquantile1 = self.df.groupby(by=group_by_col)[cont].quantile(.75).copy()
#        gquantile1.reset_index(inplace=True)
        
        cl =[]
        for x in cont:
            cl.append(x+'_Quantile(.75)')   
        gquantile1.columns = cl
        
        gmax = self.df.groupby(by=group_by_col)[cont].quantile(1).copy()
#        gmax.reset_index(inplace=True)
        
        cl =[]
        for x in cont:
            cl.append(x+'_Max')   
        gmax.columns = cl
        rolled_df=pd.concat([gmedian,gkurtosis.iloc[:,2:],gskew.iloc[:,2:],gquantile.iloc[:,2:],gquantile1.iloc[:,2:],gmax.iloc[:,2:],gmin.iloc[:,2:]],axis=1)
        rolled_df=pd.concat([rolled_df,gmean,gcount,gsum],axis=1)
        del gmedian
        del gkurtosis
        del gskew
        del gquantile
        del gquantile1
        del gmax
        del gmin
        return(rolled_df)


def create_dataframe_with_features(df):   
    """Wrapper function"""

    d=deriving_feature(df)
    
    rolled_df=df
    print(rolled_df.info())
    
    """To handle if columns has commas"""
    rolled_df.columns = rolled_df.columns.str.replace("[,]", "_")

    datecol=[x for x in rolled_df.columns if rolled_df[x].dtypes=='datetime64[ns]'].copy()
    cont = [x for x in rolled_df.columns if rolled_df[x].dtypes != 'object' and x not in datecol].copy()
    cat=[x for x in rolled_df.columns if rolled_df[x].dtypes == 'object' and x not in datecol].copy()
    
    print("Continous variables are")
    print(cont)
    print("Categorical variables are")
    print(cat)
    
    p=True
    f1=0
    while(p):
        f1=input("Enter 1 if you want to change columns into date datatype else enter 0 ")
        try:
            f1=int(f1)
            if(f1==1):
                str1=input("Enter the columns you want to change to date datatype.Please seperate it with a comma ")
                clmn_nm_list1=str1.split(",")
                f=True
            else:
                break
                f=False
            while(f):
                for i in clmn_nm_list1:
                    if i in df.columns:
                        f=False
                    else:
                        f=True
                        p1=True
                        while(p1):
                            try:
                                p1=False
                                b=input(i + " column is not found please enter 1 to continue else 0 to exit")
                                if(int(b)==1):
                                    str1=input("Enter the column names.Please seperate the column names with a comma ")
                                    clmn_nm_list1=str1.split(",")
                                    break
                                else:
                                    f=False
                            except:
                                p1=True
                                print("You have entered the wrong value. Please try again.")
                 
            if(f==False):
                    rolled_df=d.change_to_date(clmn_nm_list1)
                    p=False
        except:
            print("You have not entered correct value please try again")
            p=True
    
    f1=0
    p=True
    while(p):
        f1=input("Enter 1 if you want to change any column to object datatype else enter 0 ")
        try:
            f1=int(f1)
            if(f1==1):
                str1=input("Enter the column names you want to change.Please seperate the column names with a comma ")
                clmn_nm_list=str1.split(",")
                f=True
            else:
                break
                f=False
            while(f):
                for i in clmn_nm_list:
                    if i in df.columns:
                        f=False
                    else:
                        f=True
                        p1=True
                        while(p1):
                            try:
                                b=input(i + " column is not found enter 1 if you want to continue else 0 ")
                                b=int(b)
                                if (b==1):
                                    str1=input("Enter the column names.Please seperate the column names with a comma")
                                    clmn_nm_list=str1.split(",")
                                    break
                                else:
                                    return df
                                p1=False
                            except:
                                p1=True
                                print("You have not entered a correct value. Please enter again")
                     
            if(f==False):
                    rolled_df=d.change_to_char(clmn_nm_list)
                    p=False
        except:
            print("You have not entered correct value please try again")
            p=True    
    p=True
    while(p):
        f1=input("Enter 1 if you want to change any column to float datatype else enter 0 ")
        try:
            f1=int(f1)
            p=False
            if(int(f1)==1):
                str1=input("Enter the column names you want to change.Please seperate the column names with a comma ")
                clmn_nm_list1=str1.split(",")
                f=True
            else:
                break
                f=False
            while(f):
                for i in clmn_nm_list1:
                    if i in df.columns:
                        f=False
                    else:
                        f=True
                        p1=True
                        while(p1):
                            try:
                                p1=False
                                b=input(i + " column is not found please enter 1 to continue else 0 to exit")
                                if(int(b)==1):
                                    str1=input("Enter the column names.Please seperate the column names with a comma ")
                                    clmn_nm_list1=str1.split(",")
                                    break
                                else:
                                    f=False
                            except:
                                p1=True
                                print("You have entered wrong value enter again.")
             
            if(f==False):
                    rolled_df=d.change_to_num(clmn_nm_list1)
        except:
            print("You have not entered correct value please try again")
            p=True
            
    datecol=[x for x in rolled_df.columns if rolled_df[x].dtypes=='datetime64[ns]'].copy()
    cont = [x for x in rolled_df.columns if rolled_df[x].dtypes != 'object' and x not in datecol].copy()
    cat=[x for x in rolled_df.columns if rolled_df[x].dtypes == 'object' and x not in datecol].copy()
    print("Date columns:")
    print(datecol)
    print("Continous variables:")
    print(cont)
    print("Categorical variable:")
    print(cat)
    
    mean_col=None
    sum_col=None
    count_col=None
    p=True
    f=True
    while(p):
        f1=input("Enter 1 if you want to create any derived columns else enter 0 ")
        try:
            f1=int(f1)
            p=False
            if(f1==1):
                flg=input("Enter 1 if you want to create mean as a feature for variables")
                if(flg==1):
                    mean_col=input("Enter the column names you want mean for and seperate column names using comma:")
                flg=input("Enter 1 if you want to create sum as a feature for variables")
                if(flg==1):
                    sum_col=input("Enter the column names you want sum for and seperate column names using comma:")
                flg=input("Enter 1 if you want to create count as a feature for variables")
                if(flg==1):
                    count_col=input("Enter the column names you want count for and seperate column names using comma:")
                
                rolled_df1,group_by_col=d.user_create_function(mean_col,sum_col,count_col)
                cols_needed=rolled_df.columns.difference(rolled_df1)
                dataframe=pd.merge(rolled_df1,rolled_df[cols_needed],left_index=True,right_index=True,how='outer')
                rolled_df=pd.DataFrame()
                rolled_df=dataframe
        except:
            print("You have not entered correct value please try again")
            p=True
    f=True
    p=True
    while(p):
        f1=input("Enter 1 if you want to group data by any column and roll up data else enter 0 ")
        try:
            f1=int(f1)
            p=False
            if(int(f1)==1):
                f=True
            else:
                break
                f=False
            while(f):
                for i in group_by_col:
                    if i in df.columns or i in cat:
                        f=False
                    else:
                        f=True
                        print(i + " column is not found.")
                        g=0
                        g=input("Enter 0 if you want to exit the function else enter 1:")
                        if(int(g)==1):
                            str1=input("Enter the column names.Please seperate the column names with a comma ")
                            group_by_col=str1.split(",")
                            break
                        else:
                            return df
                    
            f=True
            while(f):
                for i in group_by_col:
                    if i in cont:
                        f=True
                        print(i + "column is considered as continous variable.")
                        p1=True
                        while(p1):
                            try:
                                p1=False
                                f1=input("Enter 1 to convert to categorical else enter 0")
                                f1=int(f1)
                            except:
                                p1=True
                                print("You have entered wrong value. Please try again.")
                        if(f1==1):
                            try:
                                p=str(df[i])
                                df[i]=p
                                del p
                                cat=[x for x in df.columns if df[x].dtypes == 'object'].copy()
                                b=input("The column is converted to categorical.Please enter 1 to enter the column names else 0 to exit from the function")
                                if(int(b)==1):
                                    str1=input(" Please enter the column names to group by.Please seperate the column names with a comma ")
                                    group_by_col=str1.split(",")
                                else:
                                    return df
                            except:
                                print("This column cannot be converted to categorical variable")
                                f=True
                            break
                        elif f1==0:
                            f=False
                    else:
                        f=False
            if(f==False):
                    rolled_df=d.create_features(rolled_df,group_by_col)
        except:
            print("You have not entered correct value please try again")
            p=True
            

                
    del f
    del cont
    del cat
    del datecol
    
    return (rolled_df)