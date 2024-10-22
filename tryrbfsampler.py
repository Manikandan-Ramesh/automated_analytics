# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 11:00:57 2018

@author: ishwarya.sriraman
"""
import pandas as pd
import numpy as np
from sklearn import svm, datasets
import matplotlib.pyplot as plt

df=pd.read_csv("Sample_Policy_Master.csv")

from sklearn.kernel_approximation import RBFSampler
from sklearn.linear_model import SGDClassifier
X = [[0, 0], [1, 1], [1, 0], [0, 1]]
y = [0, 0, 1, 1]
rbf_feature = RBFSampler(gamma=1, random_state=1)
X_features = rbf_feature.fit_transform(X)
clf = SGDClassifier()   
clf.fit(X_features, y)
SGDClassifier(alpha=0.0001, average=False, class_weight=None, epsilon=0.1,
       eta0=0.0, fit_intercept=True, l1_ratio=0.15,
       learning_rate='optimal', loss='hinge', max_iter=None, n_iter=None,
       n_jobs=1, penalty='l2', power_t=0.5, random_state=None,
       shuffle=True, tol=None, verbose=0, warm_start=False)
clf.score(X_features, y)