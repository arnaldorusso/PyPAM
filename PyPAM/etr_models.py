#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from rpy import r


def platt(light,etr):
    '''
    Adjust a curve of best fitt, following the Platt model.

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

    params : arr
        Parameters of curve ('alpha', 'Ik', 'rETR_max')

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

    opts = np.append(opts, r('min_ad(par = etr_sim$par)'))
    pars = r('etr_sim$par')

    return opts, pars

