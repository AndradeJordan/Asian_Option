#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 23:09:51 2020

@author: jordan
"""


import numpy as np   # math operations

import numpy.random as npr # random 

# Pathdependent Asian option BS 
def Asian_call_MC_BS(r,S0,sigma,T,K,N,n):
    
    delta=float(T/(2*n))
    G=npr.normal(0,1,size=(N,2*n))
    #Log returns
    LR=(r-0.5*sigma**2)*delta+np.sqrt(delta)*sigma*G
    # concatenate with log(S0)
    LR=np.concatenate((np.log(S0)*np.ones((N,1)),LR),axis=1)
    # cumsum horizontally (axis=1)
    LR=np.cumsum(LR,axis=1)
    # take the expo Spath matrix
    Spaths=np.exp(LR)
    #print(Spaths)
    print(len(Spaths[0,:]))
    
    spathsSIMP = Spaths[:,1:2*n:2]   #point millieu
    spathsSIMP0 = Spaths[:,0:2*n+1:2] # 
   
    
    Spaths = spathsSIMP0
    
    # print(len(Spaths[0,:]))
    ## Trapeze approximation
    fa = Spaths[:,0] 
    fb = Spaths[:,n] 
    spathsTRAP = Spaths[:,1:len(Spaths[0,:])-1]
    Sbar1 =np.cumsum(spathsTRAP,axis=1)[:,n-2]
    
    SbarTRAP = (Sbar1 + (fa+fb)*0.5)/n
    payoff1=np.exp(-r*T)*np.maximum(SbarTRAP-K,0) #call function
    price=np.mean(payoff1)
    #print(SbarTRAP)
    
    #simpson approximation
    Sbar2 =np.cumsum(spathsSIMP,axis=1)[:,n-1] #somm point milieu 
    
    u = float(1/3)
    v = float(1/6)
    w = float(2/3)
    
    SbarSIMP = (Sbar2*w + Sbar1*u + (fa+fb)*v)/n 
    payoff2=np.exp(-r*T)*np.maximum(SbarSIMP-K,0) #call function
    price_SIMP=np.mean(payoff2)
    

    #print(len(spathsSIMP[0,:]))
    
    #riemann approximation 
    Spaths=Spaths[:,0:len(Spaths[0,:])-1]
    Sbar=np.mean(Spaths,axis=1)
    payoff=np.exp(-r*T)*np.maximum(Sbar-K,0) #call function
    Asian_MC_price=np.mean(payoff)
     
   
    
    return Asian_MC_price,price,price_SIMP


[Asian_MC_price,price_Trap,price_Simp]=Asian_call_MC_BS(0.05,100,0.2,1,95,10000,100)    


print('*MC_Price_Riemann* *MC_Price_Trapeze* *MC_Price_Simpson* :')

print(Asian_MC_price,price_Trap, price_Simp)

