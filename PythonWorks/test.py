import pandas as pd
import numpy as np
import pickle
ss = pd.read_csv("2018_FINISH2.csv") 

e=12
x=ss.iloc[:,[e]].values
y=ss.iloc[:,[1,4]].values
from sklearn.preprocessing import StandardScaler
st_x=StandardScaler()
x=st_x.fit_transform(x)
from sklearn.neighbors import KNeighborsClassifier
classifier=KNeighborsClassifier(n_neighbors=5,metric='minkowski',p=2)
y_pred=classifier.fit(x,y)

pickle.dump(y_pred,open('college.pkl','wb'))
