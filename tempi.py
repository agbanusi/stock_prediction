import time
import autofxcm as ax
import stock_hist as st
import MetaTrader5 as ft
#import pickle
import pandas as pd
#import sys
#dat= sys.argv[1]
#i = int(dat)
instru=["EURUSD","EURGBP","EURAUD","EURNZD","EURJPY","EURCHF","EURCAD",
   "GBPUSD","AUDUSD","NZDUSD","USDJPY","USDCHF","USDCAD","GBPAUD",
   "GBPNZD","GBPJPY","GBPCHF","GBPCAD","AUDJPY","CHFJPY","CADJPY",
   "AUDNZD","AUDCHF","AUDCAD","CADCHF"]
#instru=["EURUSD","EURGBP","USDCAD","USDJPY","EURAUD","GBPAUD","EURNZD","GBPCHF","EURJPY","GBPUSD","AUDUSD","NZDUSD","EURCHF","EURCAD"]
v = ['Stochastic Gradient','MACD','RSI','Bollinger Bands','Money Flow Index','Parabolic SAR','Chaikin A/D oscillator']
#ft.initialize(server='ForexTimeFXTM-Demo02',login=67048338,password='Kenechuku217')
#v = ['Parabolic SAR','Stochastic Gradient','RSI','Bollinger Bands','Money Flow Index','On Balance Volume','Williams %R']
timer = time.localtime()[3]
while True:
  if timer>= 8 and timer<=18:
      for i in range(len(instru)):
       tf = [ft.TIMEFRAME_M15,ft.TIMEFRAME_M30,ft.TIMEFRAME_H1,ft.TIMEFRAME_H2]
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
        v1 = v[0]
        v2=v[1]
        v3=v[2]
        v4 = v[3]
        v5 = v[4]
        v6 = v[5]
        v7 = v[6]
        im=instru[i]
        t,vf,hh = ax.trade(data,interval,data_,im,i,jb,v1,v2,v3,v4,v5,v6,v7)
        if vf == 0:
            bf='buy'
        elif vf==1:
            bf='sell'
        else:
            bf='wait'
        print(bf)
        try:
            while True:
                jdb=pd.DataFrame(ft.copy_rates_from_pos(instru[i],ft.TIMEFRAME_M1,0,10))
                t1 = ax.monitor(jdb,vf,im,i,hh)
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
                 print('Bought through a predictor')
             elif list(predictt)[-1]==1:
                 hj=ft.Sell(instru[i],0.02)
                 print('Sold through a predictor')
             elif list(predictt)[-1]==2:
                 hj=[]
                 print('wait!')
             jj=list(predictt)[-1]
        else:
            hj=[]
            print('Not enough Accuracy to trade!')
        
        try:
            while True:
                jdg = pd.DataFrame(ft.copy_rates_from_pos(instru[i],ft.TIMEFRAME_M1,0,10))
                t2 = ax.monitor(jdg,jj,im,i,hj)
                if t2 == 'done':
                    break
        except:
            print('This part wasn\'t done')
        timer=time.localtime()[3]
        
  else:
      while timer <8 and timer >18:
          time.sleep(3600)
          timer=time.localtime()[3]
      continue
