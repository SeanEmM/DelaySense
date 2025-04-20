#this file was an attempt to hyperparameter tune the model

import pandas as pd
from sklearn.metrics import classification_report
# import matplotlib.pyplot as plt
# import seaborn as sns
from sklearn.preprocessing import MinMaxScaler,LabelEncoder
# from sklearn.model_selection import train_test_split
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.svm import SVC
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
# from xgboost import XGBClassifier
# from sklearn.metrics import classification_report,ConfusionMatrixDisplay
# from sklearn.model_selection import GridSearchCV
import pickle
import numpy as np
from imblearn.over_sampling import SMOTE
import warnings

warnings.simplefilter(action='ignore', category=Warning)

df = pd.read_csv('finaldata.csv')


col = ['dept_temp','dept_dwpt','dept_rhum','dept_prcp','dept_wdir','dept_wspd','dept_pres','dept_coco','arr_temp','arr_dwpt','arr_rhum','arr_prcp','arr_wdir','arr_wspd','arr_pres','arr_coco']
for i in col:
  x = df[i].median()
  df[i]=df[i].fillna(x)

df1 = df.drop(columns = ['AIRLINE','AIRLINE_DOT','AIRLINE_CODE','DOT_CODE','FL_NUMBER','DISTANCE','ORIGIN','ORIGIN_CITY','DEST','DEST_CITY','CRS_DEP_TIME','CRS_ARR_TIME','CANCELLED'],axis=1)

df1.drop(['FL_DATE'],axis=1,inplace=True)

df1.drop(['origin_latitude','origin_longitude','DEST_latitude','DEST_longitude','arr_date_time','dept_date_time'],axis=1,inplace=True)

conditions = [(df1['DELAY_DUE_WEATHER'] <=30),
              (df1['DELAY_DUE_WEATHER'] >30) & (df1['DELAY_DUE_WEATHER'] <=120),
              (df1['DELAY_DUE_WEATHER'] >120) & (df1['DELAY_DUE_WEATHER'] <=600),
              (df1['DELAY_DUE_WEATHER'] >600)]

choices = ['On-Time','Minor Delay','Moderate Delay','Severe Delay']
df1['Delay'] = np.select(conditions,choices,default='Unknown')

df1 = df1.drop(['DELAY_DUE_WEATHER'],axis=1)

encoder = LabelEncoder()
df1['Delay'] = encoder.fit_transform(df1['Delay'])
print(encoder.classes_)

df2 = df1.drop(['dept_rhum','dept_wdir','arr_wdir','arr_rhum'],axis=1)

X = df2.iloc[:,:-1]
for i in X:
    print(i)

y = df2.iloc[:,-1]


scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

print("OVERSAMPLING THE DATASET")
os = SMOTE(random_state=1)
X_os,y_os = os.fit_resample(X_scaled,y)

from sklearn.model_selection import train_test_split
X_train1,X_test1,y_train1,y_test1 = train_test_split(X_os,y_os,test_size=0.3,random_state=1)

# gb1 = GradientBoostingClassifier(random_state=1)
# gb1.fit(X_train1,y_train1)
# print('gb fitted')
#
# from sklearn.model_selection import RandomizedSearchCV
# from scipy.stats import randint, uniform
#
# params = {
#     'n_estimators': randint(100, 301),
#     'learning_rate': uniform(0.01, 0.1),
#     'max_depth': randint(3, 5),
#     'min_samples_split': randint(2, 10),
#     'min_samples_leaf': randint(1, 5)
# }
# gb = GradientBoostingClassifier()
# random_search = RandomizedSearchCV(estimator=gb, param_distributions=params, cv=10, scoring='accuracy', random_state=42, n_jobs=-1, n_iter=100, verbose=2)
# # clf = GridSearchCV(gb, params, cv=10, scoring='accuracy')
# clf.fit(X_train1, y_train1)
# print("Best Parameters:", clf.best_params_)
# print("Best Score (Cross-Validated Accuracy):", clf.best_score_)
# print("Best Estimator:", clf.best_estimator_)
# random_search.fit(X_train1, y_train1)

# print("Best Parameters:", random_search.best_params_)
# print("Best CV Score:", random_search.best_score_)



# gb = GradientBoostingClassifier()
# gb.fit(X_train1,y_train1)
# y_pred = gb.predict(X_test1)
# print(classification_report(y_test1,y_pred))
# pickle.dump(gb,open('model_final.sav','wb'))
# pickle.dump(scaler,open('scaler_final.sav','wb'))