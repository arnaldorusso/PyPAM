#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.optimize import leastsq, fmin
from rpy import r


def platt(light,etr):
    '''
    Adjust a curve of best fit, following the Platt model.

    Parameters
    ----------
    light : arr
        Generally PAR values. Where Photosynthetic Active Radiance
        interfer on Primary Production. 'light' is this parameter.

    etr : arr
        Eletron Transference Rate, by means relative ETR, obtained from
        Rapid Light Curves.

    Returns
    -------
    opts : arr
        Values optimized

    cpars : arr
        Curve parameters (alpha, Ek, ETRmax)

    See Also
    --------
    T. Platt, C.L. Gallegos and W.G. Harrison, 1980. Photoinibition of photosynthesis in natural
        assemblages of marine phytoplankton
        
    '''
    opts = []
    pars = []

    r.assign("x", light)
    r.assign("y", etr)
    min_platt = r("""
    platt<- function(params){
        alpha<-params[1]
        Beta<- params[2]
        Ps<- params[3]
        return( sum( (y-Ps*(1-exp(-alpha*x/Ps))*exp(-Beta*x/Ps))^2))
    } """)
    min_adp = r("""
    min_ad<-function(params){ 
        alpha<-params[1]
        Beta<-params[2]
        Ps<-params[3]
        return( ( (Ps*(1-exp(-alpha*x/Ps)) *exp(-Beta*x/Ps)) ))
    }""")
    r('etr_sim<-optim(par=c(0.4, 1.5 , 80),fn=platt)')
    r('p_alpha<-etr_sim$par[1]')
    r('p_Beta<-etr_sim$par[2]')
    r('p_Ps2<-etr_sim$par[3]')
    r('''
        if (p_Beta==0){
            p_etrmax<-param_Ps2
            }
        else
            p_etrmax<-p_Ps2*(p_alpha/(p_alpha+p_Beta))*(p_Beta/(p_alpha+p_Beta))^(p_Beta/p_alpha)

        p_Ek<-p_etrmax/p_alpha
    ''')

    opts = np.append(opts, r('min_ad(par = etr_sim$par)'))
    cpars = r('c(p_alpha, p_Ek, p_etrmax)')

    return opts, cpars

def eilers_peeters(ini,light,etr):
    '''
    Adjust a best fit curve to ExP curves, according to Eilers  & Peters
    Model.

    Parameters
    ----------
    ini : arr
        Initial values values to set the curve.
        At Eilers-Peeters models (a,b,c).

    light : arr
        Generally PAR values. Where Photosynthetic Active Radiance
        interfer on Primary Production. 'light' is this parameter.

    etr : arr
        Eletron Transference Rate, by means relative ETR, obtained from
        Rapid Light Curves.

    Return
    ------
    opts : arr
        Values optimized

    params : arr
        Curve Parameters (alpha, Ek, ETR_max, Eopt)

    See Also
    --------
    P.H.C. Eilers and J.C.H Peeters. 1988. A model for the relationship
    between the light intensity and the rate of photosynthesis in
    phytoplankton. Ecol. Model. 42:199-215.
    '''
    a = varis[0]
    b = varis[1]
    c = varis[2]

    opts = (light/(a*(light**2)+(b*light)+c))
    ad = fmin(ep_minimize,varis,args=(light,etr))

    alpha = (1./ad[2])
    etrmax = 1./(ad[1]+2*(ad[0]*ad[2])**0.5)
    Eopt = (ad[2]/ad[0])**0.5
    Ek = etrmax/alpha

    params = [alpha, Ek, etrmax, Eopt]
    
    return opts, params

def ep_minimize(varis,light,etr):
    '''
    Minimize values to be used on Eilers Peeters adjusting curve, as
    in `eilers_peeters` function.

    Parameters
    ----------

    Return
    ------

    '''
    a = varis[0]
    b = varis[1]
    c = varis[2]
    
    opts = np.sum((etr-(light/(a*(light**2)+(b*light)+c)))**2)

    return opts
