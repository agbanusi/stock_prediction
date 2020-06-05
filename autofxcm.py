import trial1 as tr
import MetaTrader5 as ft
import time

def monitor(jb,vf,im,i,hh):
  t = 'done'
  if len(hh) > 0:
    tickett=hh[2]
    tt=ft.positions_get(ticket=tickett)
    trade=tt[0][15]  
    if trade <=-3 and vf== 0:
        ft.Close(im,ticket=tickett)
        hy=ft.Sell(im,0.06)
        while True:
            if ft.positions_get(hy[2])[0][15] >= 20:
                ft.Close(im,hy[2])
                break
            elif ft.positions_get(hy[2])[0][15]<=-5:
                ft.Close(im,hy[2])
                break
        return t
    elif trade<=-3 and vf== 1:
        ft.Close(im,ticket=tickett)
        hy=ft.Buy(im,0.06)
        while True:
            if ft.positions_get(hy[2])[0][15] >= 20:
                ft.Close(im,hy[2])
                break
            elif ft.positions_get(hy[2])[0][15]<=-5:
                ft.Close(im,hy[2])
                break
        return t
    elif trade >= 50 and vf == 0:
        jbb=ft.symbol_info_tick(im)
        time.sleep(2)
        jbg=ft.symbol_info_tick(im)
        if jbb[2] > (jbg[2]):
                ft.Close(im,ticket=tickett)
        return t
    elif trade >=50 and vf==1:
        jbb=ft.symbol_info_tick(im)
        time.sleep(2)
        jbg=ft.symbol_info_tick(im)
        if jbb[1] < (jbg[1]):
                ft.Close(im,ticket=tickett)
        return t
    elif 50>trade>=20 and vf==0:
        jbb=ft.symbol_info_tick(im)
        time.sleep(2)
        jbg=ft.symbol_info_tick(im)
        if jbb[2] > (jbg[2]+0.00005):
            ft.Close(im,ticket=tickett)
        return t
    elif 50>trade>=20 and vf==1:
        jbb=ft.symbol_info_tick(im)
        time.sleep(2)
        jbg=ft.symbol_info_tick(im)
        if jbg[1] > (jbb[1]-0.00005):
            ft.Close(im,ticket=tickett)
        return t
    elif 20>trade>=10 and vf==0:
        jbb=ft.symbol_info_tick(im)
        time.sleep(2)
        jbg=ft.symbol_info_tick(im)
        if jbb[2] > (jbg[2]+0.000075):
            ft.Close(im,ticket=tickett)
        return t
    elif 20>trade>=10 and vf==1:
        jbb=ft.symbol_info_tick(im)
        time.sleep(2)
        jbg=ft.symbol_info_tick(im)
        if jbg[1] > (jbb[1]-0.000075):
            ft.Close(im,ticket=tickett)            
        return t
    elif 10>trade>=2.5 and vf==0:
        jbb=ft.symbol_info_tick(im)
        time.sleep(2)
        jbg=ft.symbol_info_tick(im)
        if jbb[2] > (jbg[2]+0.00010):
            ft.Close(im,ticket=tickett)
        return t
    elif 10>trade>=2.5 and vf==1:
        jbb=ft.symbol_info_tick(im)
        time.sleep(2)
        jbg=ft.symbol_info_tick(im)
        if jbg[1] > (jbb[1]-0.00010):
            ft.Close(im,ticket=tickett)
        return t
    elif trade<=-3:
        ft.Close(im,ticket=tickett)
    elif trade>=10:
        ft.Close(im,ticket=tickett)
    else:
        return 'not'
  elif len(hh)<=0:
      print('no trade done at the moment')
      return t
      
def trade(data,interval,data_,im,i,jb,v1,v2,v3,v4,v5,v6,v7):
    try:
        vf= tr.decision(data,interval,data_,v1,v2,v3,v4,v5,v6,v7)
        '''level = tr.conf_level(data,interval,data_,v1,v2,v3,v4,v5,v6,v7)[-1]
        if level <0:
            level=-level'''
        if vf[-1] ==0:
            hh = ft.Buy(im,0.03)
            print('d-checked')
            return hh[2],vf[-1],hh
        elif vf[-1]==1:
           hh= ft.Sell(im,0.03)
           print('e-checked')
           return hh[2],vf[-1],hh
        elif vf[-1]==2:
            return 0,vf[-1],[]
        else:
             print('Unknown Error Occured!')
             return 0,vf[-1],[]
    except KeyError:
         print('no Trade yet')
         return 0,vf[-1],[]
            
            
            
            
                