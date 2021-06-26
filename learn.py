from sklearn.ensemble import GradientBoostingClassifier as GBC
from sklearn.ensemble import GradientBoostingRegressor as GBR
from sklearn.model_selection import train_test_split as tts
from sklearn.metrics import accuracy_score,mean_squared_error
import pandas as pd
import numpy as np
#print("Learn")
def classification(df,label,path):
    y_table=df[label]
    x_table=df.drop(label,axis=1)
    dic={}
    num=0
    y=y_table.values
    yc=np.array(y)
    x=x_table.values
    x_name=x_table.columns
    for i in range(len(y)):
        try:
            a=dic[y[i]]
        except:
            dic[y[i]]=num            
            num=num+1
    for i in range(len(y)):
        y[i]=dic[y[i]]
    clsd={}
    for i in range(len(y)):
        clsd[y[i]]=yc[i]
    acc=[]
    imp=[]
    y=y.astype("int")
    for i in range(30):
        model=GBC(n_estimators=30)
        x_train,x_test,y_train,y_test=tts(x,y,test_size=0.2)
        y_train=np.array(y_train)
        y_test=np.array(y_test)
        model.fit(x_train,y_train)
        y_pred=model.predict(x_test)
        acc.append(accuracy_score(y_pred,y_test))   #モデル精度算出
        imp.append(model.feature_importances_)      #影響度算出
    impout=[]
    imp=np.array(imp)
    for i in range(len(x_name)):
        impout.append(np.average(imp[:,i]))
    #影響度の算出
    for i in range(len(impout)):
        impout[i]=impout[i]/sum(impout)
    for i in range(len(impout)):
        impout[i]=impout[i]*100
    #クラスごとの平均値
    tmp=[]
    clo=[]
    for i in range(len(x_name)):
        for j in range(num-1):
            tmp.append(np.average(x[y==j,i]))
        clo.append(tmp)
        tmp=[]
    per=[]
    for i in range(len(x_name)):
        for j in range(num-1):
            tmp.append(str(np.percentile(x[y==j,i],q=[0,1,25,50,75,99,100]))[1:-1].replace(" ","_"))
        per.append(tmp)
        tmp=[]
    
    out=[]
    out.append(x_name)
    out.append(impout)
    clo=np.array(clo).T
    per=np.array(per).T
    out=np.array(out)
    out=np.vstack((out,clo))
    out=np.vstack((out,per))
    out=out.T
    dfo=pd.DataFrame(out)
    col=[]
    col.append("項目")
    col.append("結果への影響度(%)")
    for i in range(num-1):
        col.append(str(clsd[i])+"が結果の場合における平均値")
    for i in range(num-1):
        col.append(str(clsd[i])+"が結果の場合における分布(最小値-1%-25%-中央値-75%-99%-最大値)")
    dfo.columns=col
    dfo=dfo.sort_values("結果への影響度(%)",ascending=False)
    dfo.to_csv(path+"/colum_importance.csv",encoding="shift-jis",index=False)
    return sum(acc)/len(acc)

def regression(df,label,path):
    y_table=df[label]
    x_table=df.drop(label,axis=1)
    #dic={}
    num=0
    y=y_table.values
    x=x_table.values
    x_name=x_table.columns
    acc=[]
    imp=[]
    y=y.astype("int")
    for i in range(30):
        model=GBR(n_estimators=30)
        x_train,x_test,y_train,y_test=tts(x,y,test_size=0.2)
        y_train=np.array(y_train)
        y_test=np.array(y_test)
        model.fit(x_train,y_train)
        y_pred=model.predict(x_test)
        acc.append(np.sqrt(mean_squared_error(y_pred,y_test)))      #モデル精度算出
        imp.append(model.feature_importances_)                      #影響度算出
    impout=[]
    imp=np.array(imp)
    for i in range(len(x_name)):
        impout.append(np.average(imp[:,i]))
    #影響度格納
    for i in range(len(impout)):
        impout[i]=impout[i]/sum(impout)
    for i in range(len(impout)):
        impout[i]=impout[i]*100
    #相関係数格納
    cor=[]
    for i in range(len(x_name)):
        cor.append(np.corrcoef(x[:,i],y)[1][0])
    per=[]
    for i in range(len(x_name)):
        per.append(str(np.percentile(x[:,i],q=[0,1,25,50,75,99,100]))[1:-1].replace(" ","_"))
    out=[]
    out.append(x_name)
    out.append(impout)
    out.append(cor)
    out.append(per)
    out=np.array(out).T
    dfo=pd.DataFrame(out)
    dfo.columns=["項目","結果への影響度(%)","相関係数","分布(最小値-1%-25%-中央値-75%-99%-最大値)"]
    dfo=dfo.sort_values("結果への影響度(%)",ascending=False)
    dfo.to_csv(path+"/colum_importance.csv",encoding="shift-jis",index=False)
    gosa=sum(acc)/len(acc)
    seido=(len(y)*gosa)/sum(y)
    return seido
    
    
    
#df=pd.read_csv("wine.csv",encoding="shift-jis")
#df=pd.get_dummies(df,columns=["天気","風"])
#regression(df,"家賃","C:/Users/decar/Desktop/勉強/test/アプリ開発/rent")
#classification(df,"Wine","C:/Users/decar/Desktop/勉強/test/アプリ開発")
