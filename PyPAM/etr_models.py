#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from rpy import r


def platt(light,etr):
    '''

    '''
    values = zip(light,etr)
    opts = []
    for vals in values:
        r.assign("x",vals[0])
        r.assign("y",vals[1])
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
        opts.append(r('min_ad(par = etr_sim$par)'))

    return opts

