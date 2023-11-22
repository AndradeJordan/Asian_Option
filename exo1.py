#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 14:23:51 2020

@author: jordan
"""

import numpy as np   # math operations

import numpy.random as npr # random 

# Pathdependent Asian option BS 
def Asian_call_MC_BS(r,S0,sigma,T,K,N,n):
    
    delta=float(T/n)
    G=npr.normal(0,1,size=(N,n))
    #Log returns
    LR=(r-0.5*sigma**2)*delta+np.sqrt(delta)*sigma*G
    # concatenate with log(S0)
    LR=np.concatenate((np.log(S0)*np.ones((N,1)),LR),axis=1)
    # cumsum horizontally (axis=1)
    LR=np.cumsum(LR,axis=1)
    # take the expo Spath matrix
    Spaths=np.exp(LR)
    
    #initial and end p_values 
    fa = Spaths[:,0] 
    fb = Spaths[:,n-1] 
   
    ## Riemann approximation
    #remove final time component
    Spaths=Spaths[:,0:len(Spaths[0,:])-1]
    #print(Spaths)
    #take the average over each row
    Sbar=np.mean(Spaths,axis=1)
    #print(Sbar)
    payoff=np.exp(-r*T)*np.maximum(Sbar-K,0) #call function
    Asian_MC_price_R=np.mean(payoff)
    # 95% C.I
    sigma=np.std(payoff) # standard deviation estimator : ecart type de monte_carlo
    error=1.96*sigma/np.sqrt(N)
    CI_up_R=Asian_MC_price_R + error
    CI_down_R=Asian_MC_price_R -error
    
    
     ## Trapeze approximation
    spathsTRAP = Spaths[:,1:len(Spaths[0,:])]
    Sbar1 =np.cumsum(spathsTRAP,axis=1)[:,n-2]
    
    SbarTRAP = (Sbar1 + (fa+fb)*0.5)/n
    payoff1=np.exp(-r*T)*np.maximum(SbarTRAP-K,0) #call function
    Asian_MC_price_T=np.mean(payoff1)
    #95% CI SbarTRAP
    sigma1=np.std(payoff1) # standard deviation estimator : ecart type de monte_carlo
    error_T=1.96*sigma1/np.sqrt(N)
    CI_up_T=Asian_MC_price_T + error_T
    CI_down_T=Asian_MC_price_T -error_T
    
    return Asian_MC_price_R,CI_up_R,CI_down_R,error,Asian_MC_price_T,CI_up_T,CI_down_T,error_T, 


[price_R,CI_up,CI_down,error,price_T,CI_up_T,CI_down_T,error_T]=Asian_call_MC_BS(0.05,100,0.2,1,95,10000,100)    

print('*******MC_Price with Riemann*****')

print(price_R,CI_up,CI_down,error)


print('*******MC_Price with Trapeze*****')

print(price_T,CI_up_T,CI_down_T,error_T)
