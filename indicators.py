from statistics import stdev
import numpy as np
import jhtalib as jh
import ta
#momentum ind
def mva(hh,n=14):
    dx=jh.SMA(hh,n)
    return dx

def kama(hh,n=14):
    gh=jh.KAMA(hh,n)
    return gh
#trend ind
def bands(hh,i=3000,n=14,m=2):
    d=[]
    for k in range(i-(n-1),i+1):
        tp = (hh['High'][k]+hh['Low'][k]+hh['Close'][k])/3
        d.append(tp)
    ma = sum(d)/len(d)
    std = stdev(d)
    bolu= ma+ m*std
    bold = ma - m*std
    return {'upper':bolu, 'lower':bold}
#mom ind
def psar(hh,n=14, iaf=0.01, maxaf=0.1):
    sar= jh.SAR(hh,af_step=iaf,af_max=maxaf,high='High',low='Low')
    return sar
def ichi(hh,n=14):
    #tenkan_sen
    high_9 = hh.High.rolling(9).max()
    low_9 = hh.Low.rolling(9).min()
    tenkan_sen=(high_9+ low_9)/2
    hh['tenkan_sen'] =tenkan_sen
    #kijun_sen
    high_26 =hh.High.rolling(26).max()
    low_26 = hh.Low.rolling(26).min()
    kijun_sen = (high_26 + low_26)/2
    hh['kijun_sen']=kijun_sen
    #senkou a
    senkou_a = ((hh['tenkan_sen']+hh['kijun_sen'])  /2).shift(26)
    hh['senkou_a']=senkou_a
    #senkou_b
    high_52 = hh.High.rolling(52).max()
    low_52 = hh.Low.rolling(52).min()
    senkou_b = ((high_52+ low_52)/2).shift(26)
    hh['senkou_b']=senkou_b
    #chikou
    chikou = hh.Close.shift(-26)
    hh['chikou'] = chikou
                 
#momentum
def stoch(hh,i=3000,n=14):
    c = hh['Close'][i]
    bb =[]
    for j in range(i-(n-1),i):
        bb.append(hh['Close'][j])
    l14 = min(bb)
    h14 = max(bb)
    cv = (c-l14)
    if cv <0:
        cv=-cv
    k = 100 * cv/(h14-l14)
    bd=[]
    for e in range(i-4,i):
       bd.append(hh['Close'][e])
    l3=min(bd)
    h3 = max(bd)
    cd=c-l3
    if cd <0:
        cd=-cd
    d = 100*(cd/(h3-l3))
    return {'k':k,'d':d}
#flow
def mfi(hh,i=3000,n=14):
    mf=[]  
    pfr=[]
    nfr=[]
    for k in range(i-(n-1),i):
        price = (hh['High'][k]+hh['Low'][k]+hh['Close'][k])/3
        mf.append(price* hh['Volume'][k])
    for j in range(len(mf)-1):
        if mf[j+1] >= mf[j]:
            pfr.append(mf[j])
        else:
            nfr.append(mf[j])
    mfr = sum(pfr)/sum(nfr)
    mfi = 100-(100/(1+mfr))
    return mfi
#momentum
def mom(hh,n=14):
    moment= jh.MOM(hh,n,price='Close')
    return moment
#trend
def rsi(hh,i=3000,n=14):
    #a=2/(n+1)
    Ut=[]
    Dt=[]
    for j in range(i-(n-1),i+1):
        chng = hh['Close'][j]-hh['Close'][j-1]
        if chng >=0:
            Ut.append(chng)
        else:
            Dt.append(chng)
    avgu=np.mean(Ut)
    avgd=np.mean(Dt)
    
    rs = avgu/avgd
    if rs <0:
        rs=-rs
    rsi = 100- (100/(1+rs))
    return rsi
def ema(hh,n=14):
     weights = np.exp(np.linspace(-1.,0.,n))
     weights /= weights.sum()
     a=np.convolve(hh['Close'],weights,mode='full')[:len(hh['Close'])]
     a[:n] = a[n]
     return a
def adxr(hh,n=14):
    d= ta.trend.adx(high=hh['High'],low=hh['Low'],close=hh['Close'],fillna=True)
    return d
def stoch_rsi(hh,n=14):
    st=jh.STOCHRSI(hh,n=14)
    return st
def william(hh,n=14):
    will=jh.WILLR(hh,n)
    return will
def atr(hh,n=14):
    hh=jh.ATR(hh,n)
    return hh
def chaikin(hh,n=14):
    ch=jh.AD(hh)
    return ch
#momentum        
def macd(hh):
   md = ema(hh,n=12)-ema(hh,n=26)
   return md
#flow
def obv(hh):
    bv= np.where(hh['Close'] > hh['Close'].shift(1),hh['Volume'], np.where(hh['Close'] < hh['Close'].shift(1), -hh['Volume'],0)).cumsum()
    return bv     
        
    
        
