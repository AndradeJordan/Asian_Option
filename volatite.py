#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 10 15:17:46 2020

@author: jordan
"""


import numpy as np   # math operations

import numpy.random as npr # random

import datetime as dt

import matplotlib.pyplot as plt # plot

from pandas_datareader import DataReader 

import pandas as pd


tickers = ['SPY'] 
portfolio_returns = pd.DataFrame() 

start, end = dt.datetime(2015,9,1), dt.datetime(2016,11,1)
portfolio_returns = DataReader(tickers,'yahoo',start,end)

portfolio_returns = portfolio_returns.loc[:,'Close']



stkcarre = portfolio_returns * portfolio_returns


stkcarre = stkcarre[:-1]


T = 14/12 #car le temps est en année 
a = stkcarre.mean()*T 




deltaStkcarre = portfolio_returns.diff()**2
deltaStkcarre=deltaStkcarre[1:]

b = deltaStkcarre.sum()

vol = np.sqrt(b/a) 

print('*Volatilite* :')
print(vol)


