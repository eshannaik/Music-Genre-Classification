# -*- coding: utf-8 -*-
"""Music Genre.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kausSdT-I-ZPRSeeXtJcIUDKcFhK6E4r
"""

pip install catboost

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC,SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier
import lightgbm as lgbm
import catboost as cb

from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score

d=pd.read_csv("dataset.csv")

d.head()

d.isnull().sum()

d.shape

for i in ['label']:
    print(d[i].unique())

from sklearn.preprocessing import LabelEncoder
le =LabelEncoder()
d['label'] = le.fit_transform(d['label'])

d = d.drop(["filename"],axis=1)

X = d.drop('label', axis = 1)
y = d.label

X_train,X_test,y_train,y_test = train_test_split(X,y,random_state=42,test_size=0.3)

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.fit_transform(X_test)

def p(models,model_names):
  acc=[]
  for m in range (len(models)):
    model = models[m]
    model.fit(X_train,y_train)
    y_pred = model.predict(X_test)
    acc.append(accuracy_score(y_pred,y_test))

  df={'Modelling Algo':model_names,'Accuracy':acc}
  return df

models = [LogisticRegression(),LinearSVC(),RandomForestClassifier(),GaussianNB(),KNeighborsClassifier(),]
model_names = ['Logistic Regression','Linear SVM','Random Forest','Guassian NB','KNearestNeighbors']
df =p(models,model_names)

acc_frame = pd.DataFrame(df)
acc_frame.sort_values(by="Accuracy",ascending=False)

def grid(parameters,model):
  model = GridSearchCV(
      model,
      parameters,
      cv=5,
      scoring="accuracy"
  )

  model.fit(X_train,y_train)

  print("Best Parameters :",model.best_params_)
  print('Mean cross-validated accuracy score of the best_estimator: ',model.best_score_)

  return model.best_params_,model.best_score_

parameters = {
    'max_depth': [3, 5, 7, 9], 
    'n_estimators': [5, 10, 15, 20, 25, 50, 100],
    'learning_rate': [0.01, 0.05, 0.1]
}

xgbc = XGBClassifier(random_state=42,class_weight='balanced')
m_n_xg,acc_xg = grid(parameters,xgbc)

parameters = {
    'iterations' : [1,2,3,4],
    'depth' : [1,2,3,4],
    'learning_rate' : [0.1,0.4,0.8,1],
}

cbc = cb.CatBoostClassifier(random_state=42)
m_n_cb,acc_cb=grid(parameters,cbc)

parameters = {
    'n_estimators': [3, 6, 11, 16, 26, 46, 86],
    'learning_rate': [0.01, 0.05, 0.1],
    'num_leaves': [10, 20, 40],
}

lgbmc = lgbm.LGBMClassifier(random_state=42,class_weight='balanced')
m_n_lgb,acc_lgb=grid(parameters,lgbmc)

d1 = pd.DataFrame({'Modelling Algo':["XG Boost","Cat Boost","Light GBM"],'Accuracy':[acc_xg,acc_cb,acc_lgb]})

acc_frame = acc_frame.append(d1,ignore_index = True)
acc_frame.sort_values(by="Accuracy",ascending=False)

plt.figure(figsize=(8,5))
ax = sns.barplot(data=acc_frame.sort_values(by="Accuracy",ascending=False),x="Accuracy",y="Modelling Algo",palette="Set3")
plt.show()