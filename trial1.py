import indicators as ind

#type1
def smva(data,interval,data_):
    gb=ind.mva(data_,n=14)
    data['smva']=gb[-120:]
    res = max(gb)
    sup =min(gb)
    result_smva=[]
    for i in range (interval):
        if data.iloc[i]['Close'] < sup:
            result_smva.append('buy')
        elif data.iloc[i]['Close'] > res:
            result_smva.append('sell')
        else:
            result_smva.append('wait')
    return result_smva
#type2
def macd_(data,data_,interval):
    frr = ind.macd(data_)
    data['macd']=frr[-120:]
    fr = frr[-120:]
    result_macd=[]
    for j in range(interval):
        if fr[j] >= 0.125:
            result_macd.append('buy')
        elif fr[j] <= -0.125:
            result_macd.append('sell')
        else:
            result_macd.append('wait')
    return result_macd
#type1
def bol(data,interval,data_):    
    b1=[]
    b2=[]
    for k in range(14,interval+14):
        bb = ind.bands(data_,k)
        b1.append(bb['upper'])
        b2.append(bb['lower'])
    data['bol_upper']=b1
    data['bol_lower']=b2
    beat=0
    bat=0
    result_bol=[]
    for i in range(interval):
        if data.iloc[i]['Close']>(b1[i]) :
            result_bol.append('buy')
        elif data.iloc[i]['Close']<(b2[i]):
            result_bol.append('sell')
        elif b1[i]> data.iloc[i]['Close']>(b1[i]-0.0015) :
            for j in range(5):
                if data.iloc[j]['Close']-b2[j]< data.iloc[j+1]['Close']-b2[j]:
                    beat+=1
                elif data.iloc[j]['Close']-b2[j]> data.iloc[j+1]['Close']-b2[j]:
                    bat+=1
                else:
                    beat+=0
                    bat+=0
            jj = max(beat,bat)
            if bat == jj:
                result_bol.append('buy')
            else:
                result_bol.append('wait')
        elif b2[i]<data.iloc[i]['Close']<(b2[i]+0.0015):
            for j in range(5):
                if data.iloc[j]['Close']-b2[j]< data.iloc[j+1]['Close']-b2[j]:
                    beat+=1
                elif data.iloc[j]['Close']-b2[j] > data.iloc[j+1]['Close']-b2[j]:
                    bat+=1
                else:
                    beat+=0
                    bat+=0
            jj = max(beat,bat)
            if beat == jj:
                result_bol.append('sell')
            else:
                result_bol.append('wait')
        else:
            result_bol.append('wait')
    return result_bol
#type1   
def rsi_(data,interval,data_):
    jj=[] 
    jj1=[]
    result_rsi=[]
    for i in range(14,interval+14):
        jj.append(ind.rsi(data_,i,n=14))
        jj1.append(ind.rsi(data_,i,n=5))
    data['rsi']= jj
    for i in range(interval):
        if data.iloc[i]['rsi']<20:
            result_rsi.append('buy')
        elif data.iloc[i]['rsi']>80:
            result_rsi.append('sell')
        elif 80 >data.iloc[i]['rsi']>60:
            bo=0
            bb=0
            for k in range(5):
                if jj1[i]<jj[i]:
                    bo+=1
                elif jj1[i]>jj[i]:
                    bb+=1
                else:
                    bb+=0
                    bo+=0
            kb =max(bo,bb)
            if bb==kb:
                result_rsi.append('buy')
            else:
                result_rsi.append('wait')
        elif 40 >data.iloc[i]['rsi']>20:
            bo=0
            bb=0
            for k in range(5):
                if jj1[i]<jj[i]:
                    bo+=1
                elif jj1[i]>jj[i]:
                    bb+=1
                else:
                    bb+=0
                    bo+=0
            kb =max(bo,bb)
            if bo==kb:
                result_rsi.append('sell') 
            else:
                result_rsi.append('wait')
        else:
            result_rsi.append('wait')
    
    return result_rsi
#type2           
def psar_(data_,data,interval):
    rr = ind.psar(data_)
    data['psar']=rr[-120:]
    ind.ichi(data)
    data = data.fillna(value=0)
    result_sar=[]
    for j in range(interval):
        if (data['Close'][j] > data['senkou_a'][j]) and (data['Close'][j] > data['senkou_b'][j]) and (data['Close'][j] > data['psar'][j]):
            result_sar.append('buy')
        elif (data['Close'][j] < data['senkou_a'][j]) and (data['Close'][j] < data['senkou_b'][j]) and (data['Close'][j] > data['psar'][j]):
            result_sar.append('sell')
        else:
            result_sar.append('wait')
    return result_sar
def stoch(data,interval,data_):
    hj=[]
    hk=[]
    for i in range(14,interval+14):
        hj.append(ind.stoch(data_,i)['k'])
        hk.append(ind.stoch(data_,i)['d'])
    data['stoch_k']=hj
    data['stock_d']=hk
    result_stoch=[]
    for j in range(interval):
        if hj[j] <= 20 and hk[j] <= 20 :
            result_stoch.append('buy')
        elif hj[j] >= 80 and hk[j] >= 80 :
            result_stoch.append('sell')
        else:
            result_stoch.append('wait')
    return result_stoch

'''def svix(data,interval):
    hj=[]
    for i in range(14,interval+14):
        hj.append(ind.svix(data_,i))'''
def mom_(data,data_,interval):
    gg=ind.mom(data_)
    gj = ind.mva(data_)
    result=[]
    for j in range(interval):
        if gg[j] >=100.3 and gg[j]>gj[j]:
            result.append('buy')
        elif gg[j] <=99.5 and gg[j]<gj[j]:
            result.append('sell')
        else:
            result.append('wait')
    return result
def will(data_,data,interval):
    ggg=ind.william(data_)
    gg=ggg[-120:]
    gjj=ind.adxr(data_)
    gj=list(gjj[-120:])
    result_mfi=[]
    for j in range(interval):
        if gg[j]<=20 and gj[j]>35:
            result_mfi.append('sell')
        elif gg[j] >=80 and gj[j]>35:
            result_mfi.append('buy')
        elif gg[j]<=20 and gj[j]<=35:
            result_mfi.append('buy')
        elif gg[j]>=80 and gj[j]<=35:
            result_mfi.append('sell')
        elif 20<gg[j]<40 and gj[j]>35:
            result_mfi.append('sell')
        elif 60<gg[j]<80 and gj[j]>35:
            result_mfi.append('buy')
        else:
            result_mfi.append('wait')
    return result_mfi
def chai(data_,interval):
    ggg=ind.chaikin(data_)
    gg=ggg[-120:]
    chi=[]
    for j in range(interval):
        if gg[j]>2500:
            chi.append('buy')
        elif gg[j]<-2500:
            chi.append('sell')
        else:
            chi.append('wait')
    return chi
            
def mfi(data,interval,data_):
    gg =[]
    gjj=ind.adxr(data_)
    gj=list(gjj[-120:])
    for i in range (14,interval+14):
        gg.append(ind.mfi(data_,i))
    data['mfi']=gg
    result_mfi=[]
    for j in range(interval):
        if gg[j] >=90:
            result_mfi.append('sell')
        elif gg[j] <=10:
            result_mfi.append('buy')
        elif 90>gg[j]>60 and gj[j]>35:
            result_mfi.append('buy')
        elif 40<gg[j]<10 and gj[j]>35:
            result_mfi.append('sell')
        else:
            result_mfi.append('wait')
    return result_mfi
            
def obv_(data_,data,interval):
    gg = ind.obv(data)
    gj = ind.adxr(data_)
    gj=list(gj[-120:])
    data['mfi']=gg
    result_mfi=[]
    for j in range(interval):
        if gg[j] >=85:
            result_mfi.append('sell')
        elif gg[j] <=15:
            result_mfi.append('buy')
        elif 85>gg[j]>60 and gj[j]>35:
            result_mfi.append('buy')
        elif 40<gg[j]<15 and gj[j]>35:
            result_mfi.append('sell')
        else:
            result_mfi.append('wait')
    return result_mfi
def conf_level(data,interval,data_,mr1,mr2,mr3,mr4,mr5,mr6,mr7):
    #inr={,}
    indic = {'momentum':mom_(data,data_,interval),'Williams %R':will(data_,data,interval),'Chaikin A/D oscillator':chai(data_,interval),'Stochastic Gradient':stoch(data,interval,data_),'Parabolic SAR':psar_(data_,data,interval),'RSI':rsi_(data,interval,data_),'Bollinger Bands':bol(data,interval,data_),'MACD':macd_(data,data_,interval),'SMVA':smva(data,interval,data_),'Money Flow Index':mfi(data,interval,data_),'On Balance Volume':obv_(data_,data,interval)}
    indicators=['Stochastic Gradient','momentum','Parabolic SAR','MACD','SMVA','Williams %R']
    indicators2 =['RSI','Bollinger Bands','Chaikin A/D oscillator']
    indicators3= ['Money Flow Index','On Balance Volume']
    '''    mr1= input('The Momentum indicator you want to use: Stochastic Gradient, Parabolic SAR, MACD, SMVA: ')
    mr2=input('The trend indicator you want to use: RSI, Bollinger_Bands: ')
    mr3 = input('The flow indicator you want to use: Money Flow Index, On Balance Volume: ')
    mr4 = input('The fourth indicator you want to use(minor): any: ')'''
    confidence_level=[]
    type_=[]
    if mr1 in indicators and mr2 in indicators and mr3 in indicators2 and mr4 in indicators2 and mr5 in indicators3:
        ind1= indic[mr1]
        ind2 = indic[mr2]
        ind3 = indic[mr3]
        ind4 = indic[mr4]
        ind5 = indic[mr5]
        ind6 = indic[mr6]
        ind7 = indic[mr7]
        data[mr4+'_result']=ind4
        data[mr1+'_result']= ind1
        data[mr2+'_result']=ind2
        data[mr3+'_result']=ind3
        data[mr5+'_result']= ind5
        data[mr6+'_result']=ind6
        data[mr7+'_result']=ind7
        for i in range(interval):
            col=0
            l1=0
            l2=0
            if ind1[i] == 'buy':
                col+=15
            elif ind1[i] == 'sell':
                l1+=15
            else:
                l2+=15
                
            if ind2[i] == 'buy':
                col+=15
            elif ind2[i] == 'sell':
                l1+=15
            else:
                l2+=15
                
            if ind3[i] == 'buy':
                col+=15
            elif ind3[i] == 'sell':
                l1+=15
            else:
                l2+=15
                
            if ind4[i] == 'buy':
                col+=15
            elif ind4[i] == 'sell':
                l1+=15
            else:
                l2+=15
                
            if ind5[i] == 'buy':
                col+=15
            elif ind5[i] == 'sell':
                l1+=15
            else:
                l2+=15
                
            if ind6[i] == 'buy':
                col+=15
            elif ind6[i] == 'sell':
                l1+=15
            else:
                l2+=15
           
            if ind7[i] == 'buy':
                col+=10
            elif ind7[i] == 'sell':
                l1+=10
            else:
                l2+=10
            last=[max(col,l1,l2)][0]   
            confidence_level.append(last)
            type_.append([col,l1,l2])
        data['Confidence_level']=confidence_level  
        return confidence_level,type_
    else:
        return('You have to take two from each type of indicator')
    
#buy=0, sell=1, wait=2
def decision(data,interval,data_,v1,v2,v3,v4,v5,v6,v7):
    lev,ty=conf_level(data,interval,data_,v1,v2,v3,v4,v5,v6,v7)
    final=[]
    for i in range(interval):
        if lev[i] >= 70 and lev[i] == ty[i][0] :
            final.append(0)
        elif lev[i] >=70 and lev[i] == ty[i][1] :
            final.append(1)
        else:
           final.append(2)
    data['final_prediction']=final
    return final
