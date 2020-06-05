import numpy as np
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
import trial1 as tr
sca = StandardScaler()
''' This python file does inputting of data,selection of the columns that is/are to be predicted, data preprocessing,
prediction using the popular machine models, classifying the data using Mean Squared Error, Mean Absolute Error,
Accuracy score, Confusion Matrix, Classification report'''
#Inputting and selection of data
#ALLOWED_EXTENSIONS = set(['csv','xlsx'])
#Choosing the columns to predict
def preset(data,interval,data_,v1,v2,v3,v4,v5,v6,v7):
    yy = tr.decision(data,interval,data_,v1,v2,v3,v4,v5,v6,v7)
    X = data.drop(['final_prediction','Confidence_level','time'],axis=1)
    #Data preprocessing
    c=[]
    for i in range(len(X.columns)):
        if (type(X.iloc[2,i])== np.int64 or type(X.iloc[2,i])== np.float64):
            c.append(X.columns[i])
    X = data[c]
    X.fillna(0,inplace=True)
    X=sca.fit_transform(X)
    #Data Splitting
    from sklearn.model_selection import train_test_split
    X_train,X_test,y_train,y_test = train_test_split(X,yy,test_size=0.3,random_state=101)
    return X,yy,X_train,y_train,X_test,y_test,data
def classification(data,prediction,y_test,y):
    try:
            from sklearn.metrics import accuracy_score
            d= accuracy_score(y_test,prediction)
            return d            
    except:
        print('something went wrong, sorry!')
    
def linearregression(data,X_train,y_train,X_test,y_test,y):
        from sklearn.linear_model import LinearRegression
        lm = LinearRegression()
        lm.fit(X_train,y_train)
        pred1 =lm.predict(X_test)
        return lm, pred1
def logisticregression(data,X_train,y_train,X_test,y_test,y):
        from sklearn.linear_model import LogisticRegression
        logmodel = LogisticRegression()
        logmodel.fit(X_train,y_train)
        pred2 = logmodel.predict(X_test)
        return logmodel, pred2,'Logistic Regression'
def KNN(data,X_train,y_train,X_test,y_test,y):
        from sklearn.neighbors import KNeighborsClassifier
        error_rate=[]
        if len(y_test) < 80 :
          for i in range(1,len(y_test)):
            knn=KNeighborsClassifier(n_neighbors= i)
            knn.fit(X_train,y_train)
            pred_i= knn.predict(X_test)
            error_rate.append(np.mean(pred_i!=y_test))
        else :
          for i in range(1,80):
            knn=KNeighborsClassifier(n_neighbors= i)
            knn.fit(X_train,y_train)
            pred_i= knn.predict(X_test)
            error_rate.append(np.mean(pred_i!=y_test))
        err = pd.DataFrame(error_rate)
        ev2 = err.min(axis=1)
        nm = ev2.idxmin()
        knn = KNeighborsClassifier(n_neighbors=(nm+1))
        knn.fit(X_train,y_train)
        pred3 = knn.predict(X_test)
        return knn, pred3, ['KNN',nm]
def trees(data,X_train,y_train,X_test,y_test,y):
        from sklearn.tree import DecisionTreeClassifier
        dtree=DecisionTreeClassifier()
        dtree.fit(X_train,y_train)
        pred4 = dtree.predict(X_test)
        return dtree,pred4  ,'Trees'
def randomforest(data,X_train,y_train,X_test,y_test,y):
        from sklearn.ensemble import RandomForestClassifier
        error_rate=[]
        if len(y_test) <120:
          for i in range(1,len(y_test)):
            rfc = RandomForestClassifier(n_estimators=i)
            rfc.fit(X_train,y_train)
            pred_i = rfc.predict(X_test)
            error_rate.append(np.mean(pred_i!=y_test))
        else:
          for i in range(1,120):
            rfc = RandomForestClassifier(n_estimators=i)
            rfc.fit(X_train,y_train)
            pred_i = rfc.predict(X_test)
            error_rate.append(np.mean(pred_i!=y_test))
        nm = error_rate.index(min(error_rate))
        rfc = RandomForestClassifier(n_estimators=(nm+1))
        rfc.fit(X_train,y_train)
        pred5 = rfc.predict(X_test)
        return rfc, pred5,'Random Forest'
def auto(data,interval,data_,v1,v2,v3,v4,v5,v6,v7):
    try:
        X,y,X_train,y_train,X_test,y_test,data = preset(data,interval,data_,v1,v2,v3,v4,v5,v6,v7)
        '''a, pred1 =linearregression(data,X_train,y_train,X_test,y_test,y)
        pickle.dump(a, open('model1.sav', 'wb'))'''
        b, pred2,name1 =logisticregression(data,X_train,y_train,X_test,y_test,y)
        pickle.dump(b, open('model2.sav', 'wb'))
        c,pred3,name2 =KNN(data,X_train,y_train,X_test,y_test,y)
        pickle.dump(c, open('model3.sav', 'wb'))
        d,pred4,name3 =trees(data,X_train,y_train,X_test,y_test,y)
        pickle.dump(d, open('model4.sav', 'wb'))
        e, pred5,name4 =randomforest(data,X_train,y_train,X_test,y_test,y)
        pickle.dump(e, open('model5.sav', 'wb'))
        vv = [pred2,pred3,pred4,pred5]
        vf=[b,c,d,e]
        print("The metric we're using is accuracy")
        name=[name1,name2,name3,name4]
        bc=[]
        for i in vv:
            dd = classification(data,i,y_test,y)
            bc.append(dd)
        see=pd.DataFrame(name,bc)
        seet=pd.DataFrame(vf,bc)
        f=see[0][max(bc)][0]
        g=seet[0][max(bc)][0]
        return {'accuracy':max(bc),'model':f,'fit':g,'data':X}
    except:
        return {'accuracy': 0,'model': 'logisticregression','fit':0,'data':0}
    

        
