import trial1 as tr
import MetaTrader5 as ft
import time
from twilio.rest import Client
client = Client(process.env.KEY,process.env.SECRET)

from_whatsapp='whatsapp:+14155238886'
#to_whatsapp='whatsapp:+2348073975086'


def monitor(jb,vf,im,i,hh,d,to_whatsapp):
  t = 'done'
  if d == 1 and len(hh) >0:
    tickett=hh[2]
    tt=ft.positions_get(ticket=tickett)
    trade=tt[0][15]  
    if trade <=-2.5 and vf== 0:
        ft.Close(im,ticket=tickett)
        hy=ft.Sell(im,0.04)
        client.messages.create(body='Close the Buy loss in '+im+' , I advise you Sell' ,from_=from_whatsapp,to=to_whatsapp)            
        while True:
            if (ft.positions_get(hy[2]))[0][15] >= 10:
                ft.Close(im,ticket=hy[2])
                break
            elif (ft.positions_get(hy[2]))[0][15]<=-2.5:
                ft.Close(im,ticket=hy[2])
                break
        return t
            
    elif trade<=-2.5 and vf== 1:
        ft.Close(im,ticket=tickett)
        hy=ft.Buy(im,0.04)
        client.messages.create(body='Close the Sell loss in '+im+' , I advise you Buy' ,from_=from_whatsapp,to=to_whatsapp)
        while True:
            if (ft.positions_get(hy[2]))[0][15] >= 10:
                ft.Close(im,ticket=hy[2])
                break
            elif (ft.positions_get(hy[2]))[0][15]<=-2.5:
                ft.Close(im,ticket=hy[2])
                break
        return t
    elif trade >= 50 and vf == 0:
        jbb=ft.symbol_info_tick(im)
        time.sleep(2)
        jbg=ft.symbol_info_tick(im)
        if jbb[2] >= (jbg[2]):
            ft.Close(im,ticket=tickett)
            client.messages.create(body='Close the profit in '+im ,from_=from_whatsapp,to=to_whatsapp)
        return t
    elif trade >=50 and vf==1:
        jbb=ft.symbol_info_tick(im)
        time.sleep(2)
        jbg=ft.symbol_info_tick(im)
        if jbb[1] <= (jbg[1]):
            ft.Close(im,ticket=tickett)
            client.messages.create(body='Close the profit in '+im ,from_=from_whatsapp,to=to_whatsapp)            
        return t
    elif 50>trade>=20 and vf==0:
        jbb=ft.symbol_info_tick(im)
        time.sleep(2)
        jbg=ft.symbol_info_tick(im)
        if jbb[2] > (jbg[2]+0.00005):
            ft.Close(im,ticket=tickett)
            client.messages.create(body='Close the profit in '+im ,from_=from_whatsapp,to=to_whatsapp)            
        return t
    elif 50>trade>=20 and vf==1:
        jbb=ft.symbol_info_tick(im)
        time.sleep(2)
        jbg=ft.symbol_info_tick(im)
        if jbg[1] > (jbb[1]-0.00005):
            ft.Close(im,ticket=tickett)
            client.messages.create(body='Close the profit in '+im ,from_=from_whatsapp,to=to_whatsapp)           
        return t
    elif 20>trade>=10 and vf==0:
        jbb=ft.symbol_info_tick(im)
        time.sleep(2)
        jbg=ft.symbol_info_tick(im)
        if jbb[2] > (jbg[2]+0.000075):
            ft.Close(im,ticket=tickett)
            client.messages.create(body='Close the profit in '+im ,from_=from_whatsapp,to=to_whatsapp)            
        return t
    elif 20>trade>=10 and vf==1:
        jbb=ft.symbol_info_tick(im)
        time.sleep(2)
        jbg=ft.symbol_info_tick(im)
        if jbg[1] > (jbb[1]-0.000075):
            ft.Close(im,ticket=tickett)
            client.messages.create(body='Close the profit in '+im ,from_=from_whatsapp,to=to_whatsapp)            
        return t
    elif 10>trade>=2 and vf==0:
        jbb=ft.symbol_info_tick(im)
        time.sleep(2)
        jbg=ft.symbol_info_tick(im)
        if jbb[2] > (jbg[2]+0.00010):
            ft.Close(im,ticket=tickett)
            client.messages.create(body='Close the profit in '+im ,from_=from_whatsapp,to=to_whatsapp)
        return t
    elif 10>trade>=2 and vf==1:
        jbb=ft.symbol_info_tick(im)
        time.sleep(2)
        jbg=ft.symbol_info_tick(im)
        if jbg[1] > (jbb[1]-0.00010):
            ft.Close(im,ticket=tickett)
            client.messages.create(body='Close the profit in '+im ,from_=from_whatsapp,to=to_whatsapp)
        return t
    elif trade<=-2.5:
        ft.Close(im,ticket=tickett)
        client.messages.create(body='Close the profit in '+im ,from_=from_whatsapp,to=to_whatsapp)
        return t
    elif trade>=10:
        ft.Close(im,ticket=tickett)
        client.messages.create(body='Close the profit in '+im ,from_=from_whatsapp,to=to_whatsapp)
        return t
    else:
        return 'not'
  elif d ==0 and len(hh)<=0:
      print('no trade done at the moment')
      return t
  else:
      print('Error occured in getting ticket')
      return 'not'
      
def trade(data,interval,data_,im,i,jb,v1,v2,v3,v4,v5,v6,v7,to_whatsapp):
    try:
        bf= tr.decision(data,interval,data_,v1,v2,v3,v4,v5,v6,v7)
        '''level = tr.conf_level(data,interval,data_,v1,v2,v3,v4,v5,v6,v7)[-1]
        if level <0:
            level=-level'''
        if bf[-1] ==0:
            hh = ft.Buy(im,0.02)
            print('d-checked')
            client.messages.create(body='Buy '+im ,from_=from_whatsapp,to=to_whatsapp)            
            return hh[2],bf[-1],hh,1
        elif bf[-1]==1:
           hh= ft.Sell(im,0.02)
           print('e-checked')
           client.messages.create(body='Sell '+im ,from_=from_whatsapp,to=to_whatsapp)            
           return hh[2],bf[-1],hh,1
        elif bf[-1]==2:
            print('none')
            return 0,bf[-1],[],0
        else:
             print('Unknown Error Occured!')
             return 0,bf[-1],[],0
    except KeyError:
         print('no Trade yet')
         return 0,bf[-1],[],0
            
            
            
                
