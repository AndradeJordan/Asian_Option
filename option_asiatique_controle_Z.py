# -*- coding: utf-8 -*-
"""
Created on Sun May 10 00:17:52 2020

@author: ousma
"""
import numpy as np   # math operations

import numpy.random as npr # random 

import matplotlib.pyplot as plt # plot

from scipy.stats import norm

def esperanceZ(r,S0,sigma,T,K):

    
    d=(np.log(K/S0)-(r-sigma**2/2)*T/2)*(1/sigma)*(np.sqrt(3/T))
    E_Z=np.exp(-r*T)*((S0*np.exp((r-sigma**2/6)*T/2)*norm.cdf(-d+sigma*np.sqrt(T/3),0,1)-K*norm.cdf(-d,0,1)));

    return E_Z

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

    #print(Spaths)

    

    ## Riemann approximation

    #remove final time component
    LR1=LR[:,0:len(Spaths[0,:])-1]
    Spaths=Spaths[:,0:len(Spaths[0,:])-1]

    #print(Spaths)

    

    #take the average over each row
    Sbar1=Sbar=np.mean(LR1,axis=1)
    Sbar=np.mean(Spaths,axis=1)

    #print(Sbar)

    prix_vec=np.exp(-r*T)*np.maximum(Sbar-K,0)-np.exp(-r*T)*np.maximum(np.exp(Sbar1)-K,0) 



    Asian_MC_price=np.mean(prix_vec) + esperanceZ(r,S0,sigma,T,K)



    # 95% C.I



    sigma=np.std(prix_vec,ddof=1) # standard deviation estimator



    error=1.96*sigma/np.sqrt(N)



    CI_up=Asian_MC_price + error

    CI_down=Asian_MC_price -error

    

    return Asian_MC_price,CI_up,CI_down,error









[Asian_MC_price,CI_up,CI_down,error]=Asian_call_MC_BS(0.05,100,0.2,1,95,10000,100)    

print('*******MC_Price*****')

print(Asian_MC_price,CI_up,CI_down,error)
