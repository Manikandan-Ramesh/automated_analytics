### Building a classification model for CC segment lower income group(<50,000))###

import pandas as pd
import numpy as np
from numpy import inf
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix


#reading the data
cc_data = pd.read_excel("C:/Users/avudaippan.ramaiah/Desktop/Bajaj/CC/Data/cc_data.xlsx")
cc_data.columns = [x.upper() for x in cc_data.columns]
cc_data_cat = cc_data.select_dtypes(include=["object"])

#selecting only top variables
cc_data_top20 = cc_data.filter(items=["CID",
                                      "DISBURSEMENTDATE",
                                      "AVG_AMT_NYEARS_OD",
"TS_AVG_SANC_CLOSED_BL",
"TOTAL_CREDITLIMIT_CLOSED_CC",
"MIN_CREDITLIMIT_LIVE_CC",
"MIN_MOB_OTHERS",
"MIN_TENNURE_OTHERS",
"SIX_IOS_FLAG",
"SUM_AMTFIN_LIVE",
"MIN_PAID_LIVE_THIN",
"MIN_MOB_THIN",
"AVG_TENNURE_THIN",
"POS_6MNTH",
"TIME_SINCE_FIRST_CL",
"TS_AVG_SANC_CLOSED_CL",
"AVG_SANC_LIVE_CL",
"TIME_SINCE_LAST_LOAN",
"INTER_PURCHASE_TIME_OTHERS",
"MAX_SANC_CLOSED_OTHERS",
"RESTYPE_RENTED",
"CITY_TIER",
"OCCUPATION_CATEGORY",
"CITY_CLUSTER",
"WEALTH_PERSONA",
"PERSONA_STAMP_V5",
"TARGET"
"SALARY"


                                        

])

cc_data_top20.to_excel("C:/Users/avudaippan.ramaiah/Desktop/Bajaj/CC/Data/cc_data_25.xlsx")

#missing values     
missing_values = pd.DataFrame(cc_data_top20.isnull().sum())

#separating categorical and continuous variables 
df_cont = cc_data_top20.select_dtypes(include=["int64","float64"])
df_cat = cc_data_top20.select_dtypes(include=["object"])
df_date = cc_data_top20.select_dtypes(include=["datetime64[ns]"])

#replacing missing values
df_cont = df_cont.fillna(0)
df_cat = df_cat.fillna("Missing")


#log transformation of continuous variables
df_cont_log = np.log(df_cont.iloc[:,1:20])
df_cont_log[df_cont_log == -inf] = 0
df_cont = pd.concat([df_cont.iloc[:,0], df_cont_log], axis=1)

target = pd.DataFrame(cc_data[["TARGET"]])
#combining all datatyppes
df = pd.concat([df_date, df_cont,df_cat, target], axis=1)
df = df.dropna(axis=0, how='any')
`#creating dummies
df = pd.get_dummies(df, columns= df_cat.columns)

df['DISBURSEMENTDATE'] = pd.to_datetime(df.DISBURSEMENTDATE)

validation = df[(df['DISBURSEMENTDATE']>'2017-04-30')]
df= df[(df['DISBURSEMENTDATE']<'2017-05-01')]
del df["DISBURSEMENTDATE"]
del validation["DISBURSEMENTDATE"]
del df["CID"]
del validation["CID"]

#split the dataset in to train and test
train, test = train_test_split(df, test_size=0.2)

x_train = train ##defining x variables
y_train = x_train['TARGET'] ## defining target variables
del x_train['TARGET']


# defining test data 
x_test = test
y_test = x_test['TARGET']
del x_test['TARGET']

# defining validation data 
x_validation = validation
y_validation = x_validation['TARGET']
del x_validation['TARGET']


##random forest classification
clf = RandomForestClassifier(n_estimators = 25, oob_score = True, class_weight="balanced",random_state=50, max_features = "auto",min_samples_split=15,max_depth=15)
clf.fit(x_train, y_train)
train_predict = pd.DataFrame(clf.predict(x_train))
train_predict_proba = pd.DataFrame(clf.predict_proba(x_train))
train_prediction = pd.concat([train_predict,y_train.reset_index(drop=True),train_predict_proba], axis=1)
train_prediction.to_excel("C:/Users/avudaippan.ramaiah/Desktop/Bajaj/CC/Results/Iteration3/Results/train_predict.xlsx")
test_predict = pd.DataFrame(clf.predict(x_test))
test_predict_proba = pd.DataFrame(clf.predict_proba(x_test))
test_prediction = pd.concat([test_predict,y_test.reset_index(drop=True),test_predict_proba], axis=1)
test_prediction.to_excel("C:/Users/avudaippan.ramaiah/Desktop/Bajaj/CC/Results/Iteration3/Results/test_predict.xlsx")

validation_predict = pd.DataFrame(clf.predict(x_validation))
validation_predict_proba = pd.DataFrame(clf.predict_proba(x_validation))
validation_prediction = pd.concat([validation_predict,y_validation.reset_index(drop=True),validation_predict_proba], axis=1)
validation_prediction.to_excel("C:/Users/avudaippan.ramaiah/Desktop/Bajaj/CC/Results/Iteration3/Results/validation_predict.xlsx")


variable_importance = pd.DataFrame(clf.feature_importances_)
final_columns = pd.DataFrame(x_train.columns)
variable_importance = pd.concat([final_columns,variable_importance], axis=1)
variable_importance.to_excel("C:/Users/avudaippan.ramaiah/Desktop/Bajaj/CC/Results/Iteration3/Results/variable_impo.xlsx")

##accuracy measures
print "Train Accuracy :: ", accuracy_score(y_train, train_predict )
print "Test Accuracy  :: ", accuracy_score(y_test, test_predict)
print "Validation Accuracy  :: ", accuracy_score(y_validation, validation_predict)

##confusion matrix
print "Train Confusion Matrix :: ", confusion_matrix(y_train, train_predict )
print "Test Confusion Matrix  :: ", confusion_matrix(y_test, test_predict)
print "Validation Confusion Matrix  :: ", confusion_matrix(y_validation, validation_predict)
