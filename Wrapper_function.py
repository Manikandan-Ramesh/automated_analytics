# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 17:24:16 2018

@author: ishwarya.sriraman
"""
import pandas as pd
import deriving_features
from eda import eda
from feature_transformation import feature_transformation
import os
from machine_learning import machine_learning
from feature_selection import feature_selection
#from derived_columns import derived_columns

def load_data(Path):
        """Function to load data"""
        f=True
        while(f):
            try:
                df=pd.read_csv(Path).copy()
                f=False
                for col in df.columns:
                    if df[col].isnull().sum()==len(df):
                        del df[col]
                return df
            except FileNotFoundError:
                f=True
                print("File not Found in the specified path. Give path again")
                Path=input("Enter the path again: ")

        return df

def main():
    Path=input("Enter path of file:")
    df=load_data(Path)
    """Wrapper function which calls all the other functions"""
    rolled_df=deriving_features.create_dataframe_with_features(df)
    print(rolled_df.columns)
    target=input("Enter the column name of y variable:")
    e=eda(rolled_df,target)
    event=input("Enter the event:")
    er=e.eventRatio(event)
    print(er)
    stat=e.impstat()
    rng=e.range()
    rng = rng.rename('Range')
    print("Size is")
    print(rng.size)
    iq=e.iqr()
    iq=iq.rename('IQR')
    cor=e.corr()
    print(cor)
    ske=e.skew()
    print(ske)
    ske=ske.rename('Skewness')
    kur=e.kurt()
    print(kur)
    kur=kur.rename('Kurtosis')
    [mi,mi1]=e.missinginfo()
    print("missing value is")
    print(pd.Series(mi1[1:]))
    mi1=mi1.rename('Missing values')
    e.missingplot()
    b=e.bin('woe','y','yes','pdays','day')
    print(b)
    try:
        os.remove('D:/Other projects/python modules/Report.xlsx')
        engine = 'xlsxwriter'
        writer = pd.ExcelWriter('Report.xlsx',engine=engine)
        stat1=pd.DataFrame(stat.T)
        print(stat1)
        stat1.to_csv(writer,startcol=0,startrow=5)
        ws = writer.sheets['Sheet1']
        ws.write_string(1, 4, 'DataDescription')
        rng.to_excel(writer,startcol=9,startrow=5,index=False)
        iq.to_excel(writer,startcol=10,startrow=5,index=False)
        ske.to_excel(writer,startcol=11,startrow=5,index=False)
        kur.to_excel(writer,startcol=12,startrow=5,index=False)
        ws.write_string(5+rng.size+2,5,'Correlation')
        cor.to_excel(writer,startcol=0,startrow=5+rng.size+4)
#        mi1[1:].to_excel(writer,startcol=rng.size+2,startrow=5+rng.size+4)
        b.to_excel(writer,startcol=12,startrow=5+rng.size+4)
#        ws.write_string(5+rng.size+2,14,'Binning')
#        misplot.to_excel(writer,startcol=0,startrow=rng.size+rng.size+5+3+5)
        writer.close()
    except:
        engine = 'xlsxwriter'
        writer = pd.ExcelWriter('Report.xlsx',engine=engine)
        stat1=pd.DataFrame(stat.T)
        print(stat1)
        stat1.to_excel(writer,startcol=0,startrow=5)
        ws = writer.sheets['Sheet1']
        ws.write_string(1, 4, 'DataDescription')
        rng.to_excel(writer,startcol=9,startrow=5,index=False)
        iq.to_excel(writer,startcol=10,startrow=5,index=False)
        ske.to_excel(writer,startcol=11,startrow=5,index=False)
        kur.to_excel(writer,startcol=12,startrow=5,index=False)
        ws.write_string(5+rng.size+2,5,'Correlation')
        cor.to_excel(writer,startcol=0,startrow=5+rng.size+4)
        mi1[1:].to_excel(writer,startcol=rng.size+2,startrow=5+rng.size+4)
        writer.close()
    ft=feature_transformation(rolled_df,target)
    p=True
    while(p):
        degree=input("Enter the degree of the polynomial features you want to derive")
        try:
            degree=int(degree)
            p=False
        except:
            print("You did not enter correct value. Try again")
            p=True
      
    poly_feature_set=ft.poly_features()
    feature_transformed_df=ft.transformation()
    cols_to_use = poly_feature_set.columns.difference(feature_transformed_df.columns)
    final_df = pd.merge(feature_transformed_df, poly_feature_set[cols_to_use], left_index=True, right_index=True, how='outer')
    print(final_df.columns)
    cat=[x for x in final_df.columns if final_df[x].dtypes == 'object'].copy()
    label_encod=ft.label_encoding(final_df)
    one_hot=ft.one_hot_encoding(label_encod,cat)
    cols_use=one_hot.columns.difference(final_df.columns)
    final_f = pd.merge(final_df, one_hot[cols_use], left_index=True, right_index=True, how='outer')
    nystroem_rbf_dataframe=ft.kernel_transformation_using_nystroem_rbf(final_f,cat)
    cols_needed=nystroem_rbf_dataframe.columns.difference(final_df)
    final_data=pd.merge(final_df,nystroem_rbf_dataframe[cols_needed],left_index=True,right_index=True,how='outer')
    f=0
    p1=True
    while(p1):
        try:
            p1=False
            f=input("Enter 1 if you want to write the dataframe into a csv file else enter 0:")
            if(int(f)==1):
                path=input("Enter the path where you want to save:")
                final_data.to_csv(path,index=False)
        except:
            p1=True
            print("You have entered wrong value. Please try again.")
            
    ml=machine_learning(final_data,target)
    datecol=[x for x in final_data.columns if final_data[x].dtypes=='datetime64[ns]']
    X1=[x for x in final_data.columns if final_data[x].dtypes != 'object' and x not in datecol and x not in target]     
    X=[x for x in X1 if x not in cat]
    fs=feature_selection(final_data,target)
#    fs.recursive_feature_elimination(X)
    X1=[]
    X1=fs.PCA(95)
    cat=[x for x in X1 if final_data[x].dtypes == 'object'].copy()
    X=[x for x in X1 if x not in cat]
    X=fs.correlation(X)
#    dc=derived_columns(final_data)
#    dc.create_derived_columns()
    
    Y_test,pred=ml.logistic_regression(cat,X)
    ml.precision_recall_score(Y_test,pred)
    ml.roc_area(Y_test,pred)
    ml.goodness_of_fit(Y_test,pred)

main()