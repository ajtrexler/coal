# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 06:21:49 2016

@author: adam
"""
import requests
import pandas as pd
import quandl
import json
import seaborn as sea
import numpy as np
import matplotlib.pyplot as plt

#coal companies
#   ARCH= arch coal
#   CLU= cloud peak energy
#   BHP= bhp billito nlimited
#   GLEN.L= glencore listed in london
#   AAL.L= anglo american

quandl_codes=['YAHOO/BHP','YAHOO/CLD','YAHOO/HK_0805','GOOG/LON_AAL','YAHOO/GE','YAHOO/MSFT','YAHOO/GOOGL','YAHOO/BAC']
quandl_names=['BHP','CLD','GLEN','ANGA','ctrlGE','ctrlMSFT','ctrlGOOG','ctrlBOA']
q_api_key='moEyreACqJUx2izM5oZR'

#imf_cc_coal_url='https://www.quandl.com/api/v3/datasets/ODA/PCOALAU_USD.json?api_key=moEyreACqJUx2izM5oZR'
#
#imf_coal=requests.get(imf_cc_coal_url)
#d=json.loads(imf_coal.text)
#dd=d['dataset']['data']
#pdd=pd.Series(dd)
coal=quandl.get("ODA/PCOALAU_USD", authtoken="moEyreACqJUx2izM5oZR")
#bhp=quandl.get('YAHOO/BHP',authtoken="moEyreACqJUx2izM5oZR")

priceframe=pd.DataFrame(index=coal.index,columns=['Coal']+quandl_names)
priceframe['Coal']=coal['Value']

for x,xname in zip(quandl_codes,quandl_names):
    data=quandl.get(x,authtoken=q_api_key)
    priceframe[xname]=data['Open']

#identify when we have company data for at least 2 companies.  make new df pf
def throwdata(row):
    r=row.isnull()
    if np.sum(r)>2:
        return True
    else:
        return False

throw_rows=priceframe.apply(throwdata,axis=1)
pf=priceframe.loc[throw_rows==False]

#normalize pf min to max, 0 to 1.  then plot everybody.
def normcols(col):
    return (col-np.min(col))/((np.max(col))-(np.min(col)))

nf=pf.apply(normcols,axis=0)
plt.figure()
nf.plot(kind='line',subplots=True)
plt.savefig('figure1.png')

for x in priceframe:
    subdf=pd.concat([priceframe['Coal'],priceframe[x]],1)
    subdf.dropna(0,inplace=True)
    print 'coal to',x,np.corrcoef(subdf,rowvar=False)[0,1]





