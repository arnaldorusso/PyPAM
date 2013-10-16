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

    pars : arr
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
        } else {
            p_etrmax<-p_Ps2*(p_alpha/(p_alpha+p_Beta))*
            (p_Beta/(p_alpha+p_Beta))^(p_Beta/p_alpha)
        }
        
        p_Ek<-p_etrmax/p_alpha
    ''')

    opts = np.append(opts, r('min_ad(par = etr_sim$par)'))
    cpars = r('as.data.frame(cbind(p_alpha, p_Ek, p_etrmax))')
    pars = [cpars['p_alpha'], cpars['p_Ek'], cpars['p_etrmax']]

    return opts, pars

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
    r('library(nls2)')
    r.assign("x", light)
    r.assign("y", etr)
    r('dat<-as.data.frame(cbind(x,y))')
    r('names(dat)<-c("light","etr")')
    r('''grid<-expand.grid(list(a=seq(1e-07,9e-06,by=2e-07),
        b=seq(-0.002,0.006,by=0.002),c=seq(-6,6,by=2)))''')
    mini = r('''
            mini<-coefficients(nls2(etr~light/(a*light^2+b*light+c),
            data=dat, start=grid, algorithm="brute-force"))
            ''')

    r('''
    ep<-nls(etr~light/(a*light^2+b*light+c),data=dat,
    start=list(a=mini[1],b=mini[2],c=mini[3]),
    lower = list(0,-Inf,-Inf), trace=FALSE,
    algorithm = "port", nls.control("maxiter"=100000, tol=0.15))

    a2<-summary(ep)$coefficients[1]
    b2<-summary(ep)$coefficients[2]
    c2<-summary(ep)$coefficients[3]

    alpha<-(1/c2)
    etrmax<-1/(b2+2*(a2*c2)^0.5)
    Eopt<-(c2/a2)^0.5
    Ek<-etrmax/alpha
    ''')
    '''
    #TODO Implement minimisation in Python.
    # It's not very clear how to apply `nls2` in Python.
    # minimize from a list of initial values.
    
    #a = varis[0]
    #b = varis[1]
    #c = varis[2]
    a = mini['a']
    b = mini['b']
    c = mini['c']

    opts = (light/(a*(light**2)+(b*light)+c))
    ad = fmin(ep_minimize,varis,args=(light,etr))

    alpha = (1./ad[2])
    etrmax = 1./(ad[1]+2*(ad[0]*ad[2])**0.5)
    Eopt = (ad[2]/ad[0])**0.5
    Ek = etrmax/alpha

    params = [alpha, Ek, etrmax, Eopt]
    '''
    alpha = r('alpha')
    Ek = r('Ek')
    etr_max = r('etrmax')
    params = [alpha, Ek, etr_max]
    opts = r('opts<-fitted(ep)')
    
    return opts, params

def ep_minimize(varis,light,etr):
    '''
    Minimize values to be used on Eilers Peeters adjusting curve, as
    in `eilers_peeters` function.

    #TODO
    # Necessary when use it from python minimize.
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
