import pandas as pd
import datetime
import time
import matplotlib.pyplot as plt
from flask import Flask, request,render_template,redirect,url_for
import autofxcm as ax
import stock_hist as st
import MetaTrader5 as ft
import pickle
ft.initialize(server='ForexTimeFXTM-Demo02',login=67048338,password='Kenechuku217')
#Inputting and selection of data
app = Flask(__name__,template_folder= 'C:/Users/Ademola/OneDrive/folder/OneDrive/Documents/template')
UPLOAD_FOLDER = 'C:/Users/Ademola/OneDrive/folder/OneDrive/Documents/template'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
#app.debug = True
instru=["EURUSD","EURGBP","EURAUD","EURNZD","EURJPY","EURCHF","EURCAD",
   "GBPUSD","AUDUSD","NZDUSD","USDJPY","USDCHF","USDCAD","GBPAUD",
   "GBPNZD","GBPJPY","GBPCHF","GBPCAD","AUDJPY","CHFJPY","CADJPY",
   "AUDNZD","AUDCHF","AUDCAD","NZDJPY","NZDCHF","NZDCAD","CADCHF"]

@app.route('/', methods=['GET', 'POST'])
def pricer():
    if request.method == 'POST':
        va = request.form.getlist('input')
        print(va)
        v1=va[0]
        v2=va[1]
        v3 = va[2]
        v4 = va[3] 
        v5 = va[4]
        v6 = va[5]
        v7 = va[6]
        vv = {'v1':v1,'v2':v2,'v3':v3,'v4':v4,'v5':v5,'v6':v6,'v7':v7}
        pickle.dump(vv,open('ans.sav','wb'))
        return render_template('price.html')
        return redirect(url_for('predictions'))   
    return render_template('price.html')


@app.route('/tt', methods=['GET', 'POST'])
def method():
    if request.method=='POST':
      v = pickle.load(open('ans.sav','rb'))
      timer = time.localtime()[3]
      if timer> 8 and timer<19:
          while timer > 8 and timer < 19:
            for i  in range(len(instru)):
                jb=pd.DataFrame(ft.copy_rates_from_pos(instru[i],ft.TIMEFRAME_M15,0,3014))
                jb['Open']=jb['open']
                jb['Close']=jb['close']
                jb['High']=jb['high']
                jb['Low']=jb['low']
                jb['Volume']=jb['tick_volume']
                data=jb[-3000:]
                data_=jb
                interval = len(data)
                v1 = v['v1']
                v2=v['v2']
                v3=v['v3']
                v4 = v['v4']
                v5 = v['v5']
                v6 = ['v6']
                v7 = ['v7']
                t,u,vf = ax.trade(data,interval,data_,i,jb,v1,v2,v3,v4,v5,v6,v7)
                for j in range(len(vf)):
                    if vf[j] == 0:
                        vf[j]='buy'
                    elif vf[j]==1:
                        vf[j]='sell'
                    else:
                        vf[j]='wait'
                plt.plot(data)
                plt.savefig('image.png')
                h = vf[-1]
                print(h)
                return render_template('method.html',t,h,u,name='data', url='image.png' )
                time.sleep(30)
            timer=time.localtime[3]
      return render_template('method.html',name='data', url='image.png' )
    return render_template('method.html')
      
@app.route('/bb', methods=['GET', 'POST'])
def predictions():
  inst='EURAUD'
  if request.method=='GET':
    b = pickle.load(open('ans.sav','rb'))
    v1 = b['v1']
    v2=b['v2']
    v3=b['v3']
    v4 = b['v4']
    v5 = b['v5']
    v6 = b['v6']
    v7 = b['v7']
    jb=pd.DataFrame(ft.copy_rates_from_pos(inst,ft.TIMEFRAME_M15,0,3014))
    jb['Open']=jb['open']
    jb['Close']=jb['close']
    jb['High']=jb['high']
    jb['Low']=jb['low']
    jb['Volume']=jb['tick_volume']
    data=jb[-3000:].reset_index()
    data_=jb
    interval = len(data)
    pred = st.auto(data, interval,data_, v1, v2, v3, v4,v5,v6,v7)
    if pred['accuracy'] >= 0.9:
     fito = pred['fit']
     predictt = fito.predict(pred['data'])
     predicto=pd.DataFrame(predictt)[-50:]
     return render_template('pred.html',table=predicto.to_html(classes='data',justify='center'), tit='Prediction',titles=['na','prediction'])
  if request.method=='POST':
     b1 = request.form.getlist('inputer')[0]
     if b1== 'b1':
         ft.Buy(inst,0.1)
     if b1 =='b2':
         ft.Sell(inst,0.1)
     return render_template('pred.html',table=predicto.to_html(classes='data'), tit='Prediction')
  return render_template('pred.html')

def parser(x): 
    return datetime.datetime.strptime(x,'%Y%m%d')        

if __name__ == '__main__':
    app.run()           
