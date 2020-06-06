import pandas as pd
import datetime
import time
import matplotlib.pyplot as plt
from flask import Flask, request,render_template,redirect,url_for
import autofxcm as ax
import stock_hist as st
import MetaTrader5 as ft
import pickle
import pandas as pd
from twilio.rest import Client
client = Client(process.env.KEY,process.env.SECRET)

from_whatsapp='whatsapp:+14155238886'

#ft.initialize(server='ForexTimeFXTM-Demo02',login=67048338,password='Kenechuku217')
#Inputting and selection of data
app = Flask(__name__)
#app.debug = True
instru=["EURUSD","EURGBP","EURAUD","EURNZD","EURJPY","EURCHF","EURCAD",
   "GBPUSD","AUDUSD","NZDUSD","USDJPY","USDCHF","USDCAD","GBPAUD",
   "GBPNZD","GBPJPY","GBPCHF","GBPCAD","AUDJPY","CHFJPY","CADJPY",
   "AUDNZD","AUDCHF","AUDCAD","NZDJPY","NZDCHF","NZDCAD","CADCHF"]

@app.route('/<ans>', methods=['GET','POST'])
def pricer(ans):
    va = request.form.getlist('input')
    #print(va)
    id=va[0]
    pwd=va[1]
    server=va[2]
    v1 =v a[3]
    v2 = va[4]
    v3 = va[5]
    v4 = va[6] 
    v5 = va[7]
    v6 = va[8]
    v7 = va[9]
    num= va[10]
    ft.initialize(server=server,login=id,password=pwd)
    to_whatsapp='whatsapp:+234'+num
    #vv = {'v1':v1,'v2':v2,'v3':v3,'v4':v4,'v5':v5,'v6':v6,'v7':v7}
    timer = time.localtime()[3]
    while True:
      if timer>= 7 and timer<=19:
          if ans == 'stop':
              break
          for i in range(len(instru)):
           tf = [ft.TIMEFRAME_M15,ft.TIMEFRAME_H1,ft.TIMEFRAME_H12,ft.TIMEFRAME_D1]
           for j in tf:
            
            jb=pd.DataFrame(ft.copy_rates_from_pos(instru[i],j,0,150))
            jb['Open']=jb['open']
            jb['Close']=jb['close']
            jb['High']=jb['high']
            jb['Low']=jb['low']
            jb['Volume']=jb['tick_volume']
            data_=jb
            data=jb[-120:].reset_index()
            interval = len(data)
            im=instru[i]
            t,vf,hh,dd = ax.trade(data,interval,data_,im,i,jb,v1,v2,v3,v4,v5,v6,v7,to_whatsapp)
            if vf == 0:
                bf='buy'
            elif vf==1:
                bf='sell'
            else:
                bf='wait'
            #print(bf)
            try:
                while True:
                    jdb=pd.DataFrame(ft.copy_rates_from_pos(instru[i],ft.TIMEFRAME_M1,0,10))
                    t1 = ax.monitor(jdb,vf,im,i,hh,dd,to_whatsapp)
                    if t1 =='done':
                        break
            except:
                print('This part wasn\'t done')

            pred = st.auto(data, interval,data_, v1, v2, v3, v4,v5,v6,v7)
            if pred['accuracy'] >= 0.9:
                 fito = pred['fit']
                 predictt = fito.predict(pred['data'])
                 if list(predictt)[-1]==0:
                     hj=ft.Buy(instru[i],0.02)
                     client.messages.create(body='Buy due to prediction in '+im ,from_=from_whatsapp,to=to_whatsapp)
                     d=1
                     print('Bought through a predictor')
                 elif list(predictt)[-1]==1:
                     hj=ft.Sell(instru[i],0.02)
                     client.messages.create(body='Sell due to prediction in '+im ,from_=from_whatsapp,to=to_whatsapp)
                     d=1
                     print('Sold through a predictor')
                 elif list(predictt)[-1]==2:
                     hj=[]
                     d=0
                     print('wait!')
                 jj=list(predictt)[-1]
            else:
                hj=[]
                d=0
                print('Not enough Accuracy to trade!')

            try:
                while True:
                    jdg = pd.DataFrame(ft.copy_rates_from_pos(instru[i],ft.TIMEFRAME_M1,0,10))
                    t2 = ax.monitor(jdg,jj,im,i,hj,d,to_whatsapp)
                    if t2 == 'done':
                        break
            except:
                print('This part wasn\'t done')
            g = ft.positions_get(symbol=im)
            for k in g:
               if k[15] <= -2 or k[15] >= 5:
                   ft.Close(im,ticket = k[0])
               else:
                   while k[15]>-2 and k[15] < 5:
                       j = ft.positions_get(ticket=k[0])
                       if k[15] <= -2 or k[15] >= 5:
                           ft.Close(im,ticket = k[0])
                           break
            timer=time.localtime()[3]
            

      else:
          try:
              for k in (instru):
                  ft.Close(symbol=k)
          except:
              print('No trade of that symbol')
          while timer <7 and timer >19:
              time.sleep(3600)
              timer=time.localtime()[3]
          continue

return render_template('index.html')
      


def parser(x): 
    return datetime.datetime.strptime(x,'%Y%m%d')        

if __name__ == '__main__':
    app.run()           
